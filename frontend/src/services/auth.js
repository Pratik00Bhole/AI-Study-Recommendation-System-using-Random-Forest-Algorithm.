export const saveAuth = (token, user) => {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user || {}));
};

const resolveApiBaseUrls = () => {
  const primary =
    import.meta.env.VITE_API_BASE_URL ||
    (import.meta.env.DEV ? 'http://127.0.0.1:5000/api' : 'http://127.0.0.1:8000/api');

  return [...new Set([
    primary,
    'http://127.0.0.1:5000/api',
    'http://127.0.0.1:8000/api',
    'http://localhost:5000/api',
    'http://localhost:8000/api',
  ])];
};

export const clearAuth = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getUser = () => {
  try {
    return JSON.parse(localStorage.getItem('user') || '{}');
  } catch {
    return {};
  }
};

export const isAuthenticated = () => Boolean(localStorage.getItem('token'));

export const validateStoredSession = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    return { valid: false, reason: 'missing-token' };
  }

  for (const baseUrl of resolveApiBaseUrls()) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    try {
      const response = await fetch(`${baseUrl}/auth/validate`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        signal: controller.signal,
      });

      if (response.ok) {
        return { valid: true, reason: 'ok' };
      }

      if (response.status === 401 || response.status === 422) {
        clearAuth();
        return { valid: false, reason: 'invalid-token' };
      }
    } catch {
      // Try next base URL candidate.
    } finally {
      clearTimeout(timeoutId);
    }
  }

  return { valid: true, reason: 'backend-unreachable' };
};
