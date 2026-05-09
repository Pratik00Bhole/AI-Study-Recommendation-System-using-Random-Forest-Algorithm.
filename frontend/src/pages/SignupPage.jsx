import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { ensureApiReady } from '../services/api';
import { saveAuth } from '../services/auth';

function SignupPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', standard: '10', password: '' });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await ensureApiReady();
      const { data } = await api.post('/auth/signup', form);
      saveAuth(data.token, data.user || { name: form.name, email: form.email });
      navigate('/profile');
    } catch (err) {
      setError(err.userMessage || 'Signup failed');
    }
  };

  return (
    <section className="auth-shell">
      <div className="card auth-card">
        <h2>Create your account</h2>
        <p className="muted">Start building your personalized AI study plan.</p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <label>Name</label>
          <input name="name" value={form.name} onChange={handleChange} required />
          <label>Email</label>
          <input name="email" value={form.email} onChange={handleChange} type="email" required />
          <label>Standard</label>
          <select name="standard" value={form.standard} onChange={handleChange} required>
            {[4, 5, 6, 7, 8, 9, 10].map((standard) => (
              <option key={standard} value={standard}>{standard}</option>
            ))}
          </select>
          <label>Password</label>
          <input name="password" value={form.password} onChange={handleChange} type="password" required minLength={6} />
          <button className="btn-primary" type="submit">Create Account</button>
        </form>
      </div>
    </section>
  );
}

export default SignupPage;
