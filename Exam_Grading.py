import streamlit as st
import tempfile
from PIL import Image
from model_interface import grade_exam_image  # Import your model logic

st.set_page_config(page_title="Exam Grading", page_icon="📝")

def main():
    st.title("📄 Upload Answer Sheet")
    st.write("Upload a scanned image of an exam sheet to auto-grade it.")

    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Sheet", use_column_width=True)

        if st.button("🧠 Process and Grade"):
            with st.spinner("Analyzing the sheet..."):

                # Save uploaded image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    image.save(tmp_file.name)
                    temp_image_path = tmp_file.name

                # Use your model function
                text, score = grade_exam_image(temp_image_path)

                st.success("Grading complete!")

                st.subheader("📄 Extracted Text:")
                st.text(text)

                st.subheader("✅ Grading Result:")
                st.metric(label="Score", value=f"{score} points")

if __name__ == "__main__":
    main()
