import { useState, useEffect } from 'react';
import { promptsAPI } from '../services/api';

function PromptList() {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPrompts();
  }, []);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      const response = await promptsAPI.getAll();
      setPrompts(response.data.prompts);
      setError(null);
    } catch (err) {
      setError('Failed to load prompts');
      console.error('Error fetching prompts:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading prompts...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (prompts.length === 0) {
    return (
      <div className="empty-state">
        <h2>No prompts yet</h2>
        <p>Create your first prompt to get started!</p>
      </div>
    );
  }

  return (
    <div className="prompt-list">
      <h1>Prompts</h1>
      <div className="prompts-grid">
        {prompts.map((prompt) => (
          <div key={prompt.id} className="prompt-card">
            <h3>{prompt.title}</h3>
            <p>{prompt.content.substring(0, 100)}...</p>
            {prompt.tags && prompt.tags.length > 0 && (
              <div className="tags">
                {prompt.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PromptList;
