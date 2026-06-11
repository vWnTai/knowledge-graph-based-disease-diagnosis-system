import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

# --- CẤU HÌNH LIÊN KẾT HỆ THỐNG ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3"


def ask_local_ai(prompt_context):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt_context,
            "stream": False,
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json().get("response", "")
        return "⚠️ Không thể kết nối với AI Local."
    except Exception as e:
        return f"❌ Lỗi kết nối Ollama: {e}. Hãy chắc chắn Container Docker đang chạy!"


# --- PHẦN KẾT NỐI NEO4J ---
class MedicalGraphApp:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def get_all_symptoms(self):
        query = "MATCH (s:Symptom) RETURN s.name AS name ORDER BY name ASC"
        with self.driver.session() as session:
            result = session.run(query)
            return [record["name"] for record in result]

    def diagnose(self, selected_symptoms, user_question=None, enable_rerank=False):
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
                # Nếu không có câu hỏi cụ thể, tự tạo câu hỏi từ triệu chứng
                question = user_question
                if not question:
                    question = f"Tôi bị các triệu chứng: {', '.join(selected_symptoms)}. Tôi có thể mắc bệnh gì?"
                
                # Lấy tối đa 15 bệnh ứng viên
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
                    # Fallback silently on error
                    pass
            
            return candidates


