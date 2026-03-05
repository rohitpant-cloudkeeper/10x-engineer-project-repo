import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { collectionsAPI, promptsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SearchBar from '../components/SearchBar';
import Button from '../components/Button';
import ConfirmDialog from '../components/ConfirmDialog';
import Toast from '../components/Toast';
import { TrashIcon, PlusIcon, ArrowLeftIcon } from '../components/Icons';
import { useToast } from '../hooks/useToast';
import './Collections.css';

function Collections() {
  const navigate = useNavigate();
  const { toast, showToast, hideToast } = useToast();
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [searchQuery, setSearchQuery] = useState('');
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, title: '', message: '', onConfirm: null, variant: 'default' });

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
      showToast('Collection name is required', 'error');
      return;
    }

    try {
      await collectionsAPI.create(formData);
      setFormData({ name: '', description: '' });
      setShowForm(false);
      fetchCollections();
      showToast('Collection created successfully', 'success');
    } catch (err) {
      showToast('Failed to create collection', 'error');
      console.error('Error creating collection:', err);
    }
  };

  const handleDelete = async (id) => {
    setConfirmDialog({
      isOpen: true,
      title: 'Delete Collection',
      message: 'Are you sure you want to delete this collection? This action cannot be undone.',
      variant: 'danger',
      onConfirm: async () => {
        try {
          await collectionsAPI.delete(id);
          setCollections(collections.filter(c => c.id !== id));
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast('Collection deleted successfully', 'success');
        } catch (err) {
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast('Failed to delete collection', 'error');
          console.error('Error deleting collection:', err);
        }
      }
    });
  };

  const handleViewPrompts = (collectionId) => {
    // Navigate to prompts page with collection pre-selected
    navigate(`/?collection=${collectionId}`);
  };

  if (loading) {
    return <LoadingSpinner size="large" message="Loading collections..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchCollections} />;
  }

  // Filter collections based on search query
  const filteredCollections = collections.filter(collection => {
    if (!searchQuery) return true;
    
    const query = searchQuery.toLowerCase();
    const nameMatch = collection.name.toLowerCase().includes(query);
    const descriptionMatch = collection.description?.toLowerCase().includes(query);
    
    return nameMatch || descriptionMatch;
  });

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

      {!showForm && collections.length > 0 && (
        <div className="search-section">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            onClear={() => setSearchQuery('')}
            placeholder="Search collections by name or description..."
          />
        </div>
      )}

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
      ) : filteredCollections.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h2>No collections found</h2>
          <p>No collections match your search "{searchQuery}"</p>
          <Button onClick={() => setSearchQuery('')} size="small" variant="secondary">
            Clear Search
          </Button>
        </div>
      ) : (
        <div className="collections-grid">
          {filteredCollections.map((collection) => (
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
                {collection.promptCount > 0 ? (
                  <button
                    onClick={() => handleViewPrompts(collection.id)}
                    className="prompt-count clickable"
                    title="View prompts in this collection"
                  >
                    {collection.promptCount} {collection.promptCount === 1 ? 'prompt' : 'prompts'}
                  </button>
                ) : (
                  <span className="prompt-count">
                    0 prompts
                  </span>
                )}
                <span className="date">
                  Created {new Date(collection.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        title={confirmDialog.title}
        message={confirmDialog.message}
        variant={confirmDialog.variant}
        onConfirm={confirmDialog.onConfirm}
        onCancel={() => setConfirmDialog({ ...confirmDialog, isOpen: false })}
      />

      {/* Toast Notification */}
      <Toast
        message={toast.message}
        type={toast.type}
        isVisible={toast.isVisible}
        onClose={hideToast}
      />
    </div>
  );
}

export default Collections;
