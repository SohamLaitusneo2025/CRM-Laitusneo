# Email Campaigns Feature

## Overview
A comprehensive email campaign management system for sub-users (salesmen) to create and send bulk promotional emails from `laitusneotechnologies@gmail.com`.

## Features

### 1. Campaign Management
- **Create Campaigns**: Design email campaigns with custom subject and body
- **Recipient Management**: Add recipients individually or via bulk import
- **Campaign Status Tracking**: Monitor Draft, Sending, Sent, and Failed statuses
- **Campaign Details View**: See complete campaign information and recipient details

### 2. Email Sending
- **Bulk Email Sending**: Send to multiple recipients in one campaign
- **Professional Templates**: Emails sent with LaitusNeo Technologies branding
- **Status Tracking**: Track sent, failed, and pending emails
- **Error Handling**: Detailed error messages for failed sends

### 3. Analytics & Reporting
- **Campaign Statistics**: View total campaigns, emails sent, pending, and failed
- **Per-Email Status**: Track individual email delivery status
- **Campaign History**: View all past campaigns with timestamps

## Database Schema

### Campaign Table
```sql
- id: Primary key
- campaign_name: Name of the campaign
- subject: Email subject line
- email_body: Email content
- status: Draft/Sending/Sent/Failed
- total_recipients: Total number of recipients
- sent_count: Number of successfully sent emails
- failed_count: Number of failed emails
- created_at: Campaign creation timestamp
- sent_at: Campaign send timestamp
- salesman_id: Foreign key to user (sub-user who created it)
```

### CampaignEmail Table
```sql
- id: Primary key
- campaign_id: Foreign key to campaign
- recipient_email: Email address
- recipient_name: Optional recipient name
- status: Pending/Sent/Failed/Bounced
- error_message: Error details if failed
- sent_at: Email send timestamp
- opened_at: Email open timestamp (for future tracking)
- created_at: Record creation timestamp
```

## API Endpoints

### 1. Get All Campaigns
```
GET /api/salesman/campaigns
Authorization: Bearer <token>
```
Returns list of all campaigns for the logged-in sub-user.

### 2. Get Campaign Details
```
GET /api/salesman/campaigns/<campaign_id>
Authorization: Bearer <token>
```
Returns detailed campaign information including all recipient emails.

### 3. Create Campaign
```
POST /api/salesman/campaigns
Authorization: Bearer <token>
Content-Type: application/json

{
  "campaignName": "Summer Product Launch",
  "subject": "Introducing Our New Product Line",
  "emailBody": "Email content here...",
  "recipients": [
    "email1@example.com",
    "email2@example.com",
    {"email": "email3@example.com", "name": "John Doe"}
  ]
}
```

### 4. Send Campaign
```
POST /api/salesman/campaigns/<campaign_id>/send
Authorization: Bearer <token>
```
Sends all pending emails in the campaign.

### 5. Delete Campaign
```
DELETE /api/salesman/campaigns/<campaign_id>
Authorization: Bearer <token>
```
Deletes a campaign and all associated emails (cascade).

## Frontend Components

### CampaignManagement Component
Located at: `src/components/SubUser/CampaignManagement/`

**Files:**
- `CampaignManagement.js` - Main component logic
- `CampaignManagement.css` - Styling
- `index.js` - Export

**Features:**
- Campaign list view with sortable table
- Create campaign modal with form validation
- Campaign details modal with recipient list
- Real-time status updates
- Success/error notifications
- Responsive design

## Email Template

Emails are sent with professional HTML formatting including:
- LaitusNeo Technologies branding
- Gradient header
- Personalized greeting (if recipient name provided)
- Custom email body content
- Salesman signature
- Company footer

## Usage Guide

### For Sub-Users (Salesmen):

1. **Navigate to Campaigns**
   - Click "Campaigns" in the sub-user navigation menu

