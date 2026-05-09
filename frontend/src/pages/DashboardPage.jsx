import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api from '../services/api';

function DashboardPage() {
  const [dashboard, setDashboard] = useState({
    completion_percentage: 0,
    completed_tasks: 0,
    total_tasks: 0,
    graph_data: [],
  });
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const { data } = await api.get('/progress/dashboard');
        setDashboard(data.dashboard || {
          completion_percentage: 0,
          completed_tasks: 0,
          total_tasks: 0,
          graph_data: [],
        });
      } catch (err) {
        setError(err.userMessage || 'Unable to load dashboard data.');
      }
    };
    load();
  }, []);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h2 className="page-title">Learning Dashboard</h2>
        <p className="page-subtitle">Track progress, completion trends, and consistency over time.</p>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="grid dashboard-kpis">
        <div className="card kpi-card">
          <h3>Completion Percentage</h3>
          <p className="kpi-value">{dashboard.completion_percentage}%</p>
          <p className="kpi-caption">Tasks completed across your current plan.</p>
        </div>
        <div className="card kpi-card">
          <h3>Completed Tasks</h3>
          <p className="kpi-value">{dashboard.completed_tasks} / {dashboard.total_tasks}</p>
          <p className="kpi-caption">Done vs assigned tasks.</p>
        </div>
      </div>

      <div className="card progress-card">
        <h3>Overall Progress</h3>
        <div className="progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow={dashboard.completion_percentage}>
          <span className="progress-fill" style={{ width: `${Math.max(0, Math.min(100, dashboard.completion_percentage))}%` }} />
        </div>
        <p className="kpi-caption">You have completed {dashboard.completion_percentage}% of your planned learning tasks.</p>
      </div>

      <div className="card chart-card">
        <h3>Progress Graph</h3>
        {dashboard.graph_data.length === 0 && (
          <p className="empty-state">No progress data yet. Add a few tasks and mark them completed to see trends.</p>
        )}
        <ResponsiveContainer width="100%" height="280px">
          <BarChart data={dashboard.graph_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="completed" fill="#16a34a" />
            <Bar dataKey="pending" fill="#f59e0b" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default DashboardPage;
