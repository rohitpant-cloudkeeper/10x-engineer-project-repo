import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { promptsAPI, versionsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import Button from '../components/Button';
import Modal from '../components/Modal';
import ConfirmDialog from '../components/ConfirmDialog';
import Toast from '../components/Toast';
import CopyButton from '../components/CopyButton';
import { ArrowLeftIcon, EditIcon, TrashIcon } from '../components/Icons';
import { useToast } from '../hooks/useToast';
import './PromptDetail.css';

function PromptDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast, showToast, hideToast } = useToast();
  
  const [prompt, setPrompt] = useState(null);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showVersions, setShowVersions] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState(null);
  const [compareMode, setCompareMode] = useState(false);
  const [compareVersions, setCompareVersions] = useState({ from: null, to: null });
  const [comparison, setComparison] = useState(null);
  const [expandedField, setExpandedField] = useState(null);
  const [confirmDialog, setConfirmDialog] = useState({ isOpen: false, title: '', message: '', onConfirm: null, variant: 'default' });

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
    setConfirmDialog({
      isOpen: true,
      title: 'Delete Prompt',
      message: 'Are you sure you want to delete this prompt? This action cannot be undone.',
      variant: 'danger',
      onConfirm: async () => {
        try {
          await promptsAPI.delete(id);
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast('Prompt deleted successfully', 'success');
          navigate('/');
        } catch (err) {
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast('Failed to delete prompt', 'error');
          console.error('Error deleting prompt:', err);
        }
      }
    });
  };

  const handleViewVersion = async (version) => {
    try {
      const response = await versionsAPI.getById(id, version);
      setSelectedVersion(response.data);
    } catch (err) {
      showToast('Failed to load version', 'error');
      console.error('Error loading version:', err);
    }
  };

  const handleRevertVersion = async (version) => {
    setConfirmDialog({
      isOpen: true,
      title: 'Revert Version',
      message: `Revert to version ${version}? This will create a new version.`,
      variant: 'default',
      onConfirm: async () => {
        try {
          await versionsAPI.revert(id, version);
          await fetchPromptData();
          setSelectedVersion(null);
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast(`Successfully reverted to version ${version}`, 'success');
        } catch (err) {
          setConfirmDialog({ ...confirmDialog, isOpen: false });
          showToast('Failed to revert version', 'error');
          console.error('Error reverting version:', err);
        }
      }
    });
  };

  const handleCompare = async () => {
    if (!compareVersions.from || !compareVersions.to) {
      showToast('Please select two versions to compare', 'info');
      return;
    }

    if (compareVersions.from === compareVersions.to) {
      showToast('Please select two different versions to compare', 'info');
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
      showToast('Failed to compare versions', 'error');
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
            <div className="section-actions">
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

                    <Button 
                      size="small" 
                      onClick={handleCompare}
                      disabled={!compareVersions.from || !compareVersions.to || compareVersions.from === compareVersions.to}
                    >
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
              <div className="accordion-list">
                {Object.entries(comparison.changes || {}).map(([field, status]) => (
                  <div key={field} className="accordion-item">
                    <button
                      className={`accordion-header change-${status}`}
                      onClick={() => setExpandedField(expandedField === field ? null : field)}
                    >
                      <span>
                        <strong>{field}:</strong> {status}
                      </span>
                      <span className="accordion-icon">
                        {expandedField === field ? '−' : '+'}
                      </span>
                    </button>
                    
                    {expandedField === field && (
                      <div className="accordion-content">
                        <div className="comparison-details">
                          <div className="comparison-column">
                            <h5>Version {comparison.from_version?.version}</h5>
                            <div className="version-content">
                              {field === 'title' && (
                                <p>{comparison.from_version?.title}</p>
                              )}
                              {field === 'content' && (
                                <pre>{comparison.from_version?.content}</pre>
                              )}
                              {field === 'description' && (
                                <p>{comparison.from_version?.description || 'No description'}</p>
                              )}
                              {field === 'tags' && (
                                <p>{comparison.from_version?.tags?.join(', ') || 'No tags'}</p>
                              )}
                            </div>
                          </div>

                          <div className="comparison-column">
                            <h5>Version {comparison.to_version?.version}</h5>
                            <div className="version-content">
                              {field === 'title' && (
                                <p>{comparison.to_version?.title}</p>
                              )}
                              {field === 'content' && (
                                <pre>{comparison.to_version?.content}</pre>
                              )}
                              {field === 'description' && (
                                <p>{comparison.to_version?.description || 'No description'}</p>
                              )}
                              {field === 'tags' && (
                                <p>{comparison.to_version?.tags?.join(', ') || 'No tags'}</p>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>

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

export default PromptDetail;
