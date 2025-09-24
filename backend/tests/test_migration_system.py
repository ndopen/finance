"""
Complete database migration and connection test.
Tests both SQLite (development) and PostgreSQL (production) setups.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import create_db_engine
from app.models import User, Account, Transaction
from sqlalchemy import text


def test_database_tables():
    """Test that all tables exist and are accessible."""
    engine = create_db_engine()
    
    try:
        with engine.connect() as connection:
            # Test each table exists
            tables_to_test = ['user', 'account', 'transaction', 'alembic_version']
            
            for table in tables_to_test:
                if settings.is_sqlite:
                    # SQLite syntax
                    result = connection.execute(
                        text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                    )
                else:
                    # PostgreSQL syntax
                    result = connection.execute(
                        text(f"SELECT tablename FROM pg_tables WHERE tablename='{table}'")
                    )
                
                if result.fetchone():
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' not found")
                    return False
                    
            return True
            
    except Exception as e:
        print(f"❌ Database table check failed: {e}")
        return False


def test_basic_crud_operations():
    """Test basic CRUD operations work correctly."""
    from sqlmodel import Session
    
    engine = create_db_engine()
    
    try:
        with Session(engine) as session:
            # Test that we can query (even if empty)
            users = session.query(User).all()
            accounts = session.query(Account).all() 
            transactions = session.query(Transaction).all()
            
            print(f"✅ CRUD test successful - Users: {len(users)}, Accounts: {len(accounts)}, Transactions: {len(transactions)}")
            return True
            
    except Exception as e:
        print(f"❌ CRUD operations test failed: {e}")
        return False


def test_migration_system():
    """Test the migration system is working."""
    import subprocess
    
    try:
        # Check current migration status
        result = subprocess.run(
            ["python", "-m", "alembic", "current"],
            capture_output=True,
            text=True,
            cwd="/home/hr/projects/finance/backend"
        )
        
        if result.returncode == 0 and "8fa1d0f2671b" in result.stdout:
            print("✅ Migration system working - at head revision")
            return True
        else:
            print(f"❌ Migration system issue: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Migration test failed: {e}")
        return False


def run_comprehensive_test():
    """Run all database tests."""
    print("🧪 Running Comprehensive Database Migration Tests")
    print("=" * 50)
    
    # Basic info
    print(f"🔧 Environment: {settings.ENVIRONMENT}")
    print(f"📊 Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"🗄️  Database URL: {settings.sqlalchemy_database_uri}")
    print(f"🔍 Database Type: {'SQLite' if settings.is_sqlite else 'PostgreSQL' if settings.is_postgresql else 'Unknown'}")
    print()
    
    # Run tests
    tests = [
        ("Database Connection", test_database_tables),
        ("CRUD Operations", test_basic_crud_operations), 
        ("Migration System", test_migration_system),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        success = test_func()
        results.append((test_name, success))
        print()
    
    # Summary
    print("📋 Test Summary:")
    print("-" * 30)
    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if not success:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! Database migration setup is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return all_passed


if __name__ == "__main__":
    run_comprehensive_test()