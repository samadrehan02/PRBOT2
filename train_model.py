import os, pandas as pd
from app.utils.preprocessor import load_and_preprocess
from app.models.ml_model import train_and_save

os.makedirs("models_saved", exist_ok=True)

df = load_and_preprocess("app/data/workout_data.csv")
print(f"Loaded {len(df)} weighted sets")
print(f"Exercises: {df['exercise_title'].nunique()} unique")
print(f"Date range: {df['start_time'].min()} → {df['start_time'].max()}")

train_and_save(df)
