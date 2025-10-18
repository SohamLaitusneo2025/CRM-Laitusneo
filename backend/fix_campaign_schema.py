#!/usr/bin/env python3
"""
Fix campaign table schema by dropping and recreating
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Campaign, CampaignEmail

def fix_schema():
    app = create_app()
    
    with app.app_context():
        try:
            print("Fixing campaign table schema...")
            print("-" * 50)
            
            # Drop existing tables if they exist
            print("Dropping old campaign tables...")
            try:
                CampaignEmail.__table__.drop(db.engine, checkfirst=True)
                print("  - Dropped campaign_emails table")
            except:
                print("  - campaign_emails table didn't exist")
            
            try:
                Campaign.__table__.drop(db.engine, checkfirst=True)
                print("  - Dropped campaigns table")
            except:
                print("  - campaigns table didn't exist")
            
            # Create new tables with correct schema
            print("\nCreating new campaign tables with correct schema...")
            Campaign.__table__.create(db.engine)
            print("  + Created campaigns table")
            
            CampaignEmail.__table__.create(db.engine)
            print("  + Created campaign_emails table")
            
            print("\n" + "-" * 50)
            print("SUCCESS! Campaign tables are now ready to use!")
            print("-" * 50)
            return True
            
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("Campaign Schema Fix")
    print("=" * 50)
    print()
    
    if fix_schema():
        print("\nYou can now use the campaign feature!")
        print("Please restart your backend server if it's running.")
        sys.exit(0)
    else:
        print("\nFailed to fix campaign schema.")
        sys.exit(1)

