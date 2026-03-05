import { useState, useEffect } from 'react';
import { collectionsAPI, promptsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import Button from '../components/Button';
import { TrashIcon, PlusIcon, ArrowLeftIcon } from '../components/Icons';
import './Collections.css';

function Collections() {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchCollections();
  }, []);

  const fetchCollections = async () => {
    try {
      setLoading(true);
      const response = await collectionsAPI.getAll();
      
      // Fetch prompt counts for each collection
      const collectionsWithCounts = await Promise.all(
        response.data.collections.map(async (col) => {
          try {
            const promptsRes = await promptsAPI.getAll({ collection_id: col.id });
            return { ...col, promptCount: promptsRes.data.prompts.length };
          } catch {
            return { ...col, promptCount: 0 };
          }
        })
      );
      
      setCollections(collectionsWithCounts);
      setError(null);
    } catch (err) {
      setError('Failed to load collections');
      console.error('Error fetching collections:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      alert('Collection name is required');
      return;
    }

    try {
      await collectionsAPI.create(formData);
      setFormData({ name: '', description: '' });
      setShowForm(false);
      fetchCollections();
    } catch (err) {
      alert('Failed to create collection');
      console.error('Error creating collection:', err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this collection?')) return;

    try {
      await collectionsAPI.delete(id);
      setCollections(collections.filter(c => c.id !== id));
    } catch (err) {
      alert('Failed to delete collection');
      console.error('Error deleting collection:', err);
    }
  };

  if (loading) {
    return <LoadingSpinner size="large" message="Loading collections..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchCollections} />;
  }

  return (
    <div className="collections-page">
      <div className="page-header">
        <h1>Collections</h1>
        <Button onClick={() => setShowForm(!showForm)} size="small">
          {showForm ? <ArrowLeftIcon size={16} /> : <PlusIcon size={16} />}
          {' '}
          {showForm ? 'Cancel' : 'New Collection'}
        </Button>
      </div>

      {showForm && (
        <div className="collection-form-card">
          <h2>Create New Collection</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                type="text"
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter collection name"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Enter collection description (optional)"
                rows="3"
              />
            </div>

            <div className="form-actions">
              <Button type="submit" size="small">Create Collection</Button>
              <Button 
                type="button" 
                variant="secondary"
                size="small"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </Button>
            </div>
          </form>
        </div>
      )}

      {collections.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <h2>No collections yet</h2>
          <p>Create your first collection to organize your prompts!</p>
          <Button onClick={() => setShowForm(true)} size="small">
            Create Collection
          </Button>
        </div>
      ) : (
        <div className="collections-grid">
          {collections.map((collection) => (
            <div key={collection.id} className="collection-card">
              <div className="collection-header">
                <h3>{collection.name}</h3>
                <button
                  onClick={() => handleDelete(collection.id)}
                  className="btn-icon btn-danger"
                  title="Delete"
                >
                  <TrashIcon size={16} />
                </button>
              </div>

              {collection.description && (
                <p className="collection-description">{collection.description}</p>
              )}

              <div className="collection-meta">
                <span className="prompt-count">
                  {collection.promptCount} {collection.promptCount === 1 ? 'prompt' : 'prompts'}
                </span>
                <span className="date">
                  Created {new Date(collection.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Collections;
