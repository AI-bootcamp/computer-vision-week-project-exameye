import cv2  # You missed this
import streamlit as st
from PIL import Image
import base64
import numpy as np

# Function to set background image
def add_bg_from_base64(base64_string):
    base64_img = f"""
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
    .feature-card {{
        background-color: #f1f5f9;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
        color: #000000 !important;
    }}
    .icon-text {{
        color: #000000 !important;
        font-size: 1.8rem;
        margin-right: 0.5rem;
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
    st.markdown(base64_img, unsafe_allow_html=True)



def main():
    st.set_page_config(
        page_title="ExamEye - Automated Exam Grading",
        page_icon="📘",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom background
    # You can replace this with an actual base64 encoded background image
    # For now, using a simple placeholder
    def get_base64_of_image(path):
     with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

    bg_image_base64 = get_base64_of_image("pic1.jpg")
    add_bg_from_base64(bg_image_base64)
    
    # Two-column layout for hero section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<h1 class="main-title">ExamEye</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Automated Grading System Powered by Computer Vision</p>', unsafe_allow_html=True)
        
        st.markdown("""
        ExamEye transforms how educators grade exams by automating the process
        with powerful computer vision technology. Save hours of manual work and
        provide students with faster feedback.
        """)
            
    
    st.markdown("---")
    
    
    # How It Works section
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
    
    # Technology section
    st.markdown("## 🔬 Technology")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Computer Vision")
        st.markdown("""
        - **OpenCV**: Advanced image processing for bubble detection
        - **Contour Analysis**: Precise identification of filled answers
        - **Spatial Recognition**: Smart grouping of questions and options
        """)
        
    with col2:
        st.markdown("### Text Recognition")
        st.markdown("""
        - **Tesseract OCR**: Converting handwritten text to digital
        - **NLP Processing**: Evaluating text answer correctness
        - **Fuzzy Matching**: Accounting for spelling variations
        """)
    
    # Testimonials (placeholder)
    st.markdown("## 💬 What Educators Say")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('> *"ExamEye saved me hours of grading time each week. Highly recommended for any educator with multiple-choice assessments."*')
        st.markdown("**- Dr. Sarah Johnson, University Professor**")
        
    with col2:
        st.markdown('> *"The accuracy is impressive. It correctly identified even lightly marked answers that I might have missed."*')
        st.markdown("**- Michael Chen, High School Teacher**")
        
    with col3:
        st.markdown('> *"Students appreciate getting their results faster, and I can focus more on addressing knowledge gaps rather than grading."*')
        st.markdown("**- Lisa Rodriguez, Middle School Educator**")
    
    # Call to action
    st.markdown("---")
    
    st.markdown("## Ready to streamline your grading process?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.button("🚀 Start Grading Now", key="start_grading_bottom")
        st.markdown("*Upload your first answer sheet in less than 2 minutes*")

if __name__ == "__main__":
    main()