from fastapi import APIRouter, HTTPException
from app.models.schemas import PRPredictRequest, PRPredictResponse
from app.models.ml_model import load_model, predict_1rm
from app.utils.formulas import epley_1rm
from app.utils.preprocessor import get_exercise_category
import os, pandas as pd
from typing import Optional

router   = APIRouter()
DATA_PATH = "app/data/workout_data.csv"

def get_personal_best(exercise_title: str) -> Optional[float]:
    try:
        df = pd.read_csv(DATA_PATH)
        df = df[(df["exercise_title"] == exercise_title)
                & df["weight_kg"].notna() & df["reps"].notna()
                & (df["weight_kg"] > 0)]
        if df.empty:
            return None
        df["epley"] = df["weight_kg"] * (1 + df["reps"] / 30)
        return round(float(df["epley"].max()), 2)
    except Exception:
        return None

@router.post("/predict/pr", response_model=PRPredictResponse)
async def predict_pr(request: PRPredictRequest):
    if not os.path.exists("models_saved/pr_model.pkl"):
        raise HTTPException(503, detail="Model not trained. Run: python train_model.py")

    model    = load_model()
    epley    = epley_1rm(request.weight_kg, request.reps)
    category = get_exercise_category(request.exercise_title)

    input_dict = {
        "exercise_title":    request.exercise_title,
        "weight_kg":         request.weight_kg,
        "reps":              request.reps,
        "set_type":          request.set_type,
        "set_index":         request.set_index,
        "volume":            request.weight_kg * request.reps,
        "epley_1rm":         epley,
        "exercise_category": category,
    }

    predicted     = predict_1rm(model, input_dict)
    personal_best = get_personal_best(request.exercise_title)
    pr_note       = f" Your log PR is {personal_best} kg." if personal_best else ""

    return PRPredictResponse(
        exercise_title    = request.exercise_title,
        predicted_1rm_kg  = round(predicted, 2),
        predicted_1rm_lbs = round(predicted * 2.20462, 2),
        epley_estimate_kg = round(epley, 2),
        confidence_range  = {"low": round(predicted * 0.95, 2), "high": round(predicted * 1.05, 2)},
        personal_best_kg  = personal_best,
        message           = f"Predicted 1RM: {round(predicted, 1)} kg.{pr_note}"
    )
