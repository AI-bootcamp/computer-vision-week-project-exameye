import streamlit as st
from PIL import Image
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Home | ExamEye",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helpers ---
def get_base64_of_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Centered Logo ---
logo_base64 = get_base64_of_image("public/logo.jpg")
st.markdown(f"""
<div style="text-align: center;">
    <img src="data:image/jpg;base64,{logo_base64}" width="190" />
    <h3>Automated Grading System Powered by Computer Vision</h3>
    <p>ExamEye transforms how educators grade exams by automating the process with powerful computer vision technology.</p>
</div>
""", unsafe_allow_html=True)

# --- How it Works Section ---
st.markdown("---")
st.header("🔄 How It Works")

cols = st.columns(4)
steps = ["1. Upload", "2. Process", "3. Grade", "4. Review"]
descs = [
    "Upload scanned exam sheets through our simple interface.",
    "Our CV algorithms identify and analyze answers automatically.",
    "Answers are compared to your key and scored instantly.",
    "Review results, make adjustments, and export final grades."
]
for col, title, desc in zip(cols, steps, descs):
    with col:
        st.subheader(title)
        st.write(desc)

# --- Technology Section ---
st.markdown("---")
st.header("🔬 Technology")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Computer Vision")
    st.markdown("""- **OpenCV**: Advanced image processing for bubble detection  
- **Contour Analysis**: Precise identification of filled answers  
- **Spatial Recognition**: Smart grouping of questions and options""")

with col2:
    st.subheader("Text Recognition")
    st.markdown("""- **Tesseract OCR**: Converting handwritten text to digital  
- **NLP Processing**: Evaluating text answer correctness  
- **Fuzzy Matching**: Accounting for spelling variations""")

# --- CTA Button (Perfectly Centered using Three Columns) ---
st.markdown("---")
st.markdown("## ")

col1, col2, col3 = st.columns([3, 2, 3])  # Wider outer columns to center the middle one
with col2:
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    if st.button("🚀 Start Grading Now", use_container_width=True):
        st.switch_page("pages/Exam_Grading.py")
    st.markdown("<p style='text-align: center;'>Upload your first answer sheet in less than 2 minutes</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)