import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from research_orchestrator.api.deps import get_research_service
from research_orchestrator.api.schemas import (
    ErrorResponse,
    ExecuteRunResponse,
    ResearchRunRequest,
    ResearchRunResponse,
)
from research_orchestrator.database.session import SessionFactory
from research_orchestrator.services.research_service import ResearchService
from research_orchestrator.services.telemetry import RESEARCH_RUNS_CREATED

router = APIRouter(prefix="/v1/research-runs", tags=["research-runs"])


async def _run_in_background(run_id: uuid.UUID) -> None:
    async with SessionFactory() as session:
        from research_orchestrator.core.config import get_settings

        service = ResearchService(session, get_settings())
        try:
            await service.execute_run(run_id)
        except Exception:
            pass


@router.post(
    "",
    response_model=ResearchRunResponse,
    status_code=202,
    summary="Create a research run",
    description=(
        "Queues a new multi-agent research run. The LangGraph pipeline will search, extract, "
        "verify, and synthesize evidence into a citation-backed report. If `execute_async` is "
        "true (default), execution happens in a background task; otherwise the request blocks "
        "until the run completes."
    ),
    response_description="The newly created research run with status `queued`.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def create_research_run(
    payload: ResearchRunRequest,
    background_tasks: BackgroundTasks,
    service: ResearchService = Depends(get_research_service),
) -> ResearchRunResponse:
    run = await service.create_run(
        query=payload.query,
        objective=payload.objective,
        constraints=payload.constraints,
        user_id=payload.user_id,
        depth=payload.depth,
        max_sources=payload.max_sources,
        min_confidence=payload.min_confidence,
    )
    RESEARCH_RUNS_CREATED.inc()
    background_tasks.add_task(_run_in_background, run.id)
    return ResearchRunResponse.model_validate(run)


@router.get(
    "",
    response_model=list[ResearchRunResponse],
    summary="List research runs",
    description="Retrieve a paginated list of research runs, ordered by creation time (newest first).",
    response_description="List of research run objects.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
    },
)
async def list_research_runs(
    limit: int = Query(default=25, ge=1, le=100, description="Maximum number of runs to return."),
    offset: int = Query(default=0, ge=0, description="Number of runs to skip for pagination."),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchRunResponse]:
    runs = await service.list_runs(limit=limit, offset=offset)
    return [ResearchRunResponse.model_validate(run) for run in runs]


@router.get(
    "/{run_id}",
    response_model=ResearchRunResponse,
    summary="Get a research run",
    description="Retrieve details for a specific research run by ID.",
    response_description="The research run object.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
        404: {"model": ErrorResponse, "description": "Run not found"},
    },
)
async def get_research_run(
    run_id: uuid.UUID,
    service: ResearchService = Depends(get_research_service),
) -> ResearchRunResponse:
    run = await service.get_run(run_id)
    return ResearchRunResponse.model_validate(run)


@router.post(
    "/{run_id}/execute",
    response_model=ExecuteRunResponse,
    summary="Execute a research run",
    description=(
        "Synchronously executes a research run and waits for completion. "
        "Use this for runs created with `execute_async: false` or to re-execute a failed run."
    ),
    response_description="Execution result with final status and confidence score.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid API key"},
        404: {"model": ErrorResponse, "description": "Run not found"},
        500: {"model": ErrorResponse, "description": "Execution failed"},
    },
)
async def execute_research_run(
    run_id: uuid.UUID,
) -> ExecuteRunResponse:
    async with SessionFactory() as session:
        from research_orchestrator.core.config import get_settings

        service = ResearchService(session, get_settings())
        result = await service.execute_run(run_id)
        return ExecuteRunResponse(
            run_id=run_id,
            status=result.get("status", "unknown"),
            confidence_score=result.get("confidence_score"),
            report_id=result.get("report_id"),
        )

