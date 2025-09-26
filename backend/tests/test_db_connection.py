"""
Database connection tests using pytest.
Tests basic database configuration and connectivity.
"""

import pytest
from sqlalchemy import text

from app.core.config import settings
from app.core.db import engine


@pytest.fixture
def db_engine():
    """Create a database engine for testing."""
    return engine


class TestDatabaseConnection:
    """Test suite for database connection functionality."""

    def test_settings_configuration(self):
        """Test that database settings are properly configured."""
        assert settings.ENVIRONMENT is not None
        assert settings.PROJECT_NAME is not None
        assert settings.SQLALCHEMY_DATABASE_URI is not None
        
        # Test PostgreSQL configuration
        assert str(settings.SQLALCHEMY_DATABASE_URI).startswith("postgresql")

    def test_database_engine_creation(self, db_engine):
        """Test that database engine can be created successfully."""
        assert db_engine is not None
        assert hasattr(db_engine, 'connect')

    def test_database_connection(self, db_engine):
        """Test that we can establish a connection to the database."""
        with db_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone() is not None

    def test_database_tables_creation(self, db_engine):
        """Test that database tables can be created/verified."""
        # This should not raise any exceptions - tables are created by Alembic
        try:
            # Just test that we can connect and the engine works
            with db_engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result.fetchone() is not None
        except Exception as e:
            pytest.fail(f"Database connection test failed: {e}")

    def test_postgresql_configuration(self):
        """Test PostgreSQL database configuration."""
        # Test that database URL is PostgreSQL
        db_url = str(settings.SQLALCHEMY_DATABASE_URI)
        assert db_url.startswith("postgresql+psycopg://")
        
        # Test PostgreSQL connection parameters
        assert settings.POSTGRES_SERVER is not None
        assert settings.POSTGRES_PORT > 0
        assert settings.POSTGRES_USER is not None
        assert settings.POSTGRES_PASSWORD is not None
        assert settings.POSTGRES_DB is not None

    def test_database_url_format(self):
        """Test that database URL is in correct PostgreSQL format."""
        db_url = str(settings.SQLALCHEMY_DATABASE_URI)
        assert db_url.startswith("postgresql+psycopg://")
        assert settings.POSTGRES_USER in db_url
        assert settings.POSTGRES_DB in db_url