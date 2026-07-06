# Section 6 - LangGraph Design

## State Definitions

The graph state is defined in `backend/research_orchestrator/agents/state.py`.

Core state keys:

- `query`: original research question.
- `objective`: desired report objective.
- `constraints`: user-supplied research constraints.
- `search_queries`: generated search strings.
- `raw_sources`: source candidates from Tavily or deterministic mode.
- `extracted_evidence`: atomic evidence items before verification.
- `verified_evidence`: claims accepted for synthesis.
- `rejected_evidence`: weak, contradicted, or unsupported claims.
- `report`: final report payload.
- `confidence_score`: calibrated report confidence.
- `critique`: critique agent output.
- `next_action`: graph routing decision.
- `loop_count`: completed research loops.
- `max_iterations`: loop guard.
- `agent_events`: audit trail.

## Agent Definitions

### Search Agent

Responsibilities:

- Generate search queries from user question, objective, constraints, and critique follow-ups.
- Retrieve source candidates.
- Deduplicate sources by URL.
- Apply source credibility scoring.

Implementation: `SearchAgent` in `backend/research_orchestrator/agents/nodes.py`.

### Extraction Agent

Responsibilities:

- Read source title, snippet, and raw content.
- Extract atomic claims.
- Preserve quotes when available.
- Attach source URL to every evidence item.

Implementation: `ExtractionAgent` in `backend/research_orchestrator/agents/nodes.py`.

### Verification Agent

Responsibilities:

- Assign support levels.
- Calibrate evidence confidence.
- Move unsupported claims into rejected evidence.
- Optionally ask an LLM verifier to cross-check evidence quality.

Implementation: `VerificationAgent` in `backend/research_orchestrator/agents/nodes.py`.

### Synthesis Agent

Responsibilities:

- Build citations.
- Produce markdown report.
- Produce structured output.
- Calculate report confidence.
- Include risks, open questions, source coverage, and citations.

Implementation: `SynthesisAgent` in `backend/research_orchestrator/agents/nodes.py`.

### Critique Agent

Responsibilities:

- Compare confidence to requested threshold.
- Detect lack of verified evidence.
- Generate follow-up search queries when another loop is warranted.
- Route to `revise`, `finalize`, or `fail`.

Implementation: `CritiqueAgent` in `backend/research_orchestrator/agents/nodes.py`.

## Tools

### TavilySearchTool

Location: `backend/research_orchestrator/agents/tools.py`

Production behavior:

- Calls Tavily with `advanced` or `basic` search depth.
- Requests raw content.
- Normalizes results into `SourceCandidate`.
- Scores credibility.

Deterministic behavior:

- If no Tavily key is configured, returns stable source records for CI and local offline review.

## Graph Topology

```python
graph = StateGraph(ResearchState)
graph.add_node("search", SearchAgent(llm, search_tool))
graph.add_node("extract", ExtractionAgent(llm))
graph.add_node("verify", VerificationAgent(llm))
graph.add_node("synthesize", SynthesisAgent())
graph.add_node("critique", CritiqueAgent())

graph.set_entry_point("search")
graph.add_edge("search", "extract")
graph.add_edge("extract", "verify")
graph.add_edge("verify", "synthesize")
graph.add_edge("synthesize", "critique")
graph.add_conditional_edges(
    "critique",
    route_after_critique,
    {"revise": "search", "finalize": END, "fail": END},
)
```

## Routing Logic

- `revise`: confidence is below threshold and loop count is below maximum.
- `finalize`: report exists and either confidence is acceptable or loop limit has been reached.
- `fail`: no report exists after graph execution.

## Retry Logic

The implementation uses layered resilience:

- Prompt nodes catch JSON parsing and model exceptions where a deterministic fallback is safe.
- The service marks the full run failed for unrecoverable graph or persistence failures.
- Critique-driven graph loops act as semantic retries when the report is low confidence.
- Provider clients are isolated behind `LLMProvider`, so provider-specific retry policy can be added in one adapter.

## Failure Recovery

- Run status transitions from `queued` to `running`.
- Successful graph output persists sources, evidence, report, and events, then sets `completed`.
- Exceptions set `failed` and store `failure_reason`.
- Partial graph details are preserved in `agent_events` when nodes complete before failure.

## Loop Prevention

Loop prevention is enforced by:

- `loop_count` incremented by the search node.
- `max_iterations` injected into initial state from settings.
- Critique agent never returns `revise` once `loop_count >= max_iterations`.

## Production-Quality Code

The full code is in:

- `backend/research_orchestrator/agents/state.py`
- `backend/research_orchestrator/agents/prompts.py`
- `backend/research_orchestrator/agents/tools.py`
- `backend/research_orchestrator/agents/nodes.py`
- `backend/research_orchestrator/agents/graph.py`
- `backend/research_orchestrator/agents/providers.py`
- `backend/research_orchestrator/agents/scoring.py`

