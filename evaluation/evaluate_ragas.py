"""
=============================================================================
RAGAS EVALUATION SCRIPT
Đánh giá Hệ Thống Chẩn Đoán Y Khoa GraphRAG bằng Framework RAGAS
=============================================================================

Metrics đánh giá:
  - Faithfulness: AI trả lời có đúng theo context từ Knowledge Graph không?
  - Answer Relevancy: Câu trả lời có liên quan đến câu hỏi không?
  - Context Precision: Context từ KG có chính xác không?
  - Context Recall: Context có đủ thông tin để trả lời không?

Yêu cầu:
  - Neo4j đang chạy (bolt://localhost:7687)
  - Ollama đang chạy (http://localhost:11434) với model gemma3
  - pip install ragas langchain-ollama datasets
=============================================================================
"""

import json
import os
import sys
import time
import types
from datetime import datetime
from pathlib import Path

# =============================================================================
# MONKEY-PATCH: Fix RAGAS 0.4.3 stale import
# langchain_community 0.4.x đã xóa module chat_models.vertexai
# nhưng ragas vẫn import từ đó. Patch này redirect sang langchain_google_vertexai
# =============================================================================
try:
    from langchain_community.chat_models import vertexai as _vertexai_module
except (ImportError, ModuleNotFoundError):
    try:
        import langchain_community.chat_models as _cm
        from langchain_google_vertexai import ChatVertexAI

        _shim = types.ModuleType("langchain_community.chat_models.vertexai")
        _shim.ChatVertexAI = ChatVertexAI
        sys.modules["langchain_community.chat_models.vertexai"] = _shim
    except ImportError:
        pass

try:
    from langchain_community import llms as _llms_module
    if not hasattr(_llms_module, "VertexAI"):
        from langchain_google_vertexai import VertexAI
        _llms_module.VertexAI = VertexAI
except (ImportError, ModuleNotFoundError):
    pass
# =============================================================================

import requests
from dotenv import load_dotenv
from neo4j import GraphDatabase

# --- Fix encoding cho Windows ---
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# =============================================================================
# CẤU HÌNH
# =============================================================================
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "gemma3"

