from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkQuestion:
    id: str
    question: str
    expected_source_types: list[str]
    quality_bar: str


BENCHMARK_QUESTIONS = [
    BenchmarkQuestion(
        id="market-ai-agents-enterprise",
        question="What evidence supports enterprise adoption of AI agents in regulated industries?",
        expected_source_types=["analyst report", "company filing", "regulator guidance"],
        quality_bar="Report distinguishes adoption claims from verified deployments.",
    ),
    BenchmarkQuestion(
        id="founder-diligence-vector-db",
        question="Which risks should a founder consider before building on a managed vector database?",
        expected_source_types=["vendor docs", "incident report", "engineering benchmark"],
        quality_bar="Report covers lock-in, latency, compliance, cost, and migration risk.",
    ),
    BenchmarkQuestion(
        id="journalist-claims-carbon-removal",
        question="Are corporate carbon removal purchase announcements translating into delivered removals?",
        expected_source_types=["company disclosure", "registry data", "independent reporting"],
        quality_bar="Report separates purchase commitments, deliveries, and retirements.",
    ),
]

