from research_orchestrator.agents.scoring import (
    calculate_report_confidence,
    domain_for,
    score_source_credibility,
)


def test_domain_for_normalizes_www() -> None:
    assert domain_for("https://www.sec.gov/filing") == "sec.gov"


def test_score_source_credibility_rewards_primary_domains() -> None:
    score = score_source_credibility(
        {
            "title": "Company filing",
            "url": "https://www.sec.gov/example",
            "publisher": "SEC",
            "snippet": "Official disclosure",
            "raw_content": "Full filing content",
            "metadata": {},
        }
    )

    assert score >= 0.9


def test_calculate_report_confidence_penalizes_empty_evidence() -> None:
    assert calculate_report_confidence([], []) == 0.0


def test_calculate_report_confidence_uses_source_diversity() -> None:
    evidence = [
        {
            "claim": "Claim A",
            "source_url": "https://example.edu/a",
            "support_level": "supports",
            "confidence_score": 0.8,
        },
        {
            "claim": "Claim B",
            "source_url": "https://sec.gov/b",
            "support_level": "supports",
            "confidence_score": 0.9,
        },
    ]
    sources = [
        {"url": "https://example.edu/a", "credibility_score": 0.8},
        {"url": "https://sec.gov/b", "credibility_score": 0.95},
    ]

    assert calculate_report_confidence(evidence, sources) > 0.75

