import hashlib
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from research_orchestrator.core.exceptions import NotFoundError
from research_orchestrator.database.models import (
    AgentEvent,
    EvaluationResult,
    Evidence,
    Report,
    ResearchRun,
    RunStatus,
    Source,
    SupportLevel,
)


def hash_url(url: str) -> str:
    return hashlib.sha256(url.strip().lower().encode("utf-8")).hexdigest()


class ResearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_run(
        self,
        *,
        query: str,
        objective: str | None,
        constraints: dict[str, Any],
        user_id: str | None,
        depth: str,
        max_sources: int,
        min_confidence: float,
    ) -> ResearchRun:
        run = ResearchRun(
            query=query,
            objective=objective,
            constraints=constraints,
            user_id=user_id,
            depth=depth,
            max_sources=max_sources,
            min_confidence=min_confidence,
        )
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_run(self, run_id: uuid.UUID, *, include_children: bool = False) -> ResearchRun:
        stmt: Select[tuple[ResearchRun]] = select(ResearchRun).where(ResearchRun.id == run_id)
        if include_children:
            stmt = stmt.options(
                selectinload(ResearchRun.sources),
                selectinload(ResearchRun.evidence),
                selectinload(ResearchRun.report),
                selectinload(ResearchRun.events),
            )
        result = await self.session.execute(stmt)
        run = result.scalar_one_or_none()
        if run is None:
            raise NotFoundError("research_run", str(run_id))
        return run

    async def list_runs(self, *, limit: int = 25, offset: int = 0) -> list[ResearchRun]:
        result = await self.session.execute(
            select(ResearchRun).order_by(ResearchRun.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def update_status(
        self,
        run_id: uuid.UUID,
        status: RunStatus,
        *,
        confidence_score: float | None = None,
        failure_reason: str | None = None,
    ) -> ResearchRun:
        run = await self.get_run(run_id)
        run.status = status
        run.failure_reason = failure_reason
        run.confidence_score = confidence_score
        run.updated_at = datetime.now(UTC)
        if status in {RunStatus.completed, RunStatus.failed}:
            run.completed_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def save_graph_result(self, run_id: uuid.UUID, graph_result: dict[str, Any]) -> Report:
        run = await self.get_run(run_id)

        source_id_by_url: dict[str, uuid.UUID] = {}
        for item in graph_result.get("raw_sources", []):
            source = Source(
                run_id=run.id,
                title=item.get("title") or "Untitled source",
                url=item["url"],
                url_hash=hash_url(item["url"]),
                publisher=item.get("publisher"),
                author=item.get("author"),
                snippet=item.get("snippet"),
                raw_content=item.get("raw_content"),
                credibility_score=float(item.get("credibility_score", 0.5)),
                source_metadata=item.get("metadata") or {},
            )
            self.session.add(source)
            await self.session.flush()
            source_id_by_url[source.url] = source.id

        for item in graph_result.get("verified_evidence", []):
            source_url = item.get("source_url")
            support_level = item.get("support_level", SupportLevel.insufficient.value)
            evidence = Evidence(
                run_id=run.id,
                source_id=source_id_by_url.get(source_url),
                claim=item["claim"],
                quote=item.get("quote"),
                summary=item.get("summary") or item["claim"],
                support_level=SupportLevel(support_level),
                confidence_score=float(item.get("confidence_score", 0.0)),
                page_section=item.get("page_section"),
                evidence_metadata=item.get("metadata") or {},
            )
            self.session.add(evidence)

        report_payload = graph_result["report"]
        report = Report(
            run_id=run.id,
            title=report_payload["title"],
            executive_summary=report_payload["executive_summary"],
            markdown=report_payload["markdown"],
            structured_output=report_payload["structured_output"],
            confidence_score=float(report_payload["confidence_score"]),
            citation_count=len(report_payload.get("citations", [])),
        )
        self.session.add(report)

        for event in graph_result.get("agent_events", []):
            self.session.add(
                AgentEvent(
                    run_id=run.id,
                    agent_name=event["agent_name"],
                    event_type=event["event_type"],
                    status=event["status"],
                    input_payload=event.get("input"),
                    output_payload=event.get("output"),
                    token_usage=event.get("token_usage"),
                    latency_ms=event.get("latency_ms"),
                    error=event.get("error"),
                )
            )

        run.status = RunStatus.completed
        run.confidence_score = report.confidence_score
        run.completed_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get_report_for_run(self, run_id: uuid.UUID) -> Report:
        result = await self.session.execute(select(Report).where(Report.run_id == run_id))
        report = result.scalar_one_or_none()
        if report is None:
            raise NotFoundError("report_for_run", str(run_id))
        return report

    async def list_sources_for_run(self, run_id: uuid.UUID) -> list[Source]:
        result = await self.session.execute(select(Source).where(Source.run_id == run_id))
        return list(result.scalars().all())

    async def save_evaluation_result(
        self,
        *,
        run_id: uuid.UUID | None,
        report_id: uuid.UUID | None,
        metric: str,
        score: float,
        details: dict[str, Any],
    ) -> EvaluationResult:
        result = EvaluationResult(
            run_id=run_id,
            report_id=report_id,
            metric=metric,
            score=score,
            details=details,
        )
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

