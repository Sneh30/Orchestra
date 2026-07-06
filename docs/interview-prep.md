# Section 14 - Interview Preparation

## 50 Technical Questions With Ideal Answers

1. What problem does this system solve technically?
   It decomposes complex research into explicit search, extraction, verification, synthesis, and critique steps so the system can track sources, reject weak claims, cite evidence, and expose confidence instead of relying on one opaque LLM response.

2. Why use LangGraph?
   LangGraph gives a typed, stateful workflow with explicit nodes, edges, and conditional routing. That makes agent execution inspectable, testable, and safer than ad hoc chained prompts.

3. What is in the graph state?
   The state contains the query, objective, constraints, search queries, raw sources, extracted evidence, verified evidence, rejected evidence, report, critique, confidence score, loop counters, status, errors, and agent events.

4. Why split agents by role?
   Each role has a different quality bar. Search optimizes coverage, extraction optimizes faithful claim capture, verification optimizes evidence quality, synthesis optimizes communication, and critique optimizes final review.

5. How does the system prevent infinite loops?
   The search node increments `loop_count`, settings inject `max_iterations`, and the critique node stops returning `revise` once the loop budget is exhausted.

6. How are citations created?
   The synthesis agent assigns stable citation IDs like `S01` to sources and maps each key finding to the source URL that supports it.

7. How does the system detect hallucination risk?
   The evaluation layer checks whether key findings have valid citation IDs. Uncited findings reduce hallucination resistance.

8. How is source credibility scored?
   The scoring function rewards high-trust domains such as government, education, regulator, and research domains, penalizes promotional hints, and adds a small bonus when raw content is available.

9. How is report confidence calculated?
   It combines mean evidence confidence, source diversity, source count, and contradiction penalties into a calibrated 0 to 1 score.

10. Why PostgreSQL?
    The entities have relational structure and need constraints: runs, sources, evidence, reports, events, and evaluations. PostgreSQL also supports JSONB for flexible structured output.

11. Why store agent events?
    Agent events create an audit trail for latency, inputs, outputs, failures, and execution behavior. They make debugging and trust review possible.

12. What is deterministic mode?
    Deterministic mode uses a non-network LLM provider and fallback search data so tests and portfolio demos can run without paid APIs.

13. What are the main API endpoints?
    Create/list/get/execute research runs, fetch reports, fetch sources, evaluate arbitrary reports, evaluate persisted runs, and health check.

14. How does the Tavily tool work?
    It accepts generated queries, calls Tavily search, asks for raw content, normalizes results into source candidates, deduplicates URLs, and scores credibility.

15. How are LLM providers abstracted?
    The `LLMProvider` protocol exposes `complete_json`. The LangChain provider wraps OpenAI or Anthropic, while deterministic mode implements the same interface.

16. Why force JSON output?
    Structured JSON is easier to validate, route, score, persist, and test than free-form text.

17. What happens when an LLM returns invalid JSON?
    Nodes catch exceptions where safe and use deterministic fallbacks for query generation or extraction. Unrecoverable failures are handled by the service and mark the run failed.

18. What makes the backend production-shaped?
    It includes FastAPI routes, Pydantic schemas, dependency injection, async SQLAlchemy, PostgreSQL migrations, structured errors, API key auth, Prometheus metrics, Docker, CI, and tests.

19. What is the role of the critique agent?
    It checks report confidence, identifies issues, creates follow-up queries, and routes the graph to revise, finalize, or fail.

20. What are support levels?
    Evidence can be labeled `supports`, `partially_supports`, `contradicts`, or `insufficient`.

21. Why store rejected evidence?
    Rejected evidence shows what was considered and excluded. It improves auditability and helps reviewers inspect weak or contradictory claims.

22. How would you improve semantic citation verification?
    Add claim-to-source entailment checks that compare each claim against quoted evidence and source snippets using an LLM judge or natural language inference model.

23. How would you handle rate limits?
    Add provider-level retry with exponential backoff, per-agent timeouts, request budgets, queue-based concurrency limits, and persistent retry state.

24. How would you scale graph execution?
    Move execution from FastAPI background tasks to a worker queue such as Celery, Dramatiq, Temporal, or a managed queue, while keeping the existing service boundary.

25. How would you add streaming updates?
    Emit graph node events to a pub/sub channel and expose server-sent events or WebSocket updates keyed by run ID.

26. How would you add user workspaces?
    Add organizations, users, memberships, and workspace IDs to runs, reports, sources, and evaluations, then enforce access control in repository queries.

27. How would you handle source deduplication?
    Normalize URLs, hash them, enforce `(run_id, url_hash)` uniqueness, and optionally canonicalize query parameters and redirects.

28. Why use JSONB for structured output?
    Research outputs vary by question, and JSONB allows flexible storage while still supporting indexed queries.

29. What is the biggest technical risk?
    Confidence can look precise while still depending on imperfect search coverage, extraction quality, and source credibility heuristics.

30. How do tests avoid external APIs?
    Tests use deterministic provider behavior and fake search tools to exercise graph contracts without live OpenAI, Anthropic, or Tavily calls.

