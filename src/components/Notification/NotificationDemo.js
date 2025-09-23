import React from 'react';
import { useNotification } from '../../contexts/NotificationContext';
import './NotificationDemo.css'; // Optional: for demo specific styling

const NotificationDemo = () => {
  const { showSuccess, showError, showWarning, showInfo } = useNotification();

  return (
    <div className="notification-demo-container">
      <h2>Notification System Demo</h2>
      <p>Click the buttons below to trigger different types of notifications.</p>
      <div className="button-group">
        <button onClick={() => showSuccess('Lead accepted successfully!', 4000, 'Success!')}>
          Show Success
        </button>
        <button onClick={() => showError('Failed to save changes. Please try again.', 5000, 'Error!')}>
          Show Error
        </button>
        <button onClick={() => showWarning('This action cannot be undone. Proceed with caution.', 4500, 'Warning!')}>
          Show Warning
        </button>
        <button onClick={() => showInfo('New updates are available. Refresh your browser.', 4000, 'Information')}>
          Show Info
        </button>
        <button onClick={() => showSuccess('Another success message!', 3000)}>
          Short Success
        </button>
        <button onClick={() => showError('Multiple errors can stack up!', 6000, 'Critical Error')}>
          Long Error
        </button>
      </div>
    </div>
  );
};

export default NotificationDemo;
