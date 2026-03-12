from pydantic import BaseModel, Field
from typing import Literal, Optional

class PRPredictRequest(BaseModel):
    exercise_title: str = Field(..., description="Exercise name exactly as in your log")
    weight_kg: float    = Field(..., gt=0)
    reps: int           = Field(..., ge=1, le=50)
    set_type: Literal["normal", "warmup", "dropset"] = "normal"
    set_index: int      = Field(default=0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "exercise_title": "Bench Press (Barbell)",
                "weight_kg": 80.0,
                "reps": 5,
                "set_type": "normal",
                "set_index": 2
            }
        }

class PRPredictResponse(BaseModel):
    exercise_title:    str
    predicted_1rm_kg:  float
    predicted_1rm_lbs: float
    epley_estimate_kg: float
    confidence_range:  dict
    personal_best_kg:  Optional[float] = None
    message:           str
