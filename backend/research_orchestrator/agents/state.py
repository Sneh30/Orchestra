from typing import Any, Literal, TypedDict


class SourceCandidate(TypedDict, total=False):
    title: str
    url: str
    publisher: str | None
    author: str | None
    snippet: str | None
    raw_content: str | None
    credibility_score: float
    metadata: dict[str, Any]


class EvidenceItem(TypedDict, total=False):
    claim: str
    quote: str | None
    summary: str
    source_url: str
    support_level: Literal["supports", "partially_supports", "contradicts", "insufficient"]
    confidence_score: float
    page_section: str | None
    metadata: dict[str, Any]


class Citation(TypedDict):
    id: str
    title: str
    url: str
    publisher: str | None
    credibility_score: float


class ResearchReport(TypedDict):
    title: str
    executive_summary: str
    markdown: str
    structured_output: dict[str, Any]
    confidence_score: float
    citations: list[Citation]


class AgentEvent(TypedDict, total=False):
    agent_name: str
    event_type: str
    status: str
    input: dict[str, Any]
    output: dict[str, Any]
    token_usage: dict[str, Any]
    latency_ms: int
    error: str


class ResearchState(TypedDict, total=False):
    run_id: str
    query: str
    objective: str | None
    constraints: dict[str, Any]
    depth: str
    max_sources: int
    min_confidence: float
    max_iterations: int
    loop_count: int
    status: Literal["queued", "running", "completed", "failed"]

    search_queries: list[str]
    raw_sources: list[SourceCandidate]
    extracted_evidence: list[EvidenceItem]
    verified_evidence: list[EvidenceItem]
    rejected_evidence: list[EvidenceItem]
    report: ResearchReport
    critique: dict[str, Any]
    confidence_score: float
    next_action: Literal["revise", "finalize", "fail"]
    errors: list[str]
    retry_counts: dict[str, int]
    agent_events: list[AgentEvent]

