"""
Application settings and configuration.
Handles environment-specific settings including database configuration.
"""

import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    """Parse CORS origins from string or list."""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra="ignore"
    )
    
    # Environment
    ENVIRONMENT: Literal["development", "production"] = "development"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Finance FastAPI"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A FastAPI backend for a finance application"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    
    @computed_field  # type: ignore[misc]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).removesuffix("/") for origin in self.BACKEND_CORS_ORIGINS]
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # PostgreSQL Configuration (used when DATABASE_URL is PostgreSQL)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "username"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "finance_db"
    
    @computed_field  # type: ignore[misc]
    @property
    def postgres_url(self) -> PostgresDsn:
        """Build PostgreSQL URL from individual components."""
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
    @computed_field  # type: ignore[misc]
    @property
    def sqlalchemy_database_uri(self) -> str:
        """Get the appropriate database URI based on environment."""
        if self.DATABASE_URL.startswith("postgresql"):
            return str(self.DATABASE_URL)
        elif self.DATABASE_URL.startswith("sqlite"):
            return self.DATABASE_URL
        else:
            # Default to SQLite for development
            return "sqlite:///./app.db"
    
    @computed_field  # type: ignore[misc]
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return self.sqlalchemy_database_uri.startswith("sqlite")
    
    @computed_field  # type: ignore[misc]
    @property
    def is_postgresql(self) -> bool:
        """Check if using PostgreSQL database."""
        return self.sqlalchemy_database_uri.startswith("postgresql")
    
    # Admin User
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"
    
    @model_validator(mode="after")
    def validate_cors_origins(self) -> "Settings":
        """Validate CORS origins configuration."""
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            self.BACKEND_CORS_ORIGINS = [
                origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")
            ]
        return self


# Global settings instance
settings = Settings()