"""
Google Calendar OAuth2 Setup for laitusneotechnologies@gmail.com
This will create real Google Meet meetings using Google Calendar API
"""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# Scopes required for Google Calendar and Google Meet
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

class GoogleCalendarOAuth:
    def __init__(self):
        self.service = None
        self.credentials = None
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.json'
        
    def authenticate(self):
        """Authenticate with Google Calendar API using OAuth2"""
        try:
            # Check if we have stored credentials
            if os.path.exists(self.token_file):
                self.credentials = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    print("Refreshing expired credentials...")
                    self.credentials.refresh(Request())
                else:
                    print("No valid credentials found. Please set up OAuth2 credentials.")
                    return False
                
                # Save the credentials for the next run
                with open(self.token_file, 'w') as token:
                    token.write(self.credentials.to_json())
            
            self.service = build('calendar', 'v3', credentials=self.credentials)
            print("✅ Google Calendar API authenticated successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Google Calendar authentication failed: {e}")
            return False
    
    def create_google_meet_meeting(self, meeting_data):
        """
        Create a real Google Meet meeting using Google Calendar API
        """
        try:
            if not self.authenticate():
                return self._fallback_meeting_creation(meeting_data)
            
            # Parse meeting data
            start_datetime = datetime.strptime(f"{meeting_data['date']} {meeting_data['time']}", '%Y-%m-%d %H:%M')
            end_datetime = start_datetime + timedelta(hours=1)  # 1 hour duration
            
            # Create the event with Google Meet
            event = {
                'summary': f"{meeting_data['clientName']} - {meeting_data['productName']} Discussion",
                'description': meeting_data.get('message', f"Meeting to discuss {meeting_data['productName']} with {meeting_data['clientName']}."),
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Asia/Kolkata',  # Adjust timezone as needed
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
                'attendees': [
                    {'email': meeting_data['email']},
                ],
                'conferenceDataVersion': 1,
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"meeting-{int(datetime.now().timestamp())}",
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 10},       # 10 minutes before
                    ],
                },
            }
            
            # Create the event with Google Meet
            event = self.service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            # Extract the Google Meet link
            meeting_link = event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', '')
            
            if not meeting_link:
                print("⚠️ No Google Meet link generated, using fallback")
                return self._fallback_meeting_creation(meeting_data)
            
            print(f"✅ Real Google Meet meeting created: {meeting_link}")
            
            return {
                'meetingLink': meeting_link,
                'meetingId': event.get('id'),
                'eventId': event.get('id'),
                'message': 'Real Google Meet meeting created successfully via Google Calendar API',
                'isReal': True
            }
            
        except HttpError as error:
            print(f"❌ Google Calendar API error: {error}")
            return self._fallback_meeting_creation(meeting_data)
        except Exception as e:
            print(f"❌ Error creating Google Meet meeting: {e}")
            return self._fallback_meeting_creation(meeting_data)
    
    def _fallback_meeting_creation(self, meeting_data):
        """
        Fallback method when Google Calendar API is not available
        """
        import random
        import string
        import time
        
        # Generate a more realistic meeting ID
        def generate_meeting_id():
            chars = string.ascii_lowercase + string.digits
            group1 = ''.join(random.choices(chars, k=3))
            group2 = ''.join(random.choices(chars, k=4))
            group3 = ''.join(random.choices(chars, k=3))
            return f"{group1}-{group2}-{group3}"
        
        meeting_id = generate_meeting_id()
        meeting_link = f"https://meet.google.com/{meeting_id}"
        
        return {
            'meetingLink': meeting_link,
            'meetingId': meeting_id,
            'eventId': f"fallback-{int(time.time())}",
            'message': 'Fallback Google Meet link created (Google Calendar API not configured)',
            'isReal': False
        }
    
    def setup_oauth_credentials(self):
        """
        Instructions for setting up OAuth2 credentials
        """
        instructions = """
        To set up Google Calendar API integration:
        
        1. Go to Google Cloud Console: https://console.cloud.google.com/
        2. Create a new project or select existing one
        3. Enable Google Calendar API
        4. Go to "Credentials" and create OAuth 2.0 Client ID
        5. Set application type to "Desktop application"
        6. Download the credentials JSON file
        7. Rename it to 'credentials.json' and place in backend folder
        8. Run the authentication flow to get token.json
        
        The system will then create real Google Meet meetings!
        """
        return instructions

# Create a global instance
google_calendar_oauth = GoogleCalendarOAuth()
