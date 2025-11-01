// API Configuration - Centralized API URL management
// Change this URL to point to your backend server (AWS instance)

const API_CONFIG = {
  // Development/Local URL
  LOCAL_URL: 'http://localhost:5000/api',
  
  // Production/AWS URL - Change this to your AWS instance IP/domain
  PRODUCTION_URL: 'http://3.110.25.207:5000/api', // Your AWS instance URL
  
  
  ENVIRONMENT: 'production', // Set to production to use AWS URL
  
  
  getBaseURL() {
    // First check for environment variable override
    if (process.env.REACT_APP_API_URL) {
      return process.env.REACT_APP_API_URL;
    }
    
  
    if (this.ENVIRONMENT === 'production') {
      return this.PRODUCTION_URL;
    }
    
    return this.LOCAL_URL;
  },
  
  getFullURL(endpoint = '') {
    const baseURL = this.getBaseURL();
    return endpoint.startsWith('/') ? `${baseURL}${endpoint}` : `${baseURL}/${endpoint}`;
  },
  
  // Method to manually set production URL (useful for quick changes)
  setProductionURL(url) {
    this.PRODUCTION_URL = url.endsWith('/api') ? url : `${url}/api`;
  },
  
  // Method to force environment
  setEnvironment(env) {
    this.ENVIRONMENT = env;
  }
};

export default API_CONFIG;

// Export base URL for backward compatibility
export const BASE_URL = API_CONFIG.getBaseURL();

// Quick setup for AWS deployment
// Your AWS instance is now configured:
API_CONFIG.setProductionURL('http://3.110.25.207:5000');
API_CONFIG.setEnvironment('production');