# M4: Reliability & Production Guardrails

> **Bedrock:** Google SRE books, Amazon Builders' Library

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** Sliding windows, token buckets, error budgets, retry amplification
- **Failure modes:** Retry storms, cascading failures, metastable failures, silent degradation
- **Tradeoffs:** Availability vs. correctness under overload; strict vs. false-positive shedding
- **AI-era bridge:** Runaway agent loops, token/cost budgets as error budgets, model fallback routing, non-deterministic tracing

| Id | Concept | Roadmap week |
|---|---|---|
| c13 | Timeouts, Retries with Exponential Backoff & Jitter | 4 |
| c14 | Circuit Breakers, Bulkheads & Load Shedding | 7 |
| c15 | SLIs, SLOs, Error Budgets & Token/Cost Budgets | 20 |
| c16 | Distributed Tracing & Non-Deterministic Agent Evals | 21 |
