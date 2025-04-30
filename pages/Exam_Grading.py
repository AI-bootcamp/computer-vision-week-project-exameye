import streamlit as st
import tempfile
import base64
from PIL import Image

st.set_page_config(page_title="Exam Grading | ExamEye", page_icon="📝")

st.markdown("## 📝 Exam Grading Panel", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Upload a scanned image **or PDF** of an exam answer sheet to preview it before grading.")

uploaded_file = st.file_uploader("📤 Upload Answer Sheet", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if uploaded_file.type == "application/pdf":
        # Save PDF to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_pdf_path = tmp_file.name

        # Encode PDF to base64
        with open(temp_pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        st.markdown("### 📄 PDF Preview")
        st.markdown(f'''
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>
        ''', unsafe_allow_html=True)

    else:
        image = Image.open(uploaded_file)
        st.markdown("### 🖼️ Image Preview")
        st.image(image, caption="Uploaded Answer Sheet", use_column_width=True)

    st.info("✅ Ready for processing once grading is implemented.")
else:
    st.warning("📎 Please upload an exam sheet to begin.")