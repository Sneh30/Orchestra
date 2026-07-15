from fastapi import APIRouter

from research_orchestrator.api.schemas import ErrorResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns service health status. Use for liveness and readiness probes.",
    response_description="Health status object.",
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}},
)
async def health() -> dict[str, str]:
    return {"status": "ok"}

