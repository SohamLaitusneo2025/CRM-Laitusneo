#!/usr/bin/env python3
"""
Setup script for Google Calendar API integration
This will help you set up real Google Meet meeting creation
"""
import os
import json
from google_calendar_oauth import google_calendar_oauth

def setup_google_calendar():
    print("🚀 Google Calendar API Setup for Real Google Meet Integration")
    print("=" * 70)
    
    # Check if credentials file exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("\n📋 Setup Instructions:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Calendar API:")
        print("   - Go to 'APIs & Services' > 'Library'")
        print("   - Search for 'Google Calendar API'")
        print("   - Click 'Enable'")
        print("4. Create OAuth 2.0 credentials:")
        print("   - Go to 'APIs & Services' > 'Credentials'")
        print("   - Click 'Create Credentials' > 'OAuth 2.0 Client ID'")
        print("   - Choose 'Desktop application'")
        print("   - Download the JSON file")
        print("   - Rename it to 'credentials.json' and place in backend folder")
        print("\n5. Run this script again after setting up credentials.json")
        return False
    
    print("✅ credentials.json found!")
    
    # Try to authenticate
    print("\n🔐 Attempting to authenticate with Google Calendar API...")
    
    try:
        # This will open a browser for OAuth2 authentication
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', 
            ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
        )
        
        print("🌐 Opening browser for authentication...")
        print("Please log in with laitusneotechnologies@gmail.com")
        
        credentials = flow.run_local_server(port=0)
        
        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
        
        print("✅ Authentication successful!")
        print("✅ Credentials saved to token.json")
        
        # Test the service
        print("\n🧪 Testing Google Calendar API...")
        service = google_calendar_oauth.authenticate()
        
        if service:
            print("✅ Google Calendar API is working!")
            print("✅ Ready to create real Google Meet meetings!")
            
            # Test creating a meeting
            test_meeting_data = {
                'clientName': 'Test User',
                'email': 'laitusneotechnologies@gmail.com',
                'date': '2025-01-15',
                'time': '14:00',
                'productName': 'Test Product',
                'message': 'Test meeting'
            }
            
            print("\n🧪 Testing meeting creation...")
            result = google_calendar_oauth.create_google_meet_meeting(test_meeting_data)
            
            if result['isReal']:
                print(f"✅ Real Google Meet meeting created: {result['meetingLink']}")
                print("🎉 Setup complete! Your system can now create real Google Meet meetings!")
            else:
                print("⚠️ Fallback meeting created. Check your API setup.")
            
            return True
        else:
            print("❌ Google Calendar API authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json is valid")
        print("2. Check that Google Calendar API is enabled")
        print("3. Verify the OAuth2 client is configured for desktop application")
        return False

if __name__ == "__main__":
    setup_google_calendar()
