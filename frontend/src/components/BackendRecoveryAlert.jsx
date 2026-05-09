function BackendRecoveryAlert({ backendReachable, isRecovering }) {
  if (backendReachable && !isRecovering) {
    return null;
  }

  if (isRecovering) {
    return (
      <div className="backend-banner backend-banner--online">
        Backend is back online. Restoring your session...
      </div>
    );
  }

  return (
    <div className="backend-banner backend-banner--offline">
      Backend is temporarily unreachable. Reconnecting automatically...
    </div>
  );
}

export default BackendRecoveryAlert;
