# Living Knowledge Base — Master Index

Status legend:
- `Queued` — Not yet started
- `In Progress` — Actively researching / building lab
- `Mastered` — Deep notes + failure modes + AI-era bridge + runnable lab complete

---

## Module 1: Storage, Data & State ([`kb_01_storage_and_data.md`](kb_01_storage_and_data.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Write-Ahead Logs (WAL) & Crash Recovery | `Queued` | OSTEP (Persistence), SQLite (AOSA) | — |
| B-Trees vs. LSM-Trees (Read/Write/Space Amp) | `Queued` | Bigtable / Dynamo papers | — |
| Partitioning, Sharding & Consistent Hashing | `Queued` | Dynamo paper, System Design Primer | — |
| Vector Indexes (HNSW/IVF) & Hybrid Agent Memory | `Queued` | Chip Huyen AI Engineering | — |

## Module 2: Distributed Coordination & Consistency ([`kb_02_distributed_coordination.md`](kb_02_distributed_coordination.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Physical vs. Logical & Vector Clocks | `Queued` | Mixu Ch. 2, Tanenbaum | — |
| CAP, PACELC & Linearizability vs. Eventual Consistency | `Queued` | Mixu Ch. 3, Tanenbaum | — |
| Consensus (Raft / Paxos) & Leader Election | `Queued` | MIT 6.824 (Raft) | — |
| Distributed Locks, Leases & Fencing Tokens | `Queued` | Martin Kleppmann / Tanenbaum | — |

## Module 3: Async Messaging & Backpressure ([`kb_03_async_and_backpressure.md`](kb_03_async_and_backpressure.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Message Queues vs. Event Logs | `Queued` | Designing Distributed Systems | — |
| Delivery Guarantees & Idempotency Keys | `Queued` | AWS Builders' Library | — |
| Backpressure, Bounded Queues & Dead Letter Queues | `Queued` | AWS Builders' Library, SRE | — |
| Durable Execution for Long-Running AI Agents | `Queued` | Anthropic Effective Agents | — |

## Module 4: Reliability & Production Guardrails ([`kb_04_reliability_and_guardrails.md`](kb_04_reliability_and_guardrails.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Timeouts, Retries with Exponential Backoff & Jitter | `Queued` | AWS Builders' Library | — |
| Circuit Breakers, Bulkheads & Load Shedding | `Queued` | Google SRE Book | — |
| SLIs, SLOs, Error Budgets & Token/Cost Budgets | `Queued` | Google SRE Book | — |
| Distributed Tracing & Non-Deterministic Agent Evals | `Queued` | Chip Huyen, Anthropic | — |

## Module 5: Network, Caching & Edge ([`kb_05_network_and_edge.md`](kb_05_network_and_edge.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Event Loops, Reverse Proxies & L4/L7 Load Balancing | `Queued` | Nginx (AOSA), OSTEP | — |
| Cache Patterns, Invalidation & Thundering Herd | `Queued` | System Design Primer | — |
| Semantic Caching, Prompt-Prefix Caching & SSE Streaming | `Queued` | Chip Huyen AI Engineering | — |

## Module 6: Agentic & AI System Architecture ([`kb_06_ai_agent_systems.md`](kb_06_ai_agent_systems.md))
| Concept | Status | Primary Bedrock | Lab |
| :--- | :--- | :--- | :--- |
| Deterministic Workflows vs. Autonomous Agents | `Queued` | Anthropic Effective Agents | — |
| Tool-Calling Contracts & Sandboxed Execution | `Queued` | Anthropic Effective Agents | — |
| Multi-Agent Orchestration & Context Engineering | `Queued` | Anthropic, Chip Huyen | — |
