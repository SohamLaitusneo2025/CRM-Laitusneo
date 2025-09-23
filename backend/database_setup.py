"""
Database setup script for CRM LaitusNeo
Run this script to create the database and tables
"""

import os
import pymysql
from config import Config

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        if Config.DB_PASSWORD:
            connection = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                charset='utf8mb4'
            )
        else:
            connection = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                charset='utf8mb4'
            )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        print(f"Database '{Config.DB_NAME}' created successfully or already exists")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        print("Please make sure MySQL is running and the database 'crm_laitusneo' exists.")
        return False
    
    return True

def create_tables():
    """Create tables using Flask app context"""
    try:
        from app import create_app
        from models import db, User
        
        app = create_app()
        
        with app.app_context():
            # Disable foreign key checks temporarily
            db.engine.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Drop all tables and recreate them to fix password hashing
            db.drop_all()
            print("Dropped existing tables")
            
            # Re-enable foreign key checks
            db.engine.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            # Create all tables
            db.create_all()
            print("Tables created successfully")
            
            # Create a default admin user
            admin_user = User(
                email='admin@crm.com',
                password='Admin123!',
                first_name='Admin',
                last_name='User',
                user_type='main'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: admin@crm.com / Admin123!")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    
    return True

def migrate_existing_data():
    """Migrate existing data to new schema"""
    try:
        from app import create_app
        from models import db, Lead
        
        app = create_app()
        
        with app.app_context():
            # Check if leads table exists and has data
            try:
                leads = Lead.query.all()
                if leads:
                    print(f"Found {len(leads)} existing leads to migrate...")
                    
                    # Generate lead_id for existing leads
                    for i, lead in enumerate(leads, 1):
                        if not lead.lead_id:
                            lead_id = f"L{i:03d}"
                            lead.lead_id = lead_id
                            print(f"Updated lead {lead.id} with lead_id: {lead_id}")
                    
                    db.session.commit()
                    print("Migration completed successfully!")
                else:
                    print("No existing leads found to migrate")
            except Exception as e:
                print(f"No existing data to migrate: {e}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("Setting up CRM LaitusNeo database...")
    
    if create_database():
        if create_tables():
            print("Database setup completed successfully!")
            # Run migration for existing data
            migrate_existing_data()
        else:
            print("Failed to create tables")
    else:
        print("Failed to create database")
