
# 🏋️ Gym PR Predictor

A machine learning app that predicts your **1 Rep Max (1RM)** for any exercise — trained entirely on **your own workout history**. Built with XGBoost, served via FastAPI, and wrapped in a sleek dark-mode frontend.

---

## ✨ Features

- 🤖 **ML-powered predictions** using XGBoost trained on your personal workout logs
- 📊 **Personal best lookup** — compares your prediction against your actual log PR
- ⚡ **Epley formula baseline** shown alongside the ML prediction for reference
- 🎯 **Confidence range** displayed as an animated gauge bar
- 🔍 **Exercise autocomplete** with fuzzy search across all exercises in your dataset
- 🕘 **Recent predictions** stored locally and reloadable in one click
- 🌐 **Full-stack** — FastAPI backend + vanilla HTML/CSS/JS frontend, zero frameworks

---

## 🗂️ Project Structure

```
gym-pr-predictor/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, static file serving
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predict.py           # POST /predict/pr
│   │   └── exercises.py         # GET /exercises
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py           # Pydantic request/response models
│   │   └── ml_model.py          # XGBoost pipeline: train, save, predict
│   ├── data/
│   │   └── workout_data.csv     # ← Your exported workout CSV goes here
│   └── utils/
│       ├── __init__.py
│       ├── formulas.py          # Epley & Brzycki 1RM formulas
│       └── preprocessor.py      # Feature engineering + category mapping
│
├── frontend/
│   └── index.html               # Full frontend (no framework)
│
├── models_saved/
│   └── pr_model.pkl             # Auto-generated after training
│
├── train_model.py               # Standalone training script
└── requirements.txt
```

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourname/gym-pr-predictor.git
cd gym-pr-predictor

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Step 1 — Add your workout data

Export your workout CSV from your tracker app and place it at:

```
app/data/workout_data.csv
```

The CSV must have these columns:

| Column | Description |
|---|---|
| `exercise_title` | Name of the exercise |
| `weight_kg` | Weight lifted |
| `reps` | Reps performed |
| `set_type` | `normal`, `warmup`, or `dropset` |
| `set_index` | Set number within the session (0-based) |
| `start_time` | Session start timestamp |

### Step 2 — Train the model

```bash
python train_model.py
```

Output:
```
Loaded 3842 weighted sets
Exercises: 47 unique
Date range: 2025-08-01 → 2025-12-08
MAE: 2.41 kg  |  R²: 0.9912
Saved → models_saved/pr_model.pkl
```

### Step 3 — Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 4 — Open the app

```
http://localhost:8000
```

For the interactive API docs:
```
http://localhost:8000/docs
```

---

## 🔌 API Reference

### `POST /predict/pr`

Predict your 1RM for a given exercise and set.

**Request body:**
```json
{
  "exercise_title": "Bench Press (Barbell)",
  "weight_kg": 80.0,
  "reps": 5,
  "set_type": "normal",
  "set_index": 2
}
```

**Response:**
```json
{
  "exercise_title": "Bench Press (Barbell)",
  "predicted_1rm_kg": 93.45,
  "predicted_1rm_lbs": 206.03,
  "epley_estimate_kg": 93.33,
  "confidence_range": { "low": 88.78, "high": 98.12 },
  "personal_best_kg": 90.67,
  "message": "Predicted 1RM: 93.5 kg. Your log PR is 90.67 kg."
}
```

---

### `GET /exercises`

Returns all exercises present in your workout data.

```json
{
  "exercises": ["Bench Press (Barbell)", "Squat (Barbell)", "..."],
  "count": 47
}
```

---

### `GET /health`

```json
{ "status": "ok" }
```

---

## 🧠 How It Works

1. **Data loading** — Your raw CSV is cleaned and filtered to only weighted sets (cardio/bodyweight rows dropped).

2. **Feature engineering** — Each set row gets derived features:
   - `volume` = `weight_kg × reps`
   - `epley_1rm` = Epley formula result (used as a feature AND training label)
   - `exercise_category` = auto-classified as `compound_push`, `compound_pull`, `compound_legs`, `isolation`, or `other`

3. **Model** — An XGBoost regressor inside a sklearn `Pipeline` with `OneHotEncoder` for categorical features and `StandardScaler` for numerical ones. Trained on all your past sets, predicts the 1RM for any new input.

4. **Personal best** — At prediction time, the API scans your CSV for the highest Epley-estimated 1RM for that exercise across all historical sessions.

---

## ⚙️ Requirements

```
fastapi
uvicorn[standard]
scikit-learn
xgboost
pandas
numpy
joblib
pydantic
python-multipart
```

---

## 📋 Notes

- The model is **personalized** — it learns patterns from your data, not population averages. The more workout history you have, the better it performs.
- Exercises with very few logged sets will fall back closer to the Epley estimate.
- Re-run `train_model.py` anytime you add new data to your CSV to retrain with fresh history.

---

## 📄 License

MIT — do whatever you want with it.