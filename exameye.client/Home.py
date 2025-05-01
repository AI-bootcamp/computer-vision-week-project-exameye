import streamlit as st

st.set_page_config(page_title="Home | ExamEye", page_icon="📘")

st.markdown("## 📘 Welcome to ExamEye", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
### 🧠 What is ExamEye?

**ExamEye** is an intelligent exam assessor that uses **Computer Vision** and **OCR** technologies to automatically check and grade student answer sheets.

### 🛠 Features
- 📝 **Multiple Choice Question** auto-detection
- ✍️ **Fill-in-the-Blank** extraction and scoring
- 📤 Easy file upload (PDF or image)
- 📈 Real-time feedback with scoring and extracted text

---

ℹ️ **Get Started:**  
Use the sidebar to go to the **Exam Grading** page and upload your answer sheet.
""")