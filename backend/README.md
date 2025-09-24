# ezBookkeeping FastAPI Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.114+-00a393.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![SQLModel](https://img.shields.io/badge/SQLModel-latest-blue.svg)](https://sqlmodel.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Pytest](https://img.shields.io/badge/pytest-7.4+-red.svg)](https://pytest.org)

> The FastAPI backend for ezBookkeeping - a lightweight, self-hosted personal finance management system.

## 🏗️ Architecture Overview

This backend provides a robust REST API for the ezBookkeeping application, built with modern Python technologies and following best practices for performance, security, and maintainability.

```
┌─────────────────────┐
│   FastAPI Router    │
├─────────────────────┤
│   Authentication    │
│   Middleware        │
├─────────────────────┤
│   Business Logic    │
│   (Routes & CRUD)   │
├─────────────────────┤
│   SQLModel & ORM    │
├─────────────────────┤
│   PostgreSQL DB     │
└─────────────────────┘
```

### Key Features

- 🚀 **High Performance**: FastAPI with async/await support
- 🔒 **Secure**: JWT authentication, password hashing, CORS protection
- 📖 **Auto-documented**: OpenAPI/Swagger documentation generation
- 🔍 **Type Safe**: Full type hints with Pydantic validation
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 🗃️ **Modern ORM**: SQLModel for type-safe database operations
- 🔄 **Database Migrations**: Alembic for schema management
- 📊 **Monitoring**: Structured logging and error tracking

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI 0.114+ | Async API server with auto docs |
| **Database ORM** | SQLModel 0.0.21+ | Type-safe ORM combining Pydantic + SQLAlchemy |
| **Database** | PostgreSQL 13+ | Primary database |
| **Authentication** | JWT + PassLib | Secure token-based auth |
| **Validation** | Pydantic v2 | Request/response validation |
| **Migrations** | Alembic | Database schema management |
| **Testing** | Pytest | Unit and integration testing |
| **Code Quality** | Ruff + mypy | Linting and type checking |
| **Documentation** | OpenAPI 3.0 | Auto-generated API docs |

## 📁 Project Structure

```
backend/
├── app/                          # Application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── core/                     # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py             # Settings and configuration
│   │   ├── security.py           # Authentication utilities
│   │   └── database.py           # Database connection
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   ├── deps.py               # Common dependencies
│   │   ├── main.py               # API router configuration
│   │   └── routes/               # Route modules
│   │       ├── __init__.py
│   │       ├── auth.py           # Authentication routes
│   │       ├── users.py          # User management
│   │       ├── accounts.py       # Account management
│   │       ├── transactions.py   # Transaction operations
│   │       ├── categories.py     # Category management
│   │       └── tags.py           # Tag management
│   ├── models/                   # SQLModel data models
│   │   ├── __init__.py
│   │   ├── user.py               # User models
│   │   ├── account.py            # Account models
│   │   ├── transaction.py        # Transaction models
│   │   ├── category.py           # Category models
│   │   └── tag.py                # Tag models
│   ├── crud/                     # Database operations
│   │   ├── __init__.py
│   │   ├── base.py               # Base CRUD class
│   │   ├── user.py               # User CRUD operations
│   │   ├── account.py            # Account CRUD operations
│   │   └── transaction.py        # Transaction CRUD operations
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py               # User API schemas
│   │   ├── account.py            # Account API schemas
│   │   ├── transaction.py        # Transaction API schemas
│   │   └── common.py             # Common schemas
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── security.py           # Security utilities
│       └── validators.py         # Custom validators
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   ├── env.py                    # Alembic environment
│   └── script.py.mako            # Migration template
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_main.py              # Application tests
│   ├── api/                      # API endpoint tests
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_transactions.py
│   ├── crud/                     # CRUD operation tests
│   └── utils/                    # Utility function tests
├── scripts/                      # Utility scripts
│   ├── init_db.py                # Database initialization
│   └── import_data.py            # Data migration script
├── pyproject.toml                # Python project configuration
├── alembic.ini                   # Alembic configuration
├── Dockerfile                    # Docker container config
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 13+ (or SQLite for development)
- uv package manager (recommended) or pip

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd finance/backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (see Configuration section below)
nano .env
```

### 3. Database Setup

```bash
# Start PostgreSQL (with Docker)
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15

# Run database migrations
alembic upgrade head

# (Optional) Initialize with sample data
python scripts/init_db.py --sample-data
```

