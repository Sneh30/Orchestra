# Section 9 - Evaluation Framework

## Evaluation Metrics

The evaluation framework is implemented in `backend/research_orchestrator/evaluation/metrics.py`.

Metrics:

- Hallucination resistance.
- Citation accuracy.
- Report quality.

## Hallucination Scoring

Definition: percentage of key findings that are backed by a valid citation.

Scoring:

```text
score = 1 - unsupported_findings / total_findings
```

A finding is unsupported when its `citation_id` is missing or marked `uncited`.

## Citation Accuracy Scoring

Definition: percentage of findings whose citation IDs exist in the report citation list.

Scoring:

```text
score = valid_cited_findings / total_findings
```

Invalid citation IDs apply an additional penalty because they create false traceability.

## Report Quality Scoring

Definition: checklist-based completeness score for production report structure.

Checks:

- executive summary exists
- markdown body exists
- key findings exist
- risks field exists
- source coverage exists
- confidence score is calibrated from 0 to 1

## Benchmark Datasets

Benchmark questions are defined in `backend/research_orchestrator/evaluation/datasets.py`.

Included benchmark categories:

- Enterprise AI agents in regulated industries.
- Founder diligence for managed vector databases.
- Journalistic verification of carbon removal announcements.

Each benchmark includes:

- question ID
- question text
- expected source types
- quality bar

## Automated Evaluation Pipeline

CLI entrypoint:

```bash
research-evaluate path/to/report.json
```

Programmatic use:

```python
from research_orchestrator.evaluation.metrics import aggregate_evaluation

results = aggregate_evaluation(report_payload)
```

API use:

```bash
curl -X POST http://localhost:8000/v1/evaluations/report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: local-dev-key" \
  -d '{"report": {...}}'
```

Persisted run evaluation:

```bash
curl -X POST http://localhost:8000/v1/evaluations/runs/{run_id} \
  -H "X-API-Key: local-dev-key"
```

## Production Quality Bar

Reports are considered portfolio-grade when:

- hallucination resistance is at least 0.85
- citation accuracy is at least 0.90
- report quality is at least 0.85
- confidence score is below threshold when source coverage is weak
- rejected evidence is not used in final synthesis

