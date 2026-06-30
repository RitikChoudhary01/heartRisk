from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Heart Disease Prediction API")

# Allow CORS for React frontend (Vite usually runs on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models on startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model = joblib.load(os.path.join(BASE_DIR, "LogisticRegression.pkl"))
    scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
    expected_columns = joblib.load(os.path.join(BASE_DIR, "columns.pkl"))
except Exception as e:
    model, scaler, expected_columns = None, None, None
    print(f"Error loading models: {e}")

class PatientData(BaseModel):
    age: int
    sex: str
    chest_pain: str
    resting_bp: float
    cholesterol: float
    fasting_bs: int
    resting_ecg: str
    max_hr: float
    exercise_angina: str
    oldpeak: float
    st_slope: str

@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API is running!"}

@app.post("/predict")
def predict_risk(data: PatientData):
    if not model:
        raise HTTPException(status_code=500, detail="Machine Learning model is not loaded.")
        
    try:
        # 1. Map to expected model format
        raw_input = {
            'Age': data.age,
            'RestingBP': data.resting_bp,
            'Cholesterol': data.cholesterol,
            'FastingBS': data.fasting_bs,
            'MaxHR': data.max_hr,
            'Oldpeak': data.oldpeak,
            f'Sex_{data.sex}': 1,
            f'ChestPainType_{data.chest_pain}': 1,
            f'RestingECG_{data.resting_ecg}': 1,
            f'ExerciseAngina_{data.exercise_angina}': 1,
            f'ST_Slope_{data.st_slope}': 1
        }
        
        # 2. Create dataframe
        input_df = pd.DataFrame([raw_input])
        
        # 3. Fill missing columns with 0
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0
                
        # 4. Reorder
        input_df = input_df[expected_columns]
        
        # 5. Scale and Predict
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
        
        # Convert NumPy int to Python int for JSON serialization
        return {"risk_prediction": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