# Đường dẫn
SCRIPT_DIR = Path(__file__).parent
TEST_DATASET_PATH = SCRIPT_DIR / "test_dataset.json"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# =============================================================================
# PHẦN 1: KẾT NỐI NEO4J (tái sử dụng từ app.py)
# =============================================================================
class MedicalGraphApp:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def diagnose(self, selected_symptoms, user_question=None, enable_rerank=False):
        """Truy vấn Knowledge Graph để chẩn đoán bệnh dựa trên triệu chứng."""
        query = """
        MATCH (d:Disease)-[r:HAS_SYMPTOM]->(s:Symptom)
        WITH d, s, r, CASE WHEN s.name IN $inputs THEN r.weight ELSE 0 END AS matched_weight
        WITH d, sum(matched_weight) AS score_user, sum(r.weight) AS total_disease_weight,
             collect(CASE WHEN s.name IN $inputs THEN s.name END) AS matched_list
        WHERE score_user > 0
        RETURN d.id AS id, d.name AS name, (score_user / total_disease_weight) * 100 AS confidence,
               [x IN matched_list WHERE x IS NOT NULL] AS matched_symptoms, score_user
        ORDER BY confidence DESC, score_user DESC, name ASC
        """
        with self.driver.session() as session:
            result = session.run(query, inputs=selected_symptoms)
            candidates = [dict(record) for record in result]
            
            if not candidates:
                return []
                
            if enable_rerank:
                question = user_question
                if not question:
                    question = f"Tôi bị các triệu chứng: {', '.join(selected_symptoms)}. Tôi có thể mắc bệnh gì?"
                
                top_candidates = candidates[:15]
                candidate_str = ""
                for idx, c in enumerate(top_candidates):
                    candidate_str += f"{idx+1}. {c['name']} (Mã bệnh: {c['id']}) - Độ tin cậy thô từ KG: {c['confidence']:.1f}%\n"
                
                prompt = f"""Bạn là một Bác sĩ chuyên khoa y tế phân tích dữ liệu lâm sàng.
Dựa trên câu hỏi/triệu chứng của bệnh nhân:
"{question}"

Và danh sách các bệnh ứng viên được tìm thấy từ Đồ thị tri thức (Knowledge Graph):
{candidate_str}

Hãy phân tích kỹ và chọn ra MỘT bệnh phù hợp nhất với mô tả của bệnh nhân trong danh sách trên.
Trả về kết quả chính xác theo định dạng JSON sau:
{{
  "chosen_id": "MÃ_BỆNH_ĐƯỢC_CHỌN",
  "reason": "Lý do ngắn gọn tại sao chọn bệnh này dựa trên triệu chứng lâm sàng"
}}

Lưu ý: Chỉ chọn mã bệnh có trong danh sách ứng viên trên. Trả về đúng định dạng JSON, không thêm bất kỳ văn bản giải thích nào ngoài khối JSON.
"""
                try:
                    payload = {
                        "model": MODEL_NAME,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
                    if response.status_code == 200:
                        res_text = response.json().get("response", "").strip()
                        data = json.loads(res_text)
                        chosen_id = data.get("chosen_id", "").strip()
                        reason = data.get("reason", "").strip()
                        
                        match_idx = -1
                        for idx, c in enumerate(candidates):
                            if c["id"] == chosen_id:
                                match_idx = idx
                                break
                                
                        if match_idx != -1:
                            chosen_candidate = candidates.pop(match_idx)
                            chosen_candidate["is_llm_chosen"] = True
                            chosen_candidate["llm_reason"] = reason
                            
                            top_conf = candidates[0]["confidence"] if candidates else 0.0
                            chosen_candidate["confidence"] = max(95.0, top_conf)
                            
                            candidates.insert(0, chosen_candidate)
                except Exception:
                    pass
            
            return candidates


# =============================================================================
# PHẦN 2: GỌI OLLAMA AI (tái sử dụng từ app.py)
# =============================================================================
def ask_local_ai(prompt_context):
    """Gửi prompt tới Ollama API và nhận câu trả lời."""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt_context,
            "stream": False,
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if response.status_code == 200:
            return response.json().get("response", "")
        return "⚠️ Không thể kết nối với AI Local."
    except Exception as e:
        return f"❌ Lỗi kết nối Ollama: {e}"


# =============================================================================
# PHẦN 3: SINH DỮ LIỆU ĐÁNH GIÁ (chạy pipeline RAG cho mỗi test case)
# =============================================================================
def build_knowledge_context(results, user_symptoms):
    """Xây dựng context từ kết quả chẩn đoán KG (giống app.py)."""
    if not results:
        return "Không tìm thấy bệnh nào khớp với triệu chứng đã cho."

    top_disease = results[0]
    context = (
        f"Bệnh nhân có các triệu chứng: {', '.join(user_symptoms)}.\n"
        f"Hệ thống đồ thị tri thức Neo4j phân tích thấy bệnh có khả năng cao nhất là: "
        f"{top_disease['name']} (Mã bệnh ICD-10: {top_disease['id']}) "
        f"với độ tin cậy {top_disease['confidence']:.2f}%.\n"
        f"Các triệu chứng đặc trưng đã khớp trong đồ thị: "
        f"{', '.join(top_disease['matched_symptoms'])}."
    )

    # Thêm thông tin các bệnh khác (top 3)
    if len(results) > 1:
        context += "\n\nCác bệnh có khả năng khác:"
        for res in results[1:4]:
            context += (
                f"\n- {res['name']} (ICD-10: {res['id']}) — "
                f"Độ tin cậy: {res['confidence']:.2f}%, "
                f"Triệu chứng khớp: {', '.join(res['matched_symptoms'])}"
            )

    return context


def build_rag_prompt(question, knowledge_context):
    """Xây dựng RAG prompt (giống app.py)."""
    return (
        f"Bạn là một Bác sĩ Trợ lý AI y khoa chuyên nghiệp, tận tâm tại Việt Nam.\n"
        f"Hãy dựa trên thông tin Đồ thị tri thức y khoa chuẩn xác sau đây:\n"
        f'"""\n{knowledge_context}\n"""\n\n'
        f"Câu hỏi của bệnh nhân: {question}\n"
        f"Trả lời bằng tiếng Việt, ngắn gọn, chính xác:"
    )


def generate_evaluation_data(test_cases, graph_app):
    """
    Chạy toàn bộ pipeline RAG cho mỗi test case và thu thập dữ liệu đánh giá.
    Returns: list of dicts với keys: question, answer, contexts, ground_truth
    """
    eval_data = []
    total = len(test_cases)

    for i, tc in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"📋 Test Case {i+1}/{total}: {tc['id']} [{tc['category']}]")
        print(f"   Câu hỏi: {tc['question'][:80]}...")
        print(f"   Triệu chứng: {', '.join(tc['symptoms'])}")

        # Bước 1: Query Knowledge Graph (Retrieval)
        print(f"   🔍 Đang truy vấn Neo4j Knowledge Graph...")
        try:
            results = graph_app.diagnose(tc["symptoms"], user_question=tc["question"], enable_rerank=True)
            if results:
                top = results[0]
                print(
                    f"   ✅ KG Result: {top['name']} ({top['id']}) — "
                    f"Confidence: {top['confidence']:.1f}%"
                )
                if top["id"] == tc["expected_disease_id"]:
                    print(f"   🎯 MATCH! Đúng bệnh expected.")
                else:
                    print(
                        f"   ⚠️  Expected: {tc['expected_disease_id']} "
                        f"({tc['expected_disease_name']})"
                    )
            else:
                print(f"   ❌ Không tìm thấy bệnh nào khớp!")
        except Exception as e:
            print(f"   ❌ Lỗi Neo4j: {e}")
            results = []

        # Bước 2: Xây dựng context (Knowledge Context)
        knowledge_context = build_knowledge_context(results, tc["symptoms"])

        # Bước 3: Gọi AI (Generation)
        print(f"   🤖 Đang gọi Ollama AI ({MODEL_NAME})...")
        rag_prompt = build_rag_prompt(tc["question"], knowledge_context)

        start_time = time.time()
        ai_answer = ask_local_ai(rag_prompt)
        elapsed = time.time() - start_time

        print(f"   ✅ AI trả lời ({elapsed:.1f}s): {ai_answer[:100]}...")

        # Thu thập dữ liệu cho RAGAS
        eval_entry = {
            "user_input": tc["question"],
            "response": ai_answer,
            "retrieved_contexts": [knowledge_context],
            "reference": tc["ground_truth"],
            # Metadata bổ sung (không dùng cho RAGAS nhưng hữu ích cho phân tích)
            "_test_id": tc["id"],
            "_category": tc["category"],
            "_expected_disease": tc["expected_disease_id"],
            "_kg_top_disease": results[0]["id"] if results else "N/A",
            "_kg_confidence": results[0]["confidence"] if results else 0,
            "_kg_match": (
                results[0]["id"] == tc["expected_disease_id"] if results else False
            ),
            "_ai_response_time": elapsed,
        }
        eval_data.append(eval_entry)

        # Delay nhẹ để không quá tải Ollama
        time.sleep(1)

    return eval_data


