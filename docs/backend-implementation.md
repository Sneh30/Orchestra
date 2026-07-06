# Section 7 - Backend Implementation

## FastAPI Application

The FastAPI application is defined in `backend/research_orchestrator/main.py`.

Implemented capabilities:

- API metadata and OpenAPI generation.
- CORS configuration from settings.
- Optional API key dependency.
- Structured exception handlers.
- Health route.
- Research run routes.
- Report and source routes.
- Evaluation routes.
- Prometheus `/metrics` endpoint.

## Models

### API Models

File: `backend/research_orchestrator/api/schemas.py`

Models:

- `ResearchRunRequest`
- `ResearchRunResponse`
- `ReportResponse`
- `SourceResponse`
- `EvaluationRequest`
- `EvaluationResponse`
- `ErrorResponse`

### Database Models

File: `backend/research_orchestrator/database/models.py`

Models:

- `ResearchRun`
- `Source`
- `Evidence`
- `Report`
- `AgentEvent`
- `EvaluationResult`

## Services

### ResearchService

File: `backend/research_orchestrator/services/research_service.py`

Responsibilities:

- Create research runs.
- Build initial graph state.
- Invoke LangGraph asynchronously.
- Persist graph results.
- Mark failures with reason.
- Retrieve and list runs.

### ReportService

File: `backend/research_orchestrator/services/report_service.py`

Responsibilities:

- Retrieve final report for a run.
- Retrieve sources for a run.

### EvaluationService

File: `backend/research_orchestrator/services/evaluation_service.py`

Responsibilities:

- Score arbitrary report payloads.
- Score persisted run reports.
- Persist evaluation results.

## Controllers

Controller logic is implemented as FastAPI routers:

- `research.py`: create, list, retrieve, and execute runs.
- `reports.py`: retrieve reports and sources.
- `evaluations.py`: evaluate reports and persisted runs.
- `health.py`: health check.

## Dependency Injection

File: `backend/research_orchestrator/api/deps.py`

Injected dependencies:

- `Settings`
- `AsyncSession`
- `ResearchService`
- `ReportService`
- `EvaluationService`

The dependency layer keeps route handlers thin and makes tests easier to override.

## Configuration System

File: `backend/research_orchestrator/core/config.py`

Configuration is environment-driven through Pydantic Settings:

- `APP_ENV`
- `LOG_LEVEL`
- `API_KEY`
- `DATABASE_URL`
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

## Error Handling

File: `backend/research_orchestrator/api/errors.py`

Application errors are translated into JSON payloads with `code`, `message`, and `details`. Unexpected exceptions are returned as `internal_error`.

## Logging

File: `backend/research_orchestrator/core/logging.py`

Structured JSON logs are configured with `structlog`, including timestamp and log level.