### 4. Run Development Server

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Server will be available at:
# - API: http://localhost:8000
# - Documentation: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Application
APP_NAME="ezBookkeeping API"
DEBUG=true
VERSION="1.0.0"

# Database
DATABASE_URL="postgresql://username:password@localhost:5432/ezbookkeeping"
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_ECHO=false

# Security
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
FRONTEND_HOST="http://localhost:5173"
BACKEND_CORS_ORIGINS=["http://localhost:5173", "https://yourdomain.com"]

# Features
ENABLE_USER_REGISTRATION=true
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=300

# External APIs
EXCHANGE_RATE_API_URL="https://api.exchangerate-api.com/v4/latest/"
EXCHANGE_RATE_API_KEY=""

# Monitoring
SENTRY_DSN=""
LOG_LEVEL="INFO"
```

### Configuration Classes

The application uses Pydantic Settings for configuration management:

```python
# app/core/config.py
class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    
    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Feature flags
    ENABLE_USER_REGISTRATION: bool = True
    
    class Config:
        env_file = ".env"
```

## 🗄️ Database Models

### Core Data Models

The application uses SQLModel for defining database models with full type safety:

```python
# User Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Account Model
class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    account_type: AccountType
    currency: str = Field(default="USD")
    balance: Decimal = Field(default=Decimal("0.00"))
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Transaction Model
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: Decimal
    description: Optional[str] = None
    transaction_type: TransactionType
    account_id: int = Field(foreign_key="account.id")
    category_id: Optional[int] = Field(foreign_key="category.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Database Relationships

```python
# User -> Accounts (One-to-Many)
class User(SQLModel, table=True):
    accounts: List["Account"] = Relationship(back_populates="user")

class Account(SQLModel, table=True):
    user: Optional[User] = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")

# Account -> Transactions (One-to-Many)
class Transaction(SQLModel, table=True):
    account: Optional[Account] = Relationship(back_populates="transactions")
```

## 🔐 Authentication & Security

### JWT Token Authentication

```python
# Token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user
```

### Security Features

- **Password Hashing**: bcrypt with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **CORS Protection**: Configurable CORS origins
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy

## 🔌 API Endpoints

### Authentication Routes (`/api/v1/auth`)

```python
POST   /auth/login          # User login
POST   /auth/register       # User registration (if enabled)
POST   /auth/refresh        # Refresh access token
POST   /auth/logout         # User logout
GET    /auth/me             # Get current user info
```

### User Management (`/api/v1/users`)

```python
GET    /users/              # List users (admin only)
POST   /users/              # Create user (admin only)
GET    /users/{user_id}     # Get user details
PUT    /users/{user_id}     # Update user
DELETE /users/{user_id}     # Delete user
```

### Account Management (`/api/v1/accounts`)

```python
GET    /accounts/           # List user accounts
POST   /accounts/           # Create new account
GET    /accounts/{id}       # Get account details
PUT    /accounts/{id}       # Update account
DELETE /accounts/{id}       # Delete account
GET    /accounts/{id}/balance # Get account balance
```

### Transaction Management (`/api/v1/transactions`)

```python
GET    /transactions/       # List transactions (with pagination/filtering)
POST   /transactions/       # Create new transaction
GET    /transactions/{id}   # Get transaction details
PUT    /transactions/{id}   # Update transaction
DELETE /transactions/{id}   # Delete transaction
GET    /transactions/stats  # Get transaction statistics
```

### Category Management (`/api/v1/categories`)

```python
GET    /categories/         # List categories
POST   /categories/         # Create category
GET    /categories/{id}     # Get category details
PUT    /categories/{id}     # Update category
DELETE /categories/{id}     # Delete category
```

### Tag Management (`/api/v1/tags`)

```python
GET    /tags/               # List tags
POST   /tags/               # Create tag
GET    /tags/{id}           # Get tag details
PUT    /tags/{id}           # Update tag
DELETE /tags/{id}          # Delete tag
```

## 📊 API Response Format

All API responses follow a consistent format matching the original ezBookkeeping API:

### Successful Response
```json
{
    "result": {
        "id": 1,
        "name": "Checking Account",
        "balance": "1500.00"
    },
    "success": true
}
```

### Error Response
```json
{
    "errorCode": 10001,
    "errorMessage": "Account not found",
    "path": "/api/v1/accounts/999",
    "success": false
}
```

### Paginated Response
```json
{
    "result": {
        "items": [...],
        "total": 150,
        "page": 1,
        "size": 20,
        "pages": 8
    },
    "success": true
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/api/test_auth.py

# Run with verbose output
pytest -v

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Test Structure

```python
# Test example for authentication
def test_login_success(client: TestClient, normal_user: User):
    data = {"email": normal_user.email, "password": "password"}
    response = client.post("/api/v1/auth/login", json=data)
    
    assert response.status_code == 200
    content = response.json()
    assert content["success"] is True
    assert "access_token" in content["result"]

def test_create_account(
    client: TestClient, 
    normal_user_token_headers: dict
):
    data = {
        "name": "Test Account",
        "account_type": "checking",
        "currency": "USD"
    }
    response = client.post(
        "/api/v1/accounts/", 
        headers=normal_user_token_headers, 
        json=data
    )
    
    assert response.status_code == 201
    content = response.json()
    assert content["result"]["name"] == "Test Account"
```

### Test Configuration

```python
# conftest.py
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def normal_user(db: Session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def normal_user_token_headers(client: TestClient, normal_user: User):
    return get_user_token_headers(client, normal_user.email, "password")
```

## 🗃️ Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add transaction table"

# Create empty migration file
alembic revision -m "Custom migration"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history

# Show current migration
alembic current
```

### Migration Best Practices

1. **Always review auto-generated migrations** before applying
2. **Test migrations on development data** first
3. **Backup production database** before major migrations
4. **Use descriptive migration messages**
5. **Handle data migrations separately** if needed

```python
# Example migration
"""Add transaction tags table

Revision ID: abc123
Create Date: 2025-01-01 12:00:00.000000
"""

def upgrade():
    op.create_table(
        'transaction_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('transaction_tags')
```

## 📈 Performance Optimization

### Database Optimization

```python
# Use async database sessions
@asynccontextmanager
async def get_async_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Optimize queries with proper indexing
class Transaction(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    amount: Decimal = Field(index=True)

# Use query optimization
def get_transactions_with_pagination(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: int = None
):
    query = db.query(Transaction)
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    return query.offset(skip).limit(limit).all()
```

### Caching Strategy

```python
from functools import lru_cache
import redis

# In-memory caching for configuration
@lru_cache()
def get_settings():
    return Settings()

# Redis caching for frequent queries
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_user_accounts_cached(user_id: int):
    cache_key = f"user:{user_id}:accounts"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    accounts = get_user_accounts(user_id)
    redis_client.setex(cache_key, 300, json.dumps(accounts))
    return accounts
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Multi-stage Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

FROM python:3.11-slim as runtime

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Configuration

```python
# Production settings
class ProductionSettings(Settings):
    DEBUG: bool = False
    DATABASE_ECHO: bool = False
    
    # Security
    SECURE_COOKIES: bool = True
    HTTPS_REDIRECT: bool = True
    
    # Performance
    WORKERS: int = 4
    MAX_CONNECTIONS: int = 100
    
    class Config:
        env_file = ".env.production"
```

### Health Checks

```python
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": VERSION
    }

@app.get("/health/db", tags=["Health"])
async def db_health_check(db: Session = Depends(get_db)):
    """Database connectivity check."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unhealthy: {str(e)}"
        )
```

## 🔧 Development Tools

### Code Quality

```bash
# Linting with Ruff
ruff check .                    # Check for issues
ruff check --fix .              # Auto-fix issues

# Type checking with mypy
mypy app/                       # Type check application

# Format code
ruff format .                   # Format code
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### Development Scripts

```bash
# Database reset (development only)
./scripts/reset_db.sh

# Load sample data
python scripts/load_sample_data.py

# Export API schema
python scripts/export_openapi.py > openapi.json

# Performance testing
python scripts/load_test.py --users=100 --duration=60s
```

## 📚 Additional Resources

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### External Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

### Migration Resources
- [Original ezBookkeeping](https://github.com/mayswind/ezbookkeeping)
- [Migration Guide](../docs/migration-guide.md)
- [API Compatibility Matrix](../docs/api-compatibility.md)

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-endpoint`
3. **Write tests first** (TDD approach)
4. **Implement feature**
5. **Ensure tests pass**: `pytest`
6. **Check code quality**: `ruff check . && mypy app/`
7. **Submit pull request**

### Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Maintain test coverage above 90%
- Use meaningful variable and function names

## 📞 Support

For backend-specific issues:
- **API Issues**: Check `/docs` for endpoint documentation
- **Database Issues**: Review migration logs and connection settings
- **Performance Issues**: Enable query logging and check database indexes
- **Authentication Issues**: Verify JWT configuration and token expiry

---

**Built with FastAPI, SQLModel, and modern Python best practices** 🐍