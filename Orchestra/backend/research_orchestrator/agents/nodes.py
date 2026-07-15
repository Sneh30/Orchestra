import time
from typing import Any

from research_orchestrator.agents.prompts import (
    CRITIQUE_AGENT_SYSTEM_PROMPT,
    EXTRACTION_AGENT_SYSTEM_PROMPT,
    SEARCH_AGENT_SYSTEM_PROMPT,
    SYNTHESIS_AGENT_SYSTEM_PROMPT,
    VERIFICATION_AGENT_SYSTEM_PROMPT,
)
from research_orchestrator.agents.providers import LLMProvider
from research_orchestrator.agents.scoring import (
    build_citation_id,
    calculate_evidence_confidence,
    calculate_report_confidence,
    score_source_credibility,
)
from research_orchestrator.agents.state import AgentEvent, Citation, EvidenceItem, ResearchState
from research_orchestrator.agents.tools import TavilySearchTool


def _event(
    *,
    agent_name: str,
    event_type: str,
    status: str,
    started_at: float,
    input_payload: dict[str, Any] | None = None,
    output_payload: dict[str, Any] | None = None,
    error: str | None = None,
) -> AgentEvent:
    payload: AgentEvent = {
        "agent_name": agent_name,
        "event_type": event_type,
        "status": status,
        "latency_ms": int((time.perf_counter() - started_at) * 1000),
    }
    if input_payload is not None:
        payload["input"] = input_payload
    if output_payload is not None:
        payload["output"] = output_payload
    if error is not None:
        payload["error"] = error
    return payload


class SearchAgent:
    def __init__(self, llm: LLMProvider, search_tool: TavilySearchTool) -> None:
        self.llm = llm
        self.search_tool = search_tool

    async def __call__(self, state: ResearchState) -> dict[str, Any]:
        started_at = time.perf_counter()
        query = state["query"]
        loop_count = state.get("loop_count", 0) + 1
        followups = state.get("critique", {}).get("required_follow_up_queries", [])
        queries = await self._build_queries(query, state, followups)
        new_sources = await self.search_tool.search_many(
            queries,
            max_results=state.get("max_sources", 12),
            depth=state.get("depth", "advanced"),
        )
        sources_by_url = {source.get("url"): source for source in state.get("raw_sources", [])}
        for source in new_sources:
            sources_by_url[source.get("url")] = source
        sources = [source for url, source in sources_by_url.items() if url][: state.get("max_sources", 12)]
        for source in sources:
            source["credibility_score"] = score_source_credibility(source)
        events = state.get("agent_events", []) + [
            _event(
                agent_name="search",
                event_type="search_completed",
                status="completed",
                started_at=started_at,
                input_payload={"query": query, "queries": queries},
                output_payload={"source_count": len(sources)},
            )
        ]
        return {
            "status": "running",
            "loop_count": loop_count,
            "search_queries": queries,
            "raw_sources": sources,
            "agent_events": events,
        }

    async def _build_queries(
        self,
        query: str,
        state: ResearchState,
        followups: list[str],
    ) -> list[str]:
        if followups:
            return followups[:4]
        prompt = (
            f"Research question: {query}\n"
            f"Objective: {state.get('objective')}\n"
            f"Constraints: {state.get('constraints', {})}\n"
            "Generate 4 search queries."
        )
        try:
            response = await self.llm.complete_json(
                system_prompt=SEARCH_AGENT_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.0,
            )
            queries = [str(item) for item in response.get("queries", []) if item]
        except Exception:
            queries = []
        if not queries:
            queries = [
                query,
                f"{query} primary sources",
                f"{query} evidence OR data",
                f"{query} criticism OR limitations",
            ]
        return queries[:4]


