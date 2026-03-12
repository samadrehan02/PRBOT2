import joblib, pandas as pd
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

MODEL_PATH  = "models_saved/pr_model.pkl"
CATEGORICAL = ["exercise_title", "set_type", "exercise_category"]
NUMERICAL   = ["weight_kg", "reps", "set_index", "volume", "epley_1rm"]

def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ("num", StandardScaler(), NUMERICAL),
    ])
    return Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBRegressor(
            n_estimators=300, learning_rate=0.05,
            max_depth=6, subsample=0.8,
            colsample_bytree=0.8, random_state=42
        ))
    ])

def train_and_save(df: pd.DataFrame):
    X = df[CATEGORICAL + NUMERICAL]
    y = df["epley_1rm"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.2f} kg  |  R²: {r2_score(y_test, preds):.4f}")

    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved → {MODEL_PATH}")
    return pipeline

def load_model():
    return joblib.load(MODEL_PATH)

def predict_1rm(model, input_dict: dict) -> float:
    return float(model.predict(pd.DataFrame([input_dict]))[0])
