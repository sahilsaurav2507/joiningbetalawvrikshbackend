#!/usr/bin/env python3
"""
Database initialization script for LawVriksh Backend
"""
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.database import init_db
from app.config import get_settings

def main():
    """Initialize the database with all tables"""
    try:
        print("🚀 Initializing LawVriksh database...")
        
        # Get settings
        settings = get_settings()
        print(f"📊 Database: {settings.DATABASE_NAME}")
        print(f"🌍 Environment: {settings.ENVIRONMENT}")
        
        # Initialize database
        init_db()
        
        print("✅ Database initialized successfully!")
        print("🔐 Default admin credentials:")
        print(f"   Username: {settings.DEFAULT_ADMIN_USERNAME}")
        print(f"   Email: {settings.DEFAULT_ADMIN_EMAIL}")
        print(f"   Password: {settings.DEFAULT_ADMIN_PASSWORD}")
        print("⚠️  Please change the default admin password in production!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()