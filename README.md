# AI Heart Disease Risk Predictor ❤️

A state-of-the-art machine learning application to predict the risk of heart disease based on clinical metrics and personal health data.

This repository contains two complete versions of the application:
1. **Option 1:** A 1-click deployable **Streamlit** application (Simplest).
2. **Option 2:** A full-stack **React + FastAPI** architecture (Premium UI & Scalable).

---

## 🌟 Features
- Machine Learning predictions powered by `scikit-learn` (Logistic Regression).
- Real-time clinical data processing and scaling.
- Two gorgeous, modern User Interfaces.
- Fully deployment-ready for 24/7 cloud hosting.

---

## 🚀 Option 1: Streamlit Application (Recommended for simple deployment)
This version runs the ML model and the UI in a single, easy-to-use Python script with premium injected CSS and animations.

### Run Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```

### Deploy to Cloud (24/7 for Free)
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Log in with your GitHub account.
3. Click **New app** and connect this repository.
4. Set the Main file path to `app.py`.
5. Click **Deploy**!

---

## ⚛️ Option 2: Full-Stack React + FastAPI
This version separates the backend ML processing from the frontend user interface, providing an ultra-premium aesthetic and standard industry architecture.

### Backend (FastAPI)
The backend loads the ML model and exposes a POST `/predict` endpoint.
```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the server (runs on http://localhost:8000)
uvicorn main:app --port 8000 --reload
```

### Frontend (React + Vite)
The frontend features a stunning glassmorphism design and talks to the FastAPI backend.
```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the React development server (runs on http://localhost:5173)
npm run dev
```

### Full-Stack Deployment
- **Frontend:** Deploy the `frontend/` folder directly to [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/).
- **Backend:** Deploy the `backend/` folder to [Render](https://render.com/) or [Railway](https://railway.app/).
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - *Note: Don't forget to update the fetch URL in `frontend/src/App.jsx` to point to your live backend URL once deployed!*

---

## 📂 Repository Structure
```
heartRisk/
│
├── app.py                     # Streamlit Application
├── requirements.txt           # Streamlit Dependencies
│
├── backend/                   # FastAPI Backend
│   ├── main.py                # API endpoints
│   ├── requirements.txt       # Backend Dependencies
│   └── *.pkl                  # Saved Machine Learning models & scalers
│
└── frontend/                  # React + Vite Frontend
    ├── src/
    │   ├── App.jsx            # Main React UI component
    │   └── index.css          # Premium Glassmorphism styling
    └── package.json           # Frontend dependencies
```

---
*Built with ❤️ and AI.*
