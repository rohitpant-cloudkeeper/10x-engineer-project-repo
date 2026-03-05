import './ErrorMessage.css';

function ErrorMessage({ message, onRetry, type = 'error' }) {
  return (
    <div className={`error-container error-${type}`}>
      <div className="error-icon">
        {type === 'error' ? '⚠️' : type === 'warning' ? '⚡' : 'ℹ️'}
      </div>
      <p className="error-message">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-retry">
          Try Again
        </button>
      )}
    </div>
  );
}

export default ErrorMessage;
