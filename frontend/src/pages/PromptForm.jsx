import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { promptsAPI, collectionsAPI, tagsAPI } from '../services/api';
import Button from '../components/Button';
import Toast from '../components/Toast';
import { ArrowLeftIcon } from '../components/Icons';
import { useToast } from '../hooks/useToast';
import './PromptForm.css';

function PromptForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);
  const { toast, showToast, hideToast } = useToast();

  const [formData, setFormData] = useState({
    title: '',
    content: '',
    description: '',
    collection_id: '',
    tags: [],
  });

  const [collections, setCollections] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);
  const [tagInput, setTagInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [collectionsRes, tagsRes] = await Promise.all([
        collectionsAPI.getAll(),
        tagsAPI.getAll(),
      ]);

      setCollections(collectionsRes.data.collections);
      setAvailableTags(tagsRes.data.tags);

      if (isEditMode) {
        const promptRes = await promptsAPI.getById(id);
        const prompt = promptRes.data;
        setFormData({
          title: prompt.title,
          content: prompt.content,
          description: prompt.description || '',
          collection_id: prompt.collection_id || '',
          tags: prompt.tags || [],
        });
      }
    } catch (err) {
      console.error('Error fetching data:', err);
      setSubmitError('Failed to load form data');
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length < 3) {
      newErrors.title = 'Title must be at least 3 characters';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be less than 200 characters';
    }

    if (!formData.content.trim()) {
      newErrors.content = 'Content is required';
    } else if (formData.content.length < 10) {
      newErrors.content = 'Content must be at least 10 characters';
    }

    if (formData.description && formData.description.length > 500) {
      newErrors.description = 'Description must be less than 500 characters';
    }

    if (formData.tags.length > 10) {
      newErrors.tags = 'Maximum 10 tags allowed';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const submitData = {
        ...formData,
        collection_id: formData.collection_id || null,
        description: formData.description || null,
      };

      if (isEditMode) {
        await promptsAPI.update(id, submitData);
        showToast('Prompt updated successfully', 'success');
      } else {
        await promptsAPI.create(submitData);
        showToast('Prompt created successfully', 'success');
      }

      navigate('/');
    } catch (err) {
      console.error('Error saving prompt:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to save prompt. Please try again.';
      setSubmitError(errorMessage);
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTag = (tag) => {
    const normalizedTag = tag.toLowerCase().trim().replace(/\s+/g, '-');
    
    if (!normalizedTag) return;
    
    if (formData.tags.includes(normalizedTag)) {
      setErrors({ ...errors, tags: 'Tag already added' });
      return;
    }

    if (formData.tags.length >= 10) {
      setErrors({ ...errors, tags: 'Maximum 10 tags allowed' });
      return;
    }

    if (!/^[a-z0-9-]+$/.test(normalizedTag)) {
      setErrors({ ...errors, tags: 'Tags can only contain lowercase letters, numbers, and hyphens' });
      return;
    }

    setFormData({ ...formData, tags: [...formData.tags, normalizedTag] });
    setTagInput('');
    setErrors({ ...errors, tags: '' });
  };

  const handleRemoveTag = (tagToRemove) => {
    setFormData({
      ...formData,
      tags: formData.tags.filter((tag) => tag !== tagToRemove),
    });
  };

  const handleTagInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag(tagInput);
    }
  };

  return (
    <div className="prompt-form-page">
      <div className="form-container">
        <div className="form-header">
          <h1>{isEditMode ? 'Edit Prompt' : 'Create New Prompt'}</h1>
          <Button variant="secondary" onClick={() => navigate('/')}>
            <ArrowLeftIcon size={16} /> Cancel
          </Button>
        </div>

        {submitError && (
          <div className="alert alert-error">
            {submitError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="prompt-form">
          <div className="form-group">
            <label htmlFor="title">
              Title <span className="required">*</span>
            </label>
            <input
              type="text"
              id="title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Enter prompt title"
              className={errors.title ? 'error' : ''}
              disabled={loading}
            />
            {errors.title && <span className="error-message">{errors.title}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="content">
              Content <span className="required">*</span>
            </label>
            <textarea
              id="content"
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              placeholder="Enter prompt content (use {{variable}} for placeholders)"
              rows="8"
              className={errors.content ? 'error' : ''}
              disabled={loading}
            />
            {errors.content && <span className="error-message">{errors.content}</span>}
            <span className="help-text">
              Tip: Use {`{{variable}}`} syntax for dynamic placeholders
            </span>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Enter optional description"
              rows="3"
              className={errors.description ? 'error' : ''}
              disabled={loading}
            />
            {errors.description && <span className="error-message">{errors.description}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="collection">Collection</label>
            <select
              id="collection"
              value={formData.collection_id}
              onChange={(e) => setFormData({ ...formData, collection_id: e.target.value })}
              disabled={loading}
            >
              <option value="">No Collection</option>
              {collections.map((col) => (
                <option key={col.id} value={col.id}>
                  {col.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="tags">Tags</label>
            <div className="tags-input-container">
              <input
                type="text"
                id="tags"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleTagInputKeyDown}
                placeholder="Type a tag and press Enter"
                className={errors.tags ? 'error' : ''}
                disabled={loading}
              />
              <button
                type="button"
                onClick={() => handleAddTag(tagInput)}
                className="btn-add-tag"
                disabled={loading || !tagInput.trim()}
              >
                Add
              </button>
            </div>
            {errors.tags && <span className="error-message">{errors.tags}</span>}
            
            {formData.tags.length > 0 && (
              <div className="tags-list">
                {formData.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="tag-remove"
                      disabled={loading}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}

            {availableTags.length > 0 && (
              <div className="suggested-tags">
                <span className="suggested-label">Suggested:</span>
                {availableTags.slice(0, 10).map((tag) => (
                  <button
                    key={tag.name}
                    type="button"
                    onClick={() => handleAddTag(tag.name)}
                    className="suggested-tag"
                    disabled={loading || formData.tags.includes(tag.name)}
                  >
                    {tag.name}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="form-actions">
            <Button
              type="submit"
              disabled={loading}
            >
              {loading ? 'Saving...' : isEditMode ? 'Update Prompt' : 'Create Prompt'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/')}
              disabled={loading}
            >
              <ArrowLeftIcon size={16} /> Cancel
            </Button>
          </div>
        </form>
      </div>

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

export default PromptForm;
