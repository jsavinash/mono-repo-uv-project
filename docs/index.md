---
icon: material/math-integral
status: new
---

# Python Monorepo Starter Kit

Welcome to the Python Monorepo Starter Kit documentation! This project provides a production-grade
Python monorepo featuring Django REST API, Flask REST API, and Streamlit Frontend — all managed
with `uv` workspace for unified dependency management.

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose (optional)

### Installation

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repo-url>
cd python-starter-kit
make install
```

### Running Services

```bash
# Terminal 1: Django API → http://localhost:8000
make django-run

# Terminal 2: Flask API → http://localhost:5000
make flask-run

# Terminal 3: Streamlit Frontend → http://localhost:8501
make frontend-run

# Or everything with Docker
make docker-up
```

## Project Structure

```
python-starter-kit/
├── apps/                    # Production applications
│   ├── django-api/          # Django REST API
│   ├── flask-api/           # Flask REST API
│   └── frontend/            # Streamlit frontend
├── libs/                    # Shared libraries
│   └── shared/              # Common contracts and DTOs
├── packages/                # Reusable Python packages
├── tools/                   # CLI tools & utilities
├── docs/                    # MkDocs documentation
├── tests/                   # Root-level tests
├── .github/workflows/       # CI/CD pipelines
├── pyproject.toml           # Root workspace config
└── docker-compose.yml       # Service orchestration
```

## Key Features

- **Unified Dependency Management**: Centralized version catalog at `config/dependencies.toml`
- **Multi-Layer Quality Gates**: Pre-commit, pre-push, and CI/CD enforcement
- **Custom Git Hooks**: Branch protection, secret scanning, commit message validation
- **Automated Testing**: Pytest with coverage, matrix testing across Python versions
- **Docker Orchestration**: All services containerized with Docker Compose