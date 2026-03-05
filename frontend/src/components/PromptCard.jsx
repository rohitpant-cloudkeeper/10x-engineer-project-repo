import { useNavigate } from 'react-router-dom';
import CopyButton from './CopyButton';
import { EditIcon, TrashIcon } from './Icons';
import './PromptCard.css';

function PromptCard({ prompt, onDelete, onEdit }) {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/prompts/${prompt.id}`);
  };

  const handleEdit = (e) => {
    e.stopPropagation();
    onEdit(prompt.id);
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    onDelete(prompt.id);
  };

  return (
    <div className="prompt-card" onClick={handleCardClick}>
      <div className="prompt-header">
        <h3>{prompt.title}</h3>
        <div className="prompt-actions">
          <CopyButton text={prompt.content} />
          <button
            onClick={handleEdit}
            className="btn-icon"
            title="Edit"
            aria-label="Edit prompt"
          >
            <EditIcon size={16} />
          </button>
          <button
            onClick={handleDelete}
            className="btn-icon btn-danger"
            title="Delete"
            aria-label="Delete prompt"
          >
            <TrashIcon size={16} />
          </button>
        </div>
      </div>

      <p className="prompt-content">
        {prompt.content.length > 150
          ? `${prompt.content.substring(0, 150)}...`
          : prompt.content}
      </p>

      {prompt.description && (
        <p className="prompt-description">{prompt.description}</p>
      )}

      {prompt.tags && prompt.tags.length > 0 && (
        <div className="tags">
          {prompt.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      )}

      <div className="prompt-meta">
        <span className="version">v{prompt.version}</span>
        <span className="date">
          {new Date(prompt.created_at).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
}

export default PromptCard;
