# ─── Python Monorepo Makefile ─────────────────────────────────
# Development workflow automation for Django API, Flask API & Streamlit Frontend
# ─────────────────────────────────────────────────────────────

.PHONY: help install clean lint format typecheck test test-all \
        django-install django-migrate django-run django-test \
        flask-install flask-run flask-test \
        frontend-install frontend-run frontend-test \
        docker-up docker-down docker-build \
        setup ci docs

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

help: ## Show this help
	@printf '\n%s%s%s\n' $(CYAN) 'Usage: make <target>' $(RESET)
	@printf '%s' '───────────────────────────────────────'
	@printf '\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-25s$(RESET) %s\n", $$1, $$2}'

# ─── Installation ──────────────────────────────────────────────

install: ## Install all dependencies (uv sync)
	uv sync --all-workspace

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	rm -rf build dist *.egg-info

# ─── Code Quality ──────────────────────────────────────────────

lint: ## Lint all Python files with Ruff
	uv run ruff check .

lint-fix: ## Fix lint issues automatically
	uv run ruff check --fix .

format: ## Format all Python files with Ruff
	uv run ruff format .

format-check: ## Check formatting without changes
	uv run ruff format --check .

typecheck: ## Type check with mypy
	uv run mypy .

# ─── Testing ──────────────────────────────────────────────────

test: ## Run all tests
	uv run pytest -v

test-cov: ## Run tests with coverage
	uv run pytest --cov=apps --cov-report=term-missing --cov-report=html

test-all: test-cov lint format-check typecheck ## Run full test suite

# ─── Django API ────────────────────────────────────────────────

django-install: ## Install Django API dependencies
	cd apps/django-api && uv sync

django-migrate: ## Run Django migrations
	cd apps/django-api && python manage.py migrate

django-makemigrations: ## Create Django migrations
	cd apps/django-api && python manage.py makemigrations

django-run: ## Run Django development server
	cd apps/django-api && python manage.py runserver 0.0.0.0:8000

django-shell: ## Django shell
	cd apps/django-api && python manage.py shell

django-createsuperuser: ## Create Django superuser
	cd apps/django-api && python manage.py createsuperuser

django-test: ## Run Django tests
	cd apps/django-api && uv run pytest -v

django-collectstatic: ## Collect Django static files
	cd apps/django-api && python manage.py collectstatic --noinput

# ─── Flask API ──────────────────────────────────────────────

flask-install: ## Install Flask API dependencies
	cd apps/flask-api && uv sync

flask-run: ## Run Flask development server
	cd apps/flask-api && flask run --host=0.0.0.0 --port=5000 --reload

flask-shell: ## Flask shell
	cd apps/flask-api && flask shell

flask-db-init: ## Initialize Flask database
	cd apps/flask-api && flask db init

flask-db-migrate: ## Create Flask database migration
	cd apps/flask-api && flask db migrate -m "auto migration"

flask-db-upgrade: ## Apply Flask database migrations
	cd apps/flask-api && flask db upgrade

flask-test: ## Run Flask tests
	cd apps/flask-api && uv run pytest -v

# ─── Streamlit Frontend ────────────────────────────────────────

frontend-install: ## Install frontend dependencies
	cd apps/frontend && uv sync

frontend-run: ## Run Streamlit frontend
	cd apps/frontend && streamlit run src/app.py --server.port=8501

frontend-test: ## Run frontend tests
	cd apps/frontend && uv run pytest -v

# ─── Docker ────────────────────────────────────────────────────

docker-build: ## Build all Docker images
	docker-compose build

docker-up: ## Start all services
	docker-compose up -d

docker-up-logs: ## Start all services with logs
	docker-compose up

docker-down: ## Stop all services
	docker-compose down

docker-down-volumes: ## Stop services and remove volumes
	docker-compose down -v

docker-logs: ## View all service logs
	docker-compose logs -f

docker-logs-django: ## View Django API logs
	docker-compose logs -f django-api

docker-logs-flask: ## View Flask API logs
	docker-compose logs -f flask-api

docker-logs-frontend: ## View Frontend logs
	docker-compose logs -f frontend

docker-clean: ## Remove all containers, networks, volumes
	docker-compose down -v --rmi all --remove-orphans

# ─── Development ──────────────────────────────────────────────

setup: install django-migrate flask-db-upgrade ## Full project setup

dev: ## Run all services locally (requires 3 terminals)
	@echo "$(YELLOW)Run these in separate terminals:$(RESET)"
	@echo "$(GREEN)  make django-run$(RESET)    → http://localhost:8000"
	@echo "$(GREEN)  make flask-run$(RESET)     → http://localhost:5000"
	@echo "$(GREEN)  make frontend-run$(RESET)  → http://localhost:8501"

# ─── Documentation ────────────────────────────────────────────

docs-serve: ## Serve MkDocs documentation
	uv run mkdocs serve

docs-build: ## Build MkDocs documentation
	uv run mkdocs build

# ─── CI ──────────────────────────────────────────────────────

ci: lint format-check test ## CI pipeline (lint + test)

# ─── Utilities ──────────────────────────────────────────────

tree: ## Show project tree structure
	@find . -maxdepth 4 -not -path './.git/*' -not -path './.venv/*' \
		-not -path './__pycache__/*' -not -path './.pytest_cache/*' \
		-not -path './.ruff_cache/*' -not -path './.mypy_cache/*' \
		-not -path './node_modules/*' -not -path './*.egg-info/*' \
		-not -path './build/*' -not -path './dist/*' \
		| sort | head -120

bump-patch: ## Bump patch version
	uv run commitizen bump --patch

bump-minor: ## Bump minor version
	uv run commitizen bump --minor

bump-major: ## Bump major version
	uv run commitizen bump --major
