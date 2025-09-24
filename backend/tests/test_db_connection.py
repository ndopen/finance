"""
Database connection test script.
Run this to test if the database configuration is working correctly.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import create_db_engine, create_db_and_tables


def test_database_connection():
    """Test database connection and display configuration info."""
    
    print(f"🔧 Environment: {settings.ENVIRONMENT}")
    print(f"📊 Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"🗄️  Database URL: {settings.sqlalchemy_database_uri}")
    print(f"🔍 Database Type: {'SQLite' if settings.is_sqlite else 'PostgreSQL' if settings.is_postgresql else 'Unknown'}")
    
    try:
        # Test engine creation
        engine = create_db_engine()
        print("✅ Database engine created successfully")
        
        # Test connection
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection test successful")
            
        # Create tables (this will be a no-op if no models are defined yet)
        create_db_and_tables()
        print("✅ Database tables creation/verification successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    test_database_connection()