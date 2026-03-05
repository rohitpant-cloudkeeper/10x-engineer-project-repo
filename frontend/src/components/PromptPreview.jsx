import { useState } from 'react';
import './PromptPreview.css';

function PromptPreview({ prompt, children }) {
  const [showPreview, setShowPreview] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseEnter = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 10
    });
    setShowPreview(true);
  };

  const handleMouseLeave = () => {
    setShowPreview(false);
  };

  return (
    <div 
      className="prompt-preview-wrapper"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      {showPreview && (
        <div 
          className="prompt-preview-tooltip"
          style={{
            left: `${position.x}px`,
            top: `${position.y}px`,
          }}
        >
          <div className="preview-header">
            <h4>{prompt.title}</h4>
            <span className="preview-version">v{prompt.version}</span>
          </div>
          <div className="preview-content">
            {prompt.content}
          </div>
          {prompt.description && (
            <div className="preview-description">
              {prompt.description}
            </div>
          )}
          {prompt.tags && prompt.tags.length > 0 && (
            <div className="preview-tags">
              {prompt.tags.map(tag => (
                <span key={tag} className="preview-tag">{tag}</span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default PromptPreview;