2. **Create a Campaign**
   - Click "Create Campaign" button
   - Enter campaign name (internal reference)
   - Enter email subject
   - Write email body
   - Add recipients:
     - Type email and click "Add"
     - Or use bulk import (paste multiple emails)

3. **Review Campaign**
   - Campaign is saved as "Draft"
   - Click eye icon to view details
   - Verify all information

4. **Send Campaign**
   - Click send icon (paper plane)
   - Confirm in dialog
   - Wait for completion
   - Check statistics for results

5. **Monitor Results**
   - View campaign details to see individual email statuses
   - Check sent/failed counts
   - Review error messages for failed sends

## Configuration

### Email Settings (backend/config.py)
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'laitusneotechnologies@gmail.com'
MAIL_PASSWORD = 'pxxt imsl qmfw xgij'  # App password
MAIL_DEFAULT_SENDER = 'laitusneotechnologies@gmail.com'
```

**Note:** The password shown is a Google App Password, not the actual Gmail password.

## Security Features

1. **Authentication**: JWT token required for all endpoints
2. **Authorization**: Only sub-users can access campaign endpoints
3. **Ownership Validation**: Users can only view/modify their own campaigns
4. **Email Validation**: All email addresses validated before accepting
5. **SQL Injection Prevention**: Using SQLAlchemy ORM

## Error Handling

### Common Errors:
- **Invalid email format**: Validated on frontend and backend
- **SMTP errors**: Caught and logged with error message
- **Network errors**: Proper error messages displayed to user
- **Authentication errors**: Redirects to login page

### Email Sending Errors:
- Each email error is tracked individually
- Campaign continues sending to other recipients even if some fail
- Error messages stored in `campaign_emails.error_message`

## Future Enhancements

1. **Email Open Tracking**: Track when recipients open emails
2. **Link Click Tracking**: Monitor engagement with email links
3. **Email Templates**: Pre-designed templates for common campaigns
4. **Scheduling**: Schedule campaigns to send at specific times
5. **A/B Testing**: Test different subject lines and content
6. **Attachments**: Support for file attachments
7. **Unsubscribe Management**: Handle unsubscribe requests
8. **Email Analytics Dashboard**: Advanced metrics and charts

## Testing

### Manual Testing Steps:

1. **Start Backend**
   ```bash
   cd backend
   python run.py
   ```

2. **Start Frontend**
   ```bash
   npm start
   ```

3. **Login as Sub-User**
   - Use a sub-user account (created by main user)

4. **Create Test Campaign**
   - Create campaign with your own email as recipient
   - Send campaign
   - Check your inbox

5. **Verify Database**
   - Check `campaigns` table for new record
   - Check `campaign_emails` table for recipient records
   - Verify status updates after sending

### API Testing with curl:

```bash
# Get campaigns
curl -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/salesman/campaigns

# Create campaign
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"campaignName":"Test","subject":"Test","emailBody":"Test content","recipients":["test@example.com"]}' \
  http://localhost:5000/api/salesman/campaigns

# Send campaign
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/salesman/campaigns/1/send
```

## Troubleshooting

### Emails Not Sending
1. Check SMTP configuration in `config.py`
2. Verify Google App Password is correct
3. Check if Gmail account has "Less secure app access" enabled (if needed)
4. Look for error messages in backend console
5. Check firewall/network settings for port 587

### Frontend Not Loading
1. Verify backend is running on port 5000
2. Check browser console for errors
3. Verify JWT token is valid
4. Check CORS settings in backend

### Database Errors
1. Ensure MySQL is running
2. Verify database `crm_laitusneo` exists
3. Check database credentials in `config.py`
4. Run `python run.py` to create tables

## Support

For issues or questions:
- Check the console logs (frontend and backend)
- Review error messages displayed in the UI
- Verify email configuration
- Ensure proper authentication

---

**Version:** 1.0  
**Last Updated:** October 16, 2025  
**Author:** CRM Development Team

