// Google Meet Integration Service
import API_CONFIG from '../config/apiConfig';

class GoogleMeetService {
  constructor() {
    this.baseURL = API_CONFIG.getBaseURL();
  }

  // Get auth token
  getAuthToken() {
    return (
      localStorage.getItem('access_token') ||
      localStorage.getItem('token') ||
      localStorage.getItem('jwt') ||
      ''
    );
  }

  // Create Google Meet meeting
  async createGoogleMeetMeeting(meetingData) {
    try {
      const token = this.getAuthToken();
      const response = await fetch(`${this.baseURL}/meetings/google-meet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : undefined
        },
        body: JSON.stringify(meetingData),
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating Google Meet meeting:', error);
      throw error;
    }
  }

  // Send meeting invitation email
  async sendMeetingInvitation(meetingData) {
    try {
      const token = this.getAuthToken();
      const response = await fetch(`${this.baseURL}/meetings/send-invitation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : undefined
        },
        body: JSON.stringify(meetingData),
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error sending meeting invitation:', error);
      throw error;
    }
  }

  // Generate Google Meet link (fallback method)
  generateGoogleMeetLink() {
    // This is a fallback method that generates a Google Meet link
    // In a real implementation, this would integrate with Google Calendar API
    const meetingId = this.generateMeetingId();
    return `https://meet.google.com/${meetingId}`;
  }

  // Generate a random meeting ID in Google Meet format: abc-defg-hij
  generateMeetingId() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    
    const generateGroup = (length) => {
      let result = '';
      for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return result;
    };
    
    const group1 = generateGroup(3);
    const group2 = generateGroup(4);
    const group3 = generateGroup(3);
    
    return `${group1}-${group2}-${group3}`;
  }

  // Format meeting data for Google Meet
  formatMeetingDataForGoogleMeet(meetingData) {
    const startDateTime = new Date(`${meetingData.date}T${meetingData.time}`);
    const endDateTime = new Date(startDateTime.getTime() + (60 * 60 * 1000)); // 1 hour duration

    return {
      summary: `Meeting with ${meetingData.clientName}`,
      description: `Product discussion meeting for ${meetingData.productName || 'our services'}`,
      start: {
        dateTime: startDateTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      end: {
        dateTime: endDateTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      attendees: [
        {
          email: meetingData.email,
          displayName: meetingData.clientName
        }
      ],
      conferenceData: {
        createRequest: {
          requestId: `meeting-${Date.now()}`,
          conferenceSolutionKey: {
            type: 'hangoutsMeet'
          }
        }
      }
    };
  }
}

const googleMeetServiceInstance = new GoogleMeetService();
export default googleMeetServiceInstance;
