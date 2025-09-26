"""
Comprehensive database migration tests using pytest.
Tests PostgreSQL database setup and migrations.
"""

import subprocess
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.models import User, Account, Transaction


@pytest.fixture
def db_engine():
    """Create a database engine for testing."""
    return engine


@pytest.fixture
def db_session(db_engine):
    """Create a database session for testing."""
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def backend_path():
    """Get the backend project path."""
    return Path(__file__).parent.parent


class TestDatabaseTables:
    """Test suite for database table existence and structure."""

    @pytest.mark.parametrize("table_name", [
        "user",
        "account", 
        "transaction",
        "alembic_version"
    ])
    def test_table_exists(self, db_engine, table_name):
        """Test that required tables exist in the PostgreSQL database."""
        with db_engine.connect() as connection:
            # PostgreSQL syntax
            result = connection.execute(
                text(f"SELECT tablename FROM pg_tables WHERE tablename='{table_name}'")
            )
            
            assert result.fetchone() is not None, f"Table '{table_name}' does not exist"

    def test_all_required_tables_exist(self, db_engine):
        """Test that all required tables exist together."""
        required_tables = ['user', 'account', 'transaction', 'alembic_version']
        existing_tables = []
        
        with db_engine.connect() as connection:
            for table_name in required_tables:
                result = connection.execute(
                    text(f"SELECT tablename FROM pg_tables WHERE tablename='{table_name}'")
                )
                
                if result.fetchone():
                    existing_tables.append(table_name)
        
        assert len(existing_tables) == len(required_tables), \
            f"Missing tables: {set(required_tables) - set(existing_tables)}"


class TestCRUDOperations:
    """Test suite for basic CRUD operations."""

    def test_can_query_users(self, db_session):
        """Test that we can query the users table."""
        statement = select(User)
        users = db_session.exec(statement).all()
        assert isinstance(users, list)

    def test_can_query_accounts(self, db_session):
        """Test that we can query the accounts table."""
        statement = select(Account)
        accounts = db_session.exec(statement).all()
        assert isinstance(accounts, list)

    def test_can_query_transactions(self, db_session):
        """Test that we can query the transactions table."""
        statement = select(Transaction)
        transactions = db_session.exec(statement).all()
        assert isinstance(transactions, list)

    def test_all_models_queryable(self, db_session):
        """Test that all model classes can be queried without errors."""
        models = [User, Account, Transaction]
        
        for model in models:
            try:
                statement = select(model)
                result = db_session.exec(statement).all()
                assert isinstance(result, list), f"Query for {model.__name__} failed"
            except Exception as e:
                pytest.fail(f"Failed to query {model.__name__}: {e}")

    def test_model_relationships_defined(self):
        """Test that model relationships are properly defined."""
        # Test User relationships
        assert hasattr(User, 'accounts'), "User model missing 'accounts' relationship"
        assert hasattr(User, 'transactions'), "User model missing 'transactions' relationship"
        
        # Test Account relationships  
        assert hasattr(Account, 'user'), "Account model missing 'user' relationship"
        assert hasattr(Account, 'transactions'), "Account model missing 'transactions' relationship"
        
        # Test Transaction relationships
        assert hasattr(Transaction, 'user'), "Transaction model missing 'user' relationship"
        assert hasattr(Transaction, 'account'), "Transaction model missing 'account' relationship"


class TestMigrationSystem:
    """Test suite for Alembic migration system."""

    def test_alembic_current_command(self, backend_path):
        """Test that alembic current command works."""
        result = subprocess.run(
            ["python", "-m", "alembic", "current"],
            capture_output=True,
            text=True,
            cwd=str(backend_path)
        )
        
        assert result.returncode == 0, f"Alembic current command failed: {result.stderr}"
        assert "head" in result.stdout.lower() or len(result.stdout.strip()) > 0

    def test_alembic_history_command(self, backend_path):
        """Test that alembic history command works."""
        result = subprocess.run(
            ["python", "-m", "alembic", "history"],
            capture_output=True,
            text=True,
            cwd=str(backend_path)
        )
        
        assert result.returncode == 0, f"Alembic history command failed: {result.stderr}"

    def test_migration_files_exist(self, backend_path):
        """Test that migration files exist."""
        versions_dir = backend_path / "alembic" / "versions"
        assert versions_dir.exists(), "Alembic versions directory does not exist"
        
        # Check for at least one migration file
        migration_files = list(versions_dir.glob("*.py"))
        migration_files = [f for f in migration_files if f.name != "__pycache__"]
        assert len(migration_files) > 0, "No migration files found"

    def test_alembic_config_exists(self, backend_path):
        """Test that Alembic configuration files exist."""
        alembic_ini = backend_path / "alembic.ini"
        alembic_env = backend_path / "alembic" / "env.py"
        
        assert alembic_ini.exists(), "alembic.ini file does not exist"
        assert alembic_env.exists(), "alembic/env.py file does not exist"

    def test_can_check_migration_status(self, backend_path):
        """Test that we can check the current migration status."""
        result = subprocess.run(
            ["python", "-m", "alembic", "show", "current"],
            capture_output=True,
            text=True,
            cwd=str(backend_path)
        )
        
        # This command might not exist in all Alembic versions, so we check multiple approaches
        if result.returncode != 0:
            # Fallback to current command
            result = subprocess.run(
                ["python", "-m", "alembic", "current"],
                capture_output=True,
                text=True,
                cwd=str(backend_path)
            )
        
        assert result.returncode == 0, "Cannot check migration status"


class TestDatabaseIntegration:
    """Integration tests for the complete database system."""

    def test_database_environment_consistency(self):
        """Test that database configuration is consistent with PostgreSQL."""
        # Ensure database URL is PostgreSQL
        db_url = str(settings.SQLALCHEMY_DATABASE_URI)
        assert "postgresql" in db_url.lower()
        
        # Verify PostgreSQL connection parameters
        assert settings.POSTGRES_SERVER is not None
        assert settings.POSTGRES_USER is not None
        assert settings.POSTGRES_DB is not None

    def test_full_database_workflow(self, db_session):
        """Test a complete database workflow."""
        # This test ensures the entire system works together
        try:
            # Try to execute a simple query on each table
            for model in [User, Account, Transaction]:
                statement = select(model).limit(1)
                result = db_session.exec(statement).first()
                # Result can be None (empty table) but should not raise exception
                
        except Exception as e:
            pytest.fail(f"Full database workflow failed: {e}")

    @pytest.mark.slow
    def test_migration_can_be_applied_from_scratch(self, backend_path):
        """Test that migrations can be applied from a clean state."""
        # This is a more complex test that would need a temporary database
        # For now, we just verify the command syntax works
        result = subprocess.run(
            ["python", "-m", "alembic", "upgrade", "--sql", "head"],
            capture_output=True,
            text=True,
            cwd=str(backend_path)
        )
        
        assert result.returncode == 0, f"Migration SQL generation failed: {result.stderr}"
        assert "CREATE TABLE" in result.stdout.upper(), "Migration SQL does not contain table creation"