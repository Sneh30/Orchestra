import uuid

from fastapi import APIRouter, Depends

from research_orchestrator.api.deps import get_report_service
from research_orchestrator.api.schemas import ErrorResponse, ReportResponse, SourceResponse
from research_orchestrator.services.report_service import ReportService

router = APIRouter(prefix="/v1/research-runs/{run_id}", tags=["reports"])


@router.get(
    "/report",
    response_model=ReportResponse,
    summary="Get research report",
    description=(
        "Retrieve the full research report for a completed run, including Markdown content, "
        "structured output with citations, and confidence scoring."
    ),
    response_description="The complete research report.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
        404: {"model": ErrorResponse, "description": "Report not found (run may not be completed)"},
    },
)
async def get_report(
    run_id: uuid.UUID,
    service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    report = await service.get_report_for_run(run_id)
    return ReportResponse(
        id=report.id,
        run_id=report.run_id,
        title=report.title,
        executive_summary=report.executive_summary,
        markdown=report.markdown,
        structured_output=report.structured_output,
        confidence_score=report.confidence_score,
        citation_count=report.citation_count,
        created_at=report.created_at,
    )


@router.get(
    "/sources",
    response_model=list[SourceResponse],
    summary="List sources",
    description="Retrieve all sources retrieved and evaluated for a research run.",
    response_description="List of source objects with credibility scores.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
        404: {"model": ErrorResponse, "description": "Run not found"},
    },
)
async def list_sources(
    run_id: uuid.UUID,
    service: ReportService = Depends(get_report_service),
) -> list[SourceResponse]:
    sources = await service.list_sources_for_run(run_id)
    return [SourceResponse.model_validate(source) for source in sources]

