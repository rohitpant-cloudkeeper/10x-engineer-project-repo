import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { promptsAPI, collectionsAPI, tagsAPI } from '../services/api';
import './PromptList.css';

function PromptList() {
  const navigate = useNavigate();
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filters
  const [selectedCollection, setSelectedCollection] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('date');

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchPrompts();
  }, [selectedCollection, selectedTags, searchQuery]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [promptsRes, collectionsRes, tagsRes] = await Promise.all([
        promptsAPI.getAll(),
        collectionsAPI.getAll(),
        tagsAPI.getAll(),
      ]);
      
      setPrompts(promptsRes.data.prompts);
      setCollections(collectionsRes.data.collections);
      setTags(tagsRes.data.tags);
      setError(null);
    } catch (err) {
      setError('Failed to load data');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPrompts = async () => {
    try {
      const params = {};
      if (selectedCollection) params.collection_id = selectedCollection;
      if (selectedTags.length > 0) params.tags = selectedTags.join(',');
      if (searchQuery) params.search = searchQuery;

      const response = await promptsAPI.getAll(params);
      setPrompts(response.data.prompts);
    } catch (err) {
      console.error('Error fetching prompts:', err);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this prompt?')) return;

    try {
      await promptsAPI.delete(id);
      setPrompts(prompts.filter(p => p.id !== id));
    } catch (err) {
      alert('Failed to delete prompt');
      console.error('Error deleting prompt:', err);
    }
  };

  const handleEdit = (id, e) => {
    e.stopPropagation();
    navigate(`/prompts/${id}/edit`);
  };

  const toggleTag = (tag) => {
    setSelectedTags(prev =>
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const sortedPrompts = [...prompts].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(b.created_at) - new Date(a.created_at);
    } else if (sortBy === 'title') {
      return a.title.localeCompare(b.title);
    }
    return 0;
  });

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading prompts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={fetchData} className="btn-retry">Retry</button>
      </div>
    );
  }

  return (
    <div className="prompt-list-page">
      <div className="page-header">
        <h1>Prompts</h1>
        <button onClick={() => navigate('/prompts/new')} className="btn-primary">
          + New Prompt
        </button>
      </div>

      <div className="filters-section">
        <div className="filter-group">
          <label>Search</label>
          <input
            type="text"
            placeholder="Search prompts..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-group">
          <label>Collection</label>
          <select
            value={selectedCollection}
            onChange={(e) => setSelectedCollection(e.target.value)}
            className="filter-select"
          >
            <option value="">All Collections</option>
            {collections.map((col) => (
              <option key={col.id} value={col.id}>
                {col.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Sort By</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="filter-select"
          >
            <option value="date">Date (Newest)</option>
            <option value="title">Title (A-Z)</option>
          </select>
        </div>
      </div>

      {tags.length > 0 && (
        <div className="tags-filter">
          <label>Filter by tags:</label>
          <div className="tags-list">
            {tags.map((tag) => (
              <button
                key={tag.name}
                onClick={() => toggleTag(tag.name)}
                className={`tag-filter ${selectedTags.includes(tag.name) ? 'active' : ''}`}
              >
                {tag.name} ({tag.usage_count})
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedTags.length > 0 && (
        <div className="active-filters">
          <span>Active filters:</span>
          {selectedTags.map((tag) => (
            <span key={tag} className="active-filter-tag">
              {tag}
              <button onClick={() => toggleTag(tag)}>×</button>
            </span>
          ))}
          <button onClick={() => setSelectedTags([])} className="clear-filters">
            Clear all
          </button>
        </div>
      )}

      {sortedPrompts.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📝</div>
          <h2>No prompts found</h2>
          <p>
            {searchQuery || selectedTags.length > 0 || selectedCollection
              ? 'Try adjusting your filters'
              : 'Create your first prompt to get started!'}
          </p>
          {!searchQuery && !selectedTags.length && !selectedCollection && (
            <button onClick={() => navigate('/prompts/new')} className="btn-primary">
              Create Prompt
            </button>
          )}
        </div>
      ) : (
        <div className="prompts-grid">
          {sortedPrompts.map((prompt) => (
            <div key={prompt.id} className="prompt-card">
              <div className="prompt-header">
                <h3>{prompt.title}</h3>
                <div className="prompt-actions">
                  <button
                    onClick={(e) => handleEdit(prompt.id, e)}
                    className="btn-icon"
                    title="Edit"
                  >
                    ✏️
                  </button>
                  <button
                    onClick={(e) => handleDelete(prompt.id, e)}
                    className="btn-icon btn-danger"
                    title="Delete"
                  >
                    🗑️
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
          ))}
        </div>
      )}
    </div>
  );
}

export default PromptList;
