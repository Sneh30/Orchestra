import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from research_orchestrator.core.config import Settings
from research_orchestrator.database.models import Report, Source
from research_orchestrator.database.repositories import ResearchRepository


class ReportService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        del settings
        self.repository = ResearchRepository(session)

    async def get_report_for_run(self, run_id: uuid.UUID) -> Report:
        return await self.repository.get_report_for_run(run_id)

    async def list_sources_for_run(self, run_id: uuid.UUID) -> list[Source]:
        return await self.repository.list_sources_for_run(run_id)

