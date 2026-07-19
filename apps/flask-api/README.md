# FlaskApi API

Flask REST API for flask-api.

## Quick Start

```bash
# Install dependencies
uv sync

# Set up environment
cp .env.example .env

# Run database migrations
flask db upgrade

# Run development server
flask run
```

## Docker

```bash
docker-compose up -d
```

## Testing

```bash
pytest
pytest --cov=src
```

## Project Structure

```
flask_api/
├── src/
│   ├── app.py              # Application factory
│   ├── celery_app.py       # Celery configuration
│   ├── config.py           # Configuration classes
│   ├── extensions.py       # Flask extensions
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API route blueprints
│   ├── schemas/            # Marshmallow schemas
│   ├── services/           # Business logic
│   └── utils/              # Shared utilities
├── tests/
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```
