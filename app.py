
import streamlit as st
from neo4j import GraphDatabase
import requests  

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""  

OLLAMA_URL = "http://localhost:11434/api/generate"  
MODEL_NAME = "gemma3"


def ask_local_ai(prompt_context):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt_context,
            "stream": False, 
        }
        # Gửi dữ liệu sang container Docker qua cổng 11434
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json().get("response", "")
        return "⚠️ Không thể kết nối với AI Local."
    except Exception as e:
        return f"❌ Lỗi kết nối Ollama: {e}. Hãy chắc chắn Container Docker đang chạy!"


# --- PHẦN KẾT NỐI NEO4J (Giữ nguyên logic cũ của bạn) ---
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

    def diagnose(self, selected_symptoms):
        query = """
        MATCH (d:Disease)-[r:HAS_SYMPTOM]->(s:Symptom)
        WITH d, s, r, CASE WHEN s.name IN $inputs THEN r.weight ELSE 0 END AS matched_weight
        WITH d, sum(matched_weight) AS score_user, sum(r.weight) AS total_disease_weight,
             collect(CASE WHEN s.name IN $inputs THEN s.name END) AS matched_list
        WHERE score_user > 0
        RETURN d.id AS id, d.name AS name, (score_user / total_disease_weight) * 100 AS confidence,
               [x IN matched_list WHERE x IS NOT NULL] AS matched_symptoms
        ORDER BY confidence DESC
        """
        with self.driver.session() as session:
            result = session.run(query, inputs=selected_symptoms)
            return [dict(record) for record in result]


st.set_page_config(page_title="Hệ Thống Chẩn Đoán GraphRAG", layout="wide")
st.title("🩺 Hệ Thống Hỗ Trợ Chẩn Đoán & Tư Vấn Y Khoa Thông Minh")
st.markdown("---")

app = MedicalGraphApp()
symptom_list = app.get_all_symptoms()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Nhập Triệu Chứng")
    user_inputs = st.multiselect(
        "Chọn các triệu chứng lâm sàng quan sát được:", options=symptom_list
    )

    # VÙNG CHAT CHỈ HIỆN KHI NGƯỜI DÙNG ĐÃ CHỌN TRIỆU CHỨNG VÀ CÓ KẾT QUẢ TỪ NEO4J
    if user_inputs:
        results = app.diagnose(user_inputs)
        if results:
            st.write("---")
            st.subheader("💬 Trò chuyện với Bác sĩ Trợ lý AI (Local)")

            # BƯỚC NÀY CỰC KỲ QUAN TRỌNG: Đóng gói dữ liệu từ đồ thị Neo4j làm bộ não thức thời cho AI
            top_disease = results[0]
            knowledge_context = (
                f"Bệnh nhân có các triệu chứng: {', '.join(user_inputs)}.\n"
                f"Hệ thống đồ thị tri thức Neo4j phân tích thấy bệnh có khả năng cao nhất là: "
                f"{top_disease['name']} (Mã bệnh ICD-10: {top_disease['id']}) với độ tin cậy {top_disease['confidence']:.2f}%.\n"
                f"Các triệu chứng đặc trưng đã khớp trong đồ thị: {', '.join(top_disease['matched_symptoms'])}."
            )

            # Ô nhập câu hỏi chat
            user_message = st.text_input(
                "Đặt câu hỏi cho AI (Ví dụ: Bệnh này có nguy hiểm không? Nên ăn kiêng gì?):",
                placeholder="Nhập nội dung hỏi tại đây...",
            )

            if user_message:
                with st.spinner("🤖 Bác sĩ AI đang đọc đồ thị và suy nghĩ..."):
                    # Thiết kế Prompt ép AI phải trả lời dựa trên Đồ thị tri thức Bộ Y Tế, không được bịa đặt
                    prompt_rag = (
                        f"Bạn là một Bác sĩ Trợ lý AI y khoa chuyên nghiệp, tận tâm tại Việt Nam.\n"
                        f"Hãy dựa trên thông tin Đồ thị tri thức y khoa chuẩn xác sau đây:\n"
                        f"\"\"\"\n{knowledge_context}\n\"\"\"\n"
                        f"Trả lời câu hỏi của bệnh nhân một cách khoa học, dễ hiểu, đưa ra lời khuyên y tế hữu ích.\n"
                        f"Câu hỏi bệnh nhân: {user_message}\n"
                        f"Trả lời bằng tiếng Việt:"
                    )
                    ai_answer = ask_local_ai(prompt_rag)
                    # Hiển thị câu trả lời dạng khung Chat chuyên nghiệp
                    st.chat_message("assistant").write(ai_answer)

with col2:
    st.header("📊 Kết Quả Phân Tích Đồ Thị Tri Thức")
    if user_inputs and "results" in locals():
        for res in results:
            with st.container(border=True):
                st.write(f"### **{res['id']} - {res['name']}**")
                st.progress(min(res["confidence"] / 100.0, 1.0))
                st.write(
                    f"🔸 Triệu chứng trùng khớp: *{', '.join(res['matched_symptoms'])}*"
                )
    else:
        st.info("👉 Vui lòng chọn ít nhất một triệu chứng ở cột bên trái.")

app.close()