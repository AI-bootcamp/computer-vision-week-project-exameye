# backend.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import cv2
import numpy as np
import math
from collections import defaultdict
import tempfile
import json

app = FastAPI()

# >50% fill to count
FILL_RATIO_MIN = 0.5

@app.post("/grade-exam/")
async def grade_exam(
    file: UploadFile = File(...),
    num_questions: int = Form(...),
    choices_per_q: int = Form(...),
    user_answers: str = Form(...)  # JSON e.g. '{"1":"A", "2":"C", …}'
):
    # — parse user answers —
    try:
        ua = json.loads(user_answers)
        user_answers_dict = {int(k): v for k, v in ua.items()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user_answers JSON: {e}")

    # — save upload to temp file —
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    # — load image —
    orig = cv2.imread(tmp_path)
    if orig is None:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    # — bubble (MCQ) grading —
    resized = cv2.resize(orig, (800, int(orig.shape[0] * 800 / orig.shape[1])))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # find candidate circles
    candidates = []
    for c in cnts:
        area = cv2.contourArea(c)
        if not (200 < area < 5000):
            continue
        (x, y), r = cv2.minEnclosingCircle(c)
        if not (8 < r < 15):
            continue
        candidates.append((int(x), int(y), int(r)))

    # filter the filled-in ones
    filled = []
    for x, y, r in candidates:
        mask = np.zeros_like(gray)
        cv2.circle(mask, (x, y), r, 255, -1)
        filled_px = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
        ratio = filled_px / (math.pi * r * r)
        if ratio > FILL_RATIO_MIN:
            filled.append((x, y, r))

    if len(filled) < num_questions:
        raise HTTPException(status_code=422, detail="Not enough filled bubbles detected.")

    # keep the top N by vertical position
    filled.sort(key=lambda t: t[1])
    filled = filled[:num_questions]

    # group by row to distinguish columns
    groups = defaultdict(list)
    for x, y, r in candidates:
        idx = min(range(len(filled)), key=lambda i: abs(filled[i][1] - y))
        groups[idx].append((x, y, r))

    # determine selected choice per question
    detected_answers = {}
    for qi, (fx, fy, fr) in enumerate(filled, start=1):
        row = groups[qi - 1]
        # count how many bubbles are above the filled one
        above = sum(1 for (_, yy, _) in row if yy < fy)
        above = min(above, choices_per_q - 1)
        detected_answers[qi] = chr(65 + above)  # 0→A, 1→B, etc.

    mcq_correct = sum(
        detected_answers.get(q) == user_answers_dict.get(q)
        for q in range(1, num_questions + 1)
    )

    return JSONResponse({
        "mcq_score": mcq_correct,
        "mcq_total": num_questions,
        "detected_answers": detected_answers,
        "expected_answers": user_answers_dict
    })