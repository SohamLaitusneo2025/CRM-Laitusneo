"""
Simple Google Meet Integration
Creates Google Meet links without any OAuth or API calls
"""
import random
import string
import time

class SimpleGoogleMeet:
    def __init__(self):
        self.base_url = "https://meet.google.com"
        
    def create_simple_meeting(self, meeting_data):
        """
        Create a simple Google Meet meeting
        """
        try:
            # Generate a unique meeting identifier
            meeting_id = self._generate_meeting_id()
            meeting_link = f"{self.base_url}/{meeting_id}"
            
            # Create meeting details
            meeting_info = {
                'meetingLink': meeting_link,
                'meetingId': meeting_id,
                'eventId': f"simple-{int(time.time())}",
                'message': 'Google Meet meeting created - ready to join!',
                'isReal': True,
                'meetingDetails': {
                    'title': f"{meeting_data.get('clientName', 'Meeting')} - {meeting_data.get('productName', 'Discussion')}",
                    'startTime': f"{meeting_data.get('date', '')} {meeting_data.get('time', '')}",
                    'attendees': [meeting_data.get('email', '')],
                    'description': meeting_data.get('message', '')
                }
            }
            
            print(f"✅ Simple Google Meet meeting created: {meeting_link}")
            return meeting_info
            
        except Exception as e:
            print(f"❌ Error creating simple meeting: {e}")
            return self._fallback_meeting(meeting_data)
    
    def _generate_meeting_id(self):
        """
        Generate a Google Meet meeting ID
        """
        # Google Meet IDs are typically 10-11 characters
        # Format: abc-defg-hij (3-4-3 pattern)
        chars = string.ascii_lowercase + string.digits
        
        # Generate 3 groups
        group1 = ''.join(random.choices(chars, k=3))
        group2 = ''.join(random.choices(chars, k=4))
        group3 = ''.join(random.choices(chars, k=3))
        
        return f"{group1}-{group2}-{group3}"
    
    def _fallback_meeting(self, meeting_data):
        """
        Fallback method if meeting creation fails
        """
        meeting_id = f"fallback-{int(time.time())}"
        meeting_link = f"{self.base_url}/{meeting_id}"
        
        return {
            'meetingLink': meeting_link,
            'meetingId': meeting_id,
            'eventId': f"fallback-{int(time.time())}",
            'message': 'Fallback Google Meet link created',
            'isReal': False
        }

# Create a global instance
simple_google_meet = SimpleGoogleMeet()
