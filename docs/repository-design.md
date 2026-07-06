# Section 3 - Repository Design

## Complete Folder Tree

```text
.
├── .env.example
├── .github
│   └── workflows
│       └── ci.yml
├── Dockerfile
├── README.md
├── backend
│   └── research_orchestrator
│       ├── __init__.py
│       ├── agents
│       │   ├── __init__.py
│       │   ├── graph.py
│       │   ├── nodes.py
│       │   ├── prompts.py
│       │   ├── providers.py
│       │   ├── scoring.py
│       │   ├── state.py
│       │   └── tools.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── deps.py
│       │   ├── errors.py
│       │   ├── routes
│       │   │   ├── __init__.py
│       │   │   ├── evaluations.py
│       │   │   ├── health.py
│       │   │   ├── reports.py
│       │   │   └── research.py
│       │   └── schemas.py
│       ├── core
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── exceptions.py
│       │   ├── logging.py
│       │   └── security.py
│       ├── database
│       │   ├── __init__.py
│       │   ├── migrations
│       │   ├── models.py
│       │   ├── repositories.py
│       │   └── session.py
│       ├── evaluation
│       │   ├── __init__.py
│       │   ├── datasets.py
│       │   ├── metrics.py
│       │   └── runner.py
│       ├── main.py
│       └── services
│           ├── __init__.py
│           ├── evaluation_service.py
│           ├── report_service.py
│           ├── research_service.py
│           └── telemetry.py
├── database
│   ├── migrations
│   │   └── 001_init.sql
│   └── schema.sql
├── docker-compose.yml
├── docs
│   ├── ai-layer.md
│   ├── api
│   │   └── openapi.yaml
│   ├── api-documentation.md
│   ├── api-design.md
│   ├── architecture.md
│   ├── backend-implementation.md
│   ├── database-design.md
│   ├── developer-guide.md
│   ├── evaluation-framework.md
│   ├── infrastructure.md
│   ├── installation-guide.md
│   ├── interview-prep.md
│   ├── langgraph-design.md
│   ├── portfolio-assets.md
│   ├── product-foundation.md
│   ├── project-review.md
│   ├── repository-design.md
│   ├── testing.md
│   └── user-guide.md
├── evaluation
│   └── benchmarks
├── infrastructure
│   ├── monitoring
│   │   └── prometheus.yml
│   └── nginx
│       └── default.conf
├── pyproject.toml
└── tests
    ├── e2e
    │   └── test_research_workflow_contract.py
    ├── integration
    │   └── test_api.py
    └── unit
        ├── test_evaluation_metrics.py
        ├── test_graph.py
        └── test_scoring.py
```

## Design Rationale

The repository separates production concerns by ownership boundary:

- `agents` owns AI workflow behavior.
- `api` owns HTTP contracts.
- `services` owns application use cases.
- `database` owns persistence.
- `evaluation` owns quality measurement.
- `docs` owns product, architecture, implementation, and portfolio artifacts.
- `infrastructure` owns deployment-adjacent configuration.
- `tests` owns verification at multiple levels.

This structure makes the project reviewable by AI engineers, backend engineers, CTOs, product leaders, and recruiters because each discipline can inspect the part it cares about without decoding one monolithic file.
