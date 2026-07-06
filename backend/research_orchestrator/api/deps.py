from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from research_orchestrator.core.config import Settings, get_settings
from research_orchestrator.database.session import get_session
from research_orchestrator.services.evaluation_service import EvaluationService
from research_orchestrator.services.report_service import ReportService
from research_orchestrator.services.research_service import ResearchService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def settings_dependency() -> Settings:
    return get_settings()


def get_research_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(settings_dependency),
) -> ResearchService:
    return ResearchService(session, settings)


def get_report_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(settings_dependency),
) -> ReportService:
    return ReportService(session, settings)


def get_evaluation_service(
    session: AsyncSession = Depends(get_db_session),
) -> EvaluationService:
    return EvaluationService(session)

