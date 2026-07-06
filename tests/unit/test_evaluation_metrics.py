from research_orchestrator.evaluation.metrics import (
    citation_accuracy_score,
    hallucination_score,
    report_quality_score,
)


def sample_report() -> dict[str, object]:
    return {
        "executive_summary": "Summary",
        "markdown": "# Report",
        "confidence_score": 0.83,
        "citations": [{"id": "S01", "title": "Source", "url": "https://example.edu"}],
        "structured_output": {
            "key_findings": [{"claim": "A", "citation_id": "S01"}],
            "risks": [],
            "source_coverage": {"source_count": 1},
        },
    }


def test_hallucination_score_full_when_all_findings_cited() -> None:
    assert hallucination_score(sample_report()).score == 1.0


def test_citation_accuracy_score_detects_valid_citation() -> None:
    assert citation_accuracy_score(sample_report()).score == 1.0


def test_report_quality_score_checks_required_sections() -> None:
    assert report_quality_score(sample_report()).score >= 0.8

