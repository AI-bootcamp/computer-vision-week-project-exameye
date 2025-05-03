# Exam Eye

## Automated Exam Grading with OCR and image processing

Exam Eye is an automated grading system that uses Optical Character Recognition (OCR) to extract and evaluate student answers from uploaded exam images. Built with a simple and interactive Streamlit interface, it provides fast and accurate grading with minimal manual effort.

## Key Features

- **OCR-Powered Assessment**: Extract text from exam papers automatically
- **Multiple Question Types**: Supports Multiple Choice Questions (MCQs) and Fill-in-the-Blank questions
- **User-Friendly Interface**: Built with Streamlit for intuitive interaction
- **Result Analysis**: Generate statistics and performance insights

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **OCR Engine**: TrOCR/EasyOCR
- **Image Processing**: OpenCV
- **Data Analysis**: Pandas, NumPy

## Installation

```bash
# Clone the repository
git clone https://github.com/AI-bootcamp/computer-vision-week-project-exameye
cd exam-eye

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
streamlit run app.py
```

2. Access the interface at [http://localhost:8501](http://localhost:8501)

3. Upload exam template with answer key

4. Upload student exams

5. Configure grading settings

6. View and export results

## Project Structure

```
exam-eye/
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── modules/
│   ├── ocr.py              # OCR functionality
│   └── preprocessing.py    # Image preprocessing
└── README.md               # readme file
```

## Contributors

This project is developed by:
- Ezdhar Altamimi
- Alhanouf Alswayed
- Mohanad Abouassonon 
- Faisal Almufarrih 
- Mrawan Alhinidi 

## Future Enhancements

- Support for additional question types (essays, short answers)
- Machine learning-based answer evaluation
- Integration with learning management systems
- Mobile application support
