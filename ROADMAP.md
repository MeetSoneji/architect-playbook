# Roadmap

**Thesis:** every hard problem in production AI is a distributed-systems problem wearing a new name. An
agent resuming after a crash is a write-ahead log. A retried tool call that double-charges a card is a
missing idempotency key. A provider outage that takes down your app is a missing circuit breaker. So the
roadmap is ordered by *what an AI system needs first to survive production*, not by textbook chapter.

**Pace:** two foundation concepts per week for the first 4 weeks, then one concept per week, pipelined
(see [AUTOMATION.md](AUTOMATION.md)). 30 concepts, 4 capstones, and buffer weeks: **32 weeks, Nov 30 2026
to mid-July 2027.** If you fall behind, automation slows down
with you (WIP limit), so the dates are a target, not a treadmill.

**The running project.** The four capstones build one thing that grows: a small **reference agent runtime**
(`capstones/agent-runtime/`, created in week 12). Each phase adds a layer, so by the end you have built,
from first principles, the skeleton every serious agent platform has.

## Phase 0 — The basics everyone skips (weeks 1–4)
*The handful of facts about hardware, kernels, networks, time, and LLM calls that every later concept
assumes. Most production bugs come from believing a comfortable half-truth about one of them.*

- W1 **c23** latency numbers & the memory hierarchy · **c25** processes, threads, async I/O & races
- W2 **c24** page cache, fsync & what "written" means · **c26** TCP & HTTP in practice
- W3 **c27** time on computers (wall vs. monotonic, NTP, pauses) · **c28** failure models & partial failure
- W4 **c29** queueing: Little's Law, utilization & tail latency · **c30** anatomy of an LLM call
- *W5 buffer (holidays)*

## Phase 1 — One request, done right (weeks 6–12)
*An agent makes a paid, side-effecting call to a slow, flaky provider. Make that one call safe.*

Start with the log because every later idea (queues, replication, consensus, durable execution) is a log
in disguise. Then delivery semantics, because retries are useless without idempotency, and retries come
next. Backpressure and circuit breakers close the loop on overload.

- W6 **c01** WAL & crash recovery → W7 **c09** queues vs. logs → W8 **c10** delivery guarantees & idempotency
  → W9 **c13** timeouts, retries, jitter → W10 **c11** backpressure & DLQs
  → W11 **c14** circuit breakers, bulkheads, load shedding
- **W12 Capstone 1:** a durable, idempotent tool-call queue in front of a fake LLM provider that returns 429s
  and hangs. Prove: no lost task, no double side effect, no retry storm, graceful shedding.

## Phase 2 — Data that outgrows one machine (weeks 13–17)
*Your agent platform now has many tenants, lots of state, and a hot cache.*

- W13 **c02** B-Trees vs. LSM → W14 **c03** partitioning & consistent hashing
  → W15 **c17** event loops, proxies, L4/L7 load balancing → W16 **c18** cache patterns & thundering herd
- **W17 Capstone 2:** add a sharded session store and a streaming gateway with request coalescing.
  Prove: a hot tenant or a cache expiry does not cascade.

## Phase 3 — Agreement under partial failure (weeks 18–23)
*Several workers, one plan. Who is in charge, what happened first, and who may act?*

- W18 **c05** clocks → W19 **c06** CAP, PACELC, linearizability → W20–21 **c07** Raft & leader election
  → W22 **c08** locks, leases, fencing tokens
- **W23 Capstone 3:** a leader-elected scheduler for agent jobs with fenced side effects.
  Prove: a paused (GC/VM) old leader cannot perform a stale action.

## Phase 4 — Seeing and budgeting production (weeks 24–25)
*You cannot run what you cannot measure, and LLM spend is a reliability problem.*

- W24 **c15** SLIs, SLOs, error budgets & token budgets → W25 **c16** distributed tracing & agent evals

## Phase 5 — Agents as distributed systems (weeks 26–32)
*Everything above, applied to the agent loop itself.*

- W26 **c20** workflows vs. agents → W27 **c21** tool contracts & sandboxing → W28 **c12** durable execution
  → W29 **c04** vector indexes & agent memory → W30 **c19** semantic/prefix caching & SSE
  → W31–32 **c22** multi-agent orchestration & context engineering
- **W32 Capstone 4:** the runtime gets budgets, tracing, durable multi-step workflows, sandboxed tools, and
  two cooperating agents sharing memory safely. Write the architecture review of your own system with
  `/challenge`.

## After week 32
INGEST keeps running weekly, so mastered concepts keep getting sharper. New concepts are added to
`curriculum.toml` with the next free id (likely candidates: consensus-backed config, CRDTs for collaborative
agents, inference serving and batching, GPU scheduling, data pipelines for evals).

## Schedule
<!-- BEGIN:schedule -->
| Week | Starts | Id | Concept | The AI-era question it answers | Stage |
|---|---|---|---|---|---|
| 1 | Nov 30 2026 | c23 | Latency Numbers, the Memory Hierarchy & Back-of-Envelope Math | Why does one LLM call take 2 s when a database read takes 0.2 ms, and what does that gap do to every design choice? | `queued` |
| 1 | Nov 30 2026 | c25 | Processes, Threads, Async I/O & Race Conditions | Your agent server runs 200 tool calls at once. Are those threads, processes, or async tasks, and where can they race? | `queued` |
| 2 | Dec 07 2026 | c24 | The Durability Path: Page Cache, fsync & What 'Written' Means | Your agent saved its checkpoint and the machine lost power. Was it really saved? | `queued` |
| 2 | Dec 07 2026 | c26 | TCP & HTTP in Practice: Connections, Timeouts & Half-Open Failures | A streaming LLM response stalls halfway. Is the connection dead, slow, or half-open, and who decides? | `queued` |
| 3 | Dec 14 2026 | c27 | Time on Computers: Wall vs. Monotonic Clocks, NTP, Skew & Pauses | Your rate limiter and your agent's timeout both read the clock. What happens when the clock jumps? | `queued` |
| 3 | Dec 14 2026 | c28 | Failure Models: Crash-Stop, Crash-Recovery, Byzantine & Partial Failure | The tool call timed out. Did it run? Why can't the caller ever be sure? | `queued` |
| 4 | Dec 21 2026 | c29 | Queueing Basics: Little's Law, Utilization & Tail Latency | Your LLM gateway is 80% busy and p99 latency just tripled. Why does the last 20% hurt so much? | `queued` |
| 4 | Dec 21 2026 | c30 | Anatomy of an LLM Call: Tokens, Context, Sampling, Latency & Cost | What actually happens inside one LLM API call, and which of its properties (latency, cost, non-determinism, limits) does your architecture have to absorb? | `queued` |
| 6 | Jan 04 2027 | c01 | Write-Ahead Logs (WAL) & Crash Recovery | An agent crashes on step 7 of 12. How does it resume without redoing paid LLM calls or side effects? | `queued` |
| 7 | Jan 11 2027 | c09 | Message Queues vs. Event Logs | Should agent tasks go through a queue or an event log, and why does replayability matter for debugging agents? | `queued` |
| 8 | Jan 18 2027 | c10 | Delivery Guarantees & Idempotency Keys | The LLM retried a tool call that already charged the card. How do idempotency keys make tool calls safe to repeat? | `queued` |
| 9 | Jan 25 2027 | c13 | Timeouts, Retries with Exponential Backoff & Jitter | An LLM call hangs for 90 s. What timeout, how many retries, and how do you avoid a retry storm against the provider? | `queued` |
| 10 | Feb 01 2027 | c11 | Backpressure, Bounded Queues & Dead Letter Queues | The model provider is rate-limiting you and requests pile up. Where do they wait, and which ones do you drop? | `queued` |
| 11 | Feb 08 2027 | c14 | Circuit Breakers, Bulkheads & Load Shedding | The model provider is degraded. How do you fail fast, fall back to another model, and protect everything else? | `queued` |
| 13 | Feb 22 2027 | c02 | B-Trees vs. LSM-Trees (Read/Write/Space Amplification) | Why do agent memory stores and vector DBs pick LSM-style storage, and what does compaction do to retrieval latency? | `queued` |
| 14 | Mar 01 2027 | c03 | Partitioning, Sharding & Consistent Hashing | How do you shard agent sessions, embeddings and tenants so one hot customer cannot melt the cluster? | `queued` |
| 15 | Mar 08 2027 | c17 | Event Loops, Reverse Proxies & L4/L7 Load Balancing | How do gateways hold thousands of slow streaming LLM connections open without a thread per user? | `queued` |
| 16 | Mar 15 2027 | c18 | Cache Patterns, Invalidation & Thundering Herd | A popular prompt's cached answer expires and 10,000 requests hit the model at once. What now? | `queued` |
| 18 | Mar 29 2027 | c05 | Physical vs. Logical & Vector Clocks | Two agents edit the same plan. Which change happened first, when their clocks disagree? | `queued` |
| 19 | Apr 05 2027 | c06 | CAP, PACELC & Linearizability vs. Eventual Consistency | Should an agent read its shared memory from a replica that may be stale? What does 'consistent' even mean for agents? | `queued` |
| 20 | Apr 12 2027 | c07 | Consensus (Raft / Paxos) & Leader Election | Who is the single coordinator of a multi-agent run, and what happens when it dies mid-plan? | `queued` |
| 22 | Apr 26 2027 | c08 | Distributed Locks, Leases & Fencing Tokens | Two workers both think they hold the lock on the same tool action. How do you stop the duplicate refund? | `queued` |
| 24 | May 10 2027 | c15 | SLIs, SLOs, Error Budgets & Token/Cost Budgets | How do you set an SLO for a non-deterministic system, and treat token spend as an error budget? | `queued` |
| 25 | May 17 2027 | c16 | Distributed Tracing & Non-Deterministic Agent Evals | How do you trace one user request through 40 LLM and tool calls, and evaluate output that differs every run? | `queued` |
| 26 | May 24 2027 | c20 | Deterministic Workflows vs. Autonomous Agents | When should you hard-code the workflow and when should the model decide the next step? | `queued` |
| 27 | May 31 2027 | c21 | Tool-Calling Contracts & Sandboxed Execution | How do you design a tool interface the model cannot misuse, and contain the blast radius when it does? | `queued` |
| 28 | Jun 07 2027 | c12 | Durable Execution for Long-Running AI Agents | How do you run an agent for hours or days, across deploys and crashes, as a durable workflow? | `queued` |
| 29 | Jun 14 2027 | c04 | Vector Indexes (HNSW/IVF) & Hybrid Agent Memory | What is an agent's long-term memory physically, and why does approximate search silently return the wrong context? | `queued` |
| 30 | Jun 21 2027 | c19 | Semantic Caching, Prompt-Prefix Caching & SSE Streaming | When is it safe to serve a cached answer for a 'similar' prompt, and how does prefix caching cut cost? | `queued` |
| 31 | Jun 28 2027 | c22 | Multi-Agent Orchestration & Context Engineering | How do many agents share context and state without races, runaway loops, or context rot? | `queued` |
<!-- END:schedule -->
