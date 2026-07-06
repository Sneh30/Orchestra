# Section 13 - Portfolio Assets

## Resume Bullet Points

- Built a production-grade multi-agent research orchestration system using Python, FastAPI, LangGraph, PostgreSQL, Tavily, OpenAI, and Anthropic to generate verified research reports with citations and confidence scoring.
- Designed a stateful LangGraph workflow with specialized Search, Extraction, Verification, Synthesis, and Critique agents, including confidence-gated loops and loop-prevention safeguards.
- Implemented durable source tracking, evidence persistence, report storage, agent event logs, and automated evaluation metrics for hallucination resistance, citation accuracy, and report quality.
- Developed a Dockerized backend with PostgreSQL migrations, Prometheus metrics, API key security, structured logging, CI checks, unit tests, integration tests, and OpenAPI documentation.
- Created a portfolio-ready AI systems project demonstrating agent architecture, backend engineering, evaluation methodology, product thinking, and startup-grade technical documentation.

## LinkedIn Project Description

I built a Multi-Agent Research Orchestrator: a production-grade AI system that coordinates specialized LangGraph agents to produce verified research reports with citations, source tracking, confidence scoring, and structured JSON output.

The system decomposes research into Search, Extraction, Verification, Synthesis, and Critique agents. It persists every run, source, evidence item, report, evaluation result, and agent event in PostgreSQL. The backend is FastAPI, containerized with Docker, instrumented with Prometheus metrics, and tested with deterministic AI provider mode.

The goal was to build a flagship AI Systems Builder portfolio project that goes beyond prompt demos: explicit graph state, verification loops, confidence scoring, source provenance, evaluation metrics, and production-style service boundaries.

## GitHub Project Description

Production-grade multi-agent research system using LangGraph, FastAPI, PostgreSQL, Tavily, OpenAI, and Anthropic. Produces verified research reports with citations, source tracking, confidence scoring, structured output, evaluation metrics, Docker deployment, CI, and full architecture documentation.

## Architecture Explanation

The system treats research as an auditable workflow instead of a single LLM call. A FastAPI service accepts research questions and stores run metadata in PostgreSQL. The Research Service creates an initial typed LangGraph state and invokes a compiled graph.

The graph runs five specialized agents:

- Search Agent creates source strategies and retrieves source candidates.
- Extraction Agent extracts atomic evidence from each source.
- Verification Agent labels evidence support and rejects weak claims.
- Synthesis Agent creates a cited markdown report and structured output.
- Critique Agent checks confidence and routes back to search when coverage is weak.

PostgreSQL stores run state, sources, evidence, final reports, events, and evaluations. The evaluation framework scores hallucination resistance, citation accuracy, and report quality.

## Case Study

### Context

AI research tools often produce fluent answers without reliable source grounding. For high-stakes users such as founders, consultants, analysts, researchers, and journalists, the missing layer is not more prose; it is traceability and verification.

### Challenge

The hard problem was building a system that could:

- retrieve diverse sources
- extract atomic evidence
- verify claims before synthesis
- preserve citations
- expose confidence
- persist an audit trail
- remain testable without paid provider calls

### Solution

I designed a LangGraph workflow with five specialized agents and a typed shared state. Each node has a narrow job and writes structured outputs. The graph has one controlled loop: the Critique Agent can route back to Search when confidence is below threshold and iteration budget remains.

The backend uses FastAPI, SQLAlchemy async, PostgreSQL, and Pydantic. The AI provider layer supports OpenAI, Anthropic, and deterministic execution. The system includes Docker Compose, Prometheus metrics, CI, unit tests, integration tests, OpenAPI, and full product/architecture documentation.

### Outcome

The project demonstrates the ability to build AI systems that are product-aware, production-shaped, and technically inspectable. It showcases agent orchestration, backend architecture, data modeling, evaluation design, and startup-grade documentation in one coherent portfolio artifact.

