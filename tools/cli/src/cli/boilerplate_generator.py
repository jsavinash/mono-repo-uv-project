#!/usr/bin/env python3
"""
Comprehensive monorepo boilerplate generator for Django API, Flask API, and Python frontend.

Usage:
    uv run python -m tools.cli.src.cli.boilerplate_generator django services/my-django-api
    uv run python -m tools.cli.src.cli.boilerplate_generator flask services/my-flask-api
    uv run python -m tools.cli.src.cli.boilerplate_generator frontend apps/my-frontend
"""

import os
from pathlib import Path
import re
import stat
from typing import Annotated, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
import typer
from typer import Argument, BadParameter, Option, Typer

app = Typer(
    add_completion=False,
    name="boilerplate",
    help="Generate boilerplate code for Django, Flask, and Python frontend projects.",
)
console = Console()

# ──────────────────────────────────────────────────────────────
#  Utility helpers
# ──────────────────────────────────────────────────────────────


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    console.print(f"  [green]✓[/] {path}")


def _make_executable(path: Path) -> None:
    st = path.stat()
    path.chmod(st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _to_snake_case(name: str) -> str:
    """Convert any string to snake_case."""
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    name = re.sub(r"[-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_").lower()


def _to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    return "".join(word.capitalize() for word in re.split(r"[-_]+", name))


def _validate_project_name(value: str) -> str:
    """Validate project name format."""
    if not re.match(r"^[a-z][a-z0-9_-]*$", value):
        raise BadParameter(
            f"'{value}' is not a valid project name. "
            "Use lowercase letters, numbers, hyphens, and underscores only. Must start with a letter."
        )
    return value


def _print_summary(base: Path, project_type: str) -> None:
    """Print a summary of the generated project."""
    tree = Tree(f"[bold]{project_type} Project: {base}[/]")
    for path in sorted(base.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            tree.add(f"[dim]{path.relative_to(base)}[/]")
    console.print(tree)

    table = Table(title="Next Steps")
    table.add_column("Step", style="cyan")
    table.add_column("Command", style="green")
    table.add_row("1. Install dependencies", "uv sync")
    table.add_row("2. Set up environment", "cp .env.example .env")
    table.add_row("3. Edit .env", "nano .env")
    table.add_row("4. Run the app", "See README.md for details")
    console.print(table)


# ──────────────────────────────────────────────────────────────
#  Django API Boilerplate
# ──────────────────────────────────────────────────────────────


def generate_django_api(target_dir: str, project_name: str) -> None:
    """Generate a complete Django REST API project."""
    base = Path(target_dir)
    src_dir = base / "src"
    project_snake = _to_snake_case(project_name)
    project_pascal = _to_pascal_case(project_name)

    console.print(
        Panel(f"[bold blue]Generating Django API: {project_name}[/]", expand=False)
    )

    # ── pyproject.toml ──────────────────────────────────────
    _write(
        base / "pyproject.toml",
        f"""[project]
name = "{project_snake}"
version = "0.1.0"
description = "Django REST API - {project_name}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "django>=5.0,<6.0",
    "djangorestframework>=3.15.0",
    "django-cors-headers>=4.3.0",
    "django-filter>=24.1",
    "django-environ>=0.11.0",
    "django-extensions>=3.2.0",
    "django-health-check>=3.17.0",
    "django-redis>=5.4.0",
    "django-silk>=5.1.0",
    "django-storages>=1.14.0",
    "django-allauth>=0.60.0",
    "djangorestframework-simplejwt>=5.3.0",
    "drf-spectacular>=0.27.0",
    "celery>=5.3.0",
    "redis>=5.0.0",
    "gunicorn>=21.2.0",
    "psycopg2-binary>=2.9.0",
    "python-dotenv>=1.0.0",
    "pillow>=10.0.0",
    "sentry-sdk>=2.0.0",
    "whitenoise>=6.6.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.5",
    "pytest-cov>=5.0",
    "model-bakery>=1.18.0",
    "factory-boy>=3.3.0",
    "faker>=22.0.0",
    "django-debug-toolbar>=5.0.0",
    "ipython>=8.0.0",
    "ruff>=0.11.0",
    "mypy>=1.16.0",
]
""",
    )

    # ── manage.py ───────────────────────────────────────────
    _write(
        base / "manage.py",
        "#!/usr/bin/env python\n"
        "# Django's command-line utility for administrative tasks.\n"
        "import os\n"
        "import sys\n"
        "\n"
        "\n"
        "def main() -> None:\n"
        '    """Run administrative tasks."""\n'
        '    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")\n'
        "    try:\n"
        "        from django.core.management import execute_from_command_line\n"
        "    except ImportError as exc:\n"
        "        raise ImportError(\n"
        "            \"Couldn't import Django. Are you sure it's installed and \"\n"
        '            "available on your PYTHONPATH environment variable? Did you "\n'
        '            "forget to activate a virtual environment?"\n'
        "        ) from exc\n"
        "    execute_from_command_line(sys.argv)\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    )
    _make_executable(base / "manage.py")

    # ── .env.example ────────────────────────────────────────
    _write(
        base / ".env.example",
        f"""# --- Django Core ---
DJANGO_SECRET_KEY=change-me-to-a-random-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_SETTINGS_MODULE=src.config.settings

# --- Database ---
DATABASE_URL=sqlite:///db.sqlite3
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# --- Redis / Cache ---
REDIS_URL=redis://localhost:6379/0
CACHE_URL=redis://localhost:6379/1

# --- Celery ---
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# --- JWT ---
JWT_SECRET_KEY=change-me-to-a-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# --- CORS ---
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8501

# --- Email ---
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@example.com

# --- Sentry ---
SENTRY_DSN=

# --- Storage ---
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# --- API ---
API_VERSION=v1
API_TITLE="{project_pascal} API"
API_DESCRIPTION="REST API for {project_name}"
""",
    )

    # ── Dockerfile ─────────────────────────────────────────
    _write(
        base / "Dockerfile",
        """# --- Build stage ---
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential libpq-dev && \\
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip && \\
    pip install --user --no-warn-script-location .

# --- Runtime stage ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    libpq-dev curl && \\
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/api/v1/health/ || exit 1

CMD ["gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--worker-class", "gthread"]
""",
    )

    # ── docker-compose.yml ─────────────────────────────────
    _write(
        base / "docker-compose.yml",
        f"""version: "3.9"

services:
  api:
    build: .
    container_name: {project_snake}_api
    command: gunicorn src.config.wsgi:application --bind 0.0.0.0:8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  celery-worker:
    build: .
    container_name: {project_snake}_celery_worker
    command: celery -A src.celery_app worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis
      - api
    restart: unless-stopped

  celery-beat:
    build: .
    container_name: {project_snake}_celery_beat
    command: celery -A src.celery_app beat --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis
      - api
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: {project_snake}_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${{POSTGRES_DB:-{project_snake}}}
      POSTGRES_USER: ${{POSTGRES_USER:-{project_snake}}}
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:-changeme}}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${{POSTGRES_USER:-{project_snake}}}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: {project_snake}_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
""",
    )

    # ── .dockerignore ──────────────────────────────────────
    _write(
        base / ".dockerignore",
        """__pycache__
*.pyc
*.pyo
.env
.git
.gitignore
*.md
.venv
venv
*.sqlite3
""",
    )

    # ── README.md ──────────────────────────────────────────
    _write(
        base / "README.md",
        f"""# {project_pascal} API

Django REST API for {project_name}.

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
{project_snake}/
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
""",
    )

    # ── src/__init__.py ────────────────────────────────────
    _write(src_dir / "__init__.py", "")

    # ── src/celery_app.py ──────────────────────────────────
    _write(
        src_dir / "celery_app.py",
        f"""import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

app = Celery("{project_snake}")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    print(f"Request: {{self.request!r}}")
""",
    )

    # ── src/config/ ────────────────────────────────────────
    _write(src_dir / "config" / "__init__.py", "")

    _write(
        src_dir / "config" / "settings.py",
        f"'''\n"
        f"Django settings for {project_name} project.\n"
        f"\n"
        f"Generated by boilerplate-generator.\n"
        f"'''\n"
        f"\n"
        f"import os\n"
        f"from datetime import timedelta\n"
        f"from pathlib import Path\n"
        f"\n"
        f"import environ\n"
        f"\n"
        f"# --- Build paths ---\n"
        f"BASE_DIR = Path(__file__).resolve().parent.parent.parent\n"
        f"\n"
        f"# --- Environment ---\n"
        f"env = environ.Env(\n"
        f"    DJANGO_DEBUG=(bool, True),\n"
        f'    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "0.0.0.0"]),\n'
        f'    CORS_ALLOWED_ORIGINS=(list, ["http://localhost:3000", "http://localhost:8501"]),\n'
        f"    JWT_ACCESS_TOKEN_LIFETIME_MINUTES=(int, 30),\n"
        f"    JWT_REFRESH_TOKEN_LIFETIME_DAYS=(int, 7),\n"
        f")\n"
        f"\n"
        f'environ.Env.read_env(BASE_DIR / ".env")\n'
        f"\n"
        f"# --- Security ---\n"
        f'SECRET_KEY = env("DJANGO_SECRET_KEY", default="insecure-dev-key-change-in-production")\n'
        f'DEBUG = env("DJANGO_DEBUG")\n'
        f'ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")\n'
        f"\n"
        f"# --- Applications ---\n"
        f"DJANGO_APPS = [\n"
        f'    "django.contrib.admin",\n'
        f'    "django.contrib.auth",\n'
        f'    "django.contrib.contenttypes",\n'
        f'    "django.contrib.sessions",\n'
        f'    "django.contrib.messages",\n'
        f'    "django.contrib.staticfiles",\n'
        f'    "django.contrib.sites",\n'
        f"]\n"
        f"\n"
        f"THIRD_PARTY_APPS = [\n"
        f'    "rest_framework",\n'
        f'    "rest_framework_simplejwt",\n'
        f'    "rest_framework_simplejwt.token_blacklist",\n'
        f'    "corsheaders",\n'
        f'    "django_filters",\n'
        f'    "django_extensions",\n'
        f'    "drf_spectacular",\n'
        f'    "drf_spectacular_sidecar",\n'
        f'    "health_check",\n'
        f'    "health_check.db",\n'
        f'    "health_check.cache",\n'
        f'    "health_check.storage",\n'
        f'    "allauth",\n'
        f'    "allauth.account",\n'
        f'    "allauth.socialaccount",\n'
        f'    "silk",\n'
        f"]\n"
        f"\n"
        f"LOCAL_APPS = [\n"
        f'    "src.apps.accounts",\n'
        f'    "src.apps.core",\n'
        f'    "src.apps.api",\n'
        f"]\n"
        f"\n"
        f"INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS\n"
        f"\n"
        f"# --- Middleware ---\n"
        f"MIDDLEWARE = [\n"
        f'    "django.middleware.security.SecurityMiddleware",\n'
        f'    "whitenoise.middleware.WhiteNoiseMiddleware",\n'
        f'    "corsheaders.middleware.CorsMiddleware",\n'
        f'    "django.contrib.sessions.middleware.SessionMiddleware",\n'
        f'    "django.middleware.common.CommonMiddleware",\n'
        f'    "django.middleware.csrf.CsrfViewMiddleware",\n'
        f'    "django.contrib.auth.middleware.AuthenticationMiddleware",\n'
        f'    "django.contrib.messages.middleware.MessageMiddleware",\n'
        f'    "django.middleware.clickjacking.XFrameOptionsMiddleware",\n'
        f'    "allauth.account.middleware.AccountMiddleware",\n'
        f"]\n"
        f"\n"
        f"if DEBUG:\n"
        f'    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")\n'
        f"\n"
        f"# --- URL Configuration ---\n"
        f'ROOT_URLCONF = "src.config.urls"\n'
        f"\n"
        f"# --- Templates ---\n"
        f"TEMPLATES = [\n"
        f"    {{\n"
        f'        "BACKEND": "django.template.backends.django.DjangoTemplates",\n'
        f'        "DIRS": [BASE_DIR / "src" / "templates"],\n'
        f'        "APP_DIRS": True,\n'
        f'        "OPTIONS": {{\n'
        f'            "context_processors": [\n'
        f'                "django.template.context_processors.debug",\n'
        f'                "django.template.context_processors.request",\n'
        f'                "django.contrib.auth.context_processors.auth",\n'
        f'                "django.contrib.messages.context_processors.messages",\n'
        f"            ],\n"
        f"        }},\n"
        f"    }},\n"
        f"]\n"
        f"\n"
        f"# --- WSGI / ASGI ---\n"
        f'WSGI_APPLICATION = "src.config.wsgi.application"\n'
        f'ASGI_APPLICATION = "src.config.asgi.application"\n'
        f"\n"
        f"# --- Database ---\n"
        f"DATABASES = {{\n"
        f'    "default": env.db_url(\n'
        f'        "DATABASE_URL",\n'
        f"        default=f\"sqlite:///{{BASE_DIR / 'db.sqlite3'}}\",\n"
        f"    ),\n"
        f"}}\n"
        f"\n"
        f"# --- Password validation ---\n"
        f"AUTH_PASSWORD_VALIDATORS = [\n"
        f'    {{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}},\n'
        f'    {{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}},\n'
        f'    {{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}},\n'
        f'    {{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}},\n'
        f"]\n"
        f"\n"
        f"# --- Authentication ---\n"
        f'AUTH_USER_MODEL = "accounts.User"\n'
        f"\n"
        f"AUTHENTICATION_BACKENDS = [\n"
        f'    "django.contrib.auth.backends.ModelBackend",\n'
        f'    "allauth.account.auth_backends.AuthenticationBackend",\n'
        f"]\n"
        f"\n"
        f"# --- REST Framework ---\n"
        f"REST_FRAMEWORK = {{\n"
        f'    "DEFAULT_AUTHENTICATION_CLASSES": (\n'
        f'        "rest_framework_simplejwt.authentication.JWTAuthentication",\n'
        f'        "rest_framework.authentication.SessionAuthentication",\n'
        f"    ),\n"
        f'    "DEFAULT_PERMISSION_CLASSES": (\n'
        f'        "rest_framework.permissions.IsAuthenticated",\n'
        f"    ),\n"
        f'    "DEFAULT_PAGINATION_CLASS": "src.apps.core.pagination.StandardPagination",\n'
        f'    "PAGE_SIZE": 25,\n'
        f'    "DEFAULT_FILTER_BACKENDS": (\n'
        f'        "django_filters.rest_framework.DjangoFilterBackend",\n'
        f'        "rest_framework.filters.SearchFilter",\n'
        f'        "rest_framework.filters.OrderingFilter",\n'
        f"    ),\n"
        f'    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",\n'
        f'    "DEFAULT_THROTTLE_CLASSES": [\n'
        f'        "rest_framework.throttling.AnonRateThrottle",\n'
        f'        "rest_framework.throttling.UserRateThrottle",\n'
        f"    ],\n"
        f'    "DEFAULT_THROTTLE_RATES": {{\n'
        f'        "anon": "100/hour",\n'
        f'        "user": "1000/hour",\n'
        f"    }},\n"
        f'    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",\n'
        f'    "DEFAULT_VERSION": "v1",\n'
        f'    "ALLOWED_VERSIONS": ["v1"],\n'
        f'    "EXCEPTION_HANDLER": "src.apps.core.exceptions.custom_exception_handler",\n'
        f'    "NON_FIELD_ERRORS_KEY": "error",\n'
        f"}}\n"
        f"\n"
        f"# --- SimpleJWT ---\n"
        f"SIMPLE_JWT = {{\n"
        f'    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env("JWT_ACCESS_TOKEN_LIFETIME_MINUTES")),\n'
        f'    "REFRESH_TOKEN_LIFETIME": timedelta(days=env("JWT_REFRESH_TOKEN_LIFETIME_DAYS")),\n'
        f'    "ROTATE_REFRESH_TOKENS": True,\n'
        f'    "BLACKLIST_AFTER_ROTATION": True,\n'
        f'    "UPDATE_LAST_LOGIN": True,\n'
        f'    "AUTH_HEADER_TYPES": ("Bearer",),\n'
        f'    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",\n'
        f'    "USER_ID_FIELD": "id",\n'
        f'    "USER_ID_CLAIM": "user_id",\n'
        f'    "TOKEN_OBTAIN_SERIALIZER": "src.apps.accounts.serializers.CustomTokenObtainPairSerializer",\n'
        f"}}\n"
        f"\n"
        f"# --- Spectacular (API Docs) ---\n"
        f"SPECTACULAR_SETTINGS = {{\n"
        f'    "TITLE": env("API_TITLE", default="{project_pascal} API"),\n'
        f'    "DESCRIPTION": env("API_DESCRIPTION", default="REST API for {project_name}"),\n'
        f'    "VERSION": env("API_VERSION", default="v1"),\n'
        f'    "SERVE_INCLUDE_SCHEMA": False,\n'
        f'    "SWAGGER_UI_DIST": "SIDECAR",\n'
        f'    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",\n'
        f'    "REDOC_DIST": "SIDECAR",\n'
        f'    "COMPONENT_SPLIT_REQUEST": True,\n'
        f'    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",\n'
        f"}}\n"
        f"\n"
        f"# --- CORS ---\n"
        f'CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")\n'
        f"CORS_ALLOW_CREDENTIALS = True\n"
        f"CORS_ALLOW_METHODS = [\n"
        f'    "DELETE",\n'
        f'    "GET",\n'
        f'    "OPTIONS",\n'
        f'    "PATCH",\n'
        f'    "POST",\n'
        f'    "PUT",\n'
        f"]\n"
        f"CORS_ALLOW_HEADERS = [\n"
        f'    "accept",\n'
        f'    "authorization",\n'
        f'    "content-type",\n'
        f'    "x-requested-with",\n'
        f"]\n"
        f"\n"
        f"# --- Celery ---\n"
        f'CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")\n'
        f'CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")\n'
        f'CELERY_ACCEPT_CONTENT = ["json"]\n'
        f'CELERY_TASK_SERIALIZER = "json"\n'
        f'CELERY_RESULT_SERIALIZER = "json"\n'
        f'CELERY_TIMEZONE = "UTC"\n'
        f"CELERY_TASK_TRACK_STARTED = True\n"
        f"CELERY_TASK_TIME_LIMIT = 30 * 60\n"
        f"CELERY_BEAT_SCHEDULE = {{}}\n"
        f"\n"
        f"# --- Cache ---\n"
        f"CACHES = {{\n"
        f'    "default": env.cache_url(\n'
        f'        "CACHE_URL",\n'
        f'        default="redis://localhost:6379/1",\n'
        f"    ),\n"
        f"}}\n"
        f"\n"
        f"# --- Internationalization ---\n"
        f'LANGUAGE_CODE = "en-us"\n'
        f'TIME_ZONE = "UTC"\n'
        f"USE_I18N = True\n"
        f"USE_TZ = True\n"
        f"\n"
        f"# --- Static files ---\n"
        f'STATIC_URL = "static/"\n'
        f'STATIC_ROOT = BASE_DIR / "staticfiles"\n'
        f'STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"\n'
        f"\n"
        f"# --- Media files ---\n"
        f'MEDIA_URL = "media/"\n'
        f'MEDIA_ROOT = BASE_DIR / "media"\n'
        f"\n"
        f"# --- Email ---\n"
        f'EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")\n'
        f'EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")\n'
        f'EMAIL_PORT = env.int("EMAIL_PORT", default=587)\n'
        f'EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)\n'
        f'EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")\n'
        f'EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")\n'
        f'DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@example.com")\n'
        f"\n"
        f"# --- Sentry ---\n"
        f'SENTRY_DSN = env("SENTRY_DSN", default=None)\n'
        f"if SENTRY_DSN:\n"
        f"    import sentry_sdk\n"
        f"    from sentry_sdk.integrations.django import DjangoIntegration\n"
        f"\n"
        f"    sentry_sdk.init(\n"
        f"        dsn=SENTRY_DSN,\n"
        f"        integrations=[DjangoIntegration()],\n"
        f"        traces_sample_rate=1.0,\n"
        f"        send_default_pii=True,\n"
        f"    )\n"
        f"\n"
        f"# --- Logging ---\n"
        f"LOGGING = {{\n"
        f'    "version": 1,\n'
        f'    "disable_existing_loggers": False,\n'
        f'    "formatters": {{\n'
        f'        "verbose": {{\n'
        f'            "format": "{{levelname}} {{asctime}} {{module}} {{process:d}} {{thread:d}} {{message}}",\n'
        f'            "style": "{{",\n'
        f"        }},\n"
        f'        "simple": {{\n'
        f'            "format": "{{levelname}} {{message}}",\n'
        f'            "style": "{{",\n'
        f"        }},\n"
        f"    }},\n"
        f'    "filters": {{\n'
        f'        "require_debug_true": {{\n'
        f'            "()": "django.utils.log.RequireDebugTrue",\n'
        f"        }},\n"
        f"    }},\n"
        f'    "handlers": {{\n'
        f'        "console": {{\n'
        f'            "level": "INFO",\n'
        f'            "filters": ["require_debug_true"],\n'
        f'            "class": "logging.StreamHandler",\n'
        f'            "formatter": "simple",\n'
        f"        }},\n"
        f'        "file": {{\n'
        f'            "level": "WARNING",\n'
        f'            "class": "logging.handlers.RotatingFileHandler",\n'
        f'            "filename": BASE_DIR / "logs" / "django.log",\n'
        f'            "maxBytes": 1024 * 1024 * 5,  # 5 MB\n'
        f'            "backupCount": 5,\n'
        f'            "formatter": "verbose",\n'
        f"        }},\n"
        f"    }},\n"
        f'    "loggers": {{\n'
        f'        "django": {{\n'
        f'            "handlers": ["console", "file"],\n'
        f'            "level": "INFO",\n'
        f"        }},\n"
        f'        "src": {{\n'
        f'            "handlers": ["console", "file"],\n'
        f'            "level": "DEBUG" if DEBUG else "INFO",\n'
        f'            "propagate": True,\n'
        f"        }},\n"
        f"    }},\n"
        f"}}\n"
        f"\n"
        f"# --- Default primary key field type ---\n"
        f'DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"\n'
        f"\n"
        f"# --- Site ID (django.contrib.sites) ---\n"
        f"SITE_ID = 1\n",
    )

    _write(
        src_dir / "config" / "urls.py",
        """from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/", include("src.apps.api.urls", namespace="v1")),

    # Health check
    path("api/v1/health/", include("health_check.urls")),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Silk profiling (debug only)
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
""",
    )

    _write(
        src_dir / "config" / "wsgi.py",
        """import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

application = get_wsgi_application()
""",
    )

    _write(
        src_dir / "config" / "asgi.py",
        """import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

application = get_asgi_application()
""",
    )

    # ── src/apps/ ───────────────────────────────────────────
    apps_dir = src_dir / "apps"
    _write(apps_dir / "__init__.py", "")

    # ── src/apps/accounts/ ──────────────────────────────────
    accounts_dir = apps_dir / "accounts"
    _write(accounts_dir / "__init__.py", "")

    _write(
        accounts_dir / "models.py",
        """from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Custom user model with additional fields.'''

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    bio = models.TextField(max_length=500, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(blank=True, null=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, choices=[("light", "Light"), ("dark", "Dark")], default="light")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email or self.username
""",
    )

    _write(
        accounts_dir / "admin.py",
        """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from src.apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''Admin configuration for custom User model.'''

    list_display = ("email", "username", "is_staff", "is_active", "email_verified", "date_joined")
    list_filter = ("is_staff", "is_active", "email_verified", "theme")
    search_fields = ("email", "username", "phone_number")
    ordering = ("-date_joined",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "bio", "avatar", "date_of_birth", "email_verified", "is_online", "last_activity")}),
        ("Preferences", {"fields": ("email_notifications", "theme")}),
    )
""",
    )

    _write(
        accounts_dir / "serializers.py",
        """from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for user model.'''

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "bio",
            "avatar",
            "date_of_birth",
            "email_verified",
            "is_online",
            "last_activity",
            "email_notifications",
            "theme",
            "date_joined",
        )
        read_only_fields = ("id", "email_verified", "is_online", "last_activity", "date_joined")


class UserCreateSerializer(serializers.ModelSerializer):
    '''Serializer for user registration.'''

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm", "phone_number")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating user profile.'''

    class Meta:
        model = User
        fields = ("phone_number", "bio", "avatar", "date_of_birth", "email_notifications", "theme")


class ChangePasswordSerializer(serializers.Serializer):
    '''Serializer for password change.'''

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        if attrs["new_password"] != attrs.pop("new_password_confirm"):
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        return attrs


class CustomTokenObtainPairSerializer(serializers.Serializer):
    '''Custom JWT token obtain serializer.'''

    email = serializers.EmailField()
    password = serializers.CharField()
""",
    )

    _write(
        accounts_dir / "views.py",
        """from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from src.apps.accounts.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    '''User registration endpoint.'''

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class UserDetailView(generics.RetrieveUpdateAPIView):
    '''Get or update current user profile.'''

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    '''Change current user's password.'''
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    if not user.check_password(serializer.validated_data["old_password"]):
        return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data["new_password"])
    user.save()
    return Response({"detail": "Password updated successfully."})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    '''Blacklist JWT refresh token.'''
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"detail": "Successfully logged out."})
    except Exception:
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
""",
    )

    _write(
        accounts_dir / "urls.py",
        """from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from src.apps.accounts import views

urlpatterns = [
    # Authentication
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", views.logout, name="logout"),
    path("auth/change-password/", views.change_password, name="change_password"),

    # Profile
    path("profile/", views.UserDetailView.as_view(), name="user_detail"),
]
""",
    )

    _write(
        accounts_dir / "tests.py",
        """import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_success(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = client.post("/api/v1/auth/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data
        assert User.objects.count() == 1

    def test_register_user_password_mismatch(self):
        client = APIClient()
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "differentpass",
        }
        response = client.post("/api/v1/auth/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserAuthentication:
    def test_login_success(self):
        User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_login_invalid_credentials(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"email": "wrong@example.com", "password": "wrongpass"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
""",
    )

    # ── src/apps/core/ ──────────────────────────────────────
    core_dir = apps_dir / "core"
    _write(core_dir / "__init__.py", "")

    _write(
        core_dir / "pagination.py",
        """from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    '''Standard pagination with configurable page size.'''

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"
""",
    )

    _write(
        core_dir / "exceptions.py",
        """from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    '''Custom exception handler that returns consistent error responses.'''
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        custom_response = {
            "success": False,
            "status_code": response.status_code,
            "message": _get_error_message(response.status_code),
            "errors": errors,
        }
        response.data = custom_response

    return response


def _get_error_message(status_code: int) -> str:
    '''Get a human-readable error message for a status code.'''
    messages = {
        status.HTTP_400_BAD_REQUEST: "Bad request. Please check your input.",
        status.HTTP_401_UNAUTHORIZED: "Authentication required.",
        status.HTTP_403_FORBIDDEN: "You do not have permission to perform this action.",
        status.HTTP_404_NOT_FOUND: "Resource not found.",
        status.HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed.",
        status.HTTP_409_CONFLICT: "Resource conflict.",
        status.HTTP_429_TOO_MANY_REQUESTS: "Too many requests. Please try again later.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error.",
    }
    return messages.get(status_code, "An error occurred.")
""",
    )

    _write(
        core_dir / "permissions.py",
        """from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    '''Allow read-only access to everyone, but write access only to admins.'''

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    '''Allow access only to the object owner or admin.'''

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return hasattr(obj, "user") and obj.user == request.user
""",
    )

    _write(
        core_dir / "mixins.py",
        """class TimestampMixin:
    '''Mixin that provides created_at and updated_at fields.'''

    @classmethod
    def setup_timestamp_fields(cls, model_class):
        from django.db import models

        if not hasattr(model_class, "created_at"):
            model_class.add_to_class(
                "created_at",
                models.DateTimeField(auto_now_add=True),
            )
        if not hasattr(model_class, "updated_at"):
            model_class.add_to_class(
                "updated_at",
                models.DateTimeField(auto_now=True),
            )
""",
    )

    _write(
        core_dir / "utils.py",
        """import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    '''Extract client IP address from request.'''
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def log_request(request, response=None, level: str = "INFO") -> None:
    '''Log API request details.'''
    log_data = {
        "method": request.method,
        "path": request.path,
        "user": str(request.user) if request.user.is_authenticated else "anonymous",
        "ip": get_client_ip(request),
    }
    if response:
        log_data["status_code"] = response.status_code

    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"API Request: {log_data}")
""",
    )

    _write(
        core_dir / "tasks.py",
        """from celery import shared_task


@shared_task
def send_email_task(subject: str, message: str, recipient_list: list[str]) -> dict[str, Any]:
    '''Send email asynchronously via Celery.'''
    from django.core.mail import send_mail

    try:
        send_mail(subject, message, None, recipient_list, fail_silently=False)
        return {"success": True, "recipients": recipient_list}
    except Exception as e:
        return {"success": False, "error": str(e)}
""",
    )

    # ── src/apps/api/ ───────────────────────────────────────
    api_dir = apps_dir / "api"
    _write(api_dir / "__init__.py", "")

    _write(
        api_dir / "urls.py",
        """from django.urls import include, path

app_name = "v1"

urlpatterns = [
    path("", include("src.apps.accounts.urls")),
]
""",
    )

    # ── src/templates/ ──────────────────────────────────────
    _write(src_dir / "templates" / ".gitkeep", "")

    # ── src/utils/ ──────────────────────────────────────────
    utils_dir = src_dir / "utils"
    _write(utils_dir / "__init__.py", "")

    _write(
        utils_dir / "helpers.py",
        """import uuid
from typing import Any


def generate_unique_id() -> str:
    '''Generate a unique identifier.'''
    return str(uuid.uuid4())


def truncate_text(text: str, max_length: int = 100) -> str:
    '''Truncate text to a maximum length.'''
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
""",
    )

    # ── tests/ ──────────────────────────────────────────────
    tests_dir = base / "tests"
    _write(tests_dir / "__init__.py", "")

    _write(
        tests_dir / "conftest.py",
        """import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_client(api_client):
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )
    api_client.force_authenticate(user=admin)
    return api_client, admin
""",
    )

    _write(
        tests_dir / "test_health.py",
        """import pytest
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_endpoint(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code == status.HTTP_200_OK
""",
    )

    # ── pytest.ini ──────────────────────────────────────────
    _write(
        base / "pytest.ini",
        """[pytest]
DJANGO_SETTINGS_MODULE = src.config.settings
python_files = tests.py test_*.py *_tests.py
testpaths = tests src
""",
    )

    # ── .gitignore ──────────────────────────────────────────
    _write(
        base / ".gitignore",
        """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.egg
.venv/
venv/

# Django
*.sqlite3
staticfiles/
media/
logs/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
""",
    )

    console.print("[bold green]✓[/] Django API boilerplate generated successfully!")
    _print_summary(base, "Django API")


# ──────────────────────────────────────────────────────────────
#  Flask API Boilerplate
# ──────────────────────────────────────────────────────────────


def generate_flask_api(target_dir: str, project_name: str) -> None:
    """Generate a complete Flask REST API project."""
    base = Path(target_dir)
    src_dir = base / "src"
    project_snake = _to_snake_case(project_name)
    project_pascal = _to_pascal_case(project_name)

    console.print(
        Panel(f"[bold green]Generating Flask API: {project_name}[/]", expand=False)
    )

    # ── pyproject.toml ──────────────────────────────────────
    _write(
        base / "pyproject.toml",
        f"""[project]
name = "{project_snake}"
version = "0.1.0"
description = "Flask REST API - {project_name}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "flask>=3.0.0",
    "flask-sqlalchemy>=3.1.0",
    "flask-migrate>=4.0.0",
    "flask-cors>=4.0.0",
    "flask-jwt-extended>=4.6.0",
    "flask-marshmallow>=0.15.0",
    "marshmallow-sqlalchemy>=0.30.0",
    "marshmallow>=3.21.0",
    "flask-limiter>=3.6.0",
    "flask-mail>=0.9.1",
    "flask-redis>=0.4.0",
    "celery>=5.3.0",
    "redis>=5.0.0",
    "gunicorn>=21.2.0",
    "psycopg2-binary>=2.9.0",
    "python-dotenv>=1.0.0",
    "webargs>=8.4.0",
    "apispec>=6.6.0",
    "apispec-webframeworks>=1.0.0",
    "marshmallow-dataclass>=8.6.0",
    "sentry-sdk>=2.0.0",
    "werkzeug>=3.0.0",
    "pillow>=10.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "factory-boy>=3.3.0",
    "faker>=22.0.0",
    "ruff>=0.11.0",
    "mypy>=1.16.0",
]
""",
    )

    # ── .env.example ────────────────────────────────────────
    _write(
        base / ".env.example",
        f"""# --- Flask Core ---
FLASK_APP=src.app:create_app
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-me-to-a-random-secret-key

# --- Database ---
DATABASE_URL=sqlite:///db.sqlite3
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# --- JWT ---
JWT_SECRET_KEY=change-me-to-a-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7

# --- Redis / Celery ---
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# --- CORS ---
CORS_ORIGINS=http://localhost:3000,http://localhost:8501

# --- Email ---
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@example.com

# --- Sentry ---
SENTRY_DSN=

# --- API ---
API_TITLE="{project_pascal} API"
API_VERSION=v1
""",
    )

    # ── Dockerfile ─────────────────────────────────────────
    _write(
        base / "Dockerfile",
        """FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential libpq-dev curl && \\
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/api/v1/health/ || exit 1

CMD ["gunicorn", "src.app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent"]
""",
    )

    # ── docker-compose.yml ─────────────────────────────────
    _write(
        base / "docker-compose.yml",
        f"""version: "3.9"

services:
  api:
    build: .
    container_name: {project_snake}_api
    command: gunicorn "src.app:create_app()" --bind 0.0.0.0:5000 --reload
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  celery-worker:
    build: .
    container_name: {project_snake}_celery_worker
    command: celery -A src.celery_app worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: {project_snake}_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${{POSTGRES_DB:-{project_snake}}}
      POSTGRES_USER: ${{POSTGRES_USER:-{project_snake}}}
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:-changeme}}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${{POSTGRES_USER:-{project_snake}}}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: {project_snake}_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
""",
    )

    # ── README.md ──────────────────────────────────────────
    _write(
        base / "README.md",
        f"""# {project_pascal} API

Flask REST API for {project_name}.

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
{project_snake}/
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
""",
    )

    # ── src/ ────────────────────────────────────────────────
    _write(src_dir / "__init__.py", "")

    _write(
        src_dir / "config.py",
        f"""import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    '''Base configuration.'''

    SECRET_KEY = os.getenv("SECRET_KEY", "insecure-dev-key-change-in-production")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{{BASE_DIR / 'db.sqlite3'}}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "30"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "7"))
    )

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")

    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RATELIMIT_DEFAULT = "100/hour"
    RATELIMIT_STRATEGY = "fixed-window"

    # API
    API_TITLE = os.getenv("API_TITLE", "{project_pascal} API")
    API_VERSION = os.getenv("API_VERSION", "v1")

    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    UPLOAD_FOLDER = BASE_DIR / "uploads"

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = BASE_DIR / "logs" / "app.log"


class DevelopmentConfig(BaseConfig):
    '''Development configuration.'''

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(BaseConfig):
    '''Production configuration.'''

    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(BaseConfig):
    '''Testing configuration.'''

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = False


config_map = {{
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}}
""",
    )

    _write(
        src_dir / "extensions.py",
        """from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
mail = Mail()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],
    storage_uri="redis://localhost:6379/0",
)
""",
    )

    _write(
        src_dir / "celery_app.py",
        f"""import os

from celery import Celery

celery_app = Celery(
    "{project_snake}",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    beat_schedule={{}},
)


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    print(f"Request: {{self.request!r}}")
""",
    )

    _write(
        src_dir / "app.py",
        f"'''\n"
        f"Flask application factory for {project_name}.\n"
        f"'''\n"
        f"\n"
        f"import logging\n"
        f"import os\n"
        f"from pathlib import Path\n"
        f"\n"
        f"from flask import Flask\n"
        f"\n"
        f"from src.config import config_map\n"
        f"from src.extensions import cors, db, jwt, limiter, ma, mail, migrate\n"
        f"\n"
        f"\n"
        f"def create_app(config_name: str | None = None) -> Flask:\n"
        f'    """Create and configure the Flask application."""\n'
        f'    config_name = config_name or os.getenv("FLASK_ENV", "development")\n'
        f"    app = Flask(__name__)\n"
        f'    app.config.from_object(config_map.get(config_name, config_map["default"]))\n'
        f"\n"
        f"    # --- Initialize Extensions ---\n"
        f"    db.init_app(app)\n"
        f"    migrate.init_app(app, db)\n"
        f"    ma.init_app(app)\n"
        f"    jwt.init_app(app)\n"
        f'    cors.init_app(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)\n'
        f"    mail.init_app(app)\n"
        f"    limiter.init_app(app)\n"
        f"\n"
        f"    # --- Setup Logging ---\n"
        f"    _setup_logging(app)\n"
        f"\n"
        f"    # --- Register Blueprints ---\n"
        f"    _register_blueprints(app)\n"
        f"\n"
        f"    # --- Error Handlers ---\n"
        f"    _register_error_handlers(app)\n"
        f"\n"
        f"    # --- Shell Context ---\n"
        f"    @app.shell_context_processor\n"
        f"    def shell_context():\n"
        f'        return {{"app": app, "db": db}}\n'
        f"\n"
        f"    return app\n"
        f"\n"
        f"\n"
        f"def _setup_logging(app: Flask) -> None:\n"
        f'    """Configure application logging."""\n'
        f'    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))\n'
        f'    log_file = app.config.get("LOG_FILE")\n'
        f"\n"
        f"    handlers = [logging.StreamHandler()]\n"
        f"    if log_file:\n"
        f"        log_path = Path(log_file)\n"
        f"        log_path.parent.mkdir(parents=True, exist_ok=True)\n"
        f"        handlers.append(logging.handlers.RotatingFileHandler(\n"
        f"            log_file, maxBytes=5 * 1024 * 1024, backupCount=5\n"
        f"        ))\n"
        f"\n"
        f"    logging.basicConfig(\n"
        f"        level=log_level,\n"
        f'        format="%(asctime)s %(levelname)s %(name)s: %(message)s",\n'
        f"        handlers=handlers,\n"
        f"    )\n"
        f"\n"
        f"\n"
        f"def _register_blueprints(app: Flask) -> None:\n"
        f'    """Register all API blueprints."""\n'
        f"    from src.routes.health import health_bp\n"
        f"    from src.routes.auth import auth_bp\n"
        f"    from src.routes.users import users_bp\n"
        f"\n"
        f'    app.register_blueprint(health_bp, url_prefix="/api/v1")\n'
        f'    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")\n'
        f'    app.register_blueprint(users_bp, url_prefix="/api/v1/users")\n'
        f"\n"
        f"\n"
        f"def _register_error_handlers(app: Flask) -> None:\n"
        f'    """Register custom error handlers."""\n'
        f"\n"
        f"    @app.errorhandler(400)\n"
        f"    def bad_request(error):\n"
        f'        return {{"success": False, "message": "Bad request.", "errors": str(error)}}, 400\n'
        f"\n"
        f"    @app.errorhandler(401)\n"
        f"    def unauthorized(error):\n"
        f'        return {{"success": False, "message": "Authentication required."}}, 401\n'
        f"\n"
        f"    @app.errorhandler(403)\n"
        f"    def forbidden(error):\n"
        f'        return {{"success": False, "message": "Forbidden."}}, 403\n'
        f"\n"
        f"    @app.errorhandler(404)\n"
        f"    def not_found(error):\n"
        f'        return {{"success": False, "message": "Resource not found."}}, 404\n'
        f"\n"
        f"    @app.errorhandler(405)\n"
        f"    def method_not_allowed(error):\n"
        f'        return {{"success": False, "message": "Method not allowed."}}, 405\n'
        f"\n"
        f"    @app.errorhandler(429)\n"
        f"    def too_many_requests(error):\n"
        f'        return {{"success": False, "message": "Too many requests. Please try again later."}}, 429\n'
        f"\n"
        f"    @app.errorhandler(500)\n"
        f"    def internal_error(error):\n"
        f'        return {{"success": False, "message": "Internal server error."}}, 500\n',
    )

    # ── src/models/ ────────────────────────────────────────
    models_dir = src_dir / "models"
    _write(models_dir / "__init__.py", "")
    _write(
        models_dir / "user.py",
        """import uuid
from datetime import datetime, timezone

from src.extensions import db


class User(db.Model):
    '''User model.'''

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(20), default="")
    bio = db.Column(db.Text, default="")
    avatar = db.Column(db.String(256), default="")
    email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    theme = db.Column(db.String(20), default="light")
    email_notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User {self.email}>"
""",
    )

    _write(
        models_dir / "token_blacklist.py",
        """from datetime import datetime, timezone

from src.extensions import db


class TokenBlacklist(db.Model):
    '''Store blacklisted JWT tokens.'''

    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)
""",
    )

    # ── src/schemas/ ───────────────────────────────────────
    schemas_dir = src_dir / "schemas"
    _write(schemas_dir / "__init__.py", "")
    _write(
        schemas_dir / "user.py",
        """from marshmallow import fields, validate, validates_schema, ValidationError

from src.extensions import ma
from src.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    '''Schema for user serialization.'''

    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)


class UserCreateSchema(ma.Schema):
    '''Schema for user registration.'''

    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    password_confirm = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            raise ValidationError({"password_confirm": "Passwords do not match."})


class UserUpdateSchema(ma.Schema):
    '''Schema for updating user profile.'''

    phone_number = fields.String()
    bio = fields.String()
    avatar = fields.String()
    theme = fields.String(validate=validate.OneOf(["light", "dark"]))
    email_notifications = fields.Boolean()


class LoginSchema(ma.Schema):
    '''Schema for user login.'''

    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class ChangePasswordSchema(ma.Schema):
    '''Schema for password change.'''

    old_password = fields.String(required=True, load_only=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    new_password_confirm = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError({"new_password_confirm": "Passwords do not match."})
""",
    )

    # ── src/services/ ──────────────────────────────────────
    services_dir = src_dir / "services"
    _write(services_dir / "__init__.py", "")
    _write(
        services_dir / "user_service.py",
        """import logging
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions import db
from src.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    '''Service layer for user operations.'''

    @staticmethod
    def create_user(data: dict[str, Any]) -> User:
        '''Create a new user.'''
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        logger.info(f"User created: {user.email}")
        return user

    @staticmethod
    def get_by_id(user_id: str) -> User | None:
        '''Get user by ID.'''
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        '''Get user by email.'''
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        '''Authenticate user by email and password.'''
        user = UserService.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def update_user(user: User, data: dict[str, Any]) -> User:
        '''Update user fields.'''
        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> bool:
        '''Change user password.'''
        if not check_password_hash(user.password_hash, old_password):
            return False
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True
""",
    )

    # ── src/routes/ ────────────────────────────────────────
    routes_dir = src_dir / "routes"
    _write(routes_dir / "__init__.py", "")

    _write(
        routes_dir / "health.py",
        """from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    '''Health check endpoint.'''
    return jsonify({
        "status": "healthy",
        "service": "api",
        "version": "1.0.0",
    })
""",
    )

    _write(
        routes_dir / "auth.py",
        """from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from src.extensions import db, limiter
from src.models.token_blacklist import TokenBlacklist
from src.schemas.user import ChangePasswordSchema, LoginSchema, UserCreateSchema
from src.services.user_service import UserService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5/minute")
def register():
    '''Register a new user.'''
    schema = UserCreateSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    # Check if user already exists
    if UserService.get_by_email(data["email"]):
        return jsonify({"success": False, "errors": {"email": "Email already registered."}}), 409

    if UserService.get_by_email(data["username"]):
        return jsonify({"success": False, "errors": {"username": "Username already taken."}}), 409

    user = UserService.create_user(data)
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "success": True,
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def login():
    '''Authenticate user and return JWT tokens.'''
    schema = LoginSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user = UserService.authenticate(data["email"], data["password"])
    if not user:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "success": True,
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "access_token": access_token,
        "refresh_token": refresh_token,
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    '''Refresh access token.'''
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"success": True, "access_token": access_token})


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    '''Logout user by blacklisting the token.'''
    jti = get_jwt()["jti"]
    token_type = get_jwt()["type"]
    user_id = get_jwt_identity()
    expires = get_jwt()["exp"]

    from datetime import datetime, timezone

    blacklisted = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires_at=datetime.fromtimestamp(expires, tz=timezone.utc),
    )
    db.session.add(blacklisted)
    db.session.commit()

    return jsonify({"success": True, "message": "Successfully logged out."})


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    '''Change current user's password.'''
    schema = ChangePasswordSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    if not UserService.change_password(user, data["old_password"], data["new_password"]):
        return jsonify({"success": False, "errors": {"old_password": "Wrong password."}}), 400

    return jsonify({"success": True, "message": "Password updated successfully."})
""",
    )

    _write(
        routes_dir / "users.py",
        """from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src.schemas.user import UserSchema, UserUpdateSchema
from src.services.user_service import UserService

users_bp = Blueprint("users", __name__)


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    '''Get current user's profile.'''
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    schema = UserSchema()
    return jsonify({"success": True, "data": schema.dump(user)})


@users_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_profile():
    '''Update current user's profile.'''
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    schema = UserUpdateSchema()
    try:
        data = schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user = UserService.update_user(user, data)
    return jsonify({"success": True, "data": UserSchema().dump(user)})
""",
    )

    # ── src/utils/ ──────────────────────────────────────────
    utils_dir = src_dir / "utils"
    _write(utils_dir / "__init__.py", "")
    _write(
        utils_dir / "helpers.py",
        """import uuid
from typing import Any


def generate_id() -> str:
    '''Generate a unique ID.'''
    return str(uuid.uuid4())


def paginate(query, page: int = 1, per_page: int = 25):
    '''Paginate a SQLAlchemy query.'''
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": pagination.items,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }
""",
    )

    # ── tests/ ──────────────────────────────────────────────
    tests_dir = base / "tests"
    _write(tests_dir / "__init__.py", "")
    _write(
        tests_dir / "conftest.py",
        """import pytest
from src.app import create_app
from src.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    '''Create application for testing.'''
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    '''Create test client.'''
    return app.test_client()


@pytest.fixture
def db(app):
    '''Get database instance.'''
    with app.app_context():
        yield _db
        _db.session.rollback()
        _db.drop_all()
        _db.create_all()
""",
    )

    _write(
        tests_dir / "test_health.py",
        """def test_health_check(client):
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
""",
    )

    _write(
        tests_dir / "test_auth.py",
        """def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "user1",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user2",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    assert response.status_code == 409


def test_login_success(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        },
    )
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
""",
    )

    # ── pytest.ini ──────────────────────────────────────────
    _write(
        base / "pytest.ini",
        """[pytest]
testpaths = tests src
python_files = test_*.py *_tests.py
""",
    )

    # ── .gitignore ──────────────────────────────────────────
    _write(
        base / ".gitignore",
        """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.egg
.venv/
venv/

# Flask
*.sqlite3
uploads/
logs/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
""",
    )

    console.print("[bold green]✓[/] Flask API boilerplate generated successfully!")
    _print_summary(base, "Flask API")


# ──────────────────────────────────────────────────────────────
#  Python Frontend (Streamlit) Boilerplate
# ──────────────────────────────────────────────────────────────


def generate_frontend(target_dir: str, project_name: str) -> None:
    """Generate a complete Python frontend using Streamlit."""
    base = Path(target_dir)
    src_dir = base / "src"
    project_snake = _to_snake_case(project_name)
    project_pascal = _to_pascal_case(project_name)

    console.print(
        Panel(
            f"[bold yellow]Generating Python Frontend (Streamlit): {project_name}[/]",
            expand=False,
        )
    )

    # ── pyproject.toml ──────────────────────────────────────
    _write(
        base / "pyproject.toml",
        f"""[project]
name = "{project_snake}"
version = "0.1.0"
description = "Streamlit frontend - {project_name}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "streamlit>=1.35.0",
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
    "pandas>=2.2.0",
    "plotly>=5.20.0",
    "httpx>=0.27.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.2.0",
    "st-pages>=0.4.0",
    "streamlit-option-menu>=0.3.0",
    "streamlit-authenticator>=0.3.0",
    "pillow>=10.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.11.0",
    "mypy>=1.16.0",
]
""",
    )

    # ── .env.example ────────────────────────────────────────
    _write(
        base / ".env.example",
        f"""# --- API Configuration ---
API_BASE_URL=http://localhost:8000/api/v1
API_TIMEOUT=30

# --- Authentication ---
AUTH_TOKEN=

# --- App Configuration ---
APP_NAME={project_pascal}
APP_ICON=🚀
APP_LAYOUT=wide
APP_SIDEBAR_STATE=expanded
""",
    )

    # ── Dockerfile ─────────────────────────────────────────
    _write(
        base / "Dockerfile",
        """FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential curl && \\
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
""",
    )

    # ── docker-compose.yml ─────────────────────────────────
    _write(
        base / "docker-compose.yml",
        f"""version: "3.9"

services:
  frontend:
    build: .
    container_name: {project_snake}_frontend
    command: streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
    volumes:
      - .:/app
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: unless-stopped
""",
    )

    # ── README.md ──────────────────────────────────────────
    _write(
        base / "README.md",
        f"""# {project_pascal} Frontend

Streamlit frontend for {project_name}.

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
{project_snake}/
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
""",
    )

    # ── src/ ────────────────────────────────────────────────
    _write(src_dir / "__init__.py", "")

    _write(
        src_dir / "config.py",
        f"""from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API
    api_base_url: str = "http://localhost:8000/api/v1"
    api_timeout: int = 30

    # Auth
    auth_token: str = ""

    # App
    app_name: str = "{project_pascal}"
    app_icon: str = "🚀"
    app_layout: str = "wide"
    app_sidebar_state: str = "expanded"


settings = Settings()
""",
    )

    _write(
        src_dir / "app.py",
        f"'''\n"
        f"{project_pascal} - Streamlit Frontend Application\n"
        f"'''\n"
        f"\n"
        f"import streamlit as st\n"
        f"\n"
        f"from src.config import settings\n"
        f"\n"
        f"\n"
        f"def initialize_app() -> None:\n"
        f'    """Initialize the Streamlit application."""\n'
        f"    st.set_page_config(\n"
        f"        page_title=settings.app_name,\n"
        f"        page_icon=settings.app_icon,\n"
        f"        layout=settings.app_layout,\n"
        f"        initial_sidebar_state=settings.app_sidebar_state,\n"
        f"    )\n"
        f"\n"
        f"\n"
        f"def main() -> None:\n"
        f'    """Main application entry point."""\n'
        f"    initialize_app()\n"
        f"\n"
        f"    # Initialize session state\n"
        f'    if "authenticated" not in st.session_state:\n'
        f"        st.session_state.authenticated = False\n"
        f'    if "user" not in st.session_state:\n'
        f"        st.session_state.user = None\n"
        f'    if "access_token" not in st.session_state:\n'
        f"        st.session_state.access_token = None\n"
        f"\n"
        f"    # Render sidebar\n"
        f"    from src.components.sidebar import render_sidebar\n"
        f"    render_sidebar()\n"
        f"\n"
        f"    # Page routing\n"
        f"    if not st.session_state.authenticated:\n"
        f"        from src.pages.login import show_login_page\n"
        f"        show_login_page()\n"
        f"    else:\n"
        f'        page = st.session_state.get("page", "Home")\n'
        f'        if page == "Home":\n'
        f"            from src.pages.home import show_home_page\n"
        f"            show_home_page()\n"
        f'        elif page == "Dashboard":\n'
        f"            from src.pages.dashboard import show_dashboard_page\n"
        f"            show_dashboard_page()\n"
        f'        elif page == "Profile":\n'
        f"            from src.pages.profile import show_profile_page\n"
        f"            show_profile_page()\n"
        f"\n"
        f"\n"
        f'if __name__ == "__main__":\n'
        f"    main()\n",
    )

    # ── src/api/ ────────────────────────────────────────────
    api_dir = src_dir / "api"
    _write(api_dir / "__init__.py", "")
    _write(
        api_dir / "client.py",
        "'''\n"
        "API client for communicating with backend services.\n"
        "'''\n"
        "\n"
        "from typing import Any\n"
        "\n"
        "import httpx\n"
        "import streamlit as st\n"
        "\n"
        "from src.config import settings\n"
        "\n"
        "\n"
        "class APIClient:\n"
        '    """HTTP client for backend API communication."""\n'
        "\n"
        "    def __init__(self, base_url: str | None = None, token: str | None = None):\n"
        '        self.base_url = (base_url or settings.api_base_url).rstrip("/")\n'
        "        self.token = token or settings.auth_token\n"
        "\n"
        "    def _get_headers(self) -> dict[str, str]:\n"
        "        headers = {\n"
        '            "Content-Type": "application/json",\n'
        '            "Accept": "application/json",\n'
        "        }\n"
        "        if self.token:\n"
        '            headers["Authorization"] = f"Bearer {self.token}"\n'
        "        return headers\n"
        "\n"
        "    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:\n"
        "        try:\n"
        "            data = response.json()\n"
        "        except Exception:\n"
        '            data = {"message": response.text}\n'
        "\n"
        "        if response.is_error:\n"
        '            error_msg = data.get("message", data.get("detail", "An error occurred"))\n'
        '            st.error(f"API Error ({response.status_code}): {error_msg}")\n'
        '            return {"success": False, "error": error_msg}\n'
        "\n"
        '        return {"success": True, "data": data}\n'
        "\n"
        "    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:\n"
        '        """Send GET request."""\n'
        "        try:\n"
        "            with httpx.Client(timeout=settings.api_timeout) as client:\n"
        "                response = client.get(\n"
        '                    f"{self.base_url}{endpoint}",\n'
        "                    headers=self._get_headers(),\n"
        "                    params=params,\n"
        "                )\n"
        "                return self._handle_response(response)\n"
        "        except httpx.RequestError as e:\n"
        '            st.error(f"Connection error: {e}")\n'
        '            return {"success": False, "error": str(e)}\n'
        "\n"
        "    def post(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:\n"
        '        """Send POST request."""\n'
        "        try:\n"
        "            with httpx.Client(timeout=settings.api_timeout) as client:\n"
        "                response = client.post(\n"
        '                    f"{self.base_url}{endpoint}",\n'
        "                    headers=self._get_headers(),\n"
        "                    json=data,\n"
        "                )\n"
        "                return self._handle_response(response)\n"
        "        except httpx.RequestError as e:\n"
        '            st.error(f"Connection error: {e}")\n'
        '            return {"success": False, "error": str(e)}\n'
        "\n"
        "    def put(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:\n"
        '        """Send PUT request."""\n'
        "        try:\n"
        "            with httpx.Client(timeout=settings.api_timeout) as client:\n"
        "                response = client.put(\n"
        '                    f"{self.base_url}{endpoint}",\n'
        "                    headers=self._get_headers(),\n"
        "                    json=data,\n"
        "                )\n"
        "                return self._handle_response(response)\n"
        "        except httpx.RequestError as e:\n"
        '            st.error(f"Connection error: {e}")\n'
        '            return {"success": False, "error": str(e)}\n'
        "\n"
        "    def patch(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:\n"
        '        """Send PATCH request."""\n'
        "        try:\n"
        "            with httpx.Client(timeout=settings.api_timeout) as client:\n"
        "                response = client.patch(\n"
        '                    f"{self.base_url}{endpoint}",\n'
        "                    headers=self._get_headers(),\n"
        "                    json=data,\n"
        "                )\n"
        "                return self._handle_response(response)\n"
        "        except httpx.RequestError as e:\n"
        '            st.error(f"Connection error: {e}")\n'
        '            return {"success": False, "error": str(e)}\n'
        "\n"
        "    def delete(self, endpoint: str) -> dict[str, Any]:\n"
        '        """Send DELETE request."""\n'
        "        try:\n"
        "            with httpx.Client(timeout=settings.api_timeout) as client:\n"
        "                response = client.delete(\n"
        '                    f"{self.base_url}{endpoint}",\n'
        "                    headers=self._get_headers(),\n"
        "                )\n"
        "                return self._handle_response(response)\n"
        "        except httpx.RequestError as e:\n"
        '            st.error(f"Connection error: {e}")\n'
        '            return {"success": False, "error": str(e)}\n',
    )

    # ── src/components/ ─────────────────────────────────────
    components_dir = src_dir / "components"
    _write(components_dir / "__init__.py", "")
    _write(
        components_dir / "sidebar.py",
        """import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar() -> None:
    '''Render the sidebar navigation menu.'''
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Logo", use_column_width=True)
        st.markdown("---")

        if st.session_state.authenticated:
            # Show navigation for authenticated users
            selected = option_menu(
                menu_title="Navigation",
                options=["Home", "Dashboard", "Profile"],
                icons=["house", "bar-chart", "person"],
                menu_icon="cast",
                default_index=0,
            )
            st.session_state.page = selected

            st.markdown("---")
            st.markdown(f"**User:** {st.session_state.user.get('username', 'N/A')}")

            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.access_token = None
                st.rerun()
        else:
            st.markdown("### Welcome!")
            st.markdown("Please log in to continue.")
""",
    )

    _write(
        components_dir / "cards.py",
        """import streamlit as st


def info_card(title: str, value: str, delta: str | None = None) -> None:
    '''Display an info card with title, value, and optional delta.'''
    with st.container(border=True):
        st.metric(label=title, value=value, delta=delta)


def status_badge(status: str) -> str:
    '''Return an emoji badge for a given status.'''
    badges = {
        "active": "🟢",
        "inactive": "🔴",
        "pending": "🟡",
        "completed": "✅",
        "failed": "❌",
    }
    return badges.get(status.lower(), "⚪")
""",
    )

    # ── src/pages/ ──────────────────────────────────────────
    pages_dir = src_dir / "pages"
    _write(pages_dir / "__init__.py", "")

    _write(
        pages_dir / "login.py",
        """import streamlit as st

from src.api.client import APIClient


def show_login_page() -> None:
    '''Display the login/registration page.'''
    st.markdown("# 🔐 Welcome")
    st.markdown("Please login or create an account.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    client = APIClient()
                    result = client.post("/auth/login/", {"email": email, "password": password})
                    if result["success"]:
                        data = result["data"]
                        st.session_state.authenticated = True
                        st.session_state.user = data.get("user", {})
                        st.session_state.access_token = data.get("access_token", "")
                        st.success("Login successful!")
                        st.rerun()

    with tab2:
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            reg_email = st.text_input("Email", placeholder="your@email.com")
            reg_password = st.text_input("Password", type="password")
            reg_password_confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register", use_container_width=True)

            if submitted:
                if not all([username, reg_email, reg_password, reg_password_confirm]):
                    st.error("Please fill in all fields.")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match.")
                elif len(reg_password) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    client = APIClient()
                    result = client.post("/auth/register/", {
                        "username": username,
                        "email": reg_email,
                        "password": reg_password,
                        "password_confirm": reg_password_confirm,
                    })
                    if result["success"]:
                        data = result["data"]
                        st.session_state.authenticated = True
                        st.session_state.user = data.get("user", {})
                        st.session_state.access_token = data.get("access_token", "")
                        st.success("Registration successful!")
                        st.rerun()
""",
    )

    _write(
        pages_dir / "home.py",
        """import streamlit as st

from src.api.client import APIClient


def show_home_page() -> None:
    '''Display the home page.'''
    st.markdown("# 🏠 Home")
    st.markdown("Welcome to the application!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", "1,234", "+5.2%")
    with col2:
        st.metric("Active Sessions", "456", "-2.1%")
    with col3:
        st.metric("API Calls", "12.5K", "+12.3%")

    st.markdown("---")
    st.markdown("## Recent Activity")

    # Fetch data from API
    client = APIClient(token=st.session_state.access_token)
    result = client.get("/health/")
    if result["success"]:
        st.json(result["data"])
    else:
        st.info("Connect to an API backend to see live data.")
""",
    )

    _write(
        pages_dir / "dashboard.py",
        """import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_dashboard_page() -> None:
    '''Display the dashboard page with charts and analytics.'''
    st.markdown("# 📊 Dashboard")
    st.markdown("Analytics and insights.")

    # Sample data
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
        "Users": [100 + i * 5 + (i % 7) * 10 for i in range(30)],
        "Revenue": [1000 + i * 50 + (i % 5) * 200 for i in range(30)],
    })

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df, x="Date", y="Users", title="User Growth")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(df, x="Date", y="Revenue", title="Revenue")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## Data Table")
    st.dataframe(df, use_container_width=True)
""",
    )

    _write(
        pages_dir / "profile.py",
        """import streamlit as st

from src.api.client import APIClient


def show_profile_page() -> None:
    '''Display the user profile page.'''
    st.markdown("# 👤 Profile")
    st.markdown("Manage your account settings.")

    client = APIClient(token=st.session_state.access_token)
    result = client.get("/users/me/")

    if result["success"]:
        user_data = result["data"].get("data", result["data"])

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown(f"**{user_data.get('username', 'N/A')}**")
            st.markdown(f"*{user_data.get('email', 'N/A')}*")

        with col2:
            with st.form("profile_form"):
                phone = st.text_input("Phone", value=user_data.get("phone_number", ""))
                bio = st.text_area("Bio", value=user_data.get("bio", ""))
                theme = st.selectbox(
                    "Theme",
                    options=["light", "dark"],
                    index=0 if user_data.get("theme", "light") == "light" else 1,
                )
                email_notifications = st.checkbox(
                    "Email Notifications",
                    value=user_data.get("email_notifications", True),
                )
                submitted = st.form_submit_button("Update Profile", use_container_width=True)

                if submitted:
                    update_result = client.patch("/users/me/", {
                        "phone_number": phone,
                        "bio": bio,
                        "theme": theme,
                        "email_notifications": email_notifications,
                    })
                    if update_result["success"]:
                        st.success("Profile updated!")
                        st.rerun()
    else:
        st.warning("Could not load profile. Make sure the API is running.")
""",
    )

    # ── src/auth/ ───────────────────────────────────────────
    auth_dir = src_dir / "auth"
    _write(auth_dir / "__init__.py", "")
    _write(
        auth_dir / "login.py",
        "'''\n"
        "Authentication utilities.\n"
        "'''\n"
        "\n"
        "import streamlit as st\n"
        "\n"
        "\n"
        "def require_authentication() -> bool:\n"
        '    """Check if user is authenticated, redirect if not."""\n'
        '    if not st.session_state.get("authenticated", False):\n'
        '        st.warning("Please log in to access this page.")\n'
        '        st.session_state.page = "Login"\n'
        "        st.rerun()\n"
        "        return False\n"
        "    return True\n"
        "\n"
        "\n"
        "def logout() -> None:\n"
        '    """Clear session state and log out."""\n'
        "    st.session_state.authenticated = False\n"
        "    st.session_state.user = None\n"
        "    st.session_state.access_token = None\n"
        "    st.rerun()\n",
    )

    # ── src/utils/ ──────────────────────────────────────────
    utils_dir = src_dir / "utils"
    _write(utils_dir / "__init__.py", "")
    _write(
        utils_dir / "helpers.py",
        """import json
from datetime import datetime
from typing import Any

import streamlit as st


def format_date(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    '''Format a date string.'''
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime(fmt)
    except (ValueError, TypeError):
        return date_str


def display_json(data: dict[str, Any]) -> None:
    '''Display JSON data in a formatted way.'''
    st.code(json.dumps(data, indent=2, default=str), language="json")


def show_toast(message: str, icon: str = "ℹ️") -> None:
    '''Show a toast notification.'''
    st.toast(f"{icon} {message}")
""",
    )

    # ── tests/ ──────────────────────────────────────────────
    tests_dir = base / "tests"
    _write(tests_dir / "__init__.py", "")
    _write(
        tests_dir / "test_config.py",
        """from src.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.app_name is not None
    assert settings.api_base_url is not None
""",
    )

    # ── .streamlit/ ─────────────────────────────────────────
    streamlit_dir = base / ".streamlit"
    _write(
        streamlit_dir / "config.toml",
        """[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333F"
font = "sans serif"

[server]
maxUploadSize = 10
enableXsrfProtection = true
enableCORS = true

[browser]
gatherUsageStats = false
""",
    )

    # ── .gitignore ──────────────────────────────────────────
    _write(
        base / ".gitignore",
        """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
*.egg
.venv/
venv/

# Streamlit
.streamlit/secrets.toml

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
""",
    )

    console.print(
        "[bold green]✓[/] Python Frontend (Streamlit) boilerplate generated successfully!"
    )
    _print_summary(base, "Python Frontend (Streamlit)")


# ──────────────────────────────────────────────────────────────
#  CLI Commands
# ──────────────────────────────────────────────────────────────


@app.command()
def django(
    target: Annotated[
        str, Argument(help="Target directory path (e.g., services/my-api)")
    ],
    name: Annotated[
        str | None,
        Option("--name", "-n", help="Project name (defaults to directory name)"),
    ] = None,
) -> None:
    """Generate a Django REST API project."""
    project_name = name or Path(target).name
    _validate_project_name(project_name)
    generate_django_api(target, project_name)


@app.command()
def flask(
    target: Annotated[
        str, Argument(help="Target directory path (e.g., services/my-api)")
    ],
    name: Annotated[
        str | None,
        Option("--name", "-n", help="Project name (defaults to directory name)"),
    ] = None,
) -> None:
    """Generate a Flask REST API project."""
    project_name = name or Path(target).name
    _validate_project_name(project_name)
    generate_flask_api(target, project_name)


@app.command()
def frontend(
    target: Annotated[
        str, Argument(help="Target directory path (e.g., apps/my-frontend)")
    ],
    name: Annotated[
        str | None,
        Option("--name", "-n", help="Project name (defaults to directory name)"),
    ] = None,
) -> None:
    """Generate a Python frontend (Streamlit) project."""
    project_name = name or Path(target).name
    _validate_project_name(project_name)
    generate_frontend(target, project_name)


@app.command()
def list_templates() -> None:
    """List available boilerplate templates."""
    table = Table(title="Available Boilerplate Templates")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Command", style="green")
    table.add_row(
        "django",
        "Django REST API with JWT auth, Celery, DRF, Swagger",
        "boilerplate django <path>",
    )
    table.add_row(
        "flask",
        "Flask REST API with JWT auth, Celery, SQLAlchemy",
        "boilerplate flask <path>",
    )
    table.add_row(
        "frontend",
        "Streamlit frontend with auth, API client, charts",
        "boilerplate frontend <path>",
    )
    console.print(table)


@app.callback(invoke_without_command=True)
def boilerplate_callback(ctx: typer.Context) -> None:
    """Monorepo Boilerplate Generator - Create production-ready Django, Flask, and Python frontend projects."""
    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                "[bold cyan]Monorepo Boilerplate Generator[/]\n\n"
                "Generate production-ready boilerplate code for:\n"
                "  * [green]Django[/] REST API with JWT, Celery, DRF, Swagger\n"
                "  * [green]Flask[/] REST API with JWT, Celery, SQLAlchemy\n"
                "  * [green]Streamlit[/] Frontend with auth, API client, charts\n\n"
                "Usage:\n"
                "  boilerplate django services/my-api\n"
                "  boilerplate flask services/my-api\n"
                "  boilerplate frontend apps/my-frontend\n"
                "  boilerplate list-templates\n",
                border_style="cyan",
            )
        )


if __name__ == "__main__":
    app()
