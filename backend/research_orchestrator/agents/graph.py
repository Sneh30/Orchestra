from typing import Any

from langgraph.graph import END, StateGraph

from research_orchestrator.agents.nodes import (
    CritiqueAgent,
    ExtractionAgent,
    SearchAgent,
    SynthesisAgent,
    VerificationAgent,
)
from research_orchestrator.agents.providers import LLMProvider, create_llm_provider
from research_orchestrator.agents.state import ResearchState
from research_orchestrator.agents.tools import TavilySearchTool
from research_orchestrator.core.config import Settings, get_settings


def route_after_critique(state: ResearchState) -> str:
    return state.get("next_action", "finalize")


def create_initial_state(
    *,
    run_id: str,
    query: str,
    objective: str | None,
    constraints: dict[str, Any],
    depth: str,
    max_sources: int,
    min_confidence: float,
    max_iterations: int,
) -> ResearchState:
    return {
        "run_id": run_id,
        "query": query,
        "objective": objective,
        "constraints": constraints,
        "depth": depth,
        "max_sources": max_sources,
        "min_confidence": min_confidence,
        "max_iterations": max_iterations,
        "loop_count": 0,
        "status": "queued",
        "search_queries": [],
        "raw_sources": [],
        "extracted_evidence": [],
        "verified_evidence": [],
        "rejected_evidence": [],
        "errors": [],
        "retry_counts": {},
        "agent_events": [],
    }


def build_research_graph(
    *,
    settings: Settings | None = None,
    llm_provider: LLMProvider | None = None,
    search_tool: TavilySearchTool | None = None,
) -> Any:
    resolved_settings = settings or get_settings()
    resolved_llm = llm_provider or create_llm_provider(resolved_settings)
    resolved_search_tool = search_tool or TavilySearchTool(resolved_settings)

    graph = StateGraph(ResearchState)
    graph.add_node("search", SearchAgent(resolved_llm, resolved_search_tool))
    graph.add_node("extract", ExtractionAgent(resolved_llm))
    graph.add_node("verify", VerificationAgent(resolved_llm))
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
        {
            "revise": "search",
            "finalize": END,
            "fail": END,
        },
    )
    return graph.compile()

