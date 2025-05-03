**Exam Eye**

Exam Eye is an automated grading system that uses OCR to extract and evaluate student answers from uploaded exam images. 
It supports two question types: Multiple Choice Questions (MCQs) and Fill-in-the-Blank. 
Built with a simple and interactive Streamlit interface, Exam Eye provides fast and accurate grading with minimal manual effort.


✨ Features:
📋 Automatic Grading for MCQs: Instantly grades multiple-choice questions based on predefined answer keys.

📝 Fill-in-the-Blank Evaluation: Evaluates fill-in-the-blank responses using customizable matching techniques.

🧑‍🏫 Streamlit File Upload: Instructors can upload answer keys and student responses via a user-friendly Streamlit interface.

📊 Result Reporting: Generates comprehensive and exportable grading reports.


👥 Team Member: 
This project was developed by a dedicated team of five:

-Ezdhar Altamimi 

-Alhanouf Al-Suwaid

-Mohanad

-Faisal 

-Marwan


📁 Project Structure:
exam-eye/
├── codes/
|   ├── MCQ_Final_Edition.py
│   └── fill_blank.py
├── requirements.txt
├── deployment/
│   ├── app.py            # Streamlit frontend
│   └── api.py            # FastAPI backend
└── README.md


🛠️ Tools & Libraries:
Python - Programming language used for all project components
pandas - Data manipulation and analysis (handling DataFrames of network traffic features)
FastAPI - Creating a RESTful API for serving the trained models (backend deployment)
Streamlit - Building an interactive web application frontend for live model interaction
Tesseract OCR - Extracts text from exam images
OpenCV / PIL - Image preprocessing

🚀 Getting Started:
1. Clone the Repository
git clone https://github.com/AI-bootcamp/computer-vision-week-project-exameye

2. Install Python Dependencies
Make sure you have Python 3.10+ installed.
You can install all the required Python packages with:
pip install -r requirements.txt

3. Run the Streamlit Frontend
In a terminal, run the Streamlit app with:
streamlit run deployment/app.py

4. Run the FastAPI Backend
In another terminal window, start the FastAPI server with Uvicorn:
uvicorn deployment.main:app --reload
