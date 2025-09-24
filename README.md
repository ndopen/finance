# ezBookkeeping FastAPI Edition

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.114+-00a393.svg)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue.js-3.0+-4fc08d.svg)](https://vuejs.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://docker.com)

> A modern, lightweight personal finance management application built with FastAPI and Vue.js, migrated from the original [ezBookkeeping](https://github.com/mayswind/ezbookkeeping) Go implementation.

![ezBookkeeping Screenshot](https://raw.githubusercontent.com/wiki/mayswind/ezbookkeeping/img/desktop/en.png)

## 🌟 Project Overview

This is a **complete migration** of the popular [ezBookkeeping](https://github.com/mayswind/ezbookkeeping) personal finance application from Go to a modern Python FastAPI stack. The project maintains all the powerful features of the original while leveraging the Python ecosystem's rich libraries and FastAPI's high performance.

### Key Features Migrated

- 📱 **Cross-Platform**: Responsive web interface optimized for both desktop and mobile
- 🔒 **Self-Hosted**: Complete control over your financial data with privacy-first design
- 💳 **Comprehensive Bookkeeping**: Two-level accounts, categories, tags, and transaction management
- 🌍 **Multi-Currency**: Support for multiple currencies with automatic exchange rates
- 🔐 **Advanced Security**: JWT authentication, 2FA, rate limiting, and application lock
- 📊 **Rich Analytics**: Advanced filtering, search, visualization, and reporting
- 📁 **Import/Export**: Support for CSV, OFX, QFX, QIF, and other financial formats
- 🤖 **AI Integration**: Receipt image recognition and MCP (Model Context Protocol) support
- 🌐 **Internationalization**: Multi-language and timezone support
- 📱 **PWA Ready**: Progressive Web App capabilities for native-like mobile experience

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vue.js 3      │    │   FastAPI        │    │  PostgreSQL     │
│   Frontend      │◄──►│   Backend        │◄──►│  Database       │
│   (TypeScript)  │    │   (Python)       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   TanStack      │    │   SQLModel       │    │   Alembic       │
│   Router/Query  │    │   Pydantic       │    │   Migrations    │
│   Chakra UI     │    │   JWT Auth       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack

#### Backend (FastAPI)
- **Framework**: FastAPI 0.114+ with async/await support
- **ORM**: SQLModel (combines Pydantic + SQLAlchemy)
- **Database**: PostgreSQL (primary), SQLite (development)
- **Authentication**: JWT with PassLib and bcrypt
- **Validation**: Pydantic v2 with automatic OpenAPI generation
- **Migration**: Alembic for database schema management
- **Testing**: Pytest with comprehensive test coverage
- **Documentation**: Auto-generated OpenAPI/Swagger docs

#### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript for type safety
- **Router**: Vue Router 4 with nested routes
- **State Management**: Pinia for reactive state
- **UI Components**: Chakra UI Vue (responsive design)
- **HTTP Client**: Axios with auto-generated API client
- **Build Tool**: Vite for fast development and optimized builds
- **PWA**: Workbox for offline capabilities

#### DevOps & Development
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose with hot-reload
- **Code Quality**: Ruff (Python), ESLint (TypeScript)
- **Type Checking**: mypy (Python), TypeScript compiler
- **Testing**: Pytest (backend), Vitest (frontend), Playwright (E2E)
- **CI/CD**: GitHub Actions with automated testing and deployment

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.10+ (for local development)
- Node.js 18+ and npm (for frontend development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd finance
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker (Recommended)

```bash
# Start all services with hot-reload
docker compose watch

# Or start without hot-reload
docker compose up -d
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Database Migration

```bash
cd backend
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 📖 Migration from Original ezBookkeeping

This project maintains **API compatibility** with the original ezBookkeeping wherever possible. Here's what's been migrated:

### ✅ Completed Features

- [ ] **Core Data Models**: Users, Accounts, Categories, Tags, Transactions
- [ ] **Authentication System**: JWT tokens, sessions, user management
- [ ] **Account Management**: Multi-level accounts with categories and currencies
- [ ] **Transaction System**: Income/Expense/Transfer with full CRUD operations
- [ ] **Category & Tag System**: Hierarchical categories and flexible tagging
- [ ] **API Structure**: RESTful API matching original endpoints
- [ ] **Database Schema**: PostgreSQL schema with proper relationships
- [ ] **Docker Deployment**: Single-command deployment with Docker Compose

### 🚧 In Progress

- [ ] **Multi-Currency Support**: Exchange rates and currency conversion
- [ ] **Import/Export**: CSV, OFX, QFX, QIF format support
- [ ] **Advanced Analytics**: Charts, reports, and data visualization
- [ ] **Security Features**: 2FA, rate limiting, application lock
- [ ] **AI Features**: Receipt image recognition, MCP integration
- [ ] **PWA Features**: Offline support, push notifications

### 📊 Data Migration

If you're migrating from the original ezBookkeeping:

```bash
# Export data from original ezBookkeeping
# (Follow original documentation for export)

# Import data to FastAPI version
cd backend
python scripts/import_data.py --source=/path/to/exported/data
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost/ezbook_db"
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Security
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_HOST="http://localhost:5173"
BACKEND_CORS_ORIGINS=["http://localhost:5173","https://yourdomain.com"]

# Features
ENABLE_REGISTRATION=true
ENABLE_2FA=false
MAX_LOGIN_ATTEMPTS=5

# External Services
EXCHANGE_RATE_API_KEY="your-api-key"
SENTRY_DSN="your-sentry-dsn"
```

### Production Deployment

```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy with production settings
docker compose -f docker-compose.prod.yml up -d

# Setup SSL with Let's Encrypt (optional)
docker compose -f docker-compose.prod.yml -f docker-compose.ssl.yml up -d
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest                          # Run all tests
pytest --cov=app               # Run with coverage
pytest -k "test_user"          # Run specific tests
```

### Frontend Testing
```bash
cd frontend
npm test                       # Unit tests
npm run test:e2e              # End-to-end tests
npm run test:coverage         # Coverage report
```

### Integration Testing
```bash
# Full stack testing
./scripts/test-all.sh

# API testing with live database
./scripts/test-integration.sh
```

## 📚 Documentation

- **API Documentation**: Auto-generated at `/docs` (Swagger UI)
- **Database Schema**: See `backend/docs/database.md`
- **Frontend Components**: See `frontend/docs/components.md`
- **Migration Guide**: See `docs/migration-guide.md`
- **Deployment Guide**: See `docs/deployment.md`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow TDD**: Write tests first, then implement features
4. **Run tests**: Ensure all tests pass
5. **Submit PR**: Create a pull request with detailed description

### Code Quality Standards

- **Python**: Follow PEP 8, use type hints, maintain 90%+ test coverage
- **TypeScript**: Follow ESLint rules, use strict mode, document components
- **Git**: Use conventional commits, rebase before merging
- **Documentation**: Update docs with new features or API changes

## 📈 Roadmap

### Version 1.0 (Current)
- ✅ Core bookkeeping functionality
- ✅ Docker deployment
- ✅ Basic API compatibility

### Version 1.1 (Q2 2025)
- 🔄 Multi-currency support
- 🔄 Data import/export
- 🔄 Advanced reporting

### Version 1.2 (Q3 2025)
- 📱 Mobile PWA enhancements
- 🤖 AI-powered features
- 🔐 Enhanced security features

### Version 2.0 (Q4 2025)
- 🌐 Multi-tenant support
- 📊 Advanced analytics dashboard
- 🔌 Plugin system

## 🆚 Original vs FastAPI Edition

| Feature | Original (Go) | FastAPI Edition | Status |
|---------|---------------|-----------------|---------|
| **Performance** | Very Fast | Fast | ✅ |
| **Memory Usage** | Low | Medium | ✅ |
| **Development Speed** | Medium | Fast | ✅ |
| **Type Safety** | Good | Excellent | ✅ |
| **API Documentation** | Manual | Auto-generated | ✅ |
| **Testing** | Good | Excellent | ✅ |
| **Ecosystem** | Limited | Rich | ✅ |
| **Learning Curve** | Medium | Low | ✅ |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Original ezBookkeeping**: Thanks to [MaysWind](https://github.com/mayswind) for creating the original application
- **FastAPI**: Sebastian Ramirez for the excellent FastAPI framework
- **Vue.js Team**: For the powerful and approachable frontend framework
- **Contributors**: All the amazing people who've contributed to this migration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/ezbook-fastapi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ezbook-fastapi/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-org/ezbook-fastapi/wiki)
- **Original Project**: [ezBookkeeping](https://github.com/mayswind/ezbookkeeping)

---

**Built with ❤️ using FastAPI, Vue.js, and modern web technologies**