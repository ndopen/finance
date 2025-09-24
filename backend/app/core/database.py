"""
Database connection and session management.
Handles both SQLite (development) and PostgreSQL (production) databases.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

from app.core.config import settings


def create_db_engine():
    """Create database engine based on configuration."""
    
    connect_args = {}
    
    if settings.is_sqlite:
        # SQLite specific configuration
        connect_args = {
            "check_same_thread": False,  # Allow SQLite to be used with FastAPI
        }
        # Enable foreign key support for SQLite
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if "sqlite" in str(dbapi_connection):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
    
    elif settings.is_postgresql:
        # PostgreSQL specific configuration
        connect_args = {
            "application_name": settings.PROJECT_NAME,
        }
    
    # Create engine with appropriate configuration
    engine = create_engine(
        settings.sqlalchemy_database_uri,
        connect_args=connect_args,
        echo=settings.ENVIRONMENT == "development",  # Log SQL queries in development
    )
    
    return engine


def create_db_and_tables():
    """Create database tables."""
    engine = create_db_engine()
    SQLModel.metadata.create_all(engine)
    return engine


def get_session():
    """Get database session."""
    engine = create_db_engine()
    with Session(engine) as session:
        yield session


# Create the engine instance
engine = create_db_engine()