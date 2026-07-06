import asyncio
from typing import Any

from research_orchestrator.agents.scoring import score_source_credibility
from research_orchestrator.agents.state import SourceCandidate
from research_orchestrator.core.config import Settings


class TavilySearchTool:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def search_many(
        self,
        queries: list[str],
        *,
        max_results: int,
        depth: str,
    ) -> list[SourceCandidate]:
        results_by_url: dict[str, SourceCandidate] = {}
        per_query = max(2, max_results // max(len(queries), 1))
        for query in queries:
            for source in await self._search(query, max_results=per_query, depth=depth):
                url = source.get("url")
                if not url or url in results_by_url:
                    continue
                source["credibility_score"] = score_source_credibility(source)
                results_by_url[url] = source
                if len(results_by_url) >= max_results:
                    return list(results_by_url.values())
        return list(results_by_url.values())

    async def _search(self, query: str, *, max_results: int, depth: str) -> list[SourceCandidate]:
        if not self.settings.tavily_api_key:
            return self._deterministic_sources(query, max_results=max_results)

        from tavily import TavilyClient

        client = TavilyClient(api_key=self.settings.tavily_api_key.get_secret_value())

        def run_search() -> dict[str, Any]:
            return client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced" if depth == "advanced" else "basic",
                include_raw_content=True,
                include_answer=False,
            )

        response = await asyncio.to_thread(run_search)
        sources: list[SourceCandidate] = []
        for item in response.get("results", []):
            sources.append(
                {
                    "title": item.get("title") or "Untitled source",
                    "url": item["url"],
                    "publisher": item.get("source"),
                    "author": None,
                    "snippet": item.get("content"),
                    "raw_content": item.get("raw_content"),
                    "metadata": {"score": item.get("score"), "query": query},
                }
            )
        return sources

    @staticmethod
    def _deterministic_sources(query: str, *, max_results: int) -> list[SourceCandidate]:
        normalized = query.replace(" ", "-").lower()[:64]
        sources = [
            {
                "title": f"Primary data brief for {query}",
                "url": f"https://example.edu/research/{normalized}",
                "publisher": "Example University Research Center",
                "author": "Research Desk",
                "snippet": f"Primary research context and baseline facts related to {query}.",
                "raw_content": (
                    f"This source provides primary research context for {query}. "
                    "It includes market structure, adoption drivers, risks, and measurable outcomes."
                ),
                "metadata": {"deterministic": True, "query": query},
            },
            {
                "title": f"Regulatory and market filing notes for {query}",
                "url": f"https://www.sec.gov/example/{normalized}",
                "publisher": "SEC",
                "author": None,
                "snippet": f"Regulatory evidence and public-market context related to {query}.",
                "raw_content": (
                    f"This official source documents constraints, disclosures, and market signals for {query}. "
                    "It highlights uncertainty, timing, and material risk factors."
                ),
                "metadata": {"deterministic": True, "query": query},
            },
        ]
        return sources[:max_results]

