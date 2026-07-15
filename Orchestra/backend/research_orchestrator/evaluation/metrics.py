from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MetricResult:
    metric: str
    score: float
    details: dict[str, Any]


def hallucination_score(report: dict[str, Any]) -> MetricResult:
    findings = report.get("structured_output", {}).get("key_findings", [])
    unsupported = [item for item in findings if item.get("citation_id") in {None, "uncited"}]
    total = max(len(findings), 1)
    score = 1.0 - (len(unsupported) / total)
    return MetricResult(
        metric="hallucination_resistance",
        score=round(score, 3),
        details={"unsupported_findings": unsupported, "finding_count": len(findings)},
    )


def citation_accuracy_score(report: dict[str, Any]) -> MetricResult:
    citations = {item["id"] for item in report.get("citations", [])}
    findings = report.get("structured_output", {}).get("key_findings", [])
    invalid = [
        item
        for item in findings
        if item.get("citation_id") not in citations and item.get("citation_id") != "uncited"
    ]
    cited = [item for item in findings if item.get("citation_id") in citations]
    score = len(cited) / max(len(findings), 1)
    if invalid:
        score *= 0.6
    return MetricResult(
        metric="citation_accuracy",
        score=round(score, 3),
        details={"invalid_citations": invalid, "valid_citation_count": len(cited)},
    )


def report_quality_score(report: dict[str, Any]) -> MetricResult:
    structured = report.get("structured_output", {})
    components = {
        "has_summary": bool(report.get("executive_summary")),
        "has_markdown": bool(report.get("markdown")),
        "has_key_findings": bool(structured.get("key_findings")),
        "has_risks": "risks" in structured,
        "has_source_coverage": bool(structured.get("source_coverage")),
        "confidence_calibrated": 0.0 <= float(report.get("confidence_score", -1)) <= 1.0,
    }
    score = sum(1 for value in components.values() if value) / len(components)
    return MetricResult(metric="report_quality", score=round(score, 3), details=components)


def aggregate_evaluation(report: dict[str, Any]) -> list[MetricResult]:
    return [
        hallucination_score(report),
        citation_accuracy_score(report),
        report_quality_score(report),
    ]