# ==============================================================================
# UI DESIGN - GIAO DIỆN PREMIUM VỚI GLASSMORPHISM & GRADIENT
# ==============================================================================
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán GraphRAG",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- INJECT CSS TOÀN BỘ ---
st.markdown(
    """
    <style>
    /* ========== GOOGLE FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

    /* ========== GLOBAL RESET ========== */
    *, *::before, *::after {
        font-family: 'Be Vietnam Pro', sans-serif !important;
    }

    /* ========== NỀN GRADIENT CHÍNH ========== */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #f5f0ff 40%, #fff0f6 100%) !important;
    }
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ========== HIDE DEFAULT ELEMENTS ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent !important;}

    /* ========== CUSTOM SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #a78bfa, #6C5CE7);
        border-radius: 10px;
    }

    /* ========== HEADER CUSTOM ========== */
    .custom-header {
        background: linear-gradient(135deg, #1a73e8 0%, #6C5CE7 50%, #a855f7 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(108, 92, 231, 0.25);
    }
    .custom-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255,255,255,0.08) 50%,
            transparent 70%
        );
        animation: shimmer 4s ease-in-out infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(0deg); }
        100% { transform: translateX(100%) rotate(0deg); }
    }
    .custom-header h1 {
        color: #ffffff !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.5rem 0 !important;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
        letter-spacing: -0.5px;
    }
    .custom-header p {
        color: rgba(255,255,255,0.88) !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        margin: 0 !important;
        position: relative;
        z-index: 1;
    }
    .header-badges {
        display: flex;
        gap: 10px;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
        flex-wrap: wrap;
    }
    .header-badge {
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 50px;
        padding: 5px 14px;
        color: #fff;
        font-size: 0.78rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* ========== GLASS CARD SECTIONS ========== */
    .glass-section {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    .glass-section:hover {
        box-shadow: 0 8px 32px rgba(108, 92, 231, 0.1);
        transform: translateY(-1px);
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e1b4b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title .icon {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .icon-blue { background: linear-gradient(135deg, #dbeafe, #bfdbfe); }
    .icon-purple { background: linear-gradient(135deg, #ede9fe, #ddd6fe); }
    .icon-green { background: linear-gradient(135deg, #d1fae5, #a7f3d0); }
    .icon-pink { background: linear-gradient(135deg, #fce7f3, #fbcfe8); }

    /* ========== DISEASE RESULT CARDS ========== */
    .disease-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .disease-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .disease-card.confidence-high::before {
        background: linear-gradient(90deg, #10b981, #34d399);
    }
    .disease-card.confidence-medium::before {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
    }
    .disease-card.confidence-low::before {
        background: linear-gradient(90deg, #ef4444, #f87171);
    }
    .disease-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(108, 92, 231, 0.12);
        border-color: rgba(108, 92, 231, 0.2);
    }
    .disease-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.7rem;
    }
    .disease-name {
        font-weight: 700;
        font-size: 1rem;
        color: #1e1b4b;
        flex: 1;
        line-height: 1.4;
    }
    .disease-id {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6C5CE7;
        background: rgba(108, 92, 231, 0.08);
        padding: 3px 10px;
        border-radius: 50px;
        white-space: nowrap;
        margin-left: 10px;
    }
    .confidence-bar-container {
        width: 100%;
        height: 8px;
        background: #f1f5f9;
        border-radius: 100px;
        overflow: hidden;
        margin-bottom: 0.6rem;
    }
    .confidence-bar {
        height: 100%;
        border-radius: 100px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .confidence-bar.high { background: linear-gradient(90deg, #10b981, #34d399); }
    .confidence-bar.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .confidence-bar.low { background: linear-gradient(90deg, #ef4444, #f87171); }

    .confidence-label {
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .confidence-label.high { color: #059669; }
    .confidence-label.medium { color: #d97706; }
    .confidence-label.low { color: #dc2626; }

    .symptom-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 0.5rem;
    }
    .symptom-tag {
        background: linear-gradient(135deg, #ede9fe, #e0e7ff);
        color: #4338ca;
        font-size: 0.73rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 50px;
        border: 1px solid rgba(99, 102, 241, 0.15);
    }

    /* ========== STATS MINI CARDS ========== */
    .stats-row {
        display: flex;
        gap: 10px;
        margin-bottom: 1rem;
    }
    .stat-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        transition: transform 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C5CE7, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 2px;
    }

    /* ========== CHAT STYLING ========== */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 0.4rem 0rem !important;
    }

    .stChatMessage[data-testid="stChatMessageUser"] {
        flex-direction: row-reverse !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] > div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #6C5CE7, #a855f7) !important;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px !important;
        border: none !important;
        padding: 12px 18px !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.25);
        max-width: 78% !important;
        margin-right: 8px !important;
        margin-left: auto !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] > div[data-testid="stChatMessageContent"] p {
        color: #ffffff !important;
    }

    .stChatMessage[data-testid="stChatMessageAssistant"] {
        flex-direction: row !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] > div[data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        color: #1e1b4b !important;
        border-radius: 18px 18px 18px 4px !important;
        border: 1px solid rgba(108, 92, 231, 0.1) !important;
        padding: 14px 20px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        max-width: 85% !important;
        margin-left: 8px !important;
    }

    /* ========== CHAT INPUT ========== */
    div[data-testid="stChatInput"] {
        background: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 14px !important;
        border: 1.5px solid rgba(108, 92, 231, 0.15) !important;
        box-shadow: 0 2px 15px rgba(108, 92, 231, 0.08) !important;
        margin-top: 10px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: rgba(108, 92, 231, 0.4) !important;
        box-shadow: 0 4px 20px rgba(108, 92, 231, 0.15) !important;
    }

    /* ========== MULTISELECT STYLING ========== */
    .stMultiSelect > div > div {
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1.5px solid rgba(108, 92, 231, 0.12) !important;
        transition: border-color 0.3s ease;
    }
    .stMultiSelect > div > div:hover,
    .stMultiSelect > div > div:focus-within {
        border-color: rgba(108, 92, 231, 0.35) !important;
        box-shadow: 0 2px 12px rgba(108, 92, 231, 0.08) !important;
    }
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #ede9fe, #e0e7ff) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 8px !important;
        color: #4338ca !important;
        font-weight: 500 !important;
    }

    /* ========== STREAMLIT CONTAINERS / BORDERS ========== */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
        background: transparent !important;
    }

    /* ========== INFO / EMPTY STATE ========== */
    .empty-state {
        text-align: center;
        padding: 3rem 1.5rem;
        color: #94a3b8;
    }
    .empty-state .icon-large {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    .empty-state p {
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ========== FOOTER ========== */
    .custom-footer {
        background: linear-gradient(135deg, rgba(108,92,231,0.05), rgba(168,85,247,0.05));
        border: 1px solid rgba(108,92,231,0.08);
        border-radius: 14px;
        padding: 1rem 1.5rem;
        margin-top: 2rem;
        text-align: center;
    }
    .custom-footer p {
        color: #94a3b8;
        font-size: 0.78rem;
        margin: 0;
        font-weight: 400;
    }
    .custom-footer .tech-stack {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-top: 8px;
        flex-wrap: wrap;
    }
    .custom-footer .tech-item {
        color: #6C5CE7;
        font-size: 0.72rem;
        font-weight: 600;
        background: rgba(108, 92, 231, 0.06);
        padding: 3px 10px;
        border-radius: 50px;
    }

    /* ========== DIVIDER ========== */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(108,92,231,0.2), transparent);
        border: none;
        margin: 1rem 0;
    }

    /* ========== SPINNER ========== */
    .stSpinner > div {
        border-top-color: #6C5CE7 !important;
    }

    /* ========== COLUMNS GAP ========== */
    [data-testid="stHorizontalBlock"] {
        gap: 1.5rem !important;
    }

    </style>
""",
    unsafe_allow_html=True,
)


