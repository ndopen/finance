# Testing Guide - Pytest Setup

This document describes the pytest-based testing setup for the finance backend application.

## 📁 Test Structure

```
backend/tests/
├── conftest.py                    # Pytest configuration and shared fixtures
├── test_db_connection.py          # Database connection tests
├── test_migration_system.py       # Migration system tests
└── postgresql_test_setup.py       # PostgreSQL configuration tests

backend/
├── pytest.ini                     # Pytest configuration file
└── run_tests.py                   # Custom test runner script
```

## 🚀 Running Tests

### Using Custom Test Runner
```bash
# Run all tests
python run_tests.py all

# Run only database tests
python run_tests.py db

# Run fast tests (exclude slow ones)
python run_tests.py fast

# Run tests with coverage report
python run_tests.py coverage

# Run tests with verbose output
python run_tests.py verbose
```

### Using Pytest Directly
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_db_connection.py

# Run with verbose output
python -m pytest tests/ -v

# Run only fast tests (exclude slow)
python -m pytest tests/ -m "not slow"

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## 🏷️ Test Markers

The following pytest markers are available:

- `@pytest.mark.slow` - Marks slow-running tests
- `@pytest.mark.integration` - Marks integration tests
- `@pytest.mark.unit` - Marks unit tests
- `@pytest.mark.postgresql` - Marks PostgreSQL-specific tests

### Using Markers
```bash
# Run only unit tests
python -m pytest tests/ -m "unit"

# Run only integration tests
python -m pytest tests/ -m "integration"

# Exclude slow tests
python -m pytest tests/ -m "not slow"

# Run PostgreSQL tests only (requires PostgreSQL)
python -m pytest tests/ -m "postgresql"
```

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- Automatic test discovery
- Custom markers registration
- Logging configuration
- Test output formatting

### Fixtures (`conftest.py`)
- `app_settings` - Application settings
- `test_db_engine` - Database engine for testing
- `clean_db_session` - Clean database session per test
- `backend_project_path` - Project root path
- Sample data factories for testing

## 📊 Test Categories

### Database Connection Tests (`test_db_connection.py`)
- ✅ Settings configuration validation
- ✅ Database engine creation
- ✅ Connection establishment
- ✅ Table creation verification
- ✅ Environment-specific settings
- ✅ Database type detection
- ✅ URL format validation

### Migration System Tests (`test_migration_system.py`)
- ✅ Table existence verification
- ✅ CRUD operations testing
- ✅ Model relationships validation
- ✅ Alembic command execution
- ✅ Migration file verification
- ✅ Database integration testing

### PostgreSQL Tests (`postgresql_test_setup.py`)
- ✅ PostgreSQL URL format validation
- ✅ Configuration parameter testing
- ✅ Environment file creation
- ✅ Migration command documentation
- ✅ Database type switching logic
- ✅ Installation workflow validation

## 🎯 Test Results Summary

Current test status:
- **24 passed, 2 skipped** (PostgreSQL tests skipped when not available)
- **100% pass rate** for available database configurations
- **Automatic skip** for unavailable dependencies

### Skipped Tests
- PostgreSQL-specific tests are automatically skipped when PostgreSQL driver is not available
- Slow tests are skipped by default (use `--run-slow` to include)

## 🔄 Continuous Integration

The test setup is ready for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd backend
    python -m pytest tests/ --cov=app --cov-report=xml
    
- name: Run Fast Tests Only
  run: |
    cd backend  
    python -m pytest tests/ -m "not slow"
```

## 🛠️ Development Workflow

### Adding New Tests
1. Create test files following the `test_*.py` pattern
2. Use appropriate test classes: `class TestFeatureName:`
3. Add markers for categorization
4. Use fixtures for setup/teardown
5. Follow AAA pattern: Arrange, Act, Assert

### Example Test Structure
```python
import pytest
from app.core.database import create_db_engine

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_basic_functionality(self, db_session):
        """Test basic functionality works."""
        # Arrange
        test_data = {"key": "value"}
        
        # Act
        result = some_function(test_data)
        
        # Assert
        assert result is not None
        assert result.status == "success"
    
    @pytest.mark.slow
    def test_complex_workflow(self, clean_db_session):
        """Test complex workflow (marked as slow)."""
        # Implementation here
        pass
```

## 📈 Coverage Reports

Generate coverage reports:
```bash
# HTML report
python -m pytest tests/ --cov=app --cov-report=html

# Terminal report
python -m pytest tests/ --cov=app --cov-report=term

# XML report (for CI)
python -m pytest tests/ --cov=app --cov-report=xml
```

Coverage reports will be generated in `htmlcov/` directory.

## 🔍 Debugging Tests

### Verbose Output
```bash
python -m pytest tests/ -v -s  # -s preserves print statements
```

### Debug Single Test
```bash
python -m pytest tests/test_db_connection.py::TestDatabaseConnection::test_database_connection -v -s
```

### PDB Debugging
```bash
python -m pytest tests/ --pdb  # Drop into debugger on failures
```

This pytest setup provides a robust, scalable testing framework for the finance backend application with proper fixtures, markers, and configuration management.