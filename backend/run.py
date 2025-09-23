#!/usr/bin/env python3
"""
Run script for CRM LaitusNeo Backend
This script sets up the database and starts the Flask application
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    """Set up the database and create tables"""
    try:
        from database_setup import create_database, create_tables
        
        print("Setting up database...")
        if create_database():
            print("Database created successfully!")
            
            print("Creating tables...")
            if create_tables():
                print("Tables created successfully!")
                return True
            else:
                print("Failed to create tables!")
                return False
        else:
            print("Failed to create database!")
            return False
            
    except Exception as e:
        print(f"Error during database setup: {e}")
        return False

def start_app():
    """Start the Flask application"""
    try:
        from app import create_app
        
        app = create_app()
        print("Starting CRM LaitusNeo Backend...")
        print("Backend will be available at: http://localhost:5000")
        print("API endpoints:")
        print("  - Health check: GET /api/health")
        print("  - Sign up: POST /api/auth/signup")
        print("  - Login: POST /api/auth/login")
        print("  - Get current user: GET /api/auth/me")
        print("  - Verify token: POST /api/auth/verify-token")
        print("\nPress Ctrl+C to stop the server")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        return False

if __name__ == '__main__':
    print("CRM LaitusNeo Backend Setup")
    print("=" * 40)
    
    # Set up database first
    if setup_database():
        print("\nDatabase setup completed successfully!")
        print("=" * 40)
        
        # Start the application
        start_app()
    else:
        print("\nDatabase setup failed!")
        print("Please check your database configuration and try again.")
        sys.exit(1)