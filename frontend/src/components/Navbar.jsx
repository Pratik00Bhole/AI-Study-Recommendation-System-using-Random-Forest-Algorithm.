import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { clearAuth, getUser, isAuthenticated } from '../services/auth';

function Navbar() {
  const navigate = useNavigate();
  const loggedIn = isAuthenticated();
  const user = getUser();
  const chatbotEnabled = import.meta.env.VITE_ENABLE_CHATBOT !== 'false';
  const [menuOpen, setMenuOpen] = useState(false);

  const profileInitial = (user?.name || 'S').slice(0, 1).toUpperCase();

  const closeMenu = () => {
    setMenuOpen(false);
  };

  const handleLogout = () => {
    clearAuth();
    closeMenu();
    navigate('/login');
  };

  return (
    <>
      <nav className="nav">
        <div className="nav-left">
          {loggedIn && (
            <button
              className="nav-menu-btn"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-label="Toggle navigation menu"
              type="button"
            >
              <span />
              <span />
              <span />
            </button>
          )}
          <Link className="nav-brand" to={loggedIn ? '/dashboard' : '/login'}>
            <span className="nav-brand-logo">S</span>
            <span>StudyFlow AI</span>
          </Link>
        </div>
        <div className="nav-right">
          {!loggedIn && <Link to="/login">Login</Link>}
          {!loggedIn && <Link to="/signup">Signup</Link>}
          {loggedIn && <div className="nav-profile" title={user?.name || 'Student'}>{profileInitial}</div>}
        </div>
      </nav>

      {loggedIn && menuOpen && <button className="sidebar-overlay" onClick={closeMenu} aria-label="Close menu" type="button" />}

      {loggedIn && (
        <aside className={`sidebar sidebar-nav ${menuOpen ? 'is-open' : ''}`} aria-label="Primary navigation">
          <NavLink className="sidebar-item" to="/dashboard" onClick={closeMenu} data-label="Dashboard">
            <span className="sidebar-icon" aria-hidden="true">🏠</span>
            <span className="sidebar-text">Dashboard</span>
          </NavLink>
          <NavLink className="sidebar-item" to="/recommendations" onClick={closeMenu} data-label="Recommendations">
            <span className="sidebar-icon" aria-hidden="true">📚</span>
            <span className="sidebar-text">Recommendations</span>
          </NavLink>
          <NavLink className="sidebar-item" to="/planner" onClick={closeMenu} data-label="Progress">
            <span className="sidebar-icon" aria-hidden="true">📈</span>
            <span className="sidebar-text">Progress</span>
          </NavLink>
          <NavLink className="sidebar-item" to="/profile" onClick={closeMenu} data-label="Settings">
            <span className="sidebar-icon" aria-hidden="true">⚙️</span>
            <span className="sidebar-text">Settings</span>
          </NavLink>
          <NavLink className="sidebar-item" to="/prediction" onClick={closeMenu} data-label="Prediction">
            <span className="sidebar-icon" aria-hidden="true">🔮</span>
            <span className="sidebar-text">Prediction</span>
          </NavLink>
          <NavLink className="sidebar-item" to="/adaptive" onClick={closeMenu} data-label="Adaptive Questions">
            <span className="sidebar-icon" aria-hidden="true">🧩</span>
            <span className="sidebar-text">Adaptive Questions</span>
          </NavLink>
          {chatbotEnabled && (
            <NavLink className="sidebar-item" to="/chatbot" onClick={closeMenu} data-label="Tutor Chatbot">
              <span className="sidebar-icon" aria-hidden="true">💬</span>
              <span className="sidebar-text">Tutor Chatbot</span>
            </NavLink>
          )}
          <button className="btn-secondary nav-logout sidebar-item sidebar-logout" onClick={handleLogout} data-label="Logout" type="button">
            <span className="sidebar-icon" aria-hidden="true">⎋</span>
            <span className="sidebar-text">Logout</span>
          </button>
        </aside>
      )}
    </>
  );
}

export default Navbar;
