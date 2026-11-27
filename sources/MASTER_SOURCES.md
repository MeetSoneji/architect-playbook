# Master Sources (100% Free & Open-Access Single Source of Truth)

All sources below are legally free, open-access, and filtered for first-principles depth.

---

## 1. Free Foundational Books (PDF / Web)

| Resource | Author(s) | Link | Core Focus |
| :--- | :--- | :--- | :--- |
| **Operating Systems: Three Easy Pieces (OSTEP)** | Remzi & Andrea Arpaci-Dusseau | [ostep.org](https://www.ostep.org/) | Virtualization, concurrency (locks, threads, event loops), persistence (FS, crash consistency). |
| **Distributed Systems (4th Ed.)** | Maarten van Steen & Andrew S. Tanenbaum | [distributed-systems.net](https://www.distributed-systems.net/) | Communication, naming, coordination, replication, consistency models, fault tolerance. |
| **Distributed Systems: For Fun and Profit** | Mikito Takada | [book.mixu.net/distsys](https://book.mixu.net/distsys/) | Time/order, CAP, vector clocks, consensus, Dynamo/BigTable/MapReduce mental models. |
| **Google SRE Books** (*SRE*, *SRE Workbook*, *Building Secure & Reliable Systems*) | Google Engineering | [sre.google](https://sre.google/) | SLIs/SLOs, error budgets, cascading failures, load shedding, observability, incident response. |
| **The Architecture of Open Source Applications** (Vol. 1, 2, *500 Lines or Less*) | Amy Brown & Greg Wilson (Eds.) | [aosabook.org](https://aosabook.org/) | Real-world architecture & tradeoffs of Nginx, SQLite, Git, LLVM, HDFS, etc. |

---

## 2. Primary Engineering Libraries & University Courses

| Resource | Link | Core Focus |
| :--- | :--- | :--- |
| **Amazon Builders' Library** | [aws.amazon.com/builders-library](https://aws.amazon.com/builders-library/) | Retries with jitter, idempotency, timeouts, shuffle sharding, overload protection. |
| **Martin Fowler's Software Architecture Guide** | [martinfowler.com/architecture](https://martinfowler.com/architecture/) | Event sourcing, CQRS, microservices vs. monoliths, DDD, evolutionary architecture. |
| **Brendan Gregg's Performance Site** | [brendangregg.com](https://www.brendangregg.com/) | USE Method, Flame Graphs, Linux `perf`/eBPF performance analysis. |
| **MIT 6.824 / 6.5840: Distributed Systems** | [pdos.csail.mit.edu/6.824](https://pdos.csail.mit.edu/6.824/) | Lectures, Raft/GFS/Dynamo/Spanner papers, fault-tolerant lab specs. |
| **Netflix TechBlog** | [netflixtechblog.com](https://netflixtechblog.com/) | Cloud resilience, chaos engineering, streaming pipelines, global scale. |

---

## 3. Free AI-Era & Agentic Architecture (Primary Sources)

| Resource | Author / Org | Link | Core Focus |
| :--- | :--- | :--- | :--- |
| **Building Effective Agents** | Anthropic | [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents) | Workflows vs. autonomous agents, prompt chaining, routing, orchestrator-workers, evaluator-optimizer, tool design. |
| **AI Engineering Companion Hub** | Chip Huyen | [github.com/chiphuyen/aie-book](https://github.com/chiphuyen/aie-book) & [huyenchip.com](https://huyenchip.com/) | Production AI stack, evaluations, RAG/context engineering, latency/cost optimization. |

---

## 4. Open-Source GitHub Repositories

| Repository | Link | Focus |
| :--- | :--- | :--- |
| **System Design Primer** | [github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | Trade-off analyses and classic large-scale system walkthroughs. |
| **Papers We Love** | [github.com/papers-we-love/papers-we-love](https://github.com/papers-we-love/papers-we-love) | Landmark CS papers (Paxos, Raft, Chubby, Dynamo, GFS). |
| **Designing Distributed Systems** | [github.com/brendandburns/designing-distributed-systems](https://github.com/brendandburns/designing-distributed-systems) | Container & cloud-native patterns (sidecars, queues, scatter/gather, leader election). |
| **ByteByteGo: System Design 101** | [github.com/ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | Visual mental models for modern infrastructure. |
| **Awesome Scalability** | [github.com/binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | Curated patterns of scalable, reliable, and performant systems. |
| **Awesome System Design Resources** | [github.com/ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) | Core concepts + Big Tech engineering case studies. |

---

## 5. High-Signal Newsletters & Voices

- **Architecture Notes** (Mahdi Yusuf) — [architecturenotes.co](https://architecturenotes.co/)
- **Arpit Bhayani** — Deep first-principles internals (databases, caching, consensus, concurrency)
- **The System Design Newsletter** (Neo Kim) — Structured architectural frameworks
- **Quastor** — Summaries & breakdowns of Big Tech engineering blog posts
- **Alex Xu** (*ByteByteGo*) — Visual architecture breakdowns

---

## 6. Incidents & Postmortems (for §3 "Incidents in the wild")

| Resource | Link | Use |
| :--- | :--- | :--- |
| **Dan Luu's post-mortems collection** | [github.com/danluu/post-mortems](https://github.com/danluu/post-mortems) | Index of public postmortems by category (config, time, database, hardware). |
| **AWS Post-Event Summaries** | [aws.amazon.com/premiumsupport/technology/pes](https://aws.amazon.com/premiumsupport/technology/pes/) | Primary write-ups of large AWS outages (e.g. us-east-1 events). |
| **Google Cloud status incident reports** | [status.cloud.google.com](https://status.cloud.google.com/) | Detailed incident reports with root causes. |
| **Cloudflare Blog (postmortems)** | [blog.cloudflare.com](https://blog.cloudflare.com/) | Unusually detailed outage analyses (BGP, config pushes, regex CPU exhaustion). |
| **Jepsen analyses** | [jepsen.io/analyses](https://jepsen.io/analyses) | Consistency and safety bugs found in real databases and queues. |
| **Metastable Failures in Distributed Systems** (Bronson et al., HotOS 2021) | [sigops.org](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf) | Why retry storms and overload loops persist after the trigger is gone. |
