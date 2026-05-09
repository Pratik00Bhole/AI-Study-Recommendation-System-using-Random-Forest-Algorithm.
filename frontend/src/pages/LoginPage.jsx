import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api, { ensureApiReady } from '../services/api';
import { saveAuth } from '../services/auth';

function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (isLoading) {
      return;
    }

    setError('');
    setIsLoading(true);
    try {
      await ensureApiReady();
      const { data } = await api.post('/auth/login', form);
      saveAuth(data.token, data.user);
      navigate('/dashboard');
    } catch (err) {
      const baseMessage = err.userMessage || 'Login failed';
      const isNetworkIssue = !err.response;
      const registrationHint = isNetworkIssue ? '' : ' If you are not registered, please create a new account.';
      setError(`${baseMessage}${registrationHint}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="auth-shell">
      <div className="card auth-card">
        <h2>Welcome back</h2>
        <p className="muted">Sign in to continue with your AI study assistant.</p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input name="email" value={form.email} onChange={handleChange} type="email" required disabled={isLoading} />
          <label>Password</label>
          <input name="password" value={form.password} onChange={handleChange} type="password" required minLength={6} disabled={isLoading} />
          <button className="btn-primary" type="submit" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="muted auth-footer-note">
          Not registered yet? <Link to="/signup">Create a new account</Link>
        </p>
      </div>
    </section>
  );
}

export default LoginPage;
