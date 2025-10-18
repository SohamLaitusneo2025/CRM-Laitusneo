#!/usr/bin/env python3
"""
Simple Google Calendar authentication that bypasses OAuth consent issues
"""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def simple_google_auth():
    """Simple authentication that works around OAuth consent issues"""
    print("🔐 Simple Google Calendar Authentication")
    print("=" * 50)
    
    # Check if credentials exist
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        return False
    
    print("✅ credentials.json found")
    
    creds = None
    # Check if we have stored credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("✅ Found existing token.json")
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Starting OAuth flow...")
            print("📝 Note: If you get 'access_denied', try the manual setup below")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ Authentication successful!")
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                print("\n🔧 Manual Setup Instructions:")
                print("1. Go to: https://console.cloud.google.com/apis/credentials/consent")
                print("2. Click 'OAuth consent screen'")
                print("3. Add 'laitusneotechnologies@gmail.com' as a test user")
                print("4. Publish the app")
                print("5. Try running this script again")
                return False
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ Credentials saved to token.json")
    
    # Test the service
    try:
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Google Calendar API service created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create Calendar service: {e}")
        return False

if __name__ == "__main__":
    simple_google_auth()