# =============================================================================
# PHẦN 4: ĐÁNH GIÁ BẰNG RAGAS
# =============================================================================
def run_ragas_evaluation(eval_data):
    """
    Chạy RAGAS evaluation trên dữ liệu đã sinh.
    Sử dụng Ollama làm LLM judge.
    """
    print(f"\n{'='*60}")
    print("📊 ĐÁNH GIÁ BẰNG RAGAS FRAMEWORK")
    print(f"{'='*60}")

    try:
        from ragas import EvaluationDataset, evaluate
        from ragas.metrics import (
            Faithfulness,
            ResponseRelevancy,
            LLMContextPrecisionWithoutReference,
            LLMContextRecall,
        )
    except ImportError:
        print("❌ Chưa cài ragas. Chạy: pip install ragas")
        print("   Sẽ chỉ đánh giá bằng metrics thủ công.")
        return None

    # --- Cấu hình Ollama làm LLM evaluator & Embeddings ---
    try:
        from langchain_ollama import ChatOllama, OllamaEmbeddings
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper

        print(f"   🔧 Đang cấu hình Ollama ({MODEL_NAME}) làm LLM judge...")
        llm = ChatOllama(model=MODEL_NAME, base_url="http://localhost:11434")
        ragas_llm = LangchainLLMWrapper(llm)

        print(f"   🔧 Đang cấu hình Ollama ({MODEL_NAME}) làm Embeddings evaluator...")
        embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url="http://localhost:11434")
        ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

        print(f"   ✅ LLM judge và Embeddings đã sẵn sàng")
    except ImportError:
        print("❌ Chưa cài langchain-ollama. Chạy: pip install langchain-ollama")
        return None

    # --- Chuẩn bị dataset cho RAGAS ---
    ragas_data = []
    for entry in eval_data:
        ragas_data.append(
            {
                "user_input": entry["user_input"],
                "response": entry["response"],
                "retrieved_contexts": entry["retrieved_contexts"],
                "reference": entry["reference"],
            }
        )

    print(f"   📝 Đã chuẩn bị {len(ragas_data)} test cases cho RAGAS")

    # --- Chạy RAGAS evaluation ---
    try:
        # Tránh lỗi OpenAI API key
        os.environ.setdefault("OPENAI_API_KEY", "sk-fake-key-for-local-eval")

        dataset = EvaluationDataset.from_list(ragas_data)

        metrics = [
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextPrecisionWithoutReference(),
            LLMContextRecall(),
        ]

        print(f"\n   🚀 Bắt đầu đánh giá RAGAS (có thể mất vài phút)...")
        print(f"   ⏳ Đang chạy {len(metrics)} metrics trên {len(ragas_data)} samples...")

        start = time.time()
        result = evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=ragas_llm,
            embeddings=ragas_embeddings,
        )
        elapsed = time.time() - start

        print(f"\n   ✅ Đánh giá hoàn tất trong {elapsed:.1f}s")
        return result

    except Exception as e:
        print(f"\n   ❌ Lỗi khi chạy RAGAS: {e}")
        print(f"   💡 Thử kiểm tra Ollama có đang chạy và model {MODEL_NAME} đã pull chưa.")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# PHẦN 5: ĐÁNH GIÁ THỦ CÔNG (KHÔNG CẦN RAGAS)
