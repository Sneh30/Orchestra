# Section 11 - Infrastructure

## Dockerfile

The Dockerfile builds a Python 3.11 application image, installs production and development dependencies, copies the backend package, exposes port 8000, and launches Uvicorn.

File: `Dockerfile`

## Docker Compose

File: `docker-compose.yml`

Services:

- `api`: FastAPI application.
- `postgres`: PostgreSQL 16 with schema initialization.
- `prometheus`: metrics scraper.

Volumes:

- `postgres_data`: durable local PostgreSQL data.

## Environment Variables

Defined in `.env.example`:

- `APP_ENV`
- `LOG_LEVEL`
- `API_KEY`
- `DATABASE_URL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `TAVILY_API_KEY`
- `LLM_PROVIDER`
- `OPENAI_MODEL`
- `ANTHROPIC_MODEL`
- `MAX_GRAPH_ITERATIONS`
- `DEFAULT_MAX_SOURCES`
- `DEFAULT_MIN_CONFIDENCE`
- `REQUEST_TIMEOUT_SECONDS`

## Deployment Setup

Local production-like deployment:

```bash
cp .env.example .env
docker compose up --build
```

The API is available at:

```text
http://localhost:8000
```

Prometheus is available at:

```text
http://localhost:9090
```

## GitHub Actions

File: `.github/workflows/ci.yml`

CI jobs:

- provision PostgreSQL
- install dependencies
- apply schema
- run Ruff
- run mypy
- run pytest with coverage

## Logging

Structured JSON logging is configured through `structlog` in `backend/research_orchestrator/core/logging.py`.

Logged events include:

- research run completion
- research run failure
- confidence score
- run ID
- error reason

## Monitoring

Prometheus metrics:

- `research_runs_created_total`
- `research_runs_completed_total`
- `research_run_latency_seconds`

Metrics endpoint:

```text
/metrics
```

Prometheus config:

```text
infrastructure/monitoring/prometheus.yml
```

## Operational Runbook

Health check:

```bash
curl http://localhost:8000/health
```

Inspect database:

```bash
docker compose exec postgres psql -U research -d research_orchestrator
```

View API logs:

```bash
docker compose logs -f api
```

Rebuild:

```bash
docker compose up --build
```

