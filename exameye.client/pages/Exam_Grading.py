# app.py (Streamlit frontend)

import streamlit as st
import tempfile
import base64
import requests
import json
import io

st.set_page_config(
    page_title="Exam Grading | ExamEye",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper: Convert image to base64 ---
def get_base64_of_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Centered Logo ---
logo_base64 = get_base64_of_image("public/logo.jpg")
st.markdown(f"""
<div style="text-align: center;">
    <img src="data:image/jpg;base64,{logo_base64}" width="190" />
    <h3>Exam Grading Panel Powered by Computer Vision</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("Upload a scanned **image** of an exam answer sheet (only PNG/JPG) and provide grading details.")

# --- File uploader (images only now) ---
uploaded_file = st.file_uploader("📤 Upload Answer Sheet", type=["png", "jpg", "jpeg"])
file_bytes = None
file_type = None

if uploaded_file:
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type

    st.image(file_bytes, caption="Uploaded Answer Sheet", use_container_width=True)

# --- MCQ Inputs ---
num_questions = st.number_input("🔢 Number of Questions",   min_value=1, value=3, step=1)
choices_per_q = st.number_input("🔠 Choices per Question",  min_value=2, max_value=4, value=4, step=1)

st.markdown("### 📝 Multiple-Choice Answer Key")
user_answers = {}
options = ["A", "B", "C", "D"][:choices_per_q]
for i in range(1, int(num_questions) + 1):
    user_answers[str(i)] = st.selectbox(f"Question {i}", options, key=f"mcq_q{i}")

# --- Fill-in-the-Blank Inputs ---
st.markdown("### ✍ Fill-in-the-Blank Answer Key")
num_blanks = st.number_input(
    "How many fill-in-the-blank questions?", min_value=0, value=2, step=1
)
fill_answers = {}
for i in range(1, int(num_blanks) + 1):
    qnum = st.number_input(
        f"Blank #{i} → question number", min_value=1, value=i, step=1, key=f"blank_q{i}"
    )
    ans = st.text_input(
        f"Expected text for Q{qnum}", key=f"blank_a{i}"
    )
    fill_answers[str(qnum)] = ans

st.markdown("##")
col1, col2, col3 = st.columns([2,2,2])
with col2:
    if st.button("🚀 Grade Now", use_container_width=True):
        if not uploaded_file:
            st.warning("📎 Please upload an image before grading.")
        else:
            # package upload
            with st.spinner("⏳ Sending to grading server…"):
                files = {
                    "file": (
                        uploaded_file.name,
                        io.BytesIO(file_bytes),
                        file_type
                    )
                }
                data = {
                    "num_questions": str(num_questions),
                    "choices_per_q": str(choices_per_q),
                    "user_answers": json.dumps(user_answers),
                    "fill_answers": json.dumps(fill_answers)
                }

                resp = requests.post(
                    "http://127.0.0.1:8000/grade-exam/",
                    files=files,
                    data=data
                )

            if resp.status_code != 200:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")
            else:
                st.success("🎉 Exam graded successfully!")
                result = resp.json()

                # MCQ Results
                mcq = result["mcq"]
                st.markdown("## 📝 Multiple-Choice Results")
                st.write(f"**Score:** {mcq['score']} / {mcq['total']}")
                st.write("**Detected:**", mcq["detected"])
                st.write("**Expected:**", mcq["expected"])

                # Fill-in-the-Blank Results
                fb = result["fill_blanks"]
                st.markdown("## ✍ Fill-in-the-Blank Results")
                st.write(f"**Score:** {fb['score']} / {fb['total']}")
                for q, detail in fb["details"].items():
                    if "error" in detail:
                        st.write(f"• Q{q}: ❓ {detail['error']}")
                    else:
                        mark = "✅" if detail["correct"] else "❌"
                        sim = detail["similarity"] * 100
                        st.write(
                            f"• Q{q}: recognized “{detail['recognized']}”, "
                            f"match “{detail['best_match']}” ({sim:.1f}% vs “{detail['expected']}”) {mark}"
                        )