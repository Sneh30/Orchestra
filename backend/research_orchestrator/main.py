from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import HTMLResponse, Response

from research_orchestrator.api.errors import register_exception_handlers
from research_orchestrator.api.routes import evaluations, health, reports, research
from research_orchestrator.core.config import Settings, get_settings
from research_orchestrator.core.logging import configure_logging
from research_orchestrator.core.security import verify_api_key

OPENAPI_TAGS = [
    {"name": "health", "description": "Service health and readiness checks."},
    {"name": "research-runs", "description": "Create, list, retrieve, and execute multi-agent research runs."},
    {"name": "reports", "description": "Retrieve reports and sources for completed research runs."},
    {"name": "evaluations", "description": "Evaluate report quality using hallucination, citation, and quality metrics."},
]

CUSTOM_CSS = """
<style>
    .swagger-ui .topbar { display: none }
    .swagger-ui .info .title { font-size: 1.5em; color: #3b82f6; }
    .swagger-ui .info .description { font-size: 1em; color: #6b7280; }
    .swagger-ui .scheme-container { background: #f8fafc; border-radius: 8px; padding: 10px; }
    .swagger-ui .opblock.opblock-post { border-color: #10b981; background: rgba(16, 185, 129, 0.05); }
    .swagger-ui .opblock.opblock-post .opblock-summary-method { background: #10b981; }
    .swagger-ui .opblock.opblock-get { border-color: #3b82f6; background: rgba(59, 130, 246, 0.05); }
    .swagger-ui .opblock.opblock-get .opblock-summary-method { background: #3b82f6; }
    .swagger-ui .model-title { font-weight: 600; }
    .swagger-ui .opblock-description-wrapper p { color: #4b5563; line-height: 1.6; }
</style>
"""


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings.log_level)

    async def api_key_dependency(
        x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    ) -> None:
        await verify_api_key(resolved_settings, x_api_key)

    app = FastAPI(
        title="Multi-Agent Research Orchestrator",
        version="0.1.0",
        description=(
            "LangGraph-powered research orchestration system that coordinates specialized agents "
            "to produce verified research reports with citations, source tracking, and confidence scoring."
        ),
        openapi_tags=OPENAPI_TAGS,
        dependencies=[Depends(api_key_dependency)] if resolved_settings.api_key else [],
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": 2,
            "docExpansion": "list",
            "filter": True,
            "tagsSorter": "alpha",
            "operationsSorter": "method",
            "deepLinking": True,
            "persistAuthorization": True,
        },
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(research.router)
    app.include_router(reports.router)
    app.include_router(evaluations.router)

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - API Explorer",
            swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
            swagger_ui_parameters=app.swagger_ui_parameters,
            additional_css=[CUSTOM_CSS],
        )

    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
