import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from research_orchestrator.agents.graph import build_research_graph, create_initial_state
from research_orchestrator.core.config import Settings
from research_orchestrator.core.logging import get_logger
from research_orchestrator.database.models import ResearchRun, RunStatus
from research_orchestrator.database.repositories import ResearchRepository

logger = get_logger(__name__)


class ResearchService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.repository = ResearchRepository(session)
        self.settings = settings

    async def create_run(
        self,
        *,
        query: str,
        objective: str | None,
        constraints: dict[str, Any],
        user_id: str | None,
        depth: str,
        max_sources: int | None,
        min_confidence: float | None,
    ) -> ResearchRun:
        return await self.repository.create_run(
            query=query,
            objective=objective,
            constraints=constraints,
            user_id=user_id,
            depth=depth,
            max_sources=max_sources or self.settings.default_max_sources,
            min_confidence=min_confidence or self.settings.default_min_confidence,
        )

    async def execute_run(self, run_id: uuid.UUID) -> dict[str, Any]:
        run = await self.repository.get_run(run_id)
        await self.repository.update_status(run_id, RunStatus.running)
        graph = build_research_graph(settings=self.settings)
        initial_state = create_initial_state(
            run_id=str(run.id),
            query=run.query,
            objective=run.objective,
            constraints=run.constraints,
            depth=run.depth,
            max_sources=run.max_sources,
            min_confidence=run.min_confidence,
            max_iterations=self.settings.max_graph_iterations,
        )
        try:
            result = await graph.ainvoke(initial_state)
            if not result.get("report"):
                raise RuntimeError("Research graph completed without producing a report.")
            report = await self.repository.save_graph_result(run.id, result)
            logger.info("research_run_completed", run_id=str(run.id), confidence=report.confidence_score)
            return result
        except Exception as exc:
            await self.repository.update_status(run_id, RunStatus.failed, failure_reason=str(exc))
            logger.error("research_run_failed", run_id=str(run.id), error=str(exc))
            raise

    async def get_run(self, run_id: uuid.UUID) -> ResearchRun:
        return await self.repository.get_run(run_id, include_children=True)

    async def list_runs(self, *, limit: int, offset: int) -> list[ResearchRun]:
        return await self.repository.list_runs(limit=limit, offset=offset)

