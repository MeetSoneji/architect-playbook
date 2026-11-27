# Roadmap

**Thesis:** every hard problem in production AI is a distributed-systems problem wearing a new name. An
agent resuming after a crash is a write-ahead log. A retried tool call that double-charges a card is a
missing idempotency key. A provider outage that takes down your app is a missing circuit breaker.

**One list, in order.** `curriculum.toml` holds 38 items in a single serial order (`seq`), grouped into 7
tracks. Similar concepts sit next to each other so each one builds on the last, and every track closes with
real-world **case studies** (📖) where you watch the track's ideas hold or fail in a real system.

**Pace:** two a week, Monday and Thursday at 07:00 IST, from **Mon Nov 30 2026 to Thu Apr 8 2027**. Each
run produces one item end to end (notes, blog post, narrated video) as one pull request. The dates below
are when that PR opens. If you fall behind on merging, automation pauses at four open PRs, so nothing
piles up unread.

## The tracks

**T1 · Foundations: the basics everyone skips (Nov 30 – Dec 28).** Latency numbers, threads and races,
fsync, TCP, clocks, failure models, queueing, and the anatomy of an LLM call. Every later concept assumes
these, and most production bugs come from a comfortable half-truth about one of them.
📖 *How a leap second broke Cloudflare DNS*: clocks and failure models in one real outage.

**T2 · Storage and state (Dec 31 – Jan 14).** The log comes first because queues, replication, consensus
and durable execution are all logs in disguise. Then how storage engines trade reads for writes, how data
splits across machines, and the vector indexes behind agent memory.
📖 *How Discord stores trillions of messages*: three databases and the migrations between them.

**T3 · One request, done right (Jan 18 – Feb 8).** An agent makes a paid, side-effecting call to a slow,
flaky provider. Queues vs. logs, idempotency, retries with jitter, backpressure, circuit breakers.
📖 *Stripe's idempotency keys* and 📖 *metastable failures and the AWS us-east-1 outage*: one design that
makes retries safe, and one outage where retries made everything worse.

**T4 · Agreement under partial failure (Feb 11 – Feb 25).** Several workers, one plan. Who is in charge,
what happened first, and who may act: clocks, CAP, Raft, locks, leases and fencing tokens.
📖 *Cloudflare's partial partition and etcd*: consensus behaving exactly as designed, and still causing an outage.

**T5 · Edge, caching and streaming (Mar 1 – Mar 11).** Load balancers, caches and stampedes, then the
AI versions: semantic caching, prompt-prefix caching and token streaming.
📖 *Scaling Memcache at Facebook*: leases, gutter pools and the thundering herd at billions of requests.

**T6 · Seeing and budgeting production (Mar 15 – Mar 18).** SLOs, error budgets and token budgets;
tracing and evals for non-deterministic agents.

**T7 · Agents as distributed systems (Mar 22 – Apr 8).** Workflows vs. agents, tool contracts and
sandboxing, durable execution, multi-agent orchestration and context engineering.
📖 *How Anthropic built its multi-agent research system* and 📖 *a production agent runtime, end to end*:
everything from T1 to T7 in one design.

## After item 38
INGEST keeps running every Sunday, so published concepts keep getting sharper. New items are added to
`curriculum.toml` with the next free id and a `seq` (likely candidates: CRDTs for collaborative agents,
inference serving and batching, GPU scheduling, data pipelines for evals, more case studies).

