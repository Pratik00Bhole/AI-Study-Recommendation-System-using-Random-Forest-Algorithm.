import { useState } from 'react';
import api from '../services/api';

function PredictionPage() {
  const [form, setForm] = useState({ avg_mark: 65, completed_tasks: 8, consistency_score: 55 });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      const { data } = await api.post('/prediction/', {
        avg_mark: Number(form.avg_mark),
        completed_tasks: Number(form.completed_tasks),
        consistency_score: Number(form.consistency_score),
      });
      setResult(data);
    } catch (err) {
      setError(err.userMessage || 'Unable to generate prediction.');
    }
  };

  return (
    <div className="card">
      <div className="page-header">
        <h2 className="page-title">Performance Prediction</h2>
        <p className="page-subtitle">Estimate your upcoming performance based on consistency and completed tasks.</p>
      </div>
      <form onSubmit={handleSubmit}>
        <label>Average Mark</label>
        <input name="avg_mark" value={form.avg_mark} onChange={handleChange} type="number" min="0" max="100" />
        <label>Completed Tasks</label>
        <input name="completed_tasks" value={form.completed_tasks} onChange={handleChange} type="number" min="0" />
        <label>Consistency Score</label>
        <input name="consistency_score" value={form.consistency_score} onChange={handleChange} type="number" min="0" max="100" />
        <button className="btn-primary" type="submit">Predict</button>
      </form>
      {error && <div className="error">{error}</div>}

      {result && (
        <div className="card">
          <h3>Prediction Result</h3>
          <p className="kpi-value">{result.predicted_score}</p>
          <p className="kpi-caption">Band: {result.prediction_band}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionPage;
