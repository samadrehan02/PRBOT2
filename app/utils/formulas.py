def epley_1rm(weight: float, reps: int) -> float:
    if reps == 1:
        return weight
    return weight * (1 + reps / 30)

def brzycki_1rm(weight: float, reps: int) -> float:
    if reps >= 37:
        return weight
    return weight * 36 / (37 - reps)
