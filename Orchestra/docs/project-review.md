# Section 15 - Project Review

## OpenAI Recruiter Critique

Strengths:

- Demonstrates modern agent orchestration with LangGraph rather than a wrapper around one chat completion.
- Shows awareness of evaluation, citations, structured output, and confidence calibration.
- Includes production service boundaries, tests, Docker, schema, and OpenAPI.
- Strong fit for roles involving applied AI systems, agent workflows, and productized LLM applications.

Weaknesses:

- The strongest version would include screenshots or recorded demos of real research reports.
- Evaluation metrics are a solid foundation but would be stronger with human-labeled benchmark results.
- Provider abstraction is clean, but deeper token accounting and cost tracking would increase production credibility.

Improvements:

- Add benchmark result tables from real runs.
- Add cost, latency, and token metrics per agent.
- Add a demo report gallery with strong and weak examples.

## Anthropic Recruiter Critique

Strengths:

- Clear emphasis on verification, critique, and uncertainty.
- Good separation between synthesis and evidence validation.
- Responsible design posture: confidence scores, rejected evidence, source traceability, and deterministic testing.

Weaknesses:

- The project should make refusal and high-stakes domain boundaries explicit in prompts and API output.
- Verification currently combines heuristics with optional LLM review; external fact-checking and claim clustering would strengthen the system.

Improvements:

- Add safety policy prompts for medical, legal, financial, and political research.
- Add contradiction clustering across sources.
- Add calibration evaluation against expert-reviewed reports.

## YC Founder Critique

Strengths:

- Clear pain point: professional research is expensive and LLM trust is low.
- Strong wedge into founders, consultants, analysts, and journalists.
- Product narrative is commercially legible: faster research with traceability.

Weaknesses:

- The project needs a narrower beachhead for a company pitch.
- The buyer is broad; the first paid customer profile should be sharper.
- The product would benefit from workflow integrations such as Google Docs, Slack, Notion, and CRM exports.

Improvements:

- Pick one initial persona, such as seed-stage founders doing market diligence.
- Add shareable report pages and export formats.
- Add team workspaces and saved source libraries.

## Startup CTO Critique

Strengths:

- Service boundaries are clean.
- PostgreSQL schema is practical and auditable.
- Deterministic mode makes CI feasible.
- Docker Compose and Prometheus provide credible deployment shape.

Weaknesses:

- Background tasks inside FastAPI are suitable for local operation but not high-volume production.
- Long-running research jobs need a worker queue, idempotency keys, cancellation, and resumability.
- Provider rate limiting and token budgeting need stronger controls.

Improvements:

- Move graph execution to a worker system.
- Add idempotent run creation.
- Add per-agent timeouts, cost limits, and rate-limit backoff.
- Add migrations through Alembic for multi-migration lifecycle management.

## AI Hiring Manager Critique

Strengths:

- Shows real AI systems judgment: graph state, specialized agents, source tracking, confidence, and evaluation.
- Not merely a demo; it includes backend, database, infra, tests, and documentation.
- Good interview surface area across LangGraph, FastAPI, PostgreSQL, evaluation, and product thinking.

Weaknesses:

- Live quality depends on provider behavior and search coverage.
- Citation accuracy scoring checks structure, but semantic citation correctness needs deeper evaluation.
- The synthesis agent currently has deterministic construction logic in code; advanced LLM synthesis could improve report richness.

Improvements:

- Add semantic citation verification using source snippets and claim matching.
- Add source reranking.
- Add report diffing between graph iterations.
- Add an interactive review UI for accepting and rejecting evidence.

