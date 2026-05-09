import { useEffect, useState } from 'react';
import api from '../services/api';

function RecommendationsPage() {
  const [data, setData] = useState({ recommendations: [], analysis: { weak_topics: [], strong_topics: [] } });
  const [error, setError] = useState('');

  const recommendationsBySubject = data.recommendations.reduce((acc, item) => {
    const subject = item.subject || 'General';
    if (!acc[subject]) {
      acc[subject] = [];
    }
    acc[subject].push(item);
    return acc;
  }, {});

  const orderedSubjects = Object.keys(recommendationsBySubject);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get('/recommendations/');
        setData(response.data || { recommendations: [], analysis: { weak_topics: [], strong_topics: [] } });
      } catch (err) {
        setError(err.userMessage || 'Unable to load recommendations. Save your profile first.');
      }
    };
    load();
  }, []);

  return (
    <div className="recommendations-page">
      <div className="page-header">
        <h2 className="page-title">AI Recommendations</h2>
        <p className="page-subtitle">Personalized study content ranked by your profile and weak topics.</p>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="card topic-snapshot-card">
        <h3>Topic Snapshot</h3>
        <p><strong>Weak topics</strong></p>
        <div className="pill-row">
          {data.analysis.weak_topics.length > 0
            ? data.analysis.weak_topics.map((topic) => <span className="pill pill--weak" key={topic}>{topic}</span>)
            : <span className="pill">None</span>}
        </div>

        <p><strong>Strong topics</strong></p>
        <div className="pill-row">
          {data.analysis.strong_topics.length > 0
            ? data.analysis.strong_topics.map((topic) => <span className="pill pill--strong" key={topic}>{topic}</span>)
            : <span className="pill">None</span>}
        </div>
      </div>

      {data.recommendations.length === 0 && !error && (
        <p className="empty-state">No recommendations yet. Save your profile details to generate personalized suggestions.</p>
      )}

      {orderedSubjects.map((subject) => (
        <div className="card" key={subject}>
          <h3>{subject}</h3>
          <p className="page-subtitle">Recommended focus paths tailored to your current performance.</p>
          <div className="recommendation-grid">
          {recommendationsBySubject[subject].map((rec) => (
            <article key={`${subject}-${rec.topic}`} className="recommendation-card">
              <div className="recommendation-card-header">
                <h4>{rec.topic}</h4>
                <span className="level-badge">{rec.difficulty}</span>
              </div>
              <p className="recommendation-description">
                Relevance score: <strong>{rec.score}</strong>
              </p>
              <h5>Recommended Videos</h5>
              <ul className="list">
                {rec.videos.map((video) => (
                  <li key={video.url}><a href={video.url} target="_blank" rel="noreferrer">{video.title}</a></li>
                ))}
              </ul>
              <h5>Practice Questions</h5>
              <ul className="list">
                {rec.practice_questions.map((question) => <li key={question}>{question}</li>)}
              </ul>
              {rec.videos[0] ? (
                <a className="btn-primary recommendation-action" href={rec.videos[0].url} target="_blank" rel="noreferrer">
                  Start
                </a>
              ) : (
                <button className="btn-secondary recommendation-action" type="button">View</button>
              )}
            </article>
          ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default RecommendationsPage;
