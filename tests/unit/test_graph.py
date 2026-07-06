from typing import Any

import pytest

from research_orchestrator.agents.graph import build_research_graph, create_initial_state
from research_orchestrator.agents.providers import DeterministicLLMProvider


class FakeSearchTool:
    async def search_many(
        self,
        queries: list[str],
        *,
        max_results: int,
        depth: str,
    ) -> list[dict[str, Any]]:
        del queries, max_results, depth
        return [
            {
                "title": "Official source",
                "url": "https://www.sec.gov/example",
                "publisher": "SEC",
                "snippet": "Official evidence about the question.",
                "raw_content": "Official evidence about the question and material risk factors.",
                "credibility_score": 0.95,
                "metadata": {},
            },
            {
                "title": "Academic source",
                "url": "https://example.edu/research",
                "publisher": "Example University",
                "snippet": "Independent academic evidence.",
                "raw_content": "Independent academic evidence and adoption analysis.",
                "credibility_score": 0.9,
                "metadata": {},
            },
        ]


@pytest.mark.asyncio
async def test_research_graph_produces_report() -> None:
    graph = build_research_graph(
        llm_provider=DeterministicLLMProvider(),
        search_tool=FakeSearchTool(),  # type: ignore[arg-type]
    )
    state = create_initial_state(
        run_id="00000000-0000-0000-0000-000000000000",
        query="What evidence supports enterprise adoption of AI agents?",
        objective="portfolio-quality research report",
        constraints={},
        depth="advanced",
        max_sources=6,
        min_confidence=0.5,
        max_iterations=2,
    )

    result = await graph.ainvoke(state)

    assert result["status"] == "completed"
    assert result["report"]["confidence_score"] >= 0.5
    assert result["report"]["citations"]

