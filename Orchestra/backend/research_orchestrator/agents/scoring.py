from collections import Counter
from urllib.parse import urlparse

from research_orchestrator.agents.state import EvidenceItem, SourceCandidate

HIGH_TRUST_DOMAINS = {
    "gov": 0.95,
    "edu": 0.9,
    "who.int": 0.95,
    "oecd.org": 0.9,
    "worldbank.org": 0.9,
    "sec.gov": 0.95,
    "federalreserve.gov": 0.95,
    "nature.com": 0.88,
    "science.org": 0.88,
}

LOW_TRUST_HINTS = ("sponsored", "affiliate", "press release", "guest post")


def domain_for(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def score_source_credibility(source: SourceCandidate) -> float:
    url = source.get("url", "")
    domain = domain_for(url)
    score = 0.55
    for trusted_domain, trusted_score in HIGH_TRUST_DOMAINS.items():
        if domain == trusted_domain or domain.endswith(f".{trusted_domain}"):
            score = max(score, trusted_score)
    text = " ".join(
        [
            source.get("title") or "",
            source.get("snippet") or "",
            source.get("publisher") or "",
        ]
    ).lower()
    if any(hint in text for hint in LOW_TRUST_HINTS):
        score -= 0.18
    if source.get("raw_content"):
        score += 0.05
    return min(max(round(score, 3), 0.0), 1.0)


def calculate_evidence_confidence(evidence: EvidenceItem, sources: list[SourceCandidate]) -> float:
    source_url = evidence.get("source_url", "")
    matching_source = next((source for source in sources if source.get("url") == source_url), None)
    source_score = matching_source.get("credibility_score", 0.5) if matching_source else 0.4
    support_level = evidence.get("support_level", "insufficient")
    support_multiplier = {
        "supports": 1.0,
        "partially_supports": 0.72,
        "contradicts": 0.3,
        "insufficient": 0.22,
    }[support_level]
    quote_bonus = 0.07 if evidence.get("quote") else 0.0
    return min(max(round(source_score * support_multiplier + quote_bonus, 3), 0.0), 1.0)


def calculate_report_confidence(evidence: list[EvidenceItem], sources: list[SourceCandidate]) -> float:
    if not evidence:
        return 0.0
    evidence_scores = [float(item.get("confidence_score", 0.0)) for item in evidence]
    mean_evidence = sum(evidence_scores) / len(evidence_scores)
    domains = [domain_for(source.get("url", "")) for source in sources]
    unique_domain_ratio = len(set(domains)) / max(len(domains), 1)
    support_counts = Counter(item.get("support_level") for item in evidence)
    contradiction_penalty = min(support_counts.get("contradicts", 0) * 0.04, 0.2)
    score = (mean_evidence * 0.72) + (unique_domain_ratio * 0.18) + (min(len(sources), 12) / 12 * 0.1)
    return min(max(round(score - contradiction_penalty, 3), 0.0), 1.0)


def build_citation_id(index: int) -> str:
    return f"S{index:02d}"

