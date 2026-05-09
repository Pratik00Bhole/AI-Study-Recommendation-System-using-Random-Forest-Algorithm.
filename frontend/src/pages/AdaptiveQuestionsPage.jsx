import { useEffect, useState } from 'react';
import api from '../services/api';

function AdaptiveQuestionsPage() {
  const [topic, setTopic] = useState('');
  const [score, setScore] = useState(60);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    const loadProfileSubjects = async () => {
      try {
        const { data } = await api.get('/student/profile');
        const profile = data?.profile || {};
        const profileSubjects = Array.isArray(profile.subjects)
          ? profile.subjects.map((item) => item?.name).filter(Boolean)
          : [];

        const fallbackSubjects = Object.keys(profile.marks || {});
        const availableSubjects = profileSubjects.length > 0 ? profileSubjects : fallbackSubjects;

        if (availableSubjects.length > 0) {
          setSubjects(availableSubjects);
          setTopic(availableSubjects[0]);
        } else {
          setTopic('General Topic');
        }
      } catch {
        setTopic('General Topic');
      }
    };

    loadProfileSubjects();
  }, []);

  const handleGenerate = async () => {
    setError('');
    try {
      const { data } = await api.post('/adaptive/questions', {
        topic,
        performance_score: Number(score),
      });
      setResult(data);
    } catch (err) {
      setError(err.userMessage || 'Unable to generate adaptive questions.');
    }
  };

  return (
    <div className="card">
      <div className="page-header">
        <h2 className="page-title">Adaptive Question Generator</h2>
        <p className="page-subtitle">Generate questions that match your current performance level.</p>
      </div>
      <label>Topic</label>
      {subjects.length > 0 ? (
        <select value={topic} onChange={(e) => setTopic(e.target.value)}>
          {subjects.map((subject) => (
            <option key={subject} value={subject}>{subject}</option>
          ))}
        </select>
      ) : (
        <input value={topic} onChange={(e) => setTopic(e.target.value)} />
      )}
      <label>Current Performance Score</label>
      <input type="number" value={score} onChange={(e) => setScore(e.target.value)} min="0" max="100" />
      <button className="btn-primary" onClick={handleGenerate}>Generate Questions</button>
      {error && <div className="error">{error}</div>}

      {result && (
        <div className="card">
          <h3>{result.topic} ({result.difficulty})</h3>
          <ul className="list">
            {result.questions.map((question) => <li key={question}>{question}</li>)}
          </ul>
          {result.questions.length === 0 && <p className="empty-state">No questions generated. Try another topic.</p>}
        </div>
      )}
    </div>
  );
}

export default AdaptiveQuestionsPage;
