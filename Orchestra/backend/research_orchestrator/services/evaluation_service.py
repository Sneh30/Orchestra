import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from research_orchestrator.database.repositories import ResearchRepository
from research_orchestrator.evaluation.metrics import aggregate_evaluation


class EvaluationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ResearchRepository(session)

    async def evaluate_report_payload(self, report: dict[str, Any]) -> list[dict[str, Any]]:
        results = aggregate_evaluation(report)
        return [{"metric": item.metric, "score": item.score, "details": item.details} for item in results]

    async def evaluate_run(self, run_id: uuid.UUID) -> list[dict[str, Any]]:
        report = await self.repository.get_report_for_run(run_id)
        results = aggregate_evaluation(
            {
                "executive_summary": report.executive_summary,
                "markdown": report.markdown,
                "structured_output": report.structured_output,
                "confidence_score": report.confidence_score,
                "citations": report.structured_output.get("citations", []),
            }
        )
        persisted = []
        for item in results:
            saved = await self.repository.save_evaluation_result(
                run_id=run_id,
                report_id=report.id,
                metric=item.metric,
                score=item.score,
                details=item.details,
            )
            persisted.append({"id": str(saved.id), "metric": item.metric, "score": item.score})
        return persisted

