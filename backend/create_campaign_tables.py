#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Campaign and CampaignEmail tables
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Campaign, CampaignEmail

def create_tables():
    """Create campaign tables"""
    try:
        app = create_app()
        
        with app.app_context():
            # Create only campaign tables
            print("Creating campaign tables...")
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'campaigns' not in existing_tables:
                print("Creating 'campaigns' table...")
                Campaign.__table__.create(db.engine)
                print("✓ 'campaigns' table created successfully")
            else:
                print("✓ 'campaigns' table already exists")
            
            if 'campaign_emails' not in existing_tables:
                print("Creating 'campaign_emails' table...")
                CampaignEmail.__table__.create(db.engine)
                print("✓ 'campaign_emails' table created successfully")
            else:
                print("✓ 'campaign_emails' table already exists")
            
            print("\n✓ Campaign tables setup completed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Error creating campaign tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Campaign Tables Setup")
    print("=" * 50)
    
    if create_tables():
        print("\nYou can now use the campaign management feature!")
        sys.exit(0)
    else:
        print("\nFailed to create campaign tables.")
        sys.exit(1)

