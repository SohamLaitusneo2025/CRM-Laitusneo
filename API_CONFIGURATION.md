# API Configuration Guide

This guide explains how to easily change the backend API URL for your CRM application when deploying to different environments (local, AWS, etc.).

## Quick Setup for AWS Deployment

### Method 1: Using the Config File (Recommended)

1. Open `src/config/apiConfig.js`
2. Find the line:
   ```javascript
   PRODUCTION_URL: 'http://localhost:5000/api', // Replace with your AWS IP: http://YOUR_AWS_IP:5000/api
   ```
3. Replace it with your AWS instance IP:
   ```javascript
   PRODUCTION_URL: 'http://YOUR_AWS_IP:5000/api', // Replace YOUR_AWS_IP with actual IP
   ```
4. At the bottom of the file, uncomment and modify these lines:
   ```javascript
   API_CONFIG.setProductionURL('http://YOUR_AWS_IP:5000');
   API_CONFIG.setEnvironment('production');
   ```

### Method 2: Using Environment Variables

1. Create a `.env` file in your project root
2. Add the following line:
   ```
   REACT_APP_API_URL=http://YOUR_AWS_IP:5000/api
   ```
3. Replace `YOUR_AWS_IP` with your actual AWS instance IP address

## Examples

### For AWS Instance with IP 3.15.123.45:
```javascript
// In apiConfig.js
PRODUCTION_URL: 'http://3.15.123.45:5000/api'

// Or in .env file
REACT_APP_API_URL=http://3.15.123.45:5000/api
```

### For Domain Name:
```javascript
// In apiConfig.js  
PRODUCTION_URL: 'https://your-domain.com/api'

// Or in .env file
REACT_APP_API_URL=https://your-domain.com/api
```

## How It Works

- **Development**: Automatically uses `http://localhost:5000/api`
- **Production**: Uses the URL you set in the config
- **Environment Variable**: Takes highest priority if set

## Files Updated

All API calls in these files now use the centralized configuration:

- `src/services/dataService.js`
- `src/services/googleMeetService.js`
- `src/contexts/AuthContext.js`
- `src/components/SubUser/PitchDeck/index.js`
- `src/components/SubUser/CampaignManagement/CampaignManagement.js`
- `src/components/SalesmanManagement/ReportGeneration.js`
- `src/components/SalesmanManagement/SalesmanManagement.js`
- `src/components/SalesmanManagement/SalesmanList.js`
- `src/components/SalesmanManagement/SalesmanEditForm.js`
- `src/components/SalesmanManagement/AccountCreation.js`
- `src/components/ProductManagement/ProductManagement.js`
- `src/components/CampaignManagement/CampaignManagement.js`

## Benefits

✅ **Single Point of Control**: Change URL in one place  
✅ **Environment Support**: Automatic local/production switching  
✅ **Easy AWS Deployment**: Just update one line for new instances  
✅ **No Code Changes**: Switch environments without touching component files  
✅ **Backward Compatible**: Still supports environment variables