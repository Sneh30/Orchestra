# Section 1 - Product Foundation

## Vision

Multi-Agent Research Orchestrator turns high-stakes research questions into verified, citation-backed research reports by coordinating specialized AI agents through a governed LangGraph workflow. The product vision is to become the trusted research engine for operators who need fast synthesis without accepting black-box hallucination risk.

The core promise is: ask a complex question, receive a structured report that shows what was found, which sources support it, how confident the system is, and where uncertainty remains.

## Problem Statement

Founders, analysts, consultants, researchers, and journalists routinely face questions that require source discovery, evidence extraction, corroboration, contradiction checks, and synthesis. Single-pass LLM workflows fail this job because they combine too many cognitive tasks into one prompt, hide intermediate reasoning, and often produce polished prose before evidence quality is known.

The resulting pain is measurable:

- Research takes too long when performed manually.
- LLM-generated reports often lack reliable citations.
- Teams cannot inspect source coverage or evidence quality.
- Decision-makers need confidence calibration, not just fluent summaries.
- Knowledge workers need repeatable workflows that preserve traceability.

## User Personas

### Startup Founder

Needs rapid market, customer, competitor, and regulatory research before strategy meetings, investor calls, and product bets. Values speed, clarity, and decision relevance. Tolerates some uncertainty if it is clearly labeled.

### Consultant

Needs polished, defensible research outputs for client work. Values citations, structured findings, and repeatable workflows. Needs to explain methodology to skeptical clients.

### Analyst

Needs reliable synthesis across filings, datasets, news, and expert material. Values source quality, confidence scoring, and evidence traceability.

### Researcher

Needs literature-style source discovery and careful claim separation. Values precise citations, uncertainty tracking, and reproducibility.

### Journalist

Needs fast background research, claim checks, and contradiction discovery. Values primary sources, source provenance, and flagged weak claims.

## User Stories

- As a founder, I want to ask a market diligence question and receive a cited report so I can make an investor-ready argument.
- As a consultant, I want claims separated from evidence so I can defend recommendations in client review.
- As an analyst, I want confidence scores per report and evidence item so I can decide what requires manual review.
- As a researcher, I want source tracking so I can inspect the origin of each synthesized claim.
- As a journalist, I want contradictory sources surfaced so I do not publish a one-sided account.
- As a technical evaluator, I want to inspect the agent workflow so I can assess whether this is more than prompt wrapping.
- As a platform owner, I want durable run history so reports, sources, and events can be audited after generation.

## Jobs To Be Done

- When I am evaluating a strategic question, help me gather credible sources, extract evidence, and synthesize a decision-ready report.
- When I need to trust AI-generated research, show me citations, source quality, rejected evidence, and confidence scoring.
- When a claim is weak or contested, identify it before it reaches the final report.
- When I need repeatable research operations, preserve the intermediate workflow state, source list, evidence, and agent events.
- When I am being interviewed or evaluated, demonstrate production-grade AI systems thinking through a real multi-agent architecture.

## Business Value

The product creates value by reducing research cycle time while increasing confidence and auditability. It is positioned as infrastructure for expert workflows rather than a generic chatbot.

For users:

- Faster time-to-insight.
- Better source coverage.
- Clear evidence provenance.
- Lower hallucination risk.
- Structured outputs that can feed briefs, dashboards, memos, and client deliverables.

For a startup:

- Strong wedge into research-heavy professional workflows.
- Usage-based pricing aligned to research runs and source depth.
- Expansion from individual analysts to teams through shared report history and quality controls.
- Differentiation through verification, not just synthesis.

## Success Metrics

### Product Metrics

- Research run completion rate: at least 95 percent outside provider outages.
- Median time to first completed report: under 3 minutes for 12-source runs.
- User-rated report usefulness: at least 4.2 out of 5.
- Manual source rework rate: under 25 percent of reports.
- Percentage of reports with at least 8 unique source URLs for advanced mode.

### AI Quality Metrics

- Citation accuracy score: at least 0.90 on benchmark reports.
- Hallucination resistance score: at least 0.85 on benchmark reports.
- Verified evidence ratio: at least 0.60 for answerable questions.
- Contradiction surfacing rate: tracked on adversarial benchmark questions.
- Confidence calibration: reports below evidence threshold should fail or request another loop.

### Engineering Metrics

- API p95 latency for run creation: under 500 ms.
- Research graph execution failure rate: under 5 percent excluding missing credentials.
- Test coverage across scoring, graph contract, API health, and evaluation metrics.
- Database migrations reproducible from a clean PostgreSQL instance.
- CI passes lint, type checking, schema application, and tests.

## Functional Requirements

- Accept complex research questions through a REST API.
- Persist research run metadata, status, parameters, and completion state.
- Generate search queries optimized for primary and contradictory sources.
- Retrieve web results through Tavily.
- Extract atomic evidence items from source content.
- Verify extracted evidence and label support levels.
- Reject insufficient or contradictory evidence from final synthesis.
- Produce markdown research reports with bracketed citation IDs.
- Produce structured JSON output for key findings, risks, confidence, open questions, source coverage, and citations.
- Track raw sources, evidence items, reports, evaluations, and agent events in PostgreSQL.
- Calculate confidence scores for sources, evidence, and reports.
- Route the LangGraph workflow through additional source collection when confidence is below threshold.
- Prevent infinite graph loops with a maximum iteration setting.
- Expose report retrieval, source retrieval, run listing, run execution, and evaluation endpoints.
- Provide deterministic test mode without external API keys.
- Emit Prometheus metrics for operational monitoring.

## Non-Functional Requirements

- Reliability: failed runs must be marked failed with a failure reason.
- Observability: graph execution events must be persisted and metrics exported.
- Security: API key protection must be supported for deployed environments.
- Auditability: every final claim must map to a source citation or be excluded.
- Configurability: model provider, model names, thresholds, graph iterations, and source counts must be environment-driven.
- Portability: Docker Compose must run the service and PostgreSQL locally.
- Maintainability: service, API, database, agent, and evaluation boundaries must remain separate.
- Testability: deterministic mode must support tests without external providers.
- Extensibility: additional search tools, rerankers, LLM providers, and evaluation metrics must be attachable without rewriting the graph.

## Risks

- Search API coverage may miss critical sources for niche questions.
- LLM extraction quality may vary across long, noisy source content.
- Source credibility scoring can be gamed if it relies only on domain heuristics.
- Confidence scores can create false precision if not calibrated against benchmark datasets.
- Background execution in a single API process is acceptable locally but should be replaced by a worker queue for heavy production throughput.
- Provider outages can interrupt graph execution.
- Some high-stakes domains require expert human review regardless of confidence score.

## Assumptions

- Users value transparent evidence workflows over purely conversational answers.
- Tavily provides sufficient initial search coverage for portfolio-grade research workflows.
- OpenAI and Anthropic models are both useful depending on extraction, verification, and synthesis preferences.
- PostgreSQL is the durable system of record for runs, sources, evidence, reports, and evaluations.
- Deterministic mode is required for CI, tests, demos, and offline portfolio review.
- Confidence scoring is a decision aid, not a guarantee of truth.

