from fastapi import APIRouter
import pandas as pd

router    = APIRouter()
DATA_PATH = "app/data/workout_data.csv"

@router.get("/exercises")
async def list_exercises():
    df = pd.read_csv(DATA_PATH)
    exercises = sorted(df["exercise_title"].dropna().unique().tolist())
    return {"exercises": exercises, "count": len(exercises)}
