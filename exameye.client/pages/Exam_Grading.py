import streamlit as st
import tempfile
import base64
import requests
import json
from PIL import Image

st.set_page_config(page_title="Exam Grading | ExamEye", page_icon="📝")

st.markdown("## 📝 Exam Grading Panel", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Upload a scanned image of an exam answer sheet and provide grading details.")

uploaded_file = st.file_uploader("📤 Upload Answer Sheet", type=["png", "jpg", "jpeg"])

with st.form("grading_form"):
    num_questions = st.number_input("🔢 Number of Questions", min_value=1, value=3)
    choices_per_q = st.number_input("🔠 Choices per Question", min_value=2, max_value=4, value=4)

    st.markdown("### 📝 Select Your Answers:")

    user_answers = {}
    options = ["A", "B", "C", "D"][:choices_per_q]

    for i in range(1, int(num_questions) + 1):
        user_answers[str(i)] = st.selectbox(
            f"Question {i}", options, key=f"q{i}"
        )

    submit_btn = st.form_submit_button("🚀 Grade Now")

if uploaded_file and submit_btn:
    try:
        st.info("⏳ Sending to grading server...")

        # Save uploaded image to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            files = {"file": (uploaded_file.name, f, uploaded_file.type)}
            data = {
                "num_questions": str(num_questions),
                "choices_per_q": str(choices_per_q),
                "user_answers": json.dumps(user_answers)
            }

            response = requests.post("http://127.0.0.1:8000/grade-exam/", files=files, data=data)

        if response.status_code == 200:
            st.success("🎉 Exam graded successfully!")
            result = response.json()
            st.markdown(f"### 🧾 Result:\n**{result['result']}**")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

elif submit_btn and not uploaded_file:
    st.warning("📎 Please upload an image before grading.")