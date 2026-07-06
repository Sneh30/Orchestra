# Section 5 - API Design

## REST Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service health check |
| POST | `/v1/research-runs` | Create a research run and optionally execute in background |
| GET | `/v1/research-runs` | List research runs |
| GET | `/v1/research-runs/{run_id}` | Retrieve run status and metadata |
| POST | `/v1/research-runs/{run_id}/execute` | Execute an existing run synchronously |
| GET | `/v1/research-runs/{run_id}/report` | Retrieve final report |
| GET | `/v1/research-runs/{run_id}/sources` | Retrieve source list for a run |
| POST | `/v1/evaluations/report` | Evaluate an arbitrary report payload |
| POST | `/v1/evaluations/runs/{run_id}` | Evaluate a persisted run report |

## Request Models

### ResearchRunRequest

```json
{
  "query": "What evidence supports enterprise adoption of AI agents in regulated industries?",
  "objective": "Produce a board-ready diligence memo.",
  "constraints": {
    "audience": "founders",
    "prefer_primary_sources": true
  },
  "user_id": "founder-123",
  "depth": "advanced",
  "max_sources": 12,
  "min_confidence": 0.72,
  "execute_async": true
}
```

Validation:

- `query`: required, 10 to 4000 characters.
- `depth`: `basic` or `advanced`.
- `max_sources`: 3 to 50.
- `min_confidence`: 0 to 1.

### EvaluationRequest

```json
{
  "report": {
    "executive_summary": "Summary",
    "markdown": "# Report",
    "confidence_score": 0.83,
    "citations": [{"id": "S01", "title": "Source", "url": "https://example.edu"}],
    "structured_output": {
      "key_findings": [{"claim": "Finding", "citation_id": "S01"}],
      "risks": [],
      "source_coverage": {"source_count": 1}
    }
  }
}
```

## Response Models

### ResearchRunResponse

```json
{
  "id": "f9d3943b-6a61-4397-8f44-84b79c05b5a1",
  "user_id": "founder-123",
  "query": "What evidence supports enterprise adoption of AI agents in regulated industries?",
  "objective": "Produce a board-ready diligence memo.",
  "constraints": {"audience": "founders"},
  "status": "queued",
  "depth": "advanced",
  "max_sources": 12,
  "min_confidence": 0.72,
  "confidence_score": null,
  "failure_reason": null,
  "created_at": "2026-06-02T12:00:00Z",
  "updated_at": "2026-06-02T12:00:00Z",
  "completed_at": null
}
```

### ReportResponse

```json
{
  "id": "77a5164c-5d66-44da-aaf2-ffda3fb789e6",
  "run_id": "f9d3943b-6a61-4397-8f44-84b79c05b5a1",
  "title": "Verified Research Report: Enterprise AI Agents",
  "executive_summary": "The report synthesizes verified evidence...",
  "markdown": "# Verified Research Report...",
  "structured_output": {
    "key_findings": [],
    "confidence": {},
    "risks": [],
    "open_questions": [],
    "source_coverage": {},
    "citations": []
  },
  "confidence_score": 0.81,
  "citation_count": 12,
  "created_at": "2026-06-02T12:04:00Z"
}
```

## Error Handling

All application errors use a consistent JSON envelope:

```json
{
  "code": "not_found",
  "message": "research_run '...' was not found.",
  "details": {
    "resource": "research_run",
    "identifier": "..."
  }
}
```

Error categories:

- `401 unauthorized`: missing or invalid `X-API-Key`.
- `404 not_found`: requested run or report does not exist.
- `422 validation_error`: invalid request fields.
- `500 internal_error`: unexpected runtime failure.

## OpenAPI Specification

The complete OpenAPI artifact is `docs/api/openapi.yaml`.

## Example Flow

Create a run:

```bash
curl -X POST http://localhost:8000/v1/research-runs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-dev-key" \
  -d '{"query":"What evidence supports enterprise adoption of AI agents in regulated industries?","execute_async":true}'
```

Fetch report:

```bash
curl http://localhost:8000/v1/research-runs/{run_id}/report \
  -H "X-API-Key: local-dev-key"
```

Evaluate report:

```bash
curl -X POST http://localhost:8000/v1/evaluations/runs/{run_id} \
  -H "X-API-Key: local-dev-key"
```

