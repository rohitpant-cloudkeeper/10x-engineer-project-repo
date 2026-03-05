import './KeyboardShortcutsHelp.css';

function KeyboardShortcutsHelp({ isOpen, onClose }) {
  if (!isOpen) return null;

  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
  const modKey = isMac ? '⌘' : 'Ctrl';

  const shortcuts = [
    { keys: `${modKey} + K`, description: 'Focus search bar' },
    { keys: `${modKey} + N`, description: 'Create new prompt' },
    { keys: 'Escape', description: 'Close modals' },
  ];

  return (
    <div className="shortcuts-overlay" onClick={onClose}>
      <div className="shortcuts-modal" onClick={(e) => e.stopPropagation()}>
        <div className="shortcuts-header">
          <h2>⌨️ Keyboard Shortcuts</h2>
          <button className="shortcuts-close" onClick={onClose}>×</button>
        </div>
        <div className="shortcuts-list">
          {shortcuts.map((shortcut, index) => (
            <div key={index} className="shortcut-item">
              <kbd className="shortcut-keys">{shortcut.keys}</kbd>
              <span className="shortcut-description">{shortcut.description}</span>
            </div>
          ))}
        </div>
        <div className="shortcuts-footer">
          Press <kbd>?</kbd> to toggle this help
        </div>
      </div>
    </div>
  );
}

export default KeyboardShortcutsHelp;
