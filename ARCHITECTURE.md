# Python Starter Kit - Architecture Documentation

## Overview

This document provides a deep dive into the architecture and design decisions of the Python Starter Kit monorepo.

## Table of Contents

1. [Monorepo Architecture](#monorepo-architecture)
2. [Build System Design](#build-system-design)
3. [Quality Gates](#quality-gates)
4. [Dependency Management](#dependency-management)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Security](#security)
7. [Best Practices](#best-practices)

## Monorepo Architecture

### High-Level Structure

```
python-starter-kit/
├── Apps (planned applications)
│   ├── django-api/              # Django REST API (not yet created)
│   ├── flask-api/               # Flask REST API (not yet created)
│   ├── frontend/                # Streamlit Frontend (not yet created)
│   └── web/                     # React Web (boilerplate - Node.js)
│
├── Shared Libraries
│   └── libs/shared/             # Common DTOs, models, utilities (Pydantic)
│
├── Educational Resources
│   └── python-programming/      # Python learning materials
│
├── Root Configuration
│   ├── pyproject.toml           # uv workspace config
│   ├── Makefile                 # Development automation
│   ├── .pre-commit-config.yaml  # Pre-commit hooks
│   └── .githooks/               # Custom git hooks
│
├── Infrastructure
│   ├── docker-compose.yml       # Service orchestration (Redis + templates)
│   ├── .github/workflows/       # CI/CD pipelines
│   └── docs/                    # MkDocs documentation
│
└── Configuration
    └── config/dependencies.toml # Centralized dependency version catalog
```

### Workspace Strategy

The monorepo uses **uv workspace** to manage Python packages:

#### 1. **Current Workspace Members**

```
[tool.uv.workspace]
members = [
    "libs/shared",
]
```

#### 2. **Shared Libraries**
- **Purpose**: Common code consumed by apps and packages
- **Benefits**:
  - Centralized utility functions
  - Shared contracts/DTOs
  - Reusable across all modules

### Why uv Workspace?

| Aspect | Traditional | uv Workspace | This Project |
|--------|-------------|--------------|--------------|
| **Dependency Resolution** | ❌ Manual | ✅ Automatic | ✅ Yes |
| **Lock File** | ❌ Per project | ✅ Single lock | ✅ uv.lock |
| **Isolation** | ❌ Global | ✅ Per package | ✅ Yes |
| **Build Speed** | ⚠️ Slow | ✅ Fast | ✅ Optimized |
| **Complexity** | ✅ Simple | ⚠️ Moderate | ✅ Managed |

## Build System Design

### Makefile Task Categories

The project uses a Makefile for development workflow automation:

```makefile
# Quality tasks
make lint          # Ruff lint check
make format        # Ruff auto-format
make typecheck     # MyPy type checking
make test          # Run all tests
make quality-check # All quality checks combined

# Infrastructure
make docker-up     # Start services
make docker-down   # Stop all services

# CI pipeline
make ci            # Lint + format + test
```

### Task Responsibilities

| Task Category | Purpose | Tools |
|--------------|---------|-------|
| **Quality** | Code quality enforcement | Ruff, MyPy |
| **Testing** | Test execution | Pytest, pytest-cov |
| **Build** | Package building | uv build, hatchling |
| **Infra** | Docker orchestration | Docker Compose |
| **Dev** | Development workflow | uv, pre-commit |

## Quality Gates

### Multi-Layer Quality Enforcement

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Pre-Commit Hook (Fast Feedback)                    │
│ ├── Branch protection                                       │
│ ├── Staged file validation                                  │
│ ├── Commit message validation                               │
│ ├── Secret scanning                                         │
│ ├── Ruff formatting check                                   │
│ ├── Ruff linting check                                      │
│ ├── MyPy type check                                         │
│ └── Unit tests (quick)                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Pre-Push Hook (Comprehensive)                      │
│ ├── Full test suite with coverage                           │
│ ├── All quality checks                                      │
│ ├── Commit history inspection                               │
│ └── Dependency vulnerability scan                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: CI/CD Pipeline (GitHub Actions)                    │
│ ├── Lint & Format job                                       │
│ ├── Test job (multiple Python versions)                     │
│ ├── Security audit job                                      │
│ ├── Docker build job                                        │
│ └── Package build job                                       │
└─────────────────────────────────────────────────────────────┘
```

### Quality Thresholds

| Metric | Threshold | Enforcement |
|--------|-----------|-------------|
| **Line Coverage** | 80% | pytest-cov |
| **Ruff Lint Issues** | 0 | Fails build |
| **Ruff Format Issues** | 0 | Fails build |
| **MyPy Errors** | 0 | Fails build |
| **Pre-commit Hooks** | All pass | Blocks commit |
| **Dependency Vulns** | 0 Critical/High | pip-audit |

## Dependency Management

### Centralized Dependency Catalog

All dependencies are managed via a centralized version catalog at `config/dependencies.toml` — the single source of truth for dependency versions across the monorepo:

```toml
# config/dependencies.toml
[versions]
django = ">=5.0,<6.0"
flask = ">=3.0.0"
pydantic = ">=2.6.0"
ruff = ">=0.11.0"
mypy = ">=1.16.0"
```

### Dependency Groups (Root pyproject.toml)

| Group | Purpose | Key Dependencies |
|-------|---------|------------------|
| **dev** | Development | poethepoet, pre-commit, commitizen |
| **test** | Testing | pytest, pytest-cov, pytest-randomly, pytest-timeout |
| **lint** | Linting | ruff |
| **type_check** | Type checking | mypy |
| **security** | Security audit | pip-audit |
| **docs** | Documentation | mkdocs-material, mkdocstrings |
| **licenses** | License compliance | pip-licenses-cli |

### UV Workspace Configuration

```toml
[tool.uv.workspace]
members = [
    "libs/shared",
]
```

### How to Override Dependencies

Individual projects can override the central catalog versions in their own `pyproject.toml`:

```bash
# Add a new dependency
uv add requests

# Add a dev dependency
uv add --dev pytest-mock
```

uv's workspace resolution automatically handles version selection — project-local declarations take precedence over the central catalog.

### Makefile Commands

```bash
make dep-catalog       # Show the centralized dependency catalog
make dep-list          # List all workspace dependencies
make dep-outdated      # Show outdated dependencies
make dep-upgrade-all   # Upgrade all deps and update lockfile
make dep-verify        # Verify no dependency conflicts
make dep-audit         # Audit dependencies for vulnerabilities
make dep-licenses      # Check dependency licenses
```

### Dependency Flow

```
config/dependencies.toml (version catalog)
    ↓ (documented versions)
Root pyproject.toml (workspace + dependency groups)
    ↓ (uv workspace resolution)
Shared Libraries (libs/shared/)
    ↓ (install dependency)
Apps (apps/*) — when created
    ↓ (runtime)
Production
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
jobs:
  lint:           # Parallel - Code quality checks
  test:           # Matrix - 3 Python versions
  security:       # Parallel - Vulnerability scan
  docker:         # Depends on lint + test
  package:        # Depends on lint + test
```

### Pipeline Stages

1. **Lint & Format** (Parallel)
   - Ruff lint check
   - Ruff format check
   - MyPy type check

2. **Test** (Matrix: py3.10, 3.11, 3.12)
   - Root tests
   - Upload test results

3. **Security Audit** (Parallel)
   - pip-audit vulnerability scan

4. **Docker Build** (Depends on lint + test)
   - Build service images

5. **Package Build** (Depends on lint + test)
   - Build all packages
   - Upload build artifacts

## Security

### Static Analysis Security

1. **Ruff Security**
   - Hardcoded passwords
   - SQL injection patterns
   - Insecure crypto

2. **MyPy Security**
   - Type safety enforcement
   - Unsafe type casts

3. **Pre-commit Security**
   - Secret scanning (detect-secrets)
   - Private key detection
   - AWS credential scanning
   - Custom high-confidence pattern matching (API keys, tokens)

### Dependency Security

```yaml
- name: Check for known vulnerabilities
  run: uv run pip-audit
```

- **pip-audit**: Scans for known vulnerabilities
- **UV lock file**: Pinned dependencies
- **Reports**: CI artifacts

### Secrets Management

```bash
# .env file (git-ignored)
DB_PASSWORD=secret
API_KEY=secret
```

- **Never commit secrets**
- **Use environment variables**
- **Git-ignored .env files**

## Best Practices

### 1. **Branching Strategy**

```
main (protected)
  └── develop (integration branch)
       ├── feature/your-feature
       ├── fix/issue-description
       └── refactor/improvement
```

### 2. **Commit Convention**

```
feat(shared): add user DTO
fix(config): resolve dependency conflict
docs(readme): update quick start
```

### 3. **Code Review Process**

1. All checks must pass (CI)
2. At least one approval
3. No unresolved conversations
4. Squash and merge

### 4. **Testing Strategy**

- **Unit Tests**: Fast, isolated, mocked
- **Integration Tests**: Real dependencies, slower
- **Coverage**: Minimum 80% line coverage

### 5. **Documentation**

- **README**: Project overview, quick start
- **CONTRIBUTING**: Contribution guidelines
- **ARCHITECTURE**: This document
- **Code Comments**: Complex logic only

## Troubleshooting

### Common Issues

#### Build Failures

```bash
# Clean and rebuild
make clean
make install

# Clear caches
rm -rf .pytest_cache .ruff_cache .mypy_cache
uv lock
```

#### Hook Issues

```bash
# Reinstall hooks
bash scripts/install-hooks.sh

# Verify
git config --get core.hooksPath
```

#### Test Failures

```bash
# Verbose output
uv run pytest -v --tb=long

# Specific test
uv run pytest tests/test_*.py -k "test_name"
```

## Future Improvements

### Planned Enhancements

1. **Application Creation**
   - Django REST API with JWT auth
   - Flask REST API with blueprint pattern
   - Streamlit frontend dashboard

2. **Remote Build Cache**
   - Shared cache across team
   - Faster CI builds

3. **Kubernetes Deployment**
   - Helm charts
   - Docker Compose for K8s

## Conclusion

This architecture provides:

- ✅ **Scalability**: Easy to add new services
- ✅ **Maintainability**: Consistent build configuration
- ✅ **Quality**: Multi-layer quality gates
- ✅ **Security**: Vulnerability scanning
- ✅ **Developer Experience**: Fast feedback loops

The monorepo structure with uv workspace offers centralized management with isolated builds.