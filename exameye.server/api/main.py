from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import cv2
import numpy as np
import math
from collections import defaultdict
import tempfile
import json

app = FastAPI()

FILL_RATIO_MIN = 0.5  # >50% fill to count


@app.post("/grade-exam/")
async def grade_exam(
    file: UploadFile = File(...),
    num_questions: int = Form(...),
    choices_per_q: int = Form(...),
    user_answers: str = Form(...)  # JSON string e.g., '{"1": "A", "2": "C", "3": "D"}'
):
    try:
        user_answers_dict = json.loads(user_answers)
        user_answers_dict = {int(k): v for k, v in user_answers_dict.items()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user_answers format. Expected JSON string. {str(e)}")

    # Save uploaded file to a temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process uploaded file.")

    # Load and preprocess image
    orig = cv2.imread(tmp_path)
    if orig is None:
        raise HTTPException(status_code=400, detail="Invalid image.")

    resized = cv2.resize(orig, (800, int(orig.shape[0] * 800 / orig.shape[1])))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find candidate bubbles
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for c in cnts:
        area = cv2.contourArea(c)
        if not (200 < area < 5000):
            continue
        (x, y), r = cv2.minEnclosingCircle(c)
        if not (8 < r < 15):
            continue
        candidates.append((int(x), int(y), int(r)))

    # Filter filled circles
    filled = []
    for (x, y, r) in candidates:
        mask = np.zeros_like(gray)
        cv2.circle(mask, (x, y), r, 255, -1)
        filled_px = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
        circle_area = math.pi * (r ** 2)
        ratio = filled_px / circle_area
        if ratio > FILL_RATIO_MIN:
            filled.append((x, y, r))

    if len(filled) < num_questions:
        raise HTTPException(status_code=422, detail="Not enough filled bubbles detected.")

    filled.sort(key=lambda t: t[1])  # Sort top→bottom
    filled = filled[:num_questions]

    # Assign answers
    groups = defaultdict(list)
    for x, y, r in candidates:
        row = min(range(len(filled)), key=lambda i: abs(filled[i][1] - y))
        groups[row].append((x, y, r))

    detected_answers = {}
    for qi, (fx, fy, fr) in enumerate(filled, start=1):
        row = groups[qi - 1]
        above_count = sum(1 for (_, y0, _) in row if y0 < fy)
        above_count = min(above_count, choices_per_q - 1)
        choice = chr(65 + above_count)
        detected_answers[qi] = choice

    # Compare with user answers
    correct = sum(detected_answers.get(q) == user_answers_dict.get(q) for q in range(1, num_questions + 1))
    result_text = (
        f"Student scored {correct} out of {num_questions}.\n\n"
        f"✔️ Detected Answers: {detected_answers}\n"
        f"📝 Expected Answers: {user_answers_dict}"
    )

    return JSONResponse(content={"result": result_text})