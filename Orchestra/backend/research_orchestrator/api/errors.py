from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from research_orchestrator.core.exceptions import AppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> ORJSONResponse:
        del request
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> ORJSONResponse:
        del request
        return ORJSONResponse(
            status_code=500,
            content={"code": "internal_error", "message": str(exc), "details": None},
        )

