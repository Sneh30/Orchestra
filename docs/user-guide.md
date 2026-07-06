# User Guide

## Creating a Research Run

Send a question to `/v1/research-runs`.

Example:

```json
{
  "query": "What evidence supports enterprise adoption of AI agents in regulated industries?",
  "objective": "Produce a board-ready diligence memo.",
  "constraints": {
    "audience": "founders",
    "prefer_primary_sources": true,
    "include_contradictory_evidence": true
  },
  "depth": "advanced",
  "max_sources": 12,
  "min_confidence": 0.72,
  "execute_async": true
}
```

## Reading Status

Use:

```text
GET /v1/research-runs/{run_id}
```

Statuses:

- `queued`: run accepted.
- `running`: graph is executing.
- `completed`: report is available.
- `failed`: run failed and includes a failure reason.

## Reading a Report

Use:

```text
GET /v1/research-runs/{run_id}/report
```

The report includes:

- title
- executive summary
- markdown report
- structured output
- confidence score
- citation count

## Reading Sources

Use:

```text
GET /v1/research-runs/{run_id}/sources
```

Each source includes:

- URL
- title
- publisher
- snippet
- credibility score
- metadata

## Interpreting Confidence

Confidence is a calibrated project score from 0 to 1:

- 0.85 to 1.00: strong source coverage and high evidence confidence.
- 0.70 to 0.84: useful report with some residual uncertainty.
- 0.45 to 0.69: partial answer that needs review.
- below 0.45: weak or insufficient evidence.

Confidence is not a truth guarantee. It is a review signal based on source quality, evidence support, and coverage.

## Interpreting Citations

Citation IDs appear as:

```text
[S01]
```

The source list maps `S01` to a source title, URL, publisher, and credibility score.

## Evaluating Reports

Use:

```text
POST /v1/evaluations/runs/{run_id}
```

Metrics:

- hallucination resistance
- citation accuracy
- report quality