31. What does the repository layer do?
    It creates and fetches runs, persists graph results, stores sources, evidence, reports, events, and evaluation results.

32. Why not make agents write directly to the database?
    Agents should transform state. Persistence belongs to the service/repository layer so graph logic remains testable and side effects are controlled.

33. How does FastAPI validation help?
    Pydantic validates request shape, query length, confidence ranges, source counts, and depth before execution starts.

34. How does the system expose observability?
    It exports Prometheus metrics, structured JSON logs, run statuses, failure reasons, and persisted agent events.

35. What would you log per agent in production?
    Agent name, run ID, event type, latency, token usage, model, provider, source count, evidence count, confidence score, and error details.

36. How would you add cost tracking?
    Capture token usage from provider responses, attach cost metadata by model, persist it in `agent_events.token_usage`, and aggregate per run.

37. How would you improve extraction quality?
    Chunk long source content, extract claims per chunk, deduplicate claims, cluster related evidence, and use source-aware extraction prompts.

38. How would you improve search quality?
    Add query expansion, domain filters, source type targets, reranking, freshness filters, adversarial searches, and source diversity constraints.

39. What is a confidence-gated loop?
    A graph loop that only repeats when the report confidence is below the requested threshold and the max iteration budget has not been reached.

40. How does the system handle failed runs?
    `ResearchService` catches execution exceptions, updates run status to `failed`, records `failure_reason`, logs the error, and re-raises for API handling.

41. Why include OpenAPI?
    It makes the API contract inspectable, usable by clients, and credible for engineering review.

42. Why include evaluation endpoints?
    Evaluation should be part of the product surface, not only a notebook. It lets reports be scored after generation.

43. How would you add human review?
    Add review states for evidence and reports, reviewer decisions, comments, and endpoints for accepting, rejecting, or editing evidence before synthesis.

44. How would you prevent prompt injection from sources?
    Treat source text as untrusted data, wrap it clearly in prompts, instruct models not to follow source instructions, and verify outputs against schema.

45. How would you add caching?
    Cache search results by normalized query, source fetches by URL hash, and provider responses by prompt hash for deterministic replays.

46. What is the value of structured output?
    It allows downstream workflows to consume findings, confidence, risks, open questions, and source coverage programmatically.

47. What is the value of storing raw content?
    It supports later re-verification, debugging, and semantic citation checks without re-fetching the source.

48. How would you handle deleted or changed web pages?
    Store retrieval timestamps, snippets, raw content, source metadata, and optionally archived snapshots.

49. Why is this not a toy MVP?
    It includes durable persistence, graph orchestration, role-specific agents, confidence loops, evaluation, tests, Docker, monitoring, CI, and complete documentation.

50. What would you demo first in an interview?
    I would show the graph, run a research question, inspect the stored report, show source/evidence records, then run evaluation metrics to prove traceability.

## 20 Architecture Questions With Ideal Answers

1. What are the primary service boundaries?
   API, service, repository, agent, provider, tool, and evaluation boundaries.

2. Why keep graph execution behind a service?
   The service coordinates persistence, status transitions, and error handling while the graph focuses on state transformation.

3. How would you scale this system to many concurrent users?
   Move execution to workers, add queueing, enforce rate limits, shard or pool database connections, cache source retrieval, and track per-user budgets.

4. What is the most important architecture tradeoff?
   The multi-agent graph improves traceability and quality control at the cost of latency, provider calls, and operational complexity.

5. Why not use a vector database as the primary database?
   The core lifecycle is relational and auditable. Vector storage is useful for semantic recall but not a replacement for run, evidence, report, and event records.

6. How would you add a vector database?
   Embed source chunks and evidence items, store vectors with source IDs, and use retrieval for follow-up runs, deduplication, and source memory.

7. How would you make executions resumable?
   Persist graph checkpoints, node outputs, and routing decisions, then resume from the last completed node after failure.

8. How would you make it multi-tenant?
   Add organization and user tables, attach tenant IDs to all run artifacts, enforce tenant filters in repositories, and add role-based access control.

9. How would you deploy it?
   Containerize API and worker services, provision PostgreSQL, configure secrets, run migrations, add metrics/logging, and place the API behind a load balancer.

10. What belongs in the database versus logs?
    Durable research artifacts and audit events belong in the database. Operational traces and high-cardinality runtime diagnostics belong in logs.

11. How does the design support provider switching?
    Provider-specific logic is isolated behind `LLMProvider`, and settings select OpenAI, Anthropic, or deterministic mode.

12. How would you handle model-specific prompt differences?
    Store prompt variants by model/provider and evaluate them against the same benchmark suite.

13. What is the failure domain of Tavily?
    Source discovery can fail or be incomplete. The graph can only verify sources it sees, so search quality is a critical dependency.

14. What is the failure domain of LLM providers?
    JSON failures, hallucinated extraction, latency, rate limits, and cost. The system mitigates this through schema prompts, fallbacks, evaluation, and service failure handling.

15. Why use async SQLAlchemy?
    FastAPI is async-friendly, and graph execution may involve concurrent I/O. Async persistence avoids blocking the event loop.