class ExtractionAgent:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def __call__(self, state: ResearchState) -> dict[str, Any]:
        started_at = time.perf_counter()
        evidence: list[EvidenceItem] = []
        for source in state.get("raw_sources", []):
            evidence.extend(await self._extract_from_source(source, state["query"]))
        events = state.get("agent_events", []) + [
            _event(
                agent_name="extraction",
                event_type="evidence_extracted",
                status="completed",
                started_at=started_at,
                input_payload={"source_count": len(state.get("raw_sources", []))},
                output_payload={"evidence_count": len(evidence)},
            )
        ]
        return {"extracted_evidence": evidence, "agent_events": events}

    async def _extract_from_source(self, source: dict[str, Any], query: str) -> list[EvidenceItem]:
        source_text = source.get("raw_content") or source.get("snippet") or ""
        prompt = (
            f"Question: {query}\n"
            f"Source URL: {source.get('url')}\n"
            f"Source title: {source.get('title')}\n"
            f"Source text:\n{source_text[:8000]}"
        )
        try:
            response = await self.llm.complete_json(
                system_prompt=EXTRACTION_AGENT_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.0,
            )
            extracted = response.get("evidence", [])
        except Exception:
            extracted = []
        if not extracted:
            extracted = [
                {
                    "claim": f"{source.get('title')} provides evidence relevant to: {query}",
                    "quote": source.get("snippet"),
                    "summary": source.get("snippet") or source.get("title") or "Relevant source evidence.",
                    "source_url": source.get("url"),
                    "page_section": None,
                    "confidence_score": source.get("credibility_score", 0.5),
                    "metadata": {"fallback_extraction": True},
                }
            ]
        return [
            EvidenceItem(
                claim=str(item["claim"]),
                quote=item.get("quote"),
                summary=str(item.get("summary") or item["claim"]),
                source_url=str(item.get("source_url") or source["url"]),
                page_section=item.get("page_section"),
                confidence_score=float(item.get("confidence_score", 0.4)),
                metadata=item.get("metadata") or {},
            )
            for item in extracted
            if item.get("claim")
        ]


class VerificationAgent:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def __call__(self, state: ResearchState) -> dict[str, Any]:
        started_at = time.perf_counter()
        verified: list[EvidenceItem] = []
        rejected: list[EvidenceItem] = []
        for item in state.get("extracted_evidence", []):
            support_level = "supports" if item.get("source_url") else "insufficient"
            item["support_level"] = support_level
            item["confidence_score"] = calculate_evidence_confidence(item, state.get("raw_sources", []))
            if item["confidence_score"] >= 0.45:
                verified.append(item)
            else:
                rejected.append(item)
        await self._llm_cross_check(state, verified, rejected)
        events = state.get("agent_events", []) + [
            _event(
                agent_name="verification",
                event_type="evidence_verified",
                status="completed",
                started_at=started_at,
                input_payload={"evidence_count": len(state.get("extracted_evidence", []))},
                output_payload={"verified_count": len(verified), "rejected_count": len(rejected)},
            )
        ]
        return {
            "verified_evidence": verified,
            "rejected_evidence": rejected,
            "agent_events": events,
        }

    async def _llm_cross_check(
        self,
        state: ResearchState,
        verified: list[EvidenceItem],
        rejected: list[EvidenceItem],
    ) -> None:
        prompt = (
            f"Question: {state['query']}\n"
            f"Sources: {state.get('raw_sources', [])[:8]}\n"
            f"Evidence: {state.get('extracted_evidence', [])[:20]}"
        )
        try:
            response = await self.llm.complete_json(
                system_prompt=VERIFICATION_AGENT_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.0,
            )
        except Exception:
            return
        rejected_claims = {item.get("claim") for item in response.get("rejected_evidence", [])}
        if not rejected_claims:
            return
        moved: list[EvidenceItem] = []
        for item in list(verified):
            if item.get("claim") in rejected_claims:
                item["support_level"] = "insufficient"
                item["confidence_score"] = min(float(item.get("confidence_score", 0.0)), 0.35)
                verified.remove(item)
                moved.append(item)
        rejected.extend(moved)


class SynthesisAgent:
    async def __call__(self, state: ResearchState) -> dict[str, Any]:
        started_at = time.perf_counter()
        evidence = state.get("verified_evidence", [])
        sources = state.get("raw_sources", [])
        citations = self._build_citations(sources)
        citation_by_url = {citation["url"]: citation["id"] for citation in citations}
        confidence = calculate_report_confidence(evidence, sources)
        key_findings = [
            {
                "claim": item["claim"],
                "confidence_score": item.get("confidence_score", 0.0),
                "citation_id": citation_by_url.get(item.get("source_url", ""), "uncited"),
            }
            for item in evidence
        ]
        markdown = self._build_markdown(state["query"], evidence, citations, citation_by_url, confidence)
        report = {
            "title": f"Verified Research Report: {state['query']}",
            "executive_summary": self._executive_summary(evidence, confidence),
            "markdown": markdown,
            "structured_output": {
                "query": state["query"],
                "key_findings": key_findings,
                "confidence": {
                    "overall": confidence,
                    "minimum_required": state.get("min_confidence", 0.72),
                    "evidence_items": len(evidence),
                    "sources": len(sources),
                },
                "risks": self._risks(state),
                "open_questions": self._open_questions(state),
                "source_coverage": {
                    "source_count": len(sources),
                    "citation_count": len(citations),
                    "verified_evidence_count": len(evidence),
                    "rejected_evidence_count": len(state.get("rejected_evidence", [])),
                },
                "citations": citations,
            },
            "confidence_score": confidence,
            "citations": citations,
        }
        events = state.get("agent_events", []) + [
            _event(
                agent_name="synthesis",
                event_type="report_synthesized",
                status="completed",
                started_at=started_at,
                input_payload={"verified_evidence_count": len(evidence)},
                output_payload={"confidence_score": confidence, "citation_count": len(citations)},
            )
        ]
        return {"report": report, "confidence_score": confidence, "agent_events": events}

    @staticmethod
    def _build_citations(sources: list[dict[str, Any]]) -> list[Citation]:
        citations: list[Citation] = []
        for index, source in enumerate(sources, start=1):
            citations.append(
                {
                    "id": build_citation_id(index),
                    "title": source.get("title") or "Untitled source",
                    "url": source.get("url") or "",
                    "publisher": source.get("publisher"),
                    "credibility_score": float(source.get("credibility_score", 0.5)),
                }
            )
        return citations

    @staticmethod
    def _executive_summary(evidence: list[EvidenceItem], confidence: float) -> str:
        if not evidence:
            return "The system could not verify enough evidence to answer the question reliably."
        top_claims = "; ".join(item["claim"] for item in evidence[:3])
        return f"The report synthesizes {len(evidence)} verified evidence items. Overall confidence is {confidence:.2f}. Key findings: {top_claims}."

    @staticmethod
    def _build_markdown(
        query: str,
        evidence: list[EvidenceItem],
        citations: list[Citation],
        citation_by_url: dict[str, str],
        confidence: float,
    ) -> str:
        lines = [
            f"# Verified Research Report: {query}",
            "",
            f"**Overall confidence:** {confidence:.2f}",
            "",
            "## Key Findings",
        ]
        if evidence:
            for item in evidence:
                citation_id = citation_by_url.get(item.get("source_url", ""), "uncited")
                lines.append(f"- {item['claim']} [{citation_id}]")
        else:
            lines.append("- No claims passed verification.")
        lines.extend(["", "## Source Notes"])
        for citation in citations:
            lines.append(
                f"- [{citation['id']}] {citation['title']} - {citation['url']} "
                f"(credibility {citation['credibility_score']:.2f})"
            )
        return "\n".join(lines)

    @staticmethod
    def _risks(state: ResearchState) -> list[str]:
        risks = []
        if len(state.get("raw_sources", [])) < 4:
            risks.append("Limited source diversity reduces confidence.")
        if state.get("rejected_evidence"):
            risks.append("Some extracted claims were rejected or could not be verified.")
        return risks

    @staticmethod
    def _open_questions(state: ResearchState) -> list[str]:
        if state.get("confidence_score", 0.0) >= state.get("min_confidence", 0.72):
            return []
        return ["Additional primary sources may be needed to raise confidence."]


class CritiqueAgent:
    async def __call__(self, state: ResearchState) -> dict[str, Any]:
        started_at = time.perf_counter()
        confidence = float(state.get("confidence_score", 0.0))
        min_confidence = float(state.get("min_confidence", 0.72))
        loop_count = int(state.get("loop_count", 1))
        max_iterations = int(state.get("max_iterations", 3))
        issues = []
        followups = []
        if confidence < min_confidence:
            issues.append("Report confidence is below the requested threshold.")
            followups.append(f"{state['query']} primary source evidence")
            followups.append(f"{state['query']} independent corroboration")
        if not state.get("verified_evidence"):
            issues.append("No evidence passed verification.")
        if issues and loop_count < max_iterations:
            decision = "revise"
        elif state.get("report"):
            decision = "finalize"
        else:
            decision = "fail"
        critique = {
            "decision": decision,
            "confidence_score": confidence,
            "issues": issues,
            "required_follow_up_queries": followups,
        }
        events = state.get("agent_events", []) + [
            _event(
                agent_name="critique",
                event_type="report_critiqued",
                status="completed",
                started_at=started_at,
                input_payload={"confidence_score": confidence},
                output_payload=critique,
            )
        ]
        status = "completed" if decision == "finalize" else "running"
        if decision == "fail":
            status = "failed"
        return {
            "critique": critique,
            "next_action": decision,
            "status": status,
            "agent_events": events,
        }
