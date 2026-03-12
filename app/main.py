from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.predict import router as predict_router
from app.routes.exercises import router as exercises_router

app = FastAPI(
    title="Gym PR Predictor API",
    description="Predict your 1RM using your personal workout history",
    version="1.0.0"
)

# ── CORS (allows the HTML page to call the API) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ──
app.include_router(predict_router, tags=["Prediction"])
app.include_router(exercises_router, tags=["Exercises"])

# ── Serve frontend ──
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
async def health():
    return {"status": "ok"}
