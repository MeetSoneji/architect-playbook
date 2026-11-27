# Architect Playbook: First-Principles System Design for the AI Agent Era

> **In the AI era, syntax is cheap—architecture is expensive.**  
> When AI agents can generate functions and services in seconds, the real differentiator is **system-level judgment**: understanding state, consistency, failure modes, backpressure, observability, and how to orchestrate non-deterministic AI workflows safely in production.

This repository is a **living, open Single Source of Truth (SSOT)** designed to build deep, first-principles mastery across every layer of system design—bridging classic distributed systems fundamentals with modern AI agent architectures.

---

## Who This Is For
- **Engineers building foundations:** Clear, zero-fluff explanations starting from OS, storage, and networking primitives.
- **Experienced architects (10–25+ yrs):** Direct mapping of battle-tested distributed systems patterns to the new failure modes of LLM and multi-agent production systems.

---

## Structure

| Directory | Purpose |
| :--- | :--- |
| [`00_sources/MASTER_SOURCES.md`](00_sources/MASTER_SOURCES.md) | Curated, 100% free & open-access books, primary engineering libraries, papers, repos, and newsletters. |
| [`01_tier1_bedrock/`](01_tier1_bedrock/README.md) | Immutable foundational textbooks & primary guides. |
| [`02_living_kb/`](02_living_kb/kb_00_master_index.md) | Evolving, distilled deep-dive notes organized into 6 core modules. |
| [`03_inbox/`](03_inbox/weekly_drops.md) | Weekly staging area for new articles, newsletters, and papers before distillation. |
| [`04_labs/`](04_labs/README.md) | Runnable code prototypes proving internals (WAL, rate limiters, circuit breakers, idempotent queues). |
| [`05_publications/`](05_publications/README.md) | Polished deep-dive articles and visual breakdowns. |

---

## The 6 Core Modules

1. **Storage, Data & State** — B-Trees vs. LSM-Trees, WAL, partitioning, consistent hashing, vector indexes & agent memory.
2. **Distributed Coordination & Consistency** — Clocks, CAP/PACELC, linearizability, Raft/Paxos, multi-agent state races.
3. **Async Messaging & Backpressure** — Queues vs. event logs, delivery guarantees, idempotency, DLQs, durable agent execution.
4. **Reliability & Production Guardrails** — Cascading failures, circuit breakers, load shedding, SLOs/error budgets, token/cost budgets.
5. **Network, Caching & Edge** — TCP/HTTP, L4/L7 load balancing, CDN/cache invalidation, semantic/prefix caching, SSE streaming.
6. **Agentic & AI System Architecture** — Workflows vs. autonomous agents, tool contracts, sandboxing, evals, context engineering.

---

## How This Repo Evolves
This repo is designed to be operated with AI coding/research agents (see [`CLAUDE.md`](CLAUDE.md)):
1. **Capture** high-signal articles/papers into `03_inbox/weekly_drops.md`.
2. **Interrogate & Distill** against Tier 1 bedrock into `02_living_kb/`.
3. **Build** a minimal working prototype in `04_labs/`.
4. **Publish** clear, rigorous breakdowns in `05_publications/`.
