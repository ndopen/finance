#!/usr/bin/env python3
"""
Test runner script for the finance backend application.
Provides convenient commands for running different types of tests.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and display results."""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
    else:
        print(f"❌ {description} failed with exit code {result.returncode}")
    
    return result.returncode == 0


def main():
    """Main test runner function."""
    backend_path = Path(__file__).parent
    
    # Change to backend directory
    import os
    os.chdir(backend_path)
    
    print("🚀 Finance Backend Test Runner")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <test_type>")
        print("\nAvailable test types:")
        print("  all          - Run all tests")
        print("  unit         - Run unit tests only")  
        print("  integration  - Run integration tests only")
        print("  db           - Run database tests only")
        print("  fast         - Run fast tests only (exclude slow)")
        print("  coverage     - Run tests with coverage report")
        print("  verbose      - Run tests with verbose output")
        sys.exit(1)
    
    test_type = sys.argv[1].lower()
    
    # Test commands
    commands = {
        "all": "python -m pytest tests/",
        "unit": "python -m pytest tests/ -m 'unit'",
        "integration": "python -m pytest tests/ -m 'integration'", 
        "db": "python -m pytest tests/test_db_connection.py tests/test_migration_system.py",
        "fast": "python -m pytest tests/ -m 'not slow'",
        "coverage": "python -m pytest tests/ --cov=app --cov-report=html --cov-report=term",
        "verbose": "python -m pytest tests/ -v -s",
    }
    
    if test_type not in commands:
        print(f"❌ Unknown test type: {test_type}")
        print(f"Available options: {', '.join(commands.keys())}")
        sys.exit(1)
    
    # Run the selected test command
    success = run_command(commands[test_type], f"Running {test_type} tests")
    
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 All {test_type} tests completed successfully!")


if __name__ == "__main__":
    main()