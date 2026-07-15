# API Documentation

## Authentication

When `API_KEY` is configured, all endpoints require:

```text
X-API-Key: <configured-api-key>
```

## Content Type

Requests and responses use JSON:

```text
Content-Type: application/json
```

## Endpoint Reference

### Health

```http
GET /health
```

Response:

```json
{"status": "ok"}
```

### Create Research Run

```http
POST /v1/research-runs
```

Request:

```json
{
  "query": "What evidence supports enterprise adoption of AI agents in regulated industries?",
  "objective": "Produce a board-ready diligence memo.",
  "constraints": {"audience": "founders"},
  "depth": "advanced",
  "max_sources": 12,
  "min_confidence": 0.72,
  "execute_async": true
}
```

Response: `202 Accepted` with a `ResearchRun` object.

### List Research Runs

```http
GET /v1/research-runs?limit=25&offset=0
```

Response: array of `ResearchRun` objects.

### Get Research Run

```http
GET /v1/research-runs/{run_id}
```

Response: `ResearchRun`.

### Execute Research Run

```http
POST /v1/research-runs/{run_id}/execute
```

Response:

```json
{
  "run_id": "uuid",
  "status": "completed",
  "confidence_score": 0.81,
  "report": {}
}
```

### Get Report

```http
GET /v1/research-runs/{run_id}/report
```

Response: `Report`.

### Get Sources

```http
GET /v1/research-runs/{run_id}/sources
```

Response: array of `Source` objects.

### Evaluate Report Payload

```http
POST /v1/evaluations/report
```

Response: array of evaluation metrics.

### Evaluate Persisted Run

```http
POST /v1/evaluations/runs/{run_id}
```

Response: persisted evaluation metric references.

## OpenAPI

Machine-readable OpenAPI spec:

```text
docs/api/openapi.yaml
```

Runtime OpenAPI JSON:

```text
GET /openapi.json
```

