import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie

# ----------------------------------------
# 1. Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Heart Risk Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------
# 2. Custom CSS & Animations
# ----------------------------------------
def local_css():
    st.markdown("""
    <style>
        /* Global Font & Background */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Glassmorphism containers */
        .glass-container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        }

        /* Gradient Text */
        .title-text {
            background: -webkit-linear-gradient(45deg, #FF416C, #FF4B2B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem !important;
            padding-bottom: 10px;
        }

        /* Stlye the main predict button globally */
        div.stButton > button {
            background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 30px;
            padding: 10px 30px;
            transition: all 0.3s ease;
            width: 100%;
        }

        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0px 5px 15px rgba(255, 75, 43, 0.4);
            color: white;
            border: none;
        }
        
        div.stButton > button:active {
            transform: scale(0.98);
        }

        /* Alert Styling */
        .custom-alert {
            padding: 20px;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
            animation: pulse 2s infinite;
        }
        .high-risk {
            background-color: rgba(255, 75, 43, 0.2);
            color: #FF4B2B;
            border: 2px solid #FF4B2B;
        }
        .low-risk {
            background-color: rgba(76, 175, 80, 0.2);
            color: #4CAF50;
            border: 2px solid #4CAF50;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
    </style>
    """, unsafe_allow_html=True)

local_css()

# ----------------------------------------
# 3. Helper Functions
# ----------------------------------------
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Medical / Heart Lottie Animation URL
lottie_heart = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5n8oxcpj.json")

@st.cache_resource
def load_models():
    try:
        model = joblib.load("LogisticRegression.pkl")
        scaler = joblib.load("scaler.pkl")
        expected_columns = joblib.load("columns.pkl")
        return model, scaler, expected_columns
    except Exception as e:
        st.error(f"Error loading model files. Ensure 'LogisticRegression.pkl', 'scaler.pkl', and 'columns.pkl' exist. Details: {e}")
        return None, None, None

model, scaler, expected_columns = load_models()

# ----------------------------------------
# 4. App UI & Layout
# ----------------------------------------
st.markdown('<h1 class="title-text">AI Heart Disease Risk Predictor</h1>', unsafe_allow_html=True)

# Top section with Lottie & Introduction
col1, col2 = st.columns([1, 2])

with col1:
    if lottie_heart:
        st_lottie(lottie_heart, height=250, key="heart_animation")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/875/875564.png", width=200)

with col2:
    st.markdown("""
    ### Welcome to the AI-powered Risk Assessment Tool 🩺
    This application uses Machine Learning to analyze your clinical parameters and predict your risk of developing heart disease.
    
    **Instructions:**
    1. Fill in your personal and clinical details below.
    2. Click **Predict Risk**.
    3. Get instant, AI-driven feedback on your cardiovascular health.
    """)

st.divider()

# Inputs Section
st.markdown("### 📋 Patient Details")

# Use multiple columns for better UI aesthetics
form_col1, form_col2, form_col3 = st.columns(3)

with form_col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("#### Personal Info")
    age = st.slider("Age (Years)", 18, 100, 45, help="Your current age in years.")
    sex = st.selectbox("Sex", ["M", "F"], help="Biological sex.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("#### Symptoms")
    chest_pain = st.selectbox(
        "Chest Pain Type", 
        ["ATA", "NAP", "TA", "ASY"], 
        help="ATA: Atypical Angina, NAP: Non-Anginal Pain, TA: Typical Angina, ASY: Asymptomatic"
    )
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"], help="Do you experience chest pain during exercise?")
    st.markdown('</div>', unsafe_allow_html=True)

with form_col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("#### Vitals")
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120, help="Systolic resting blood pressure.")
    max_hr = st.slider("Max Heart Rate Achieved", 60, 220, 150, help="Maximum heart rate achieved during exercise.")
    st.markdown('</div>', unsafe_allow_html=True)

with form_col3:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("#### Lab Results")
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200, help="Serum cholesterol level.")
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"], help="Resting electrocardiogram results.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("#### ECG Metrics")
    oldpeak = st.slider("Oldpeak", 0.0, 6.0, 1.0, help="ST depression induced by exercise relative to rest.")
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"], help="The slope of the peak exercise ST segment.")
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# 5. Prediction Logic
# ----------------------------------------
predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:
    if st.button("🚀 Predict Risk Now"):
        if model is None:
            st.error("Model is not loaded. Cannot make prediction.")
        else:
            with st.spinner('Analyzing clinical data...'):
                
                # 1. Create a raw input dictionary
                raw_input = {
                    'Age': age,
                    'RestingBP': resting_bp,
                    'Cholesterol': cholesterol,
                    'FastingBS': fasting_bs,
                    'MaxHR': max_hr,
                    'Oldpeak': oldpeak,
                    'Sex_' + sex: 1,
                    'ChestPainType_' + chest_pain: 1,
                    'RestingECG_' + resting_ecg: 1,
                    'ExerciseAngina_' + exercise_angina: 1,
                    'ST_Slope_' + st_slope: 1
                }

                # 2. Create input dataframe
                input_df = pd.DataFrame([raw_input])

                # 3. Fill in missing columns with 0s (for one-hot encoding columns not selected)
                for col in expected_columns:
                    if col not in input_df.columns:
                        input_df[col] = 0

                # 4. Reorder columns to match model's expected input
                input_df = input_df[expected_columns]

                # 5. Scale the input
                scaled_input = scaler.transform(input_df)

                # 6. Make prediction
                prediction = model.predict(scaled_input)[0]

                # 7. Show result beautifully
                st.markdown("<br>", unsafe_allow_html=True)
                if prediction == 1:
                    st.markdown("""
                    <div class="custom-alert high-risk">
                        ⚠️ HIGH RISK DETECTED <br>
                        <span style="font-size: 1rem; font-weight: normal;">Our model indicates a high probability of heart disease. Please consult a healthcare professional immediately.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.balloons()
                    st.markdown("""
                    <div class="custom-alert low-risk">
                        ✅ LOW RISK DETECTED <br>
                        <span style="font-size: 1rem; font-weight: normal;">Your clinical metrics look good. Maintain a healthy lifestyle!</span>
                    </div>
                    """, unsafe_allow_html=True)
