import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Mail, Send, Clock, AlertCircle } from 'lucide-react';
import API_CONFIG from '../../../config/apiConfig';
import './CampaignManagement.css';

const CampaignManagement = () => {
  const [activeTab, setActiveTab] = useState('email');
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form state
  const [campaignName, setCampaignName] = useState('');
  const [subject, setSubject] = useState('');
  const [emailBody, setEmailBody] = useState('');
  const [recipientInput, setRecipientInput] = useState('');
  const [recipients, setRecipients] = useState([]);
  const [bulkEmails, setBulkEmails] = useState('');

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_CONFIG.getBaseURL()}/salesman/campaigns`);
      setCampaigns(response.data.campaigns || []);
      setError('');
    } catch (err) {
      console.error('Error fetching campaigns:', err);
      setError('Failed to load campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handleAddRecipient = () => {
    const email = recipientInput.trim();
    if (email && validateEmail(email) && !recipients.includes(email)) {
      setRecipients([...recipients, email]);
      setRecipientInput('');
    } else if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleRemoveRecipient = (email) => {
    setRecipients(recipients.filter(r => r !== email));
  };

  const handleBulkImport = () => {
    const emails = bulkEmails
      .split(/[\n,;]/)
      .map(e => e.trim())
      .filter(e => e && validateEmail(e));
    
    const uniqueEmails = [...new Set([...recipients, ...emails])];
    setRecipients(uniqueEmails);
    setBulkEmails('');
  };

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const handleCreateCampaign = async (e) => {
    e.preventDefault();
    
    if (recipients.length === 0) {
      setError('Please add at least one recipient');
      return;
    }

    try {
      const response = await axios.post(`${API_CONFIG.getBaseURL()}/salesman/campaigns`, {
        campaignName,
        subject,
        emailBody,
        recipients
      });

      setSuccess('Campaign created successfully!');
      setCampaigns([response.data.campaign, ...campaigns]);
      resetForm();
      setShowCreateModal(false);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error creating campaign:', err);
      setError(err.response?.data?.error || 'Failed to create campaign');
    }
  };

  const handleSendCampaign = async (campaignId) => {
    if (!window.confirm('Are you sure you want to send this campaign? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await axios.post(`${API_CONFIG.getBaseURL()}/salesman/campaigns/${campaignId}/send`);
      setSuccess(`Campaign sent! ${response.data.sentCount} emails sent successfully.`);
      fetchCampaigns();
      setTimeout(() => setSuccess(''), 5000);
    } catch (err) {
      console.error('Error sending campaign:', err);
      setError(err.response?.data?.error || 'Failed to send campaign');
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleDeleteCampaign = async (campaignId) => {
    if (!window.confirm('Are you sure you want to delete this campaign?')) {
      return;
    }

    try {
      await axios.delete(`${API_CONFIG.getBaseURL()}/salesman/campaigns/${campaignId}`);
      setCampaigns(campaigns.filter(c => c.id !== campaignId));
      setSuccess('Campaign deleted successfully');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error deleting campaign:', err);
      setError(err.response?.data?.error || 'Failed to delete campaign');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleViewDetails = async (campaignId) => {
    try {
      const response = await axios.get(`${API_CONFIG.getBaseURL()}/salesman/campaigns/${campaignId}`);
      setSelectedCampaign(response.data);
      setShowDetailsModal(true);
    } catch (err) {
      console.error('Error fetching campaign details:', err);
      setError('Failed to load campaign details');
      setTimeout(() => setError(''), 3000);
    }
  };

  const resetForm = () => {
    setCampaignName('');
    setSubject('');
    setEmailBody('');
    setRecipients([]);
    setRecipientInput('');
    setBulkEmails('');
  };

  const getTotalCampaigns = () => campaigns.length;
  const getTotalSent = () => campaigns.reduce((sum, c) => sum + (c.sentCount || 0), 0);
  const getTotalPending = () => campaigns.filter(c => c.status === 'Draft').length;
  const getTotalFailed = () => campaigns.reduce((sum, c) => sum + (c.failedCount || 0), 0);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  return (
    <div className="campaign-management">
      <div className="campaign-header">
        <div className="header-content">
          <h2>Campaigns</h2>
        </div>
        <div className="header-actions">
          <div className="view-toggle">
            <button
              className={`view-btn ${activeTab === 'email' ? 'active' : ''}`}
              onClick={() => setActiveTab('email')}
            >
              <Mail size={18} />
              Email
            </button>
            <button
              className={`view-btn ${activeTab === 'whatsapp' ? 'active' : ''}`}
              onClick={() => setActiveTab('whatsapp')}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              WhatsApp
            </button>
          </div>
          {activeTab === 'email' && (
            <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
              <span>+</span> Create Campaign
            </button>
          )}
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      {activeTab === 'email' ? (
        <>
          <div className="campaign-stats">
        <div className="stat-card primary">
          <div className="stat-icon">
            <Mail size={24} />
          </div>
          <div className="stat-info">
            <h3>Total Campaigns</h3>
            <p className="stat-value">{getTotalCampaigns()}</p>
          </div>
        </div>
        <div className="stat-card success">
          <div className="stat-icon">
            <Send size={24} />
          </div>
          <div className="stat-info">
            <h3>Emails Sent</h3>
            <p className="stat-value">{getTotalSent()}</p>
          </div>
        </div>
        <div className="stat-card warning">
          <div className="stat-icon">
            <Clock size={24} />
          </div>
          <div className="stat-info">
            <h3>Pending</h3>
            <p className="stat-value">{getTotalPending()}</p>
          </div>
        </div>
        <div className="stat-card error">
          <div className="stat-icon">
            <AlertCircle size={24} />
          </div>
          <div className="stat-info">
            <h3>Failed</h3>
            <p className="stat-value">{getTotalFailed()}</p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading campaigns...</div>
      ) : campaigns.length === 0 ? (
        <div className="empty-state">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <h3>No campaigns yet</h3>
          <p>Create your first email campaign to get started</p>
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            Create Your First Campaign
          </button>
        </div>
      ) : (
        <div className="campaigns-list">
          <table className="campaigns-table">
            <thead>
              <tr>
                <th>Campaign ID</th>
                <th>Campaign</th>
                <th>Status</th>
                <th>Recipients</th>
                <th>Sent / Failed</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {campaigns.map((campaign) => (
                <tr key={campaign.id}>
                  <td>
                    <span className="campaign-id">{campaign.campaignId}</span>
                  </td>
                  <td>
                    <div className="campaign-name">{campaign.campaignName}</div>
                    <div className="campaign-subject">{campaign.subject}</div>
                  </td>
                  <td>
                    <span className={`status-badge ${campaign.status.toLowerCase()}`}>
                      {campaign.status}
                    </span>
                  </td>
                  <td className="text-center">{campaign.totalRecipients}</td>
                  <td>
                    <div className="campaign-metrics">
                      <span className="metric success">{campaign.sentCount || 0} sent</span>
                      {campaign.failedCount > 0 && (
                        <span className="metric error">{campaign.failedCount} failed</span>
                      )}
                    </div>
                  </td>
                  <td className="text-small">{formatDate(campaign.createdAt)}</td>
                  <td>
                    <div className="campaign-actions-cell">
                      <button
                        className="btn-icon view"
                        onClick={() => handleViewDetails(campaign.id)}
                        title="View Details"
                      >
                        <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>
                      {campaign.status === 'Draft' && (
                        <button
                          className="btn-icon send"
                          onClick={() => handleSendCampaign(campaign.id)}
                          title="Send Campaign"
                        >
                          <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                          </svg>
                        </button>
                      )}
                      <button
                        className="btn-icon delete"
                        onClick={() => handleDeleteCampaign(campaign.id)}
                        title="Delete Campaign"
                      >
                        <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Campaign Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Create Email Campaign</h3>
              <button className="modal-close" onClick={() => setShowCreateModal(false)}>
                ×
              </button>
            </div>
            <form onSubmit={handleCreateCampaign}>
              <div className="modal-body">
                <div className="form-group">
                  <label>Campaign Name *</label>
                  <input
                    type="text"
                    value={campaignName}
                    onChange={(e) => setCampaignName(e.target.value)}
                    placeholder="e.g., Summer Product Launch"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Email Subject *</label>
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="e.g., Introducing Our New Product Line"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Email Body *</label>
                  <textarea
                    value={emailBody}
                    onChange={(e) => setEmailBody(e.target.value)}
                    placeholder="Write your email content here..."
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Recipients *</label>
                  <div className="recipients-input-wrapper">
                    <input
                      type="email"
                      value={recipientInput}
                      onChange={(e) => setRecipientInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddRecipient())}
                      placeholder="Enter email address"
                    />
                    <button
                      type="button"
                      className="btn-add"
                      onClick={handleAddRecipient}
                    >
                      Add
                    </button>
                  </div>
                  
                  {recipients.length > 0 && (
                    <div className="recipients-list">
                      {recipients.map((email, index) => (
                        <div key={index} className="recipient-chip">
                          <span>{email}</span>
                          <button type="button" onClick={() => handleRemoveRecipient(email)}>
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="bulk-import-section">
                    <h4>Bulk Import</h4>
                    <textarea
                      value={bulkEmails}
                      onChange={(e) => setBulkEmails(e.target.value)}
                      placeholder="Paste multiple emails (one per line or comma-separated)"
                    />
                    <p>Add multiple emails at once by pasting them above</p>
                    <button type="button" className="btn-add" onClick={handleBulkImport}>
                      📥 Import
                    </button>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn-cancel"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-submit"
                  disabled={!campaignName || !subject || !emailBody || recipients.length === 0}
                >
                  Create Campaign
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Campaign Details Modal */}
      {showDetailsModal && selectedCampaign && (
        <div className="modal-overlay" onClick={() => setShowDetailsModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Campaign Details</h3>
              <button className="modal-close" onClick={() => setShowDetailsModal(false)}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="campaign-details">
                <div className="details-section">
                  <h4>Campaign Information</h4>
                  <div className="detail-row">
                    <span className="detail-label">Campaign Name:</span>
                    <span className="detail-value">{selectedCampaign.campaignName}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Subject:</span>
                    <span className="detail-value">{selectedCampaign.subject}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Status:</span>
                    <span className="detail-value">
                      <span className={`status-badge ${selectedCampaign.status.toLowerCase()}`}>
                        {selectedCampaign.status}
                      </span>
                    </span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Created:</span>
                    <span className="detail-value">{formatDate(selectedCampaign.createdAt)}</span>
                  </div>
                  {selectedCampaign.sentAt && (
                    <div className="detail-row">
                      <span className="detail-label">Sent:</span>
                      <span className="detail-value">{formatDate(selectedCampaign.sentAt)}</span>
                    </div>
                  )}
                  <div className="detail-row">
                    <span className="detail-label">Total Recipients:</span>
                    <span className="detail-value">{selectedCampaign.totalRecipients}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Sent:</span>
                    <span className="detail-value">{selectedCampaign.sentCount || 0}</span>
                  </div>
                  {selectedCampaign.failedCount > 0 && (
                    <div className="detail-row">
                      <span className="detail-label">Failed:</span>
                      <span className="detail-value" style={{ color: '#ef4444' }}>
                        {selectedCampaign.failedCount}
                      </span>
                    </div>
                  )}
                </div>

                <div className="details-section">
                  <h4>Email Body</h4>
                  <div className="email-body-preview">{selectedCampaign.emailBody}</div>
                </div>

                {selectedCampaign.emails && selectedCampaign.emails.length > 0 && (
                  <div className="details-section">
                    <h4>Recipients ({selectedCampaign.emails.length})</h4>
                    <div className="emails-table-wrapper">
                      <table className="emails-table">
                        <thead>
                          <tr>
                            <th>Email</th>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Sent At</th>
                          </tr>
                        </thead>
                        <tbody>
                          {selectedCampaign.emails.map((email) => (
                            <tr key={email.id}>
                              <td>{email.recipientEmail}</td>
                              <td>{email.recipientName || '-'}</td>
                              <td>
                                <span className={`status-badge ${email.status.toLowerCase()}`}>
                                  {email.status}
                                </span>
                              </td>
                              <td>{email.sentAt ? formatDate(email.sentAt) : '-'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button
                className="btn-cancel"
                onClick={() => setShowDetailsModal(false)}
              >
                Close
              </button>
              {selectedCampaign.status === 'Draft' && (
                <button
                  className="btn-submit"
                  onClick={() => {
                    setShowDetailsModal(false);
                    handleSendCampaign(selectedCampaign.id);
                  }}
                >
                  Send Campaign
                </button>
              )}
            </div>
          </div>
        </div>
      )}
        </>
      ) : (
        <div className="whatsapp-placeholder">
          <div className="placeholder-content">
            <div className="placeholder-icon">💬</div>
            <h3>WhatsApp Campaigns</h3>
            {/* <p>WhatsApp campaign feature coming soon...</p> */}
          </div>
        </div>
      )}
    </div>
  );
};

export default CampaignManagement;