## Schedule
<!-- BEGIN:schedule -->
| # | Release | Track | Id | Concept | The AI-era question it answers | Stage |
|---|---|---|---|---|---|---|
| 1 | Mon Nov 30 2026 | t1 | c23 | Latency Numbers, the Memory Hierarchy & Back-of-Envelope Math | Why does one LLM call take 2 s when a database read takes 0.2 ms, and what does that gap do to every design choice? | `queued` |
| 2 | Thu Dec 03 2026 | t1 | c25 | Processes, Threads, Async I/O & Race Conditions | Your agent server runs 200 tool calls at once. Are those threads, processes, or async tasks, and where can they race? | `queued` |
| 3 | Mon Dec 07 2026 | t1 | c24 | The Durability Path: Page Cache, fsync & What 'Written' Means | Your agent saved its checkpoint and the machine lost power. Was it really saved? | `queued` |
| 4 | Thu Dec 10 2026 | t1 | c26 | TCP & HTTP in Practice: Connections, Timeouts & Half-Open Failures | A streaming LLM response stalls halfway. Is the connection dead, slow, or half-open, and who decides? | `queued` |
| 5 | Mon Dec 14 2026 | t1 | c27 | Time on Computers: Wall vs. Monotonic Clocks, NTP, Skew & Pauses | Your rate limiter and your agent's timeout both read the clock. What happens when the clock jumps? | `queued` |
| 6 | Thu Dec 17 2026 | t1 | c28 | Failure Models: Crash-Stop, Crash-Recovery, Byzantine & Partial Failure | The tool call timed out. Did it run? Why can't the caller ever be sure? | `queued` |
| 7 | Mon Dec 21 2026 | t1 | c29 | Queueing Basics: Little's Law, Utilization & Tail Latency | Your LLM gateway is 80% busy and p99 latency just tripled. Why does the last 20% hurt so much? | `queued` |
| 8 | Thu Dec 24 2026 | t1 | c30 | Anatomy of an LLM Call: Tokens, Context, Sampling, Latency & Cost | What actually happens inside one LLM API call, and which of its properties (latency, cost, non-determinism, limits) does your architecture have to absorb? | `queued` |
| 9 | Mon Dec 28 2026 | t1 | c31 | 📖 Case Study: How a Leap Second Broke Cloudflare DNS (2017) | A clock went backwards for one second. Why did that crash production code, and what does it mean for every timeout and rate limit in an agent platform? | `queued` |
| 10 | Thu Dec 31 2026 | t2 | c01 | Write-Ahead Logs (WAL) & Crash Recovery | An agent crashes on step 7 of 12. How does it resume without redoing paid LLM calls or side effects? | `published` |
| 11 | Mon Jan 04 2027 | t2 | c02 | B-Trees vs. LSM-Trees (Read/Write/Space Amplification) | Why do agent memory stores and vector DBs pick LSM-style storage, and what does compaction do to retrieval latency? | `queued` |
| 12 | Thu Jan 07 2027 | t2 | c03 | Partitioning, Sharding & Consistent Hashing | How do you shard agent sessions, embeddings and tenants so one hot customer cannot melt the cluster? | `queued` |
| 13 | Mon Jan 11 2027 | t2 | c04 | Vector Indexes (HNSW/IVF) & Hybrid Agent Memory | What is an agent's long-term memory physically, and why does approximate search silently return the wrong context? | `queued` |
| 14 | Thu Jan 14 2027 | t2 | c32 | 📖 Case Study: How Discord Stores Trillions of Messages | How did Discord's message store evolve from MongoDB to Cassandra to ScyllaDB, and what does that teach about storing every agent conversation forever? | `queued` |
| 15 | Mon Jan 18 2027 | t3 | c09 | Message Queues vs. Event Logs | Should agent tasks go through a queue or an event log, and why does replayability matter for debugging agents? | `queued` |
| 16 | Thu Jan 21 2027 | t3 | c10 | Delivery Guarantees & Idempotency Keys | The LLM retried a tool call that already charged the card. How do idempotency keys make tool calls safe to repeat? | `queued` |
| 17 | Mon Jan 25 2027 | t3 | c13 | Timeouts, Retries with Exponential Backoff & Jitter | An LLM call hangs for 90 s. What timeout, how many retries, and how do you avoid a retry storm against the provider? | `queued` |
| 18 | Thu Jan 28 2027 | t3 | c11 | Backpressure, Bounded Queues & Dead Letter Queues | The model provider is rate-limiting you and requests pile up. Where do they wait, and which ones do you drop? | `queued` |
| 19 | Mon Feb 01 2027 | t3 | c14 | Circuit Breakers, Bulkheads & Load Shedding | The model provider is degraded. How do you fail fast, fall back to another model, and protect everything else? | `queued` |
| 20 | Thu Feb 04 2027 | t3 | c33 | 📖 Case Study: Stripe's Idempotency Keys | How does Stripe let clients retry payment calls safely, and how do you copy that design for agent tool calls? | `queued` |
| 21 | Mon Feb 08 2027 | t3 | c34 | 📖 Case Study: Metastable Failures and the AWS us-east-1 Outage (December 2021) | Why do some overloads keep a system down after the trigger is gone, and how do retrying agents turn a blip into an outage? | `queued` |
| 22 | Thu Feb 11 2027 | t4 | c05 | Physical vs. Logical & Vector Clocks | Two agents edit the same plan. Which change happened first, when their clocks disagree? | `queued` |
| 23 | Mon Feb 15 2027 | t4 | c06 | CAP, PACELC & Linearizability vs. Eventual Consistency | Should an agent read its shared memory from a replica that may be stale? What does 'consistent' even mean for agents? | `queued` |
| 24 | Thu Feb 18 2027 | t4 | c07 | Consensus (Raft / Paxos) & Leader Election | Who is the single coordinator of a multi-agent run, and what happens when it dies mid-plan? | `queued` |
| 25 | Mon Feb 22 2027 | t4 | c08 | Distributed Locks, Leases & Fencing Tokens | Two workers both think they hold the lock on the same tool action. How do you stop the duplicate refund? | `queued` |
| 26 | Thu Feb 25 2027 | t4 | c35 | 📖 Case Study: Cloudflare's Partial Network Partition and etcd (2020) | What happens to a Raft cluster when the network fails only in one direction, and what does that mean for agents that coordinate through a shared store? | `queued` |
| 27 | Mon Mar 01 2027 | t5 | c17 | Event Loops, Reverse Proxies & L4/L7 Load Balancing | How do gateways hold thousands of slow streaming LLM connections open without a thread per user? | `queued` |
| 28 | Thu Mar 04 2027 | t5 | c18 | Cache Patterns, Invalidation & Thundering Herd | A popular prompt's cached answer expires and 10,000 requests hit the model at once. What now? | `queued` |
| 29 | Mon Mar 08 2027 | t5 | c19 | Semantic Caching, Prompt-Prefix Caching & SSE Streaming | When is it safe to serve a cached answer for a 'similar' prompt, and how does prefix caching cut cost? | `queued` |
| 30 | Thu Mar 11 2027 | t5 | c36 | 📖 Case Study: Scaling Memcache at Facebook | How did Facebook stop thundering herds and stale reads across billions of cache requests, and which of those tricks apply to caching LLM answers? | `queued` |
| 31 | Mon Mar 15 2027 | t6 | c15 | SLIs, SLOs, Error Budgets & Token/Cost Budgets | How do you set an SLO for a non-deterministic system, and treat token spend as an error budget? | `queued` |
| 32 | Thu Mar 18 2027 | t6 | c16 | Distributed Tracing & Non-Deterministic Agent Evals | How do you trace one user request through 40 LLM and tool calls, and evaluate output that differs every run? | `queued` |
| 33 | Mon Mar 22 2027 | t7 | c20 | Deterministic Workflows vs. Autonomous Agents | When should you hard-code the workflow and when should the model decide the next step? | `queued` |
| 34 | Thu Mar 25 2027 | t7 | c21 | Tool-Calling Contracts & Sandboxed Execution | How do you design a tool interface the model cannot misuse, and contain the blast radius when it does? | `queued` |
| 35 | Mon Mar 29 2027 | t7 | c12 | Durable Execution for Long-Running AI Agents | How do you run an agent for hours or days, across deploys and crashes, as a durable workflow? | `queued` |
| 36 | Thu Apr 01 2027 | t7 | c22 | Multi-Agent Orchestration & Context Engineering | How do many agents share context and state without races, runaway loops, or context rot? | `queued` |
| 37 | Mon Apr 05 2027 | t7 | c37 | 📖 Case Study: How Anthropic Built Its Multi-Agent Research System | What did a production multi-agent system need beyond the prompts: orchestration, state, evals and failure recovery? | `queued` |
| 38 | Thu Apr 08 2027 | t7 | c38 | 📖 Case Study: Designing a Production Agent Runtime End to End | Put every concept together: how would you design an agent platform that survives crashes, overload, partitions and runaway cost? | `queued` |
<!-- END:schedule -->
