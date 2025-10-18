#!/usr/bin/env python3
"""
Test campaign endpoint
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Campaign

def test_endpoint():
    app = create_app()
    
    with app.app_context():
        # Test query
        try:
            print("Testing Campaign query...")
            campaigns = Campaign.query.all()
            print(f"Found {len(campaigns)} campaigns")
            print("✓ Campaign endpoint should work!")
            
            # Get a sub-user
            sub_user = User.query.filter_by(user_type='sub').first()
            if sub_user:
                print(f"\nFound sub-user: {sub_user.username}")
                user_campaigns = Campaign.query.filter_by(salesman_id=sub_user.id).all()
                print(f"Sub-user has {len(user_campaigns)} campaigns")
            else:
                print("\nNo sub-users found. Create a sub-user account first.")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_endpoint()

