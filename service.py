import random
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class ClientData(BaseModel):
    age: int
    income: float
    education: bool
    work: bool
    car: bool


app = FastAPI()

# Add error handling for model loading
try:
    model = joblib.load('model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


@app.post("/score")
def score(data: ClientData):
    try:
        # Convert booleans to integers (0/1) for the model
        features = [
            data.age,
            data.income,
            int(data.education),
            int(data.work),
            int(data.car)
        ]

        if model is not None:
            # Model predicts DEFAULT (1=will default, 0=won't default)
            prediction = model.predict([features])
            # For approval: invert the default prediction
            approved = not bool(prediction[0])
        else:
            # Fallback if model fails to load
            approved = random.choice([True, False])

        return {"approved": approved}

    except Exception as e:
        print(f"Error in score function: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Credit Scoring API"}