16. How would you isolate long-running jobs?
    Use a worker process with queue-backed jobs, status polling, cancellation, retries, and idempotency.

17. How would you handle schema evolution?
    Use versioned migrations, contract tests, backward-compatible API response changes, and report schema versions.

18. What is the system of record?
    PostgreSQL is the system of record for runs, sources, evidence, reports, events, and evaluations.

19. What should be immutable?
    Completed source records, evidence records, reports, and agent events should be treated as immutable audit artifacts.

20. Where would you add authorization?
    At API dependency level for coarse auth and repository level for tenant/user ownership checks.

## 20 Product Questions With Ideal Answers

1. Who is the first customer?
   A founder or analyst doing market diligence who needs fast, cited research before strategic decisions.

2. What is the core user value?
   Faster research with traceable evidence and calibrated confidence.

3. Why would users choose this over ChatGPT?
   It shows sources, stores evidence, verifies claims, rejects weak evidence, and exposes confidence instead of returning a single polished answer.

4. What is the wedge?
   Decision-ready market and competitive research for founders and consultants.

5. What is the aha moment?
   Seeing a final report where each key claim maps to a source and weak claims are excluded or flagged.

6. What is the main UX risk?
   Users may overtrust confidence scores unless uncertainty and source coverage are clearly displayed.

7. What should the first UI show?
   The active research run, source coverage, evidence status, confidence, and final report.

8. What should users be able to export?
   Markdown, PDF, DOCX, JSON structured output, source bibliography, and evidence table.

9. What is the product moat?
   Workflow quality, evaluation data, source memory, domain-specific benchmarks, and trusted research UX.

10. How would you price it?
    Usage-based pricing per research run with tiers based on source depth, team seats, export formats, and evaluation volume.

11. What is the riskiest assumption?
    That users will trust and pay for AI-generated research if it exposes evidence and confidence.

12. How would you validate demand?
    Run concierge research workflows for founders and consultants, compare time saved, and measure repeat usage.

13. What is the best first vertical?
    Startup market diligence because urgency is high and research quality directly affects fundraising and strategy.

14. What is a bad first vertical?
    Medical diagnosis because risk and regulatory requirements exceed the product’s current assurance level.

15. How does the product handle uncertainty?
    It scores confidence, lists risks, records open questions, rejects weak evidence, and can run another search loop.

16. What is a premium feature?
    Human-in-the-loop evidence review, team workspaces, source libraries, and client-ready exports.

17. What is the retention driver?
    Saved research history, trusted source memory, repeatable workflows, and team collaboration.

18. What should be measured after launch?
    Completion rate, report usefulness, source rework, citation accuracy, latency, cost per run, and repeat usage.

19. What would make users churn?
    Poor source quality, slow runs, confusing confidence scores, or reports that require too much manual correction.

20. How would you position it?
    Verified AI research infrastructure for professionals who need cited, inspectable answers.

## 20 Business Questions With Ideal Answers

1. What market does this serve?
   Professional research workflows across startups, consulting, analysis, journalism, and research teams.

2. What is the business model?
   SaaS with usage-based research runs, seat-based collaboration, and premium exports/evaluation.

3. Who pays?
   Founders, independent consultants, consulting teams, analyst teams, research orgs, and media teams.

4. Why now?
   LLM adoption is high, but trust and verification remain unresolved for professional research.

5. What is the competitive advantage?
   Transparent multi-agent verification, source tracking, evaluation metrics, and workflow integration.

6. What are substitutes?
   ChatGPT, Perplexity, manual analysts, consulting research teams, and internal knowledge tools.

7. How do you beat generic chatbots?
   By focusing on repeatable research operations, citation accuracy, source auditability, and structured outputs.

8. How do you beat manual research?
   By reducing cycle time while preserving source traceability and review paths.

9. What is the go-to-market?
   Start with founder and consultant workflows, publish example reports, sell to power users, then expand into teams.

10. What is a good pilot?
    A two-week pilot producing market diligence reports for a consulting team or accelerator portfolio.

11. What are expansion opportunities?
    Team workspaces, report libraries, source monitoring, competitive intelligence, exports, and domain-specific research packs.

12. What are the cost drivers?
    Search API calls, LLM tokens, source fetching, long context extraction, and graph retries.

13. How do you protect margins?
    Use source caching, prompt optimization, model routing, max source limits, and tiered pricing.

14. What is the main operational risk?
    Provider reliability and inconsistent source coverage.

15. What is the main trust risk?
    Users treating confidence as truth rather than calibrated evidence quality.

16. How would you create defensibility?
    Collect evaluation benchmarks, source-quality signals, user feedback, workflow data, and domain-specific report templates.

17. What would investors ask?
    Who is the initial buyer, what is the wedge, why will users switch, how accurate is it, and what prevents commoditization.

18. What is the answer to commoditization?
    The value is not the model alone; it is workflow, verification, evaluation, source memory, UX, and domain trust.

19. What is the long-term vision?
    A trusted research operating system that can answer complex questions, monitor sources, and produce audit-ready reports across domains.

20. What is the strongest business proof point?
    A measured reduction in research time with equal or better citation accuracy compared to manual workflows.

