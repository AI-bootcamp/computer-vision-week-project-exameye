import cv2
import streamlit as st
from PIL import Image
import base64
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Home | ExamEye",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper functions (can stay outside)
def get_base64_of_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def add_bg_from_base64(base64_string):
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("pic1.jpg,{base64_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .block-container {{
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }}
    h1, h2, h3, p, li, span, div {{
        color: #000000 !important;
    }}
    .main-title {{
        font-size: 3rem !important;
        font-weight: 800;
        margin-bottom: 0;
        background: none !important;
        color: #000000 !important;
        -webkit-background-clip: none !important;
    }}
    .subtitle {{
        font-size: 1.3rem !important;
        color: #000000 !important;
        margin-top: 0.5rem;
    }}
    .stButton button {{
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 30px;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Apply background
bg_image_base64 = get_base64_of_image("pic1 (1).jpg")
add_bg_from_base64(bg_image_base64)

# Logo and welcome section
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    logo_base64 = get_base64_of_image("3330bf49-c818-4f5c-8a94-2053f85ac648.jpg")
    st.markdown(f'''
        <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;">
            <img src="data:image/jpg;base64,{logo_base64}" width="190" />
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('<p class="subtitle" style="text-align:center;">Automated Grading System Powered by Computer Vision</p>', unsafe_allow_html=True)
    st.markdown("""<p style="text-align:center;">ExamEye transforms how educators grade exams by automating the process
    with powerful computer vision technology. Save hours of manual work and provide students with faster feedback.</p>""", unsafe_allow_html=True)

# Sections
st.markdown("---")
st.markdown("## 🔄 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1. Upload")
    st.markdown("Upload scanned exam sheets through our simple interface.")

with col2:
    st.markdown("### 2. Process")
    st.markdown("Our CV algorithms identify and analyze answers automatically.")

with col3:
    st.markdown("### 3. Grade")
    st.markdown("Answers are compared to your key and scored instantly.")

with col4:
    st.markdown("### 4. Review")
    st.markdown("Review results, make adjustments, and export final grades.")

st.markdown("---")
st.markdown("## 🔬 Technology")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Computer Vision")
    st.markdown("""- **OpenCV**: Advanced image processing for bubble detection  
    - **Contour Analysis**: Precise identification of filled answers  
    - **Spatial Recognition**: Smart grouping of questions and options""")

with col2:
    st.markdown("### Text Recognition")
    st.markdown("""- **Tesseract OCR**: Converting handwritten text to digital  
    - **NLP Processing**: Evaluating text answer correctness  
    - **Fuzzy Matching**: Accounting for spelling variations""")

st.markdown("---")

# CTA Button
st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
    <button style="
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 30px;
        font-size: 1rem;
        border: none;
        cursor: pointer;
    ">🚀 Start Grading Now</button>
    <p style="margin-top: 0.5rem;"><em>Upload your first answer sheet in less than 2 minutes</em></p>
</div>
""", unsafe_allow_html=True)