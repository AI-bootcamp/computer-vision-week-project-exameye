import streamlit as st

st.set_page_config(page_title="Home", page_icon="📘")

def main():
    st.set_page_config(page_title="ExamEye - Automated Grading", layout="centered")
    
    st.title("📘 ExamEye")
    st.subheader("Automated Grading System for Exam Sheets")

    st.markdown("""
    **ExamEye** leverages Computer Vision and OCR technologies to automatically grade:
    - 📝 Multiple Choice Questions (MCQs)
    - ✍️ Fill-in-the-Blank questions

    Our system uses **OpenCV** for image processing and **Tesseract OCR** for extracting text from scanned sheets.

    ---
    """)
    
    st.info("To get started, go to the 'Exam Grading' page from the sidebar and upload a scanned answer sheet.")

if __name__ == "__main__":
    main()
