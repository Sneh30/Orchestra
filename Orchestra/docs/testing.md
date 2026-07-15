# Section 10 - Testing

## Test Layers

### Unit Tests

Files:

- `tests/unit/test_scoring.py`
- `tests/unit/test_evaluation_metrics.py`
- `tests/unit/test_graph.py`

Coverage:

- source credibility scoring
- report confidence scoring
- hallucination scoring
- citation accuracy scoring
- report quality scoring
- LangGraph report production with fake search tool and deterministic model provider

### Integration Tests

File:

- `tests/integration/test_api.py`

Coverage:

- FastAPI app creation
- health endpoint
- generated OpenAPI contract contains research endpoints

### End-to-End Contract Tests

File:

- `tests/e2e/test_research_workflow_contract.py`

Coverage:

- initial state contract for representative research questions
- graph input defaults
- loop guard initialization

## Test Commands

```bash
pytest
```

With coverage:

```bash
pytest --cov=research_orchestrator --cov-report=term-missing
```

Lint:

```bash
ruff check backend tests
```

Type check:

```bash
mypy backend
```

## Deterministic Test Mode

Set:

```bash
export LLM_PROVIDER=deterministic
```

Deterministic mode avoids external LLM and search dependencies in CI while preserving graph behavior.

## QA Acceptance Criteria

- Unit tests pass.
- Integration tests pass.
- Graph contract test produces a report.
- OpenAPI spec exposes all expected endpoints.
- Database migration applies cleanly to PostgreSQL.
- CI runs lint, type check, schema application, and tests.

