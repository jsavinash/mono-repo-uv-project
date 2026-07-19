# Mono Repo UV Project

This repository now follows a more template-like Python monorepo structure with a modern developer workflow:

- A React/Vite web shell in [apps/web](apps/web)
- A FastAPI-backed API service in [services/api_gateway](services/api_gateway)
- Shared contracts and packages under [libs/shared](libs/shared) and [packages](packages)
- A streamlined entrypoint, test setup, and pre-commit hooks for everyday development

## Quick start

### Python entrypoint

```bash
python main.py
```

### Web app

```bash
cd apps/web
npm install
npm run dev
```

### API service

```bash
cd services/api_gateway
python -m uvicorn app:app --reload --port 8000
```

### Quality checks

```bash
python -m pytest
ruff check .
ruff format --check .
```

## Project layout

```text
apps/            Web application shell
services/        Service-oriented Python apps
libs/            Shared libraries
packages/        Reusable Python packages
tests/           Repository-level smoke tests
```

## Development notes

- Use [pre-commit-config.yaml](pre-commit-config.yaml) for formatting and lint hooks.
- Copy [.env.example](.env.example) to `.env` for local environment values.
- The root [pyproject.toml](pyproject.toml) is the single place to manage dependencies and tooling.