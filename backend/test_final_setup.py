#!/usr/bin/env python3
"""
Final test to verify Google Calendar API setup
"""
import os
from google_calendar_oauth import google_calendar_oauth

def test_final_setup():
    print("🧪 Final Setup Test")
    print("=" * 40)
    
    # Check if credentials file exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please complete Step 2 of the setup guide.")
        return False
    
    print("✅ credentials.json found")
    
    # Check if token file exists
    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        print("Please run: python setup_google_calendar.py")
        return False
    
    print("✅ token.json found")
    
    # Test authentication
    print("\n🔐 Testing authentication...")
    if google_calendar_oauth.authenticate():
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
        return False
    
    # Test meeting creation
    print("\n📅 Testing meeting creation...")
    test_meeting = {
        'clientName': 'Test User',
        'email': 'laitusneotechnologies@gmail.com',
        'date': '2025-01-15',
        'time': '14:00',
        'productName': 'Test Product',
        'message': 'Test meeting for verification'
    }
    
    result = google_calendar_oauth.create_google_meet_meeting(test_meeting)
    
    if result['isReal']:
        print("✅ Real Google Meet meeting created!")
        print(f"✅ Meeting Link: {result['meetingLink']}")
        print("🎉 Setup is complete and working!")
        return True
    else:
        print("⚠️ Fallback meeting created")
        print("Check your Google Calendar API setup")
        return False

if __name__ == "__main__":
    test_final_setup()
