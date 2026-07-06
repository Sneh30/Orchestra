import pytest

from research_orchestrator.agents.graph import create_initial_state


@pytest.mark.parametrize(
    "query",
    [
        "What evidence supports enterprise adoption of AI agents in regulated industries?",
        "What risks should founders evaluate before choosing managed vector databases?",
    ],
)
def test_initial_state_contract(query: str) -> None:
    state = create_initial_state(
        run_id="00000000-0000-0000-0000-000000000000",
        query=query,
        objective="contract test",
        constraints={"audience": "founders"},
        depth="advanced",
        max_sources=12,
        min_confidence=0.72,
        max_iterations=3,
    )

    assert state["query"] == query
    assert state["status"] == "queued"
    assert state["loop_count"] == 0
    assert state["agent_events"] == []

