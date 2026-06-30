import { useState } from 'react'
import './index.css'

function App() {
  const [formData, setFormData] = useState({
    age: 40,
    sex: 'M',
    chest_pain: 'ATA',
    resting_bp: 120,
    cholesterol: 200,
    fasting_bs: 0,
    resting_ecg: 'Normal',
    max_hr: 150,
    exercise_angina: 'N',
    oldpeak: 1.0,
    st_slope: 'Up'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); // null, 0 (low risk), 1 (high risk)
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: (name === 'age' || name === 'resting_bp' || name === 'cholesterol' || name === 'max_hr' || name === 'oldpeak' || name === 'fasting_bs')
        ? Number(value) 
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction from server');
      }

      const data = await response.json();
      setResult(data.risk_prediction);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1 className="title">AI Heart Risk Predictor</h1>
        <p className="subtitle">Enter your clinical data below for an instant machine learning risk assessment.</p>
      </header>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          
          {/* Card 1: Personal Info */}
          <div className="glass-card">
            <h3>👤 Personal Info</h3>
            <div className="input-group">
              <label>Age (Years)</label>
              <input type="number" name="age" min="18" max="100" value={formData.age} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>Sex</label>
              <select name="sex" value={formData.sex} onChange={handleChange}>
                <option value="M">Male</option>
                <option value="F">Female</option>
              </select>
            </div>
          </div>

          {/* Card 2: Symptoms */}
          <div className="glass-card">
            <h3>🤒 Symptoms</h3>
            <div className="input-group">
              <label>Chest Pain Type</label>
              <select name="chest_pain" value={formData.chest_pain} onChange={handleChange}>
                <option value="ATA">Atypical Angina</option>
                <option value="NAP">Non-Anginal Pain</option>
                <option value="TA">Typical Angina</option>
                <option value="ASY">Asymptomatic</option>
              </select>
            </div>
            <div className="input-group">
              <label>Exercise-Induced Angina</label>
              <select name="exercise_angina" value={formData.exercise_angina} onChange={handleChange}>
                <option value="Y">Yes</option>
                <option value="N">No</option>
              </select>
            </div>
          </div>

          {/* Card 3: Vitals */}
          <div className="glass-card">
            <h3>🩺 Vitals</h3>
            <div className="input-group">
              <label>Resting Blood Pressure (mm Hg)</label>
              <input type="number" name="resting_bp" min="80" max="200" value={formData.resting_bp} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>Max Heart Rate</label>
              <input type="number" name="max_hr" min="60" max="220" value={formData.max_hr} onChange={handleChange} required />
            </div>
          </div>

          {/* Card 4: Labs & ECG */}
          <div className="glass-card">
            <h3>🔬 Labs & ECG</h3>
            <div className="input-group">
              <label>Cholesterol (mg/dL)</label>
              <input type="number" name="cholesterol" min="0" max="600" value={formData.cholesterol} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>Fasting Blood Sugar {'>'} 120 mg/dL</label>
              <select name="fasting_bs" value={formData.fasting_bs} onChange={handleChange}>
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>
            <div className="input-group">
              <label>Resting ECG</label>
              <select name="resting_ecg" value={formData.resting_ecg} onChange={handleChange}>
                <option value="Normal">Normal</option>
                <option value="ST">ST-T wave abnormality</option>
                <option value="LVH">Left Ventricular Hypertrophy</option>
              </select>
            </div>
            <div className="input-group">
              <label>Oldpeak</label>
              <input type="number" step="0.1" name="oldpeak" min="-2.0" max="6.0" value={formData.oldpeak} onChange={handleChange} required />
            </div>
            <div className="input-group">
              <label>ST Slope</label>
              <select name="st_slope" value={formData.st_slope} onChange={handleChange}>
                <option value="Up">Upsloping</option>
                <option value="Flat">Flat</option>
                <option value="Down">Downsloping</option>
              </select>
            </div>
          </div>

        </div>

        {error && <p style={{color: 'var(--danger)', textAlign: 'center'}}>{error}</p>}

        <div className="btn-container">
          <button type="submit" className="btn-predict" disabled={loading}>
            {loading ? 'Analyzing...' : '🚀 Predict Risk Now'}
          </button>
        </div>
      </form>

      {/* Result Modal */}
      {result !== null && (
        <div className="modal-overlay">
          <div className="modal-content">
            {result === 1 ? (
              <>
                <div className="result-icon result-high">⚠️</div>
                <h2 className="result-high">High Risk Detected</h2>
                <p>Our model indicates a high probability of heart disease. Please consult a healthcare professional immediately.</p>
              </>
            ) : (
              <>
                <div className="result-icon result-low">✅</div>
                <h2 className="result-low">Low Risk Detected</h2>
                <p>Your clinical metrics look good. Maintain a healthy lifestyle!</p>
              </>
            )}
            <button className="btn-close" onClick={() => setResult(null)}>Close</button>
          </div>
        </div>
      )}

    </div>
  )
}

export default App
