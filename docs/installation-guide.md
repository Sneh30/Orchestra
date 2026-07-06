# Installation Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 16 for non-Docker local development
- Tavily API key for live search
- OpenAI or Anthropic API key for live model execution

## Docker Installation

Copy environment configuration:

```bash
cp .env.example .env
```

Set credentials in `.env`:

```bash
API_KEY=local-dev-key
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
TAVILY_API_KEY=...
LLM_PROVIDER=openai
```

Start the stack:

```bash
docker compose up --build
```

Verify:

```bash
curl http://localhost:8000/health
```

Open:

```text
http://localhost:8000/docs
```

## Local Python Installation

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install:

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev]"
```

Run deterministic mode:

```bash
export LLM_PROVIDER=deterministic
export DATABASE_URL=postgresql+asyncpg://research:research@localhost:5432/research_orchestrator
uvicorn research_orchestrator.main:app --reload --app-dir backend
```

## Database Setup Without Docker

Create database:

```bash
createdb research_orchestrator
```

Apply schema:

```bash
psql postgresql://research:research@localhost:5432/research_orchestrator -f database/migrations/001_init.sql
```

## Verification

Run tests:

```bash
pytest
```

Run quality checks:

```bash
ruff check backend tests
mypy backend
```

