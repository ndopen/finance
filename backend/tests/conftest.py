"""
Pytest configuration and shared fixtures.
"""

import sys
from pathlib import Path

import pytest

# Add the app directory to Python path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))


@pytest.fixture(scope="session")
def app_settings():
    """Load application settings for testing."""
    from app.core.config import settings
    return settings


@pytest.fixture(scope="session") 
def test_db_engine(app_settings):
    """Create a test database engine."""
    from app.core.db import engine
    return engine


@pytest.fixture
def clean_db_session(test_db_engine):
    """Create a clean database session for each test."""
    from sqlmodel import Session
    
    with Session(test_db_engine) as session:
        # Start a transaction
        transaction = session.begin()
        try:
            yield session
        finally:
            # Rollback transaction to ensure clean state
            transaction.rollback()


@pytest.fixture(scope="session")
def backend_project_path():
    """Get the backend project root path."""
    return Path(__file__).parent.parent


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Register custom markers
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")  
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "postgresql: mark test as requiring PostgreSQL")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark slow tests
        if "slow" in item.keywords or "integration" in item.keywords:
            item.add_marker(pytest.mark.slow)
        
        # Auto-mark PostgreSQL tests (all database tests are PostgreSQL now)
        if "db" in item.name.lower() or "database" in item.name.lower():
            item.add_marker(pytest.mark.postgresql)


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, tmp_path):
    """Set up test environment for each test."""
    # Ensure we're using test configuration compatible with new settings
    monkeypatch.setenv("ENVIRONMENT", "local")
    
    # Set up temporary directory for test files if needed
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path))


def pytest_runtest_setup(item):
    """Run before each test."""
    # Ensure PostgreSQL driver is available for all database tests
    if "postgresql" in item.keywords or "db" in item.name.lower():
        try:
            import psycopg  # psycopg3 driver
        except ImportError:
            pytest.skip("PostgreSQL driver not available")
    
    # Skip slow tests unless specifically requested
    if "slow" in item.keywords and not item.config.getoption("--run-slow"):
        pytest.skip("Slow test skipped (use --run-slow to include)")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-slow",
        action="store_true", 
        default=False,
        help="Run slow tests"
    )
    
    parser.addoption(
        "--postgresql-url",
        action="store",
        default="postgresql://postgres:password@localhost:5432/finance_test",
        help="PostgreSQL database URL for testing"
    )


# Test data factories (you can expand these as needed)
@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "is_active": True,
        "is_superuser": False
    }


@pytest.fixture  
def sample_account_data():
    """Sample account data for testing."""
    return {
        "name": "Test Checking Account",
        "account_type": "checking", 
        "balance": "1000.00",
        "currency": "USD",
        "is_active": True
    }


@pytest.fixture
def sample_transaction_data():
    """Sample transaction data for testing."""
    return {
        "amount": "50.00",
        "description": "Test transaction",
        "category": "Food",
        "is_recurring": False
    }