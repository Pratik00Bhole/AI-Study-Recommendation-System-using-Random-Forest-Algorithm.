import axios from 'axios';
import { clearAuth } from './auth';

const envApiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const defaultDevBaseUrl = 'http://127.0.0.1:5000/api';
const defaultLiveBaseUrl = 'http://127.0.0.1:8000/api';
const localhostDevBaseUrl = 'http://localhost:5000/api';
const localhostLiveBaseUrl = 'http://localhost:8000/api';

const unique = (items) => [...new Set(items.filter(Boolean))];
const candidateApiBaseUrls = unique([
  envApiBaseUrl,
  defaultDevBaseUrl,
  defaultLiveBaseUrl,
  localhostDevBaseUrl,
  localhostLiveBaseUrl,
]);

export let API_BASE_URL = envApiBaseUrl || (import.meta.env.DEV ? defaultDevBaseUrl : defaultLiveBaseUrl);

const MAX_NETWORK_RETRIES = 2;
const DETECTION_RETRIES = 2;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
let apiDetectionPromise = null;

const shouldRetryNetworkError = (error) => {
  if (error.response) {
    return false;
  }

  const config = error.config || {};
  if (config.skipNetworkRetry) {
    return false;
  }

  const method = String(config.method || 'get').toLowerCase();
  const url = String(config.url || '');
  const retryCount = config.__networkRetryCount || 0;
  const isSafeMethod = ['get', 'head', 'options'].includes(method);
  const isLoginRequest = method === 'post' && url.includes('/auth/login');

  return (isSafeMethod || isLoginRequest) && retryCount < MAX_NETWORK_RETRIES;
};

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getApiBaseUrl = () => API_BASE_URL;

export const detectReachableApiBaseUrl = async () => {
  for (const baseUrl of candidateApiBaseUrls) {
    try {
      const healthUrl = `${baseUrl.replace(/\/?api\/?$/, '')}/api/health`;
      await axios.get(healthUrl, { timeout: 2000 });
      const reachableBaseUrl = baseUrl;
      API_BASE_URL = reachableBaseUrl;
      api.defaults.baseURL = reachableBaseUrl;
      window.dispatchEvent(new CustomEvent('backend-status', { detail: { reachable: true } }));
      return reachableBaseUrl;
    } catch {
      // Continue trying candidate base URLs.
    }
  }

  window.dispatchEvent(new CustomEvent('backend-status', { detail: { reachable: false } }));
  return null;
};

const detectWithRetry = async () => {
  for (let attempt = 0; attempt <= DETECTION_RETRIES; attempt += 1) {
    const detected = await detectReachableApiBaseUrl();
    if (detected) {
      return detected;
    }

    if (attempt < DETECTION_RETRIES) {
      await sleep(900 * (attempt + 1));
    }
  }

  return null;
};

export const initializeApiDetection = () => {
  if (!apiDetectionPromise) {
    apiDetectionPromise = detectWithRetry();
  }
  return apiDetectionPromise;
};

export const ensureApiReady = async () => {
  const detected = await initializeApiDetection();
  if (!detected) {
    throw new Error('Backend not reachable');
  }
};

initializeApiDetection();

api.interceptors.request.use(async (config) => {
  if (!config.skipApiReadyCheck) {
    await ensureApiReady();
  }

  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (shouldRetryNetworkError(error)) {
      const config = error.config;
      if (!config.__apiRedetected) {
        config.__apiRedetected = true;
        apiDetectionPromise = null;
        await initializeApiDetection();
      }
      config.__networkRetryCount = (config.__networkRetryCount || 0) + 1;
      const delayMs = 800 * (2 ** (config.__networkRetryCount - 1));
      await sleep(delayMs);
      return api.request(config);
    }

    const status = error.response?.status;

    if (status === 401 || status === 422) {
      clearAuth();
      if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
        window.location.href = '/login';
      }
    }

    if (!error.response) {
      window.dispatchEvent(new CustomEvent('backend-status', { detail: { reachable: false } }));
      error.userMessage = 'Unable to reach server. Please ensure backend is running.';
      return Promise.reject(error);
    }

    error.userMessage = error.response?.data?.error || 'Request failed. Please try again.';
    return Promise.reject(error);
  }
);

export default api;
