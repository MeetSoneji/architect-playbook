# M0: Foundations: the Basics Everyone Skips

> **Bedrock:** OSTEP, Tanenbaum & van Steen 4e, Mixu, Google SRE Book, Dean & Barroso (*The Tail at Scale*),
> Chip Huyen (*AI Engineering*)

These are the ideas most engineers half-know and that every later concept silently depends on. Each one
must end with a **"you will need this for"** list linking forward to the later concepts that build on it.

What every concept in this module must emphasize (DEEP_DIVE reads this):

- **Mechanics:** what the hardware, kernel, or protocol actually does, not the API on top of it
- **Failure modes:** the misconceptions that cause real bugs ("write() means saved", "a timeout means it failed",
  "the clock only moves forward", "70% CPU is safe")
- **Tradeoffs:** the cost model each layer imposes (latency, throughput, memory, money)
- **AI-era bridge:** the same property showing up in LLM calls and agent runtimes
- **Labs:** measure or simulate, e.g. time fsync vs. write, simulate a queue at rising utilization, make a
  wall clock jump and break a timeout

| Id | Concept | Roadmap week | Needed later by |
|---|---|---|---|
| c23 | Latency Numbers, the Memory Hierarchy & Back-of-Envelope Math | 1 | c02, c24, c26, c29, c30 |
| c25 | Processes, Threads, Async I/O & Race Conditions | 1 | c08, c17, c27 |
| c24 | The Durability Path: Page Cache, fsync & What 'Written' Means | 2 | c01, c02 |
| c26 | TCP & HTTP in Practice: Connections, Timeouts & Half-Open Failures | 2 | c13, c17, c19, c28 |
| c27 | Time on Computers: Wall vs. Monotonic Clocks, NTP, Skew & Pauses | 3 | c05, c08 |
| c28 | Failure Models: Crash-Stop, Crash-Recovery, Byzantine & Partial Failure | 3 | c06, c10, c13 |
| c29 | Queueing Basics: Little's Law, Utilization & Tail Latency | 4 | c11, c14, c15, c30 |
| c30 | Anatomy of an LLM Call: Tokens, Context, Sampling, Latency & Cost | 4 | c19, c20, and every AI bridge |
