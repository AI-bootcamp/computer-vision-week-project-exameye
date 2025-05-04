# Exam_Grader.py

import streamlit as st
import requests
import json
import pandas as pd

def main():
    st.set_page_config(page_title="MCQ Exam Grader", page_icon="📝")
    st.title("📄 MCQ Exam Grader")
    st.write("Upload an answer-sheet image and select your answers; this will auto-grade the bubbles.")

    # --- Inputs ---
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    num_questions = st.number_input("Number of questions", min_value=1, step=1, value=5)
    choices_per_q = st.number_input("Choices per question", min_value=2, step=1, value=4)

    # Dynamically generate selectboxes for each question
    answers = {}
    cols = st.columns(min(num_questions, 5))
    for i in range(1, num_questions + 1):
        opts = [chr(65 + j) for j in range(choices_per_q)]
        col = cols[(i - 1) % len(cols)]
        answers[i] = col.selectbox(f"Q{i}", opts, key=f"ans_{i}")

    # --- Grade button ---
    if st.button("🧠 Grade Exam"):
        if not uploaded_file:
            st.error("Please upload an image first.")
            return

        with st.spinner("Grading..."):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            data = {
                "num_questions": num_questions,
                "choices_per_q": choices_per_q,
                "user_answers": json.dumps(answers)
            }

            try:
                resp = requests.post(
                    "http://localhost:8000/grade-exam/",
                    files=files,
                    data=data,
                    timeout=30
                )
                resp.raise_for_status()
            except Exception as e:
                st.error(f"Request failed: {e}")
                return

            result = resp.json()

        # --- Display results ---
        st.success(f"Score: **{result['mcq_score']}** / **{result['mcq_total']}**")
        st.subheader("Detected vs Expected Answers")
        # Build a table
        rows = []
        for q in range(1, num_questions + 1):
            detected = result["detected_answers"].get(str(q), result["detected_answers"].get(q))
            expected = result["expected_answers"].get(str(q), result["expected_answers"].get(q))
            rows.append({"Question": f"Q{q}", "Detected": detected, "Expected": expected})
        df = pd.DataFrame(rows)
        st.table(df)

if __name__ == "__main__":
    main()