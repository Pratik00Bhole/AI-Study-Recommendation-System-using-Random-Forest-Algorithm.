import { useEffect, useState } from 'react';
import api from '../services/api';

function PlannerPage() {
  const [plan, setPlan] = useState({ daily_tasks: [], weekly_tasks: [] });
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get('/planner/');
        setPlan(data || { daily_tasks: [], weekly_tasks: [] });
      } catch (err) {
        setError(err.userMessage || 'Unable to load planner. Save your profile first.');
      }
    };
    load();
  }, []);

  return (
    <div>
      <div className="page-header">
        <h2 className="page-title">Study Planner</h2>
        <p className="page-subtitle">Actionable daily and weekly tasks generated from your recommendations.</p>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="grid">
      <div className="card">
        <h2>Daily Tasks</h2>
        <ul className="list">
          {plan.daily_tasks.map((task) => (
            <li key={`${task.date}-${task.topic}`}>{task.date}: {task.task}</li>
          ))}
        </ul>
        {plan.daily_tasks.length === 0 && !error && (
          <p className="empty-state">No daily plan yet. Generate recommendations first.</p>
        )}
      </div>

      <div className="card">
        <h2>Weekly Tasks</h2>
        <ul className="list">
          {plan.weekly_tasks.map((task) => (
            <li key={`${task.week}-${task.topic}`}>{task.week}: {task.task}</li>
          ))}
        </ul>
        {plan.weekly_tasks.length === 0 && !error && (
          <p className="empty-state">No weekly plan yet. Generate recommendations first.</p>
        )}
      </div>
      </div>
    </div>
  );
}

export default PlannerPage;