# =============================================================================
def run_manual_evaluation(eval_data):
    """
    Đánh giá thủ công dựa trên các metrics đo lường được trực tiếp:
    1. KG Accuracy: Tỷ lệ KG trả về đúng bệnh expected
    2. Response Time: Thời gian AI trả lời trung bình
    3. Category Coverage: Phủ sóng các nhóm bệnh
    """
    print(f"\n{'='*60}")
    print("📊 ĐÁNH GIÁ THỦ CÔNG (Manual Metrics)")
    print(f"{'='*60}")

    total = len(eval_data)

    # 1. KG Accuracy
    kg_matches = sum(1 for e in eval_data if e.get("_kg_match", False))
    kg_accuracy = (kg_matches / total) * 100 if total > 0 else 0

    # 2. Response Time
    times = [e["_ai_response_time"] for e in eval_data]
    avg_time = sum(times) / len(times) if times else 0
    min_time = min(times) if times else 0
    max_time = max(times) if times else 0

    # 3. KG Confidence Stats
    confidences = [e["_kg_confidence"] for e in eval_data if e["_kg_confidence"] > 0]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0

    # 4. Category Breakdown
    categories = {}
    for e in eval_data:
        cat = e["_category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "correct": 0}
        categories[cat]["total"] += 1
        if e.get("_kg_match", False):
            categories[cat]["correct"] += 1

    # 5. AI Response Quality (basic check)
    valid_responses = sum(
        1 for e in eval_data if len(e["response"]) > 50 and "❌" not in e["response"]
    )
    response_rate = (valid_responses / total) * 100 if total > 0 else 0

    # Print results
    manual_results = {
        "kg_accuracy": kg_accuracy,
        "kg_matches": kg_matches,
        "total_tests": total,
        "avg_response_time": avg_time,
        "min_response_time": min_time,
        "max_response_time": max_time,
        "avg_kg_confidence": avg_conf,
        "ai_response_rate": response_rate,
        "category_breakdown": categories,
    }

    print(f"\n   📌 Knowledge Graph Accuracy: {kg_matches}/{total} ({kg_accuracy:.1f}%)")
    print(f"   📌 AI Response Rate: {valid_responses}/{total} ({response_rate:.1f}%)")
    print(f"   📌 Avg KG Confidence: {avg_conf:.1f}%")
    print(f"   📌 Avg AI Response Time: {avg_time:.1f}s")
    print(f"   📌 Response Time Range: {min_time:.1f}s — {max_time:.1f}s")
    print(f"\n   📊 Category Breakdown:")
    for cat, info in sorted(categories.items()):
        acc = (info["correct"] / info["total"] * 100) if info["total"] > 0 else 0
        print(f"      [{cat}] {info['correct']}/{info['total']} ({acc:.0f}%)")

    return manual_results


# =============================================================================
# PHẦN 6: XUẤT BÁO CÁO
# =============================================================================
def export_results(eval_data, ragas_results, manual_results):
    """Xuất kết quả đánh giá ra file JSON và Markdown."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Export JSON ---
    json_path = RESULTS_DIR / f"evaluation_{timestamp}.json"
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "total_test_cases": len(eval_data),
        "manual_metrics": manual_results,
        "ragas_metrics": str(ragas_results) if ragas_results else "N/A",
        "details": [
            {
                "test_id": e["_test_id"],
                "category": e["_category"],
                "question": e["user_input"],
                "expected_disease": e["_expected_disease"],
                "kg_top_disease": e["_kg_top_disease"],
                "kg_confidence": e["_kg_confidence"],
                "kg_match": e["_kg_match"],
                "ai_response_time": e["_ai_response_time"],
                "ai_answer_preview": e["response"][:200],
                "ground_truth_preview": e["reference"][:200],
            }
            for e in eval_data
        ],
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    print(f"\n   💾 JSON saved: {json_path}")

    # --- Export Markdown Report ---
    md_path = RESULTS_DIR / f"evaluation_report_{timestamp}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Báo Cáo Đánh Giá Hệ Thống GraphRAG\n\n")
        f.write(f"**Ngày đánh giá:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"**Model AI:** {MODEL_NAME}\n")
        f.write(f"**Số test cases:** {len(eval_data)}\n\n")
        f.write("---\n\n")

        # Manual Metrics
        f.write("## 1. Kết Quả Đánh Giá Thủ Công\n\n")
        f.write("| Metric | Giá trị |\n")
        f.write("|--------|--------|\n")
        f.write(
            f"| KG Accuracy | {manual_results['kg_matches']}/{manual_results['total_tests']} "
            f"({manual_results['kg_accuracy']:.1f}%) |\n"
        )
        f.write(
            f"| AI Response Rate | {manual_results['ai_response_rate']:.1f}% |\n"
        )
        f.write(
            f"| Avg KG Confidence | {manual_results['avg_kg_confidence']:.1f}% |\n"
        )
        f.write(
            f"| Avg Response Time | {manual_results['avg_response_time']:.1f}s |\n"
        )
        f.write("\n")

        # Category breakdown
        f.write("### Phân Tích Theo Nhóm Bệnh\n\n")
        f.write("| Nhóm | Đúng/Tổng | Accuracy |\n")
        f.write("|------|-----------|----------|\n")
        for cat, info in sorted(manual_results["category_breakdown"].items()):
            acc = (
                (info["correct"] / info["total"] * 100) if info["total"] > 0 else 0
            )
            f.write(f"| {cat} | {info['correct']}/{info['total']} | {acc:.0f}% |\n")
        f.write("\n")

        # RAGAS Metrics
        if ragas_results:
            f.write("## 2. Kết Quả RAGAS\n\n")
            f.write("| Metric | Score |\n")
            f.write("|--------|-------|\n")
            try:
                for metric_name, score in ragas_results.items():
                    if isinstance(score, (int, float)):
                        f.write(f"| {metric_name} | {score:.4f} |\n")
            except Exception:
                f.write(f"| Raw Results | {ragas_results} |\n")
            f.write("\n")

        # Detail per test case
        f.write("## 3. Chi Tiết Từng Test Case\n\n")
        for e in eval_data:
            match_icon = "✅" if e["_kg_match"] else "❌"
            f.write(f"### {e['_test_id']} [{e['_category']}] {match_icon}\n\n")
            f.write(f"- **Câu hỏi:** {e['user_input']}\n")
            f.write(f"- **Expected:** {e['_expected_disease']}\n")
            f.write(
                f"- **KG Result:** {e['_kg_top_disease']} "
                f"(confidence: {e['_kg_confidence']:.1f}%)\n"
            )
            f.write(f"- **AI Time:** {e['_ai_response_time']:.1f}s\n")
            f.write(f"- **AI Answer:** {e['response'][:300]}...\n\n")

    print(f"   📄 Report saved: {md_path}")
    return json_path, md_path


# =============================================================================
# MAIN — CHẠY TOÀN BỘ PIPELINE ĐÁNH GIÁ
# =============================================================================
def main():
    print("=" * 60)
    print("🩺 ĐÁNH GIÁ HỆ THỐNG CHẨN ĐOÁN Y KHOA GraphRAG")
    print("   Framework: RAGAS + Manual Metrics")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Neo4j: {NEO4J_URI}")
    print("=" * 60)

    # 1. Load test dataset
    print(f"\n📂 Đang load test dataset từ {TEST_DATASET_PATH}...")
    with open(TEST_DATASET_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
    print(f"   ✅ Đã load {len(test_cases)} test cases")
    print(f"   Categories: {set(tc['category'] for tc in test_cases)}")

    # 2. Kết nối Neo4j
    print(f"\n🔗 Đang kết nối Neo4j...")
    try:
        graph_app = MedicalGraphApp()
        print(f"   ✅ Kết nối Neo4j thành công")
    except Exception as e:
        print(f"   ❌ Lỗi kết nối Neo4j: {e}")
        print(f"   💡 Hãy chắc chắn Neo4j đang chạy tại {NEO4J_URI}")
        return

    # 3. Kiểm tra Ollama
    print(f"\n🤖 Đang kiểm tra Ollama...")
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            print(f"   ✅ Ollama đang chạy. Models: {models}")
        else:
            print(f"   ⚠️ Ollama status: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ Không thể kết nối Ollama: {e}")
        print(f"   💡 Hãy chạy Docker: docker start ollama")
        graph_app.close()
        return

    # 4. Sinh dữ liệu đánh giá (chạy pipeline RAG)
    print(f"\n{'='*60}")
    print("🔄 BƯỚC 1: SINH DỮ LIỆU ĐÁNH GIÁ (Chạy RAG Pipeline)")
    print(f"{'='*60}")
    eval_data = generate_evaluation_data(test_cases, graph_app)

    # 5. Đánh giá thủ công
    manual_results = run_manual_evaluation(eval_data)

    # 6. Đánh giá RAGAS
    ragas_results = run_ragas_evaluation(eval_data)

    # 7. Xuất báo cáo
    print(f"\n{'='*60}")
    print("💾 XUẤT BÁO CÁO")
    print(f"{'='*60}")
    json_path, md_path = export_results(eval_data, ragas_results, manual_results)

    # 8. Tổng kết
    print(f"\n{'='*60}")
    print("🎉 HOÀN TẤT ĐÁNH GIÁ")
    print(f"{'='*60}")
    print(f"   📌 KG Accuracy: {manual_results['kg_accuracy']:.1f}%")
    print(f"   📌 AI Response Rate: {manual_results['ai_response_rate']:.1f}%")
    if ragas_results:
        print(f"   📊 RAGAS Results: {ragas_results}")
    print(f"\n   📁 Output files:")
    print(f"      {json_path}")
    print(f"      {md_path}")

    graph_app.close()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
