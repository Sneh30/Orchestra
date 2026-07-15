# Developer Guide

## Development Workflow

1. Install dependencies with `python -m pip install ".[dev]"`.
2. Use deterministic provider for repeatable local tests.
3. Run `pytest` before changing graph behavior.
4. Keep API contracts in `docs/api/openapi.yaml` aligned with route changes.
5. Keep prompts in `agents/prompts.py` versioned and explicit.

## Adding a New Agent

1. Add state fields in `agents/state.py`.
2. Add prompt text in `agents/prompts.py`.
3. Implement the node in `agents/nodes.py`.
4. Wire the node in `agents/graph.py`.
5. Add unit or graph contract tests.
6. Persist any new durable artifacts through repository methods.

## Adding a New Tool

1. Create a tool adapter with a narrow method signature.
2. Normalize output into typed dictionaries or Pydantic models.
3. Inject the tool through `build_research_graph`.
4. Add deterministic behavior for CI.
5. Add tests that use a fake tool implementation.

## Adding a New Evaluation Metric

1. Add a function returning `MetricResult` in `evaluation/metrics.py`.
2. Add it to `aggregate_evaluation`.
3. Add a unit test.
4. Persist metric output through `EvaluationService`.

## Database Changes

1. Add a new migration under `database/migrations`.
2. Update SQLAlchemy models in `database/models.py`.
3. Update repositories where query behavior changes.
4. Update docs in `docs/database-design.md`.
5. Run the migration against a fresh PostgreSQL database.

## Coding Standards

- Keep routes thin.
- Keep graph nodes deterministic where possible.
- Keep provider-specific code behind provider adapters.
- Preserve source and evidence traceability.
- Avoid hiding research decisions inside unstructured prose.
- Favor structured JSON outputs for agent-to-agent communication.

## Debugging Graph Runs

Inspect:

- `research_runs.status`
- `research_runs.failure_reason`
- `agent_events`
- `sources`
- `evidence`
- `reports.structured_output`

The most useful debugging query:

```sql
SELECT agent_name, event_type, status, latency_ms, error, created_at
FROM agent_events
WHERE run_id = '<run-id>'
ORDER BY created_at;
```

