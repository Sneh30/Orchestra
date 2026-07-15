import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ResearchRunRequest(BaseModel):
    """Request body for creating a new research run."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "query": "What evidence supports enterprise adoption of AI agents in regulated industries?",
                    "objective": "Produce a board-ready diligence memo.",
                    "constraints": {"audience": "founders", "prefer_primary_sources": True},
                    "depth": "advanced",
                    "max_sources": 12,
                    "min_confidence": 0.72,
                    "execute_async": True,
                }
            ]
        }
    )

    query: str = Field(
        min_length=10,
        max_length=4000,
        description="The research question to investigate.",
        json_schema_extra={"example": "What evidence supports enterprise adoption of AI agents in regulated industries?"},
    )
    objective: str | None = Field(
        default=None,
        max_length=4000,
        description="Optional research objective or deliverable description.",
        json_schema_extra={"example": "Produce a board-ready diligence memo."},
    )
    constraints: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value constraints to guide the research (e.g., audience, source preferences).",
        json_schema_extra={"example": {"audience": "founders", "prefer_primary_sources": True}},
    )
    user_id: str | None = Field(
        default=None,
        max_length=128,
        description="Optional user identifier for tracking.",
    )
    depth: Literal["basic", "advanced"] = Field(
        default="advanced",
        description="Research depth: 'basic' for quick overview, 'advanced' for thorough analysis.",
    )
    max_sources: int | None = Field(
        default=None,
        ge=3,
        le=50,
        description="Maximum number of sources to retrieve (3-50).",
        json_schema_extra={"example": 12},
    )
    min_confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold (0.0-1.0). Runs below this threshold trigger re-evaluation.",
        json_schema_extra={"example": 0.72},
    )
    execute_async: bool = Field(
        default=True,
        description="If true, executes asynchronously and returns immediately. If false, waits for completion.",
    )


class ResearchRunResponse(BaseModel):
    """Response model for a research run."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(description="Unique identifier for the research run.")
    user_id: str | None = Field(description="User identifier if provided.")
    query: str = Field(description="The research question.")
    objective: str | None = Field(description="Research objective if provided.")
    constraints: dict[str, Any] = Field(description="Research constraints.")
    status: str = Field(description="Run status: queued, running, completed, or failed.")
    depth: str = Field(description="Research depth level.")
    max_sources: int = Field(description="Maximum sources requested.")
    min_confidence: float = Field(description="Minimum confidence threshold.")
    confidence_score: float | None = Field(description="Final confidence score (null if not completed).")
    failure_reason: str | None = Field(description="Error message if run failed.")
    created_at: datetime = Field(description="Timestamp when the run was created.")
    updated_at: datetime = Field(description="Timestamp of last update.")
    completed_at: datetime | None = Field(description="Timestamp when the run completed.")


class CitationResponse(BaseModel):
    """A citation reference within a report."""

    id: str = Field(description="Citation identifier (e.g., S01).")
    title: str = Field(description="Source title.")
    url: str = Field(description="Source URL.")
    publisher: str | None = Field(description="Publisher or organization name.")
    credibility_score: float = Field(description="Source credibility score (0.0-1.0).")


class ReportResponse(BaseModel):
    """Response model for a completed research report."""

    id: uuid.UUID = Field(description="Unique identifier for the report.")
    run_id: uuid.UUID = Field(description="Identifier of the associated research run.")
    title: str = Field(description="Report title.")
    executive_summary: str = Field(description="Brief executive summary of findings.")
    markdown: str = Field(description="Full report in Markdown format.")
    structured_output: dict[str, Any] = Field(description="Structured JSON output with citations, findings, and metadata.")
    confidence_score: float = Field(description="Overall confidence score (0.0-1.0).")
    citation_count: int = Field(description="Number of citations in the report.")
    created_at: datetime = Field(description="Timestamp when the report was generated.")


class SourceResponse(BaseModel):
    """Response model for a retrieved source."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(description="Unique identifier for the source.")
    run_id: uuid.UUID = Field(description="Identifier of the associated research run.")
    title: str = Field(description="Source title.")
    url: str = Field(description="Source URL.")
    publisher: str | None = Field(description="Publisher or organization name.")
    author: str | None = Field(description="Author name if available.")
    snippet: str | None = Field(description="Relevant snippet from the source.")
    credibility_score: float = Field(description="Source credibility score (0.0-1.0).")
    source_metadata: dict[str, Any] = Field(description="Additional metadata about the source.")


class EvaluationRequest(BaseModel):
    """Request body for evaluating a report payload."""

    report: dict[str, Any] = Field(
        description="The report payload to evaluate (structured_output from ReportResponse).",
        json_schema_extra={
            "example": {
                "query": "What is quantum computing?",
                "citations": [{"id": "S01", "url": "https://example.com", "title": "Example"}],
                "key_findings": [{"claim": "Quantum computing uses qubits", "citation_id": "S01"}],
                "confidence": {"overall": 0.85},
            }
        },
    )


class EvaluationResponse(BaseModel):
    """Response model for a single evaluation metric."""

    metric: str = Field(description="Metric name (e.g., hallucination_resistance, citation_accuracy, report_quality).")
    score: float = Field(description="Metric score (0.0-1.0).")
    details: dict[str, Any] = Field(description="Detailed breakdown of the metric calculation.")


class ErrorResponse(BaseModel):
    """Standard error response."""

    code: str = Field(description="Error code (e.g., unauthorized, not_found, validation_error).")
    message: str = Field(description="Human-readable error message.")
    details: dict[str, Any] | None = Field(default=None, description="Additional error details.")


class ExecuteRunResponse(BaseModel):
    """Response model for synchronous execution of a research run."""

    run_id: uuid.UUID = Field(description="Identifier of the executed research run.")
    status: str = Field(description="Final status after execution.")
    confidence_score: float | None = Field(description="Confidence score if completed.")
    report_id: uuid.UUID | None = Field(description="Report ID if a report was generated.")

