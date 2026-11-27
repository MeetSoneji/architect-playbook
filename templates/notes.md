---
id: {{id}}
title: "{{title}}"
module: "{{module}}"
requires: "{{requires}}"
bedrock: "{{bedrock}}"
last_ingest: never
---

# {{id}} · {{title}}

> **Reader baseline:** you have shipped backend code. You know HTTP, a SQL database, threads, and what a
> process crash is. Everything beyond that is defined the first time it appears.
>
> **Builds on:** {{requires}}

Every concept page uses the same eight parts in the same order, so you always know where to look.
Parts 1–8 are the explanation. *Going deeper* is for the second read.

## 1. The AI problem it prevents
<!-- FILL: Open with the production AI problem: {{ai_question}}
     Tell it as a short, concrete story (what the agent was doing, what broke, what it cost).
     Then one sentence: "This is an old problem. Distributed systems call it X." -->

## 2. Intuition
<!-- FILL: An everyday analogy that is *mechanically* faithful (say where it breaks down), then one
     mermaid diagram of the core idea. A reader who stops here should still have the right mental model. -->

## 3. Mechanics, step by step
<!-- FILL: Walk one operation end to end in numbered steps: bytes on disk, messages on the wire, states in
     a state machine. Define each term on first use. Include the key numbers with citations, or say
     "measure it" and point at the lab. -->

## 4. Break it
<!-- FILL: The ways it fails (trigger → what happens → what the user sees → how you detect it), then the lab:
     the fault injected, the naive version failing (real output), the mechanism surviving (real output),
     and the exact lines of code that make the difference. Link lab/README.md. -->

## 5. Real incidents
<!-- FILL: At least 2 public postmortems or write-ups, linked. For each: what happened, the exact
     mechanism that failed, and what changed afterwards. -->

## 6. Tradeoffs and where it is used
<!-- FILL: What you pay for this, the alternatives and when each wins, the named systems that use it and
     how their choices differ, and one case where it is the wrong tool. -->

## 7. Apply it to agents
<!-- FILL: A concrete design for the AI problem in part 1, built from this mechanism. Not a metaphor:
     records, fields, the order of writes, what happens on restart. Link the lab if it covers this. -->

## 8. Check yourself
<!-- FILL: 5–8 questions that test understanding, not recall (answers in a collapsed <details> block),
     and one open design challenge to bring to /challenge. -->

## Going deeper
<!-- FILL: Three short subsections:
     ### Veteran's corner (the non-obvious insight a 25-year engineer would still learn from)
     ### Open questions (where sources disagree, what to look for in future INGEST runs)
     ### Self-review (the strongest attacks the reviewer pass made on this page, and how each was resolved) -->

## Sources
<!-- FILL: At least 3. Format: - [Title](url), Author, year, section/page. Bedrock first. -->
