import { useEffect, useRef, useState } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import BackendRecoveryAlert from './components/BackendRecoveryAlert';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ProfilePage from './pages/ProfilePage';
import RecommendationsPage from './pages/RecommendationsPage';
import PlannerPage from './pages/PlannerPage';
import DashboardPage from './pages/DashboardPage';
import PredictionPage from './pages/PredictionPage';
import AdaptiveQuestionsPage from './pages/AdaptiveQuestionsPage';
import ChatbotPage from './pages/ChatbotPage';
import { isAuthenticated } from './services/auth';
import { validateStoredSession } from './services/auth';
import { detectReachableApiBaseUrl } from './services/api';
import { startBackendHealthMonitor } from './services/healthMonitor';

function App() {
  const location = useLocation();
  const loggedIn = isAuthenticated();
  const [backendReachable, setBackendReachable] = useState(true);
  const [isRecovering, setIsRecovering] = useState(false);
  const outageDetectedRef = useRef(false);

  useEffect(() => {
    let mounted = true;

    const initializeSession = async () => {
      await detectReachableApiBaseUrl();

      const result = await validateStoredSession();
      if (!mounted) {
        return;
      }

      if (!result.valid && result.reason === 'invalid-token') {
        window.location.href = '/login';
      }
    };

    initializeSession();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let stopMonitoring = () => {};

    const initializeMonitoring = async () => {
      await detectReachableApiBaseUrl();

      stopMonitoring = startBackendHealthMonitor({
        onStatusChange: (reachable) => {
          setBackendReachable(reachable);

          if (!reachable) {
            outageDetectedRef.current = true;
            return;
          }

          if (outageDetectedRef.current) {
            setIsRecovering(true);
            window.setTimeout(() => {
              window.location.reload();
            }, 1200);
          }
        },
      });
    };

    initializeMonitoring();

    const backendStatusListener = (event) => {
      const reachable = Boolean(event.detail?.reachable);
      setBackendReachable(reachable);
      if (!reachable) {
        outageDetectedRef.current = true;
      }
    };

    window.addEventListener('backend-status', backendStatusListener);

    return () => {
      stopMonitoring();
      window.removeEventListener('backend-status', backendStatusListener);
    };
  }, []);

  return (
    <div className={`app-shell ${loggedIn ? 'app-shell--dashboard' : ''}`}>
      <Navbar />
      <BackendRecoveryAlert backendReachable={backendReachable} isRecovering={isRecovering} />
      <main className="container app-main">
        <div className="page-fade" key={location.pathname}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/recommendations" element={<ProtectedRoute><RecommendationsPage /></ProtectedRoute>} />
          <Route path="/planner" element={<ProtectedRoute><PlannerPage /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/prediction" element={<ProtectedRoute><PredictionPage /></ProtectedRoute>} />
          <Route path="/adaptive" element={<ProtectedRoute><AdaptiveQuestionsPage /></ProtectedRoute>} />
          <Route path="/chatbot" element={<ProtectedRoute><ChatbotPage /></ProtectedRoute>} />
        </Routes>
        </div>
      </main>
    </div>
  );
}

export default App;
