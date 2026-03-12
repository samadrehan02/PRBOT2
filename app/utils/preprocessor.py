import pandas as pd

EXERCISE_CATEGORIES = {
    "compound_push": ["Bench Press", "Incline Bench Press", "Decline Bench Press",
                      "Overhead Press", "Shoulder Press", "Chest Press", "Push Up", "Chest Dip"],
    "compound_pull": ["Pull Up", "Chin Up", "Lat Pulldown", "Bent Over Row",
                      "Dumbbell Row", "T Bar Row", "Iso-Lateral Row", "Seated Row",
                      "Reverse Grip Lat Pulldown"],
    "compound_legs": ["Squat", "Leg Press", "Romanian Deadlift", "Deadlift"],
    "isolation":     ["Bicep Curl", "Hammer Curl", "Preacher Curl", "Triceps",
                      "Lateral Raise", "Leg Extension", "Leg Curl", "Calf Raise",
                      "Butterfly", "Shrug"],
}

def get_exercise_category(exercise_title: str) -> str:
    for category, keywords in EXERCISE_CATEGORIES.items():
        if any(kw.lower() in exercise_title.lower() for kw in keywords):
            return category
    return "other"

def load_and_preprocess(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[df["weight_kg"].notna() & df["reps"].notna()].copy()
    df = df[df["weight_kg"] > 0].copy()

    df["set_type"]  = df["set_type"].fillna("normal")
    df["set_index"] = df["set_index"].fillna(0).astype(int)

    df["volume"]   = df["weight_kg"] * df["reps"]
    df["epley_1rm"] = df.apply(
        lambda r: r["weight_kg"] if r["reps"] == 1
        else r["weight_kg"] * (1 + r["reps"] / 30),
        axis=1
    )
    df["exercise_category"] = df["exercise_title"].apply(get_exercise_category)
    return df