# --- CUSTOM HTML HEADER ---
st.markdown(
    """
    <div class="custom-header">
        <h1>🩺 Hệ Thống Hỗ Trợ Chẩn Đoán & Tư Vấn Y Khoa Thông Minh</h1>
        <p>Kết hợp Đồ thị Tri thức Y khoa (Knowledge Graph) và Trí tuệ Nhân tạo để hỗ trợ chẩn đoán chính xác</p>
        <div class="header-badges">
            <span class="header-badge">🔗 Neo4j Knowledge Graph</span>
            <span class="header-badge">🤖 Ollama AI (gemma3)</span>
            <span class="header-badge">📊 ICD-10 Standard</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

app = MedicalGraphApp()
symptom_list = app.get_all_symptoms()

col1, col2 = st.columns([1.1, 0.9])

with col1:
    # --- SYMPTOM SELECTOR SECTION ---
    st.markdown(
        """
        <div class="section-title">
            <span class="icon icon-blue">📋</span>
            Nhập Triệu Chứng Lâm Sàng
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color: #64748b; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 0.8rem;">'
        "Chọn các triệu chứng quan sát được từ danh sách bên dưới để bắt đầu chẩn đoán.</p>",
        unsafe_allow_html=True,
    )
    user_inputs = st.multiselect(
        "Chọn triệu chứng:",
        options=symptom_list,
        label_visibility="collapsed",
    )

    enable_rerank = st.toggle(
        "🧠Reranking (Tăng độ chính xác chẩn đoán)",
        value=True,
        help="Sử dụng Bác sĩ AI gemma3 hội chẩn và lựa chọn mã bệnh tối ưu từ danh sách ứng viên của Đồ thị Tri thức."
    )

    if user_inputs:
        user_question = None
        if "messages" in st.session_state and st.session_state.messages:
            user_questions = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
            if user_questions:
                user_question = user_questions[-1]
                
        results = app.diagnose(user_inputs, user_question=user_question, enable_rerank=enable_rerank)
        if results:
            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

            # --- CHAT SECTION ---
            st.markdown(
                """
                <div class="section-title">
                    <span class="icon icon-purple">💬</span>
                    Trò Chuyện Với Bác Sĩ Trợ Lý AI
                </div>
                """,
                unsafe_allow_html=True,
            )

            top_disease = results[0]
            ai_note = ""
            if top_disease.get("is_llm_chosen"):
                ai_note = f"\nBác sĩ AI hội chẩn khuyên dùng mã bệnh này với lý do: {top_disease['llm_reason']}."
                
            knowledge_context = (
                f"Bệnh nhân có các triệu chứng: {', '.join(user_inputs)}.\n"
                f"Hệ thống đồ thị tri thức Neo4j phân tích thấy bệnh có khả năng cao nhất là: "
                f"{top_disease['name']} (Mã bệnh ICD-10: {top_disease['id']}) với độ tin cậy {top_disease['confidence']:.2f}%."
                f"{ai_note}\n"
                f"Các triệu chứng đặc trưng đã khớp trong đồ thị: {', '.join(top_disease['matched_symptoms'])}."
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Tạo vùng chứa hội thoại chat
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.messages:
                    avatar_icon = "🔵" if message["role"] == "user" else "🤖"
                    with st.chat_message(message["role"], avatar=avatar_icon):
                        st.markdown(message["content"])

            # Ô nhập liệu
            if user_message := st.chat_input(
                "💡 Đặt câu hỏi tư vấn y khoa tại đây..."
            ):
                with chat_container:
                    with st.chat_message("user", avatar="🔵"):
                        st.markdown(user_message)
                st.session_state.messages.append(
                    {"role": "user", "content": user_message}
                )

                history_str = ""
                for msg in st.session_state.messages[-4:]:
                    role_label = (
                        "Bệnh nhân" if msg["role"] == "user" else "Bác sĩ AI"
                    )
                    history_str += f"{role_label}: {msg['content']}\n"

                prompt_rag = (
                    f"Bạn là một Bác sĩ Trợ lý AI y khoa chuyên nghiệp, tận tâm tại Việt Nam.\n"
                    f"Hãy dựa trên thông tin Đồ thị tri thức y khoa chuẩn xác sau đây:\n"
                    f'"""\n{knowledge_context}\n"""\n\n'
                    f"Lịch sử cuộc trò chuyện trước đó:\n"
                    f"{history_str}\n"
                    f"Hãy dựa vào ngữ cảnh đồ thị và lịch sử trò chuyện trên để trả lời câu hỏi mới nhất của bệnh nhân một cách logic, liên tục.\n"
                    f"Câu hỏi mới nhất: {user_message}\n"
                    f"Trả lời bằng tiếng Việt:"
                )

                with chat_container:
                    with st.spinner("🤖 Bác sĩ AI đang phân tích đồ thị tri thức..."):
                        ai_answer = ask_local_ai(prompt_rag)
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(ai_answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_answer}
                )
                st.rerun()

with col2:
    # --- RESULTS SECTION ---
    st.markdown(
        """
        <div class="section-title">
            <span class="icon icon-green">📊</span>
            Kết Quả Phân Tích Đồ Thị Tri Thức
        </div>
        """,
        unsafe_allow_html=True,
    )
    if user_inputs and "results" in locals() and results:
        # --- MINI STATS ---
        num_symptoms = len(user_inputs)
        num_diseases = len(results)
        avg_confidence = sum(r["confidence"] for r in results) / len(results) if results else 0
        top_confidence = results[0]["confidence"] if results else 0

        st.markdown(
            f"""
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-value">{num_symptoms}</div>
                    <div class="stat-label">Triệu chứng</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{num_diseases}</div>
                    <div class="stat-label">Bệnh khớp</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{top_confidence:.0f}%</div>
                    <div class="stat-label">Cao nhất</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- DISEASE CARDS ---
        for idx, res in enumerate(results):
            confidence = res["confidence"]
            clamped = min(confidence, 100.0)

            if confidence >= 60:
                level = "high"
            elif confidence >= 30:
                level = "medium"
            else:
                level = "low"

            # Build symptom tags HTML
            tags_html = "".join(
                f'<span class="symptom-tag">{s}</span>'
                for s in res["matched_symptoms"]
            )

            rank_emoji = ["🥇", "🥈", "🥉"]
            rank = rank_emoji[idx] if idx < 3 else f"#{idx+1}"

            ai_badge_html = ""
            reason_html = ""
            if res.get("is_llm_chosen"):
                ai_badge_html = '<span style="background: linear-gradient(135deg, #FF007F, #7B2CBF); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; margin-left: 8px; font-weight: bold; display: inline-block; vertical-align: middle;">🩺 Bác sĩ AI Khuyên Dùng</span>'
                if res.get("llm_reason"):
                    reason_html = f'<div style="font-size: 0.8rem; color: #475569; font-style: italic; margin-top: 8px; border-top: 1px dashed #cbd5e1; padding-top: 6px;">💡 <b>Lý do chọn:</b> {res["llm_reason"]}</div>'

            st.markdown(
                f"""
                <div class="disease-card confidence-{level}">
                    <div class="disease-card-header" style="align-items: center;">
                        <div class="disease-name" style="display: flex; align-items: center; flex-wrap: wrap;">{rank} {res['name']}{ai_badge_html}</div>
                        <div class="disease-id">{res['id']}</div>
                    </div>
                    <div class="confidence-label {level}">Độ tin cậy: {confidence:.1f}%</div>
                    <div class="confidence-bar-container">
                        <div class="confidence-bar {level}" style="width: {clamped}%;"></div>
                    </div>
                    <div class="symptom-tags">
                        {tags_html}
                    </div>
                    {reason_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="icon-large">🔍</div>
                <p><strong>Chưa có dữ liệu chẩn đoán</strong><br/>
                Vui lòng chọn ít nhất một triệu chứng lâm sàng<br/>
                ở cột bên trái để bắt đầu phân tích.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --- FOOTER ---
st.markdown(
    """
    <div class="custom-footer">
        <p>Hệ thống hỗ trợ chẩn đoán dựa trên Đồ thị Tri thức Y khoa </p>
        <div class="tech-stack">
            <span class="tech-item">🔗 Neo4j</span>
            <span class="tech-item">🤖 Ollama</span>
            <span class="tech-item">📊 ICD-10</span>
            <span class="tech-item">🐍 Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

app.close()