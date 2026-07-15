from prometheus_client import Counter, Histogram

RESEARCH_RUNS_CREATED = Counter(
    "research_runs_created_total",
    "Total research runs created.",
)
RESEARCH_RUNS_COMPLETED = Counter(
    "research_runs_completed_total",
    "Total research runs completed.",
)
RESEARCH_RUN_LATENCY = Histogram(
    "research_run_latency_seconds",
    "End-to-end research run latency.",
    buckets=(5, 15, 30, 60, 120, 300, 600),
)

