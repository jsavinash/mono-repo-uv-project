# DjangoApi API

Django REST API for django-api.

## Quick Start

```bash
# Install dependencies
uv sync

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Docker

```bash
docker-compose up -d
```

## API Documentation

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Testing

```bash
pytest
pytest --cov=src
```

## Project Structure

```
django_api/
├── src/
│   ├── apps/           # Django applications
│   │   ├── accounts/   # User authentication & management
│   │   ├── core/       # Core functionality (health, config)
│   │   └── api/        # API versioning & routing
│   ├── config/         # Django settings (dev/prod)
│   ├── templates/      # Email templates, etc.
│   └── utils/          # Shared utilities
├── manage.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```
