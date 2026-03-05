import { useState } from 'react';

export function useClipboard(timeout = 2000) {
  const [copied, setCopied] = useState(false);

  const copy = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), timeout);
      return true;
    } catch (err) {
      console.error('Failed to copy:', err);
      setCopied(false);
      return false;
    }
  };

  return { copied, copy };
}
