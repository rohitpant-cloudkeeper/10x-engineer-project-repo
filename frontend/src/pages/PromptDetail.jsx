import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { promptsAPI, versionsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import Button from '../components/Button';
import Modal from '../components/Modal';
import CopyButton from '../components/CopyButton';
import { ArrowLeftIcon, EditIcon, TrashIcon } from '../components/Icons';
import './PromptDetail.css';

function PromptDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [prompt, setPrompt] = useState(null);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showVersions, setShowVersions] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState(null);
  const [compareMode, setCompareMode] = useState(false);
  const [compareVersions, setCompareVersions] = useState({ from: null, to: null });
  const [comparison, setComparison] = useState(null);

  useEffect(() => {
    fetchPromptData();
  }, [id]);

  const fetchPromptData = async () => {
    try {
      setLoading(true);
      const [promptRes, versionsRes] = await Promise.all([
        promptsAPI.getById(id),
        versionsAPI.getAll(id)
      ]);
      
      setPrompt(promptRes.data);
      setVersions(versionsRes.data.versions || []);
      setError(null);
    } catch (err) {
      setError('Failed to load prompt details');
      console.error('Error fetching prompt:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this prompt?')) return;

    try {
      await promptsAPI.delete(id);
      navigate('/');
    } catch (err) {
      alert('Failed to delete prompt');
      console.error('Error deleting prompt:', err);
    }
  };

  const handleViewVersion = async (version) => {
    try {
      const response = await versionsAPI.getById(id, version);
      setSelectedVersion(response.data);
    } catch (err) {
      alert('Failed to load version');
      console.error('Error loading version:', err);
    }
  };

  const handleRevertVersion = async (version) => {
    if (!window.confirm(`Revert to version ${version}? This will create a new version.`)) return;

    try {
      await versionsAPI.revert(id, version);
      await fetchPromptData();
      setSelectedVersion(null);
      alert(`Successfully reverted to version ${version}`);
    } catch (err) {
      alert('Failed to revert version');
      console.error('Error reverting version:', err);
    }
  };

  const handleCompare = async () => {
    if (!compareVersions.from || !compareVersions.to) {
      alert('Please select two versions to compare');
      return;
    }

    try {
      const response = await versionsAPI.compare(
        id, 
        compareVersions.from, 
        compareVersions.to
      );
      setComparison(response.data);
    } catch (err) {
      alert('Failed to compare versions');
      console.error('Error comparing versions:', err);
    }
  };

  if (loading) {
    return <LoadingSpinner size="large" message="Loading prompt details..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchPromptData} />;
  }

  if (!prompt) {
    return <ErrorMessage message="Prompt not found" type="warning" />;
  }

  return (
    <div className="prompt-detail-page">
      <div className="detail-header">
        <Button variant="secondary" onClick={() => navigate('/')}>
          <ArrowLeftIcon size={16} /> Back to Prompts
        </Button>
        <div className="detail-actions">
          <Button onClick={() => navigate(`/prompts/${id}/edit`)}>
            <EditIcon size={16} /> Edit
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            <TrashIcon size={16} /> Delete
          </Button>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-main">
          <div className="detail-title-section">
            <h1>{prompt.title}</h1>
            <span className="version-badge">Version {prompt.version}</span>
          </div>

          {prompt.description && (
            <p className="detail-description">{prompt.description}</p>
          )}

          <div className="detail-section">
            <h2>Content</h2>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '0.5rem' }}>
              <CopyButton text={prompt.content} label="Copy Content" />
            </div>
            <pre className="prompt-content-display">{prompt.content}</pre>
          </div>

          {prompt.tags && prompt.tags.length > 0 && (
            <div className="detail-section">
              <h2>Tags</h2>
              <div className="tags-display">
                {prompt.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="detail-metadata">
            <div className="metadata-item">
              <span className="metadata-label">Created:</span>
              <span className="metadata-value">
                {new Date(prompt.created_at).toLocaleString()}
              </span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">Last Updated:</span>
              <span className="metadata-value">
                {new Date(prompt.updated_at).toLocaleString()}
              </span>
            </div>
            {prompt.collection_id && (
              <div className="metadata-item">
                <span className="metadata-label">Collection ID:</span>
                <span className="metadata-value">{prompt.collection_id}</span>
              </div>
            )}
          </div>
        </div>

        <div className="detail-sidebar">
          <div className="sidebar-section">
            <h3>Version History</h3>
            <Button 
              variant="secondary" 
              size="small"
              onClick={() => setShowVersions(!showVersions)}
            >
              {showVersions ? 'Hide' : 'Show'} Versions ({versions.length})
            </Button>

            {showVersions && versions.length > 0 && (
              <div className="versions-list">
                {versions.map((v) => (
                  <div key={v.version} className="version-item">
                    <div className="version-info">
                      <strong>v{v.version}</strong>
                      {v.version === prompt.version && (
                        <span className="current-badge">Current</span>
                      )}
                      <span className="version-date">
                        {new Date(v.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="version-actions">
                      <button
                        className="btn-link"
                        onClick={() => handleViewVersion(v.version)}
                      >
                        View
                      </button>
                      {v.version !== prompt.version && (
                        <button
                          className="btn-link"
                          onClick={() => handleRevertVersion(v.version)}
                        >
                          Revert
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {versions.length > 1 && (
              <div className="compare-section">
                <Button
                  variant="secondary"
                  size="small"
                  onClick={() => setCompareMode(!compareMode)}
                >
                  Compare Versions
                </Button>

                {compareMode && (
                  <div className="compare-form">
                    <select
                      value={compareVersions.from || ''}
                      onChange={(e) => setCompareVersions({
                        ...compareVersions,
                        from: parseInt(e.target.value)
                      })}
                    >
                      <option value="">From version...</option>
                      {versions.map((v) => (
                        <option key={v.version} value={v.version}>
                          v{v.version}
                        </option>
                      ))}
                    </select>

                    <select
                      value={compareVersions.to || ''}
                      onChange={(e) => setCompareVersions({
                        ...compareVersions,
                        to: parseInt(e.target.value)
                      })}
                    >
                      <option value="">To version...</option>
                      {versions.map((v) => (
                        <option key={v.version} value={v.version}>
                          v{v.version}
                        </option>
                      ))}
                    </select>

                    <Button size="small" onClick={handleCompare}>
                      Compare
                    </Button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Version Detail Modal */}
      <Modal
        isOpen={selectedVersion !== null}
        onClose={() => setSelectedVersion(null)}
        title={`Version ${selectedVersion?.version}`}
      >
        {selectedVersion && (
          <div className="version-detail">
            <div className="version-field">
              <strong>Title:</strong>
              <p>{selectedVersion.title}</p>
            </div>
            <div className="version-field">
              <strong>Content:</strong>
              <pre>{selectedVersion.content}</pre>
            </div>
            {selectedVersion.description && (
              <div className="version-field">
                <strong>Description:</strong>
                <p>{selectedVersion.description}</p>
              </div>
            )}
            {selectedVersion.tags && selectedVersion.tags.length > 0 && (
              <div className="version-field">
                <strong>Tags:</strong>
                <div className="tags-display">
                  {selectedVersion.tags.map((tag) => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                </div>
              </div>
            )}
            <div className="version-field">
              <strong>Created:</strong>
              <p>{new Date(selectedVersion.created_at).toLocaleString()}</p>
            </div>
          </div>
        )}
      </Modal>

      {/* Comparison Modal */}
      <Modal
        isOpen={comparison !== null}
        onClose={() => setComparison(null)}
        title="Version Comparison"
      >
        {comparison && (
          <div className="comparison-view">
            <div className="comparison-summary">
              <h4>Changes Summary</h4>
              <ul>
                {Object.entries(comparison.changes || {}).map(([field, status]) => (
                  <li key={field} className={`change-${status}`}>
                    <strong>{field}:</strong> {status}
                  </li>
                ))}
              </ul>
            </div>

            <div className="comparison-details">
              <div className="comparison-column">
                <h4>Version {comparison.from_version?.version}</h4>
                <div className="version-content">
                  <p><strong>Title:</strong> {comparison.from_version?.title}</p>
                  <p><strong>Content:</strong></p>
                  <pre>{comparison.from_version?.content}</pre>
                </div>
              </div>

              <div className="comparison-column">
                <h4>Version {comparison.to_version?.version}</h4>
                <div className="version-content">
                  <p><strong>Title:</strong> {comparison.to_version?.title}</p>
                  <p><strong>Content:</strong></p>
                  <pre>{comparison.to_version?.content}</pre>
                </div>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default PromptDetail;
