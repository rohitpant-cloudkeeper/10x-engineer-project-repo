import { useEffect } from 'react';

export function useKeyboardShortcuts(shortcuts) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const modKey = isMac ? event.metaKey : event.ctrlKey;

      shortcuts.forEach(({ key, ctrl, shift, alt, callback }) => {
        const keyMatch = event.key.toLowerCase() === key.toLowerCase();
        const ctrlMatch = ctrl ? modKey : true;
        const shiftMatch = shift ? event.shiftKey : true;
        const altMatch = alt ? event.altKey : true;

        // Only trigger if all required modifiers match and no extra modifiers are pressed
        const noExtraModifiers = 
          (!ctrl || modKey) &&
          (!shift || event.shiftKey) &&
          (!alt || event.altKey) &&
          (ctrl || !modKey) &&
          (shift || !event.shiftKey) &&
          (alt || !event.altKey);

        if (keyMatch && ctrlMatch && shiftMatch && altMatch && noExtraModifiers) {
          event.preventDefault();
          callback(event);
        }
      });
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);
}
