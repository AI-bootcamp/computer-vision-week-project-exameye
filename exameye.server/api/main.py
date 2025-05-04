from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import cv2
import numpy as np
import math
from collections import defaultdict
import tempfile
import json

import easyocr
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from difflib import SequenceMatcher

app = FastAPI()

# ——— Globals ———
reader = easyocr.Reader(['en'])
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

FILL_RATIO_MIN = 0.5  # >50% fill to count


def process_blank(image: np.ndarray, q_num: int, correct_answer: str, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Locate question box Q{q_num}, crop just to the right, run TrOCR,
    then fuzzy-match against correct_answer.
    """
    # 1) find the printed “4” or “Q4” (or “5” / “Q5”)
    results = reader.readtext(image, detail=1)
    q_box = next((bbox for bbox, text, _ in results
                  if str(q_num) in text.strip() or f"Q{q_num}" in text.strip()),
                 None)
    if q_box is None:
        raise HTTPException(status_code=422, detail=f"Could not find Q{q_num}")

    # 2) crop right of that box
    xs = [pt[0] for pt in q_box]
    ys = [pt[1] for pt in q_box]
    # per-question tweaks
    if q_num == 4:
        top, bot, x_off, width = 10, 10, 5, 100
    else:  # q_num == 5
        top, bot, x_off, width = 5, 5, 30, 200

    y1 = max(min(ys) - top, 0)
    y2 = min(max(ys) + bot, image.shape[0])
    x1 = min(max(xs) + x_off, image.shape[1])
    x2 = min(x1 + width, image.shape[1])
    crop = image[y1:y2, x1:x2]

    # 3) preprocess for TrOCR
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    up = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    rgb = cv2.cvtColor(up, cv2.COLOR_GRAY2RGB)
    pil = Image.fromarray(rgb)

    # 4) run TrOCR
    pv = processor(images=pil, return_tensors="pt").pixel_values
    gen = trocr_model.generate(pv)
    text = processor.batch_decode(gen, skip_special_tokens=True)[0].strip()

    # 5) fuzzy-grade
    toks = text.lower().split()
    if toks:
        best = max(toks, key=lambda t: SequenceMatcher(None, t, correct_answer).ratio())
        score = SequenceMatcher(None, best, correct_answer).ratio()
        is_correct = score >= threshold
    else:
        best, score, is_correct = "", 0.0, False

    return {
        "recognized_text": text,
        "best_match": best,
        "score": round(score, 3),
        "correct": is_correct
    }


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

    # — save upload to disk —
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
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
    # find all candidate circles
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

    # pick top N and sort by vertical
    filled.sort(key=lambda t: t[1])
    filled = filled[:num_questions]

    # group by row
    groups = defaultdict(list)
    for x, y, r in candidates:
        # assign to closest filled row
        idx = min(range(len(filled)), key=lambda i: abs(filled[i][1] - y))
        groups[idx].append((x, y, r))

    # determine choices
    detected_answers = {}
    for qi, (fx, fy, fr) in enumerate(filled, start=1):
        row = groups[qi - 1]
        above = sum(1 for (_, yy, _) in row if yy < fy)
        above = min(above, choices_per_q - 1)
        detected_answers[qi] = chr(65 + above)

    mcq_correct = sum(
        detected_answers.get(q) == user_answers_dict.get(q)
        for q in range(1, num_questions + 1)
    )

    # — handwritten-blank grading for Q4 & Q5 —
    blank_results = {
        "Q4": process_blank(orig, 4, "relu"),
        "Q5": process_blank(orig, 5, "lasso"),
    }

    return JSONResponse({
        "mcq_score": mcq_correct,
        "mcq_total": num_questions,
        "detected_answers": detected_answers,
        "expected_answers": user_answers_dict,
        "blank_results": blank_results
    })