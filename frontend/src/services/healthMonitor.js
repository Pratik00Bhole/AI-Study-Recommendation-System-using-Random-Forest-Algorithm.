import axios from 'axios';
import { getApiBaseUrl } from './api';

export const startBackendHealthMonitor = ({
  intervalMs = 5000,
  timeoutMs = 2500,
  onStatusChange,
} = {}) => {
  let lastReachable = null;
  let active = true;

  const notify = (reachable) => {
    if (lastReachable !== reachable) {
      lastReachable = reachable;
      if (typeof onStatusChange === 'function') {
        onStatusChange(reachable);
      }
      window.dispatchEvent(new CustomEvent('backend-status', { detail: { reachable } }));
    }
  };

  const check = async () => {
    if (!active) {
      return;
    }

    try {
      const healthUrl = `${getApiBaseUrl().replace(/\/?api\/?$/, '')}/api/health`;
      await axios.get(healthUrl, {
        timeout: timeoutMs,
        skipNetworkRetry: true,
      });
      notify(true);
    } catch {
      notify(false);
    }
  };

  check();
  const timerId = window.setInterval(check, intervalMs);

  return () => {
    active = false;
    window.clearInterval(timerId);
  };
};
