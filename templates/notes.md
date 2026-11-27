---
id: {{id}}
title: "{{title}}"
module: "{{module}}"
requires: "{{requires}}"
bedrock: "{{bedrock}}"
last_ingest: never
---

# {{id}} · {{title}}

> **Reader baseline.** You have shipped backend code: you know HTTP, a SQL database, threads,
> and what a process crash is. Everything beyond that is built up here, and every term is
> defined the first time it appears.

> **The AI-era question this answers:** {{ai_question}}

## 0. Why this exists
<!-- FILL: Start from the AI-era question above, then show that it is an instance of a classic
     problem distributed systems solved decades ago. One story a working engineer has lived through.
     What breaks if this mechanism did not exist? State what the reader is assumed to know
     and link the prerequisite concepts (requires) by relative path. -->

## 1. First-principles mechanics
<!-- FILL: What physically happens: bytes on disk, messages on the wire, locks in memory,
     states in a state machine. Walk one operation end to end, step by step. Include at least
     one diagram (mermaid or ASCII) and the key numbers (latency, sizes, fsync cost) with a citation. -->

## 2. Failure modes & edge cases
<!-- FILL: For each failure: trigger, what the system does, what the user sees, how you detect it.
     Cover crash mid-operation, partial failure, partition, clock skew, 10x and 100x load. -->

## 3. Incidents in the wild
<!-- FILL: At least 2 public postmortems or incident write-ups where this mechanism (or its absence)
     was the root cause or the save. For each: link, date, one-paragraph timeline, the exact
     mechanism that failed, and what changed afterwards. -->

## 4. Explicit tradeoffs
<!-- FILL: What you give up to get this. Name the alternative designs and when each wins.
     A table is welcome; every row needs a reason, not just a label. -->

## 5. Where it is used
<!-- FILL: Real systems that use this mechanism (named databases, brokers, services) and how
     their choices differ. Include one use case where it is the WRONG tool. -->

## 6. AI-agent era bridge
<!-- FILL: How this exact mechanism protects or breaks LLM / agent systems in production:
     tool calls, retries of non-deterministic steps, token cost, agent memory, multi-agent state.
     Make it concrete: a design, not a metaphor. -->

## 7. Lab spec
<!-- FILL: The invariant the lab proves, the fault it injects, the negative control
     (system without the mechanism visibly breaks) and the recovery test. -->

## 8. Veteran's corner
<!-- FILL: The non-obvious insight a 25-year engineer would still learn something from:
     a subtle interaction, a common misconception in famous systems, a modern twist. -->

## 9. Open questions & contradictions
<!-- FILL: Where sources disagree, what you could not verify, what a later INGEST should look for. -->

## 10. Adversarial self-review
<!-- FILL: Written by the reviewer pass in DEEP_DIVE (workflows/DEEP_DIVE.md step 6).
     The strongest attacks on these notes and how each was resolved. -->

## Sources
<!-- FILL: At least 3. Format: - [Title](url), Author, year, section/page. Bedrock first. -->
