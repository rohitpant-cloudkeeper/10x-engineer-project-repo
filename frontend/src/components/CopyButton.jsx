import { useClipboard } from '../hooks/useClipboard';
import { CopyIcon, CheckIcon } from './Icons';
import './CopyButton.css';

function CopyButton({ text, label = 'Copy', className = '' }) {
  const { copied, copy } = useClipboard();

  const handleCopy = (e) => {
    e.stopPropagation();
    copy(text);
  };

  return (
    <button
      className={`copy-button ${className} ${copied ? 'copied' : ''}`}
      onClick={handleCopy}
      title={copied ? 'Copied!' : label}
      aria-label={copied ? 'Copied!' : label}
    >
      {copied ? (
        <>
          <CheckIcon size={14} /> Copied
        </>
      ) : (
        <>
          <CopyIcon size={14} /> Copy
        </>
      )}
    </button>
  );
}

export default CopyButton;
