import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { promptsAPI, collectionsAPI, tagsAPI } from '../services/api';
import PromptCard from '../components/PromptCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SearchBar from '../components/SearchBar';
import Button from '../components/Button';
import { PlusIcon } from '../components/Icons';
import { searchPrompts } from '../utils/searchUtils';
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
  const [tagSearchQuery, setTagSearchQuery] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchPrompts();
  }, [selectedCollection, selectedTags, searchQuery]);

  // Update available tags when collection changes
  useEffect(() => {
    updateAvailableTags();
  }, [selectedCollection, prompts]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [promptsRes, collectionsRes] = await Promise.all([
        promptsAPI.getAll(),
        collectionsAPI.getAll(),
      ]);
      
      setPrompts(promptsRes.data.prompts);
      setCollections(collectionsRes.data.collections);
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

  const updateAvailableTags = () => {
    // Get tags from currently filtered prompts (by collection only, not by selected tags)
    let relevantPrompts = prompts;
    if (selectedCollection) {
      relevantPrompts = prompts.filter(p => p.collection_id === selectedCollection);
    }

    // Count tag usage in relevant prompts
    const tagCounts = {};
    relevantPrompts.forEach(prompt => {
      if (prompt.tags && Array.isArray(prompt.tags)) {
        prompt.tags.forEach(tag => {
          tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
      }
    });

    // Convert to array format matching the API response
    const tagsArray = Object.entries(tagCounts).map(([name, usage_count]) => ({
      name,
      usage_count
    }));

    setTags(tagsArray);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this prompt?')) return;

    try {
      await promptsAPI.delete(id);
      setPrompts(prompts.filter(p => p.id !== id));
    } catch (err) {
      alert('Failed to delete prompt');
      console.error('Error deleting prompt:', err);
    }
  };

  const handleEdit = (id) => {
    navigate(`/prompts/${id}/edit`);
  };

  const toggleTag = (tag) => {
    setSelectedTags(prev =>
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  // Fuzzy search for tags
  const fuzzyMatchTag = (tag, query) => {
    if (!query) return true;
    
    const tagLower = tag.toLowerCase();
    const queryLower = query.toLowerCase();
    
    // Exact match or contains
    if (tagLower.includes(queryLower)) return true;
    
    // Fuzzy match - check if all characters in query appear in order in tag
    let queryIndex = 0;
    for (let i = 0; i < tagLower.length && queryIndex < queryLower.length; i++) {
      if (tagLower[i] === queryLower[queryIndex]) {
        queryIndex++;
      }
    }
    return queryIndex === queryLower.length;
  };

  // Sort tags by usage count (descending) and filter by search
  const filteredAndSortedTags = tags
    .filter(tag => fuzzyMatchTag(tag.name, tagSearchQuery))
    .sort((a, b) => b.usage_count - a.usage_count);

  // Apply all filters
  let filteredPrompts = [...prompts];

  // Filter by collection
  if (selectedCollection) {
    filteredPrompts = filteredPrompts.filter(p => p.collection_id === selectedCollection);
  }

  // Filter by tags
  if (selectedTags.length > 0) {
    filteredPrompts = filteredPrompts.filter(p => 
      selectedTags.every(tag => p.tags?.includes(tag))
    );
  }

  // Filter by search
  if (searchQuery) {
    filteredPrompts = searchPrompts(filteredPrompts, searchQuery);
  }

  // Sort
  const sortedPrompts = [...filteredPrompts].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(b.created_at) - new Date(a.created_at);
    } else if (sortBy === 'title') {
      return a.title.localeCompare(b.title);
    }
    return 0;
  });

  if (loading) {
    return <LoadingSpinner size="large" message="Loading prompts..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />;
  }

  return (
    <div className="prompt-list-page">
      <div className="page-header">
        <h1>Prompts</h1>
        <Button onClick={() => navigate('/prompts/new')}>
          <PlusIcon size={16} /> New Prompt
        </Button>
      </div>

      <div className="filters-section">
        <div className="filter-group">
          <label>Search</label>
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            onClear={() => setSearchQuery('')}
            placeholder="Search prompts..."
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
          <div className="tags-filter-header">
            <label>Filter by tags:</label>
            <input
              type="text"
              placeholder="Search tags..."
              value={tagSearchQuery}
              onChange={(e) => setTagSearchQuery(e.target.value)}
              className="tag-search-input"
            />
          </div>
          <div className="tags-list-container">
            <div className="tags-list">
              {filteredAndSortedTags.map((tag) => (
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
          {filteredAndSortedTags.length === 0 && tagSearchQuery && (
            <div className="no-tags-found">No tags found matching "{tagSearchQuery}"</div>
          )}
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
            <Button onClick={() => navigate('/prompts/new')}>
              <PlusIcon size={16} /> Create Prompt
            </Button>
          )}
        </div>
      ) : (
        <div className="prompts-grid">
          {sortedPrompts.map((prompt) => (
            <PromptCard
              key={prompt.id}
              prompt={prompt}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default PromptList;
