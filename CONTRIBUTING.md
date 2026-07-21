# Contributing to Python Starter Kit

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Install hooks: `bash scripts/install-hooks.sh` or `uv run pre-commit install`
4. Make changes
5. Run quality checks: `make test-all`
6. Commit with conventional commit message: `git commit -m "feat(scope): description"`
7. Push and create Pull Request

## Development Workflow

### Setup

```bash
# Clone and install
git clone <repo-url>
cd python-starter-kit
make install

# Install git hooks (custom + pre-commit)
bash scripts/install-hooks.sh
uv run pre-commit install

# Set up environment
cp .env.example .env
```

### Making Changes

```bash
# Create feature branch
git checkout -b feat/my-feature

# Make your changes...

# Run quality checks
make lint          # Ruff lint
make format        # Ruff format
make typecheck     # MyPy type check
make test          # Run tests
make test-cov      # Tests with coverage

# Commit (hooks run automatically)
git add .
git commit -m "feat(scope): description"

# Push (pre-push hooks run)
git push origin feat/my-feature
```

## Code Quality Standards

### Python Style Guide

- **Formatter**: Ruff (line length 88, double quotes)
- **Linter**: Ruff with selected rulesets
- **Type Checker**: MyPy (strict mode)

### Naming Conventions

- **Packages**: `snake_case` (e.g., `data_structure`)
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Apps**: `kebab-case` (e.g., `django-api`)

### Testing Requirements

- **Framework**: pytest
- **Coverage**: Minimum 80% line coverage
- **Test Location**: `tests/` directory in each module
- **File Pattern**: `test_*.py` or `*_test.py`

## Commit Convention

### Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Code style (formatting) |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `build` | Build system |
| `ci` | CI/CD changes |
| `chore` | Maintenance |
| `revert` | Revert changes |

### Scopes

| Scope | Module |
|-------|--------|
| `shared` | Shared libraries |
| `web` | React web app |
| `config` | Configuration |
| `deps` | Dependencies |
| `docs` | Documentation |
| `build` | Build configuration |
| `ci` | CI/CD pipeline |
| `infra` | Docker/K8s infrastructure |
| `hooks` | Git hooks |
| `educational` | Educational resources |

### Examples

```
feat(shared): add user DTO with validation
fix(config): resolve dependency version conflict
docs(readme): update quick start instructions
refactor(hooks): improve secret scanning performance
test(shared): add unit tests for number_utils
ci: add dependency vulnerability scanning job
```

## Pull Request Process

### Before Submitting

1. **Run full test suite**: `make test-all`
2. **Check coverage**: `make test-cov` (aim for 80%+)
3. **Verify lint**: `make lint` and `make format-check`
4. **Type check**: `make typecheck`
5. **Review your changes**: `git diff --stat`

### PR Requirements

- [ ] All CI checks passing
- [ ] Test coverage maintained or improved
- [ ] Code follows style guide
- [ ] Commit messages follow convention
- [ ] Documentation updated if needed
- [ ] No merge conflicts

### Review Process

1. Self-review your PR first
2. Request review from maintainers
3. Address all feedback
4. Maintainers approve
5. Squash and merge

## Branch Strategy

```
main ─────────────── (production, protected)
  └── develop ────── (integration branch, protected)
       ├── feat/*    (new features)
       ├── fix/*     (bug fixes)
       ├── refactor/* (code improvements)
       ├── docs/*    (documentation)
       └── chore/*   (maintenance)
```

### Branch Naming

- `feat/my-feature` - New features
- `fix/issue-description` - Bug fixes
- `refactor/component-name` - Refactoring
- `docs/update-readme` - Documentation
- `chore/update-deps` - Maintenance

## Project Structure

```
python-starter-kit/
├── apps/                    # Application projects
│   ├── django-api/          # Django REST API (planned)
│   ├── flask-api/           # Flask REST API (planned)
│   ├── frontend/            # Streamlit frontend (planned)
│   └── web/                 # React web app (boilerplate)
├── libs/                    # Shared libraries
│   └── shared/              # Common contracts and utilities
├── educational-resources/   # Learning materials
├── tests/                   # Root-level tests
├── docs/                    # MkDocs documentation
├── config/                  # Centralized dependency catalog
├── .githooks/               # Custom git hooks
├── .github/workflows/       # CI/CD pipelines
├── pyproject.toml           # Root workspace config
├── Makefile                 # Development automation
└── docker-compose.yml       # Service orchestration
```

## Dependency Management

### Centralized Version Catalog

All dependency versions are managed centrally in `config/dependencies.toml` — the single source of truth. This file catalogs every dependency used across the monorepo, organized by ecosystem (Django, Flask, FastAPI, testing, linting, etc.).

### How to Add/Override Dependencies

```bash
# Add a new dependency
uv add requests

# Add a dev dependency
uv add --dev pytest-mock

# Add a workspace-level dependency group
uv add --group test pytest-xdist

# View all dependencies
make dep-list

# Check for outdated dependencies
make dep-outdated

# Audit for vulnerabilities
make dep-audit
```

### Dependency Groups

| Group | Purpose | Install Command |
|-------|---------|-----------------|
| `test` | Testing | `uv sync --group test` |
| `lint` | Linting | `uv sync --group lint` |
| `type_check` | Type checking | `uv sync --group type_check` |
| `docs` | Documentation | `uv sync --group docs` |
| `dev` | Development | `uv sync --group dev` |
| `security` | Security audit | `uv sync --group security` |

## Environment Setup

### Required Tools

- **Python**: 3.10+
- **uv**: Latest (package manager)
- **Docker**: Optional (for containerized development)
- **Git**: Latest

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Ruff
- MyPy
- Pre-commit
- Docker

Settings (.vscode/settings.json):
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "ruff.path": ["uv", "run", "ruff"],
  "mypy.runUsingActiveInterpreter": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  }
}
```

#### PyCharm

- Enable Ruff as formatter
- Configure MyPy for type checking
- Enable automatic imports optimization

## Testing Guidelines

### Writing Tests

```python
# Unit test example
def test_user_creation():
    """Test user creation with valid data."""
    # Given
    user_data = {"name": "John", "email": "john@example.com"}
    
    # When
    result = create_user(user_data)
    
    # Then
    assert result.id is not None
    assert result.name == "John"

# Integration test example
def test_api_health_check(client):
    """Test health check endpoint returns 200."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json
```

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
└── test_main.py             # Root-level tests
```

### Coverage Requirements

- **Minimum**: 80% line coverage
- **Excluded**: `__init__.py`, `setup.py`, `manage.py`
- **Report**: `make test-cov` generates HTML report

## Documentation

### Writing Documentation

- Use type hints for all functions
- Add docstrings for public APIs
- Keep README up to date
- Document architectural decisions

### Docstring Style

```python
def calculate_discount(price: float, percent: float) -> float:
    """Calculate discounted price.
    
    Args:
        price: Original price
        percent: Discount percentage (0-100)
        
    Returns:
        Discounted price
        
    Raises:
        ValueError: If percent is not between 0 and 100
    """
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be between 0 and 100")
    return price * (1 - percent / 100)
```

## Need Help?

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: ARCHITECTURE.md, README.md

## License

By contributing, you agree that your contributions will be licensed under the MIT License.