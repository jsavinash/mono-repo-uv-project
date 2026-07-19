# Frontend Frontend

Streamlit frontend for frontend.

## Quick Start

```bash
# Install dependencies
uv sync

# Set up environment
cp .env.example .env

# Run the app
streamlit run src/app.py
```

## Docker

```bash
docker-compose up -d
```

## Project Structure

```
frontend/
├── src/
│   ├── app.py              # Main application entry point
│   ├── config.py           # Configuration & settings
│   ├── api/                # API client
│   │   ├── __init__.py
│   │   └── client.py       # HTTP client for backend APIs
│   ├── components/         # Reusable UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   └── cards.py
│   ├── pages/              # Multi-page app pages
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── dashboard.py
│   │   └── profile.py
│   ├── auth/               # Authentication
│   │   ├── __init__.py
│   │   └── login.py
│   └── utils/              # Shared utilities
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── pyproject.toml
└── Dockerfile
```
