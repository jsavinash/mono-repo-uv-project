# 🏗️ Python Monorepo Starter Kit

A production-grade Python monorepo featuring **Django REST API**, **Flask REST API**, and **Streamlit Frontend** — all managed with `uv` workspace for unified dependency management.

## 📋 Architecture Overview

```
mono-repo-uv-project/
│
├── apps/                          # Application projects
│   ├── django-api/                # Django REST API (port 8000)
│   │   ├── src/
│   │   │   ├── config/            # Settings, WSGI, ASGI, URLs
│   │   │   ├── apps/
│   │   │   │   ├── accounts/      # JWT auth, user management
│   │   │   │   ├── core/          # Pagination, exceptions, permissions
│   │   │   │   └── api/           # API versioning & routing
│   │   │   ├── celery_app.py      # Async task queue
│   │   │   └── utils/             # Shared utilities
│   │   ├── tests/                 # Pytest suite
│   │   ├── manage.py              # Django CLI
│   │   └── Dockerfile             # Multi-stage build
│   │
│   ├── flask-api/                 # Flask REST API (port 5000)
│   │   ├── src/
│   │   │   ├── app.py             # Application factory
│   │   │   ├── config.py          # Dev/Prod/Testing configs
│   │   │   ├── extensions.py      # Flask extensions
│   │   │   ├── models/            # SQLAlchemy models
│   │   │   ├── routes/            # API blueprints
│   │   │   ├── schemas/           # Marshmallow validation
│   │   │   ├── services/          # Business logic layer
│   │   │   └── utils/             # Helpers
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   └── frontend/                  # Streamlit Frontend (port 8501)
│       ├── src/
│       │   ├── app.py             # Main app with routing
│       │   ├── pages/             # Login, Home, Dashboard, Profile
│       │   ├── components/        # Reusable UI components
│       │   ├── api/               # HTTP client (httpx)
│       │   ├── auth/              # Auth utilities
│       │   └── utils/             # Helpers
│       ├── tests/
│       └── Dockerfile
│
├── libs/                          # Shared libraries
│   └── shared/                    # Common DTOs, models, utilities
│
├── packages/                      # Reusable Python packages
│   ├── core/                      # Core business logic
│   ├── algorithms/                # Algorithm implementations
│   ├── data_structure/            # Data structure implementations
│   ├── machine-learning/          # ML models & utilities
│   └── ...                        # Domain packages
│
├── tools/                         # CLI tools & utilities
│   └── cli/
│       └── src/cli/
│           ├── boilerplate_generator.py  # Project scaffolding
│           ├── flask_boilerplate.py      # Flask CLI
│           └── migrations.py             # DB migration tools
│
├── tests/                         # Root-level integration tests
├── docs/                          # MkDocs documentation
├── .github/workflows/             # CI/CD pipelines
│
├── pyproject.toml                 # Root workspace config
├── docker-compose.yml             # All services orchestration
├── Makefile                       # Development automation
├── noxfile.py                     # Test session management
└── .pre-commit-config.yaml        # Git hooks
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose (optional)

### 1. Install Dependencies
```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repo-url>
cd mono-repo-uv-project
make install
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Database Migrations
```bash
# Django API
make django-migrate

# Flask API
make flask-db-upgrade
```

### 4. Start Development Servers
```bash
# Terminal 1: Django API → http://localhost:8000
make django-run

# Terminal 2: Flask API → http://localhost:5000
make flask-run

# Terminal 3: Streamlit Frontend → http://localhost:8501
make frontend-run
```

### 5. Or Run Everything with Docker
```bash
make docker-up
# All services start in background
# View logs: make docker-logs
```

## 🎯 Features

### Django REST API (`apps/django-api`)
| Feature | Implementation |
|---------|---------------|
| **Framework** | Django 5.0 + Django REST Framework 3.15 |
| **Auth** | JWT (SimpleJWT) with access/refresh tokens, token blacklisting |
| **User Model** | Custom AbstractUser with profile fields, preferences |
| **API Docs** | Swagger UI + ReDoc via drf-spectacular |
| **Async Tasks** | Celery + Redis for background jobs |
| **Database** | PostgreSQL (SQLite for dev) via django-environ |
| **Caching** | Redis cache backend |
| **CORS** | Configurable CORS headers |
| **Rate Limiting** | Anon: 100/hr, User: 1000/hr |
| **Error Tracking** | Sentry integration |
| **Static Files** | WhiteNoise for production |
| **Profiling** | django-silk for debug performance |
| **Testing** | Pytest with model-bakery, factory-boy |
| **Admin** | Custom UserAdmin with extended fields |

### Flask REST API (`apps/flask-api`)
| Feature | Implementation |
|---------|---------------|
| **Framework** | Flask 3.0 + SQLAlchemy 2.0 |
| **Auth** | JWT (flask-jwt-extended) with refresh/blacklist |
| **Validation** | Marshmallow schemas with input validation |
| **API Design** | Application factory pattern with blueprints |
| **Async Tasks** | Celery + Redis |
| **Rate Limiting** | flask-limiter with Redis storage |
| **Database** | PostgreSQL (SQLite for dev) |
| **CORS** | Configurable origins |
| **Email** | Flask-Mail integration |
| **Error Tracking** | Sentry integration |
| **Logging** | Rotating file + console handlers |
| **Testing** | Pytest with app factory pattern |

### Streamlit Frontend (`apps/frontend`)
| Feature | Implementation |
|---------|---------------|
| **Framework** | Streamlit 1.35+ |
| **Auth UI** | Login/Register forms with validation |
| **API Client** | httpx with Bearer token auth |
| **Charts** | Plotly (line, bar, interactive) |
| **Pages** | Home, Dashboard, Profile |
| **State** | Session state management |
| **Config** | Pydantic-settings with .env support |
| **Theme** | Customizable via .streamlit/config.toml |
| **Components** | Reusable sidebar, cards, badges |

## 📦 Dependency Management

### Centralized Version Catalog

All dependency versions are managed centrally in `config/dependencies.toml` — the single source of truth for the entire monorepo. This file catalogs every dependency organized by ecosystem (Django, Flask, FastAPI, testing, linting, etc.).

### How to Manage Dependencies

```bash
# View the dependency catalog
make dep-catalog

# List all workspace dependencies
make dep-list

# Check for outdated dependencies
make dep-outdated

# Add a dependency to a specific project
make dep-add PROJECT=apps/django-api PKG=requests

# Remove a dependency from a project
make dep-remove PROJECT=apps/django-api PKG=requests

# Upgrade all dependencies
make dep-upgrade-all

# Audit for vulnerabilities
make dep-audit

# Check dependency licenses
make dep-licenses
```

### Override Central Versions

Individual projects can override the central catalog by specifying a different version in their own `pyproject.toml`:

```bash
cd apps/django-api
uv add "django==5.2.0"  # Overrides the central >=5.0,<6.0
```

## 🛠️ Development Workflow

### Code Quality
```bash
make lint          # Ruff lint check
make format        # Ruff auto-format
make typecheck     # MyPy type checking
make test          # Run all tests
make test-cov      # Tests with coverage report
make test-all      # Full suite: test + lint + format + types
```

### Project Scaffolding
```bash
# List available templates
python -m tools.cli.src.cli.boilerplate_generator list-templates

# Generate new Django API
python -m tools.cli.src.cli.boilerplate_generator django apps/my-new-api

# Generate new Flask API
python -m tools.cli.src.cli.boilerplate_generator flask apps/my-new-api

# Generate new Streamlit frontend
python -m tools.cli.src.cli.boilerplate_generator frontend apps/my-new-frontend
```

### Docker Commands
```bash
make docker-build          # Build all images
make docker-up             # Start all services
make docker-up-logs        # Start with logs
make docker-down           # Stop all services
make docker-logs           # View all logs
make docker-logs-django    # Django logs only
make docker-logs-flask     # Flask logs only
make docker-logs-frontend  # Frontend logs only
```

## 🔗 API Endpoints

### Django API (`http://localhost:8000`)
```
POST   /api/v1/auth/register/         # Register new user
POST   /api/v1/auth/login/            # Login (get JWT tokens)
POST   /api/v1/auth/login/refresh/    # Refresh access token
POST   /api/v1/auth/login/verify/     # Verify token
POST   /api/v1/auth/logout/           # Logout (blacklist token)
POST   /api/v1/auth/change-password/  # Change password
GET    /api/v1/profile/               # Get user profile
PATCH  /api/v1/profile/               # Update user profile
GET    /api/v1/health/                # Health check
GET    /api/docs/                     # Swagger UI
GET    /api/redoc/                    # ReDoc
```

### Flask API (`http://localhost:5000`)
```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login (get JWT tokens)
POST   /api/v1/auth/refresh           # Refresh access token
POST   /api/v1/auth/logout            # Logout (blacklist token)
POST   /api/v1/auth/change-password   # Change password
GET    /api/v1/users/me               # Get user profile
PATCH  /api/v1/users/me               # Update user profile
GET    /api/v1/health                 # Health check
```

## 📦 Project Structure Best Practices

### Naming Conventions
- **Apps**: `kebab-case` (e.g., `django-api`, `flask-api`)
- **Packages**: `snake_case` (e.g., `data_structure`, `machine_learning`)
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`

### Architecture Principles
1. **Separation of Concerns**: Each app has its own responsibility
2. **DRY**: Shared code goes in `libs/` or `packages/`
3. **Testability**: Each app has its own test suite
4. **Configurability**: Environment-based configuration
5. **Security**: JWT auth, CORS, rate limiting, secret detection
6. **Observability**: Logging, Sentry, health checks

## 🤝 Contributing

1. Install pre-commit hooks: `pre-commit install`
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and ensure tests pass: `make test-all`
4. Commit using conventional commits: `git commit -m "feat: add new feature"`
5. Push and create a Pull Request

## 📄 License

MIT License - see LICENSE file for details.
