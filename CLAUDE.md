# CLAUDE.md — Architect Playbook Operating Instructions

> This repository is an evergreen, first-principles **System Design & AI-Era Architecture** Single Source of Truth (SSOT).
> It is built by a 3-year SDE to master deep systems fundamentals and bridge them to production AI & agentic systems—written with enough clarity for newcomers and enough rigor for 25-year veterans.

---

## 1. Repository Architecture

- `00_sources/MASTER_SOURCES.md` — Canonical whitelist of free books, primary engineering blogs, papers, GitHub repos, and newsletters.
- `01_tier1_bedrock/` — Immutable foundational textbooks, PDFs, and primary engineering guides.
- `02_living_kb/` — Evolving, distilled Markdown knowledge base (`kb_00_master_index.md` + `kb_01` through `kb_06`).
- `03_inbox/weekly_drops.md` — Staging area for daily/weekly articles, newsletters, and raw links before distillation.
- `04_labs/` — Small, runnable code prototypes proving each concept under the hood (e.g., WAL, circuit breaker, rate limiter, idempotent queue).
- `05_publications/` — Polished deep-dive writeups, architecture specs, and visual breakdowns derived from `02_living_kb/`.

---

## 2. Core Behavioral Rules for Claude

1. **NO SURFACE-LEVEL SUMMARIES:**
   Never produce shallow "5-bullet interview prep" answers. Every deep-dive must cover:
   - **First-Principles Mechanics:** What actually happens in memory, disk, network, locks, and state.
   - **Failure Modes & Edge Cases:** What breaks at 10x/100x load, during partial failures, network partitions, or clock skew.
   - **Explicit Tradeoffs:** What is sacrificed to gain X (latency vs. consistency, throughput vs. cost, complexity vs. operability).
   - **AI-Agent Era Bridge:** How this exact mechanism breaks or protects non-deterministic LLM/agent workflows in production.

2. **TWO-AUDIENCE TEST:**
   Every explanation must be accessible to an engineer starting out, yet technically rigorous enough that a 25-year veteran gains a sharp, modern AI-era insight.

3. **GROUNDING & CITATION:**
   Always check `01_tier1_bedrock/`, `02_living_kb/`, and `00_sources/MASTER_SOURCES.md` first. Cite exact sources when referencing concepts or numbers.

---

## 3. Dynamic Research & Scraping Protocol

When asked to research a topic, ingest a new link, or build an artifact:
1. **Check Local SSOT First:** Read `02_living_kb/kb_00_master_index.md` and the relevant `kb_0X_*.md` file.
2. **Fetch / Search High-Signal Sources Only:** Prioritize:
   - **Engineering Blogs:** `aws.amazon.com/builders-library`, `netflixtechblog.com`, `engineering.fb.com`, `cloudflare.com/blog`, `martinfowler.com`
   - **AI & Agents:** `anthropic.com/research`, `huyenchip.com`, `openai.com/index`
   - **Deep Technical Voices:** `arpitbhayani.me`, `architecturenotes.co`, `newsletter.pragmaticengineer.com`, `systemdesign.one`
   - **Papers & Primary Code:** `arxiv.org`, `pdos.csail.mit.edu`, `github.com` (official repos & `papers-we-love`)
   - **Avoid:** Shallow SEO listicles, clickbait summaries, or unverified claims.
3. **Synthesize & Evolve (Do Not Just Append):**
   - Compare new findings against existing `02_living_kb/` notes.
   - Identify what is genuinely new, what refines an existing mental model, or what contradicts older assumptions.
   - Update the relevant `kb_0X_*.md` file and `kb_00_master_index.md`.
   - Propose or build a minimal runnable experiment in `04_labs/`.

---

## 4. Definition of "Done" for Any Concept in `kb_00_master_index.md`

A concept is only marked `Mastered` when it has:
1. Deep first-principles notes + failure modes in `02_living_kb/kb_0X_*.md`.
2. Explicit AI-Agent Era production mapping.
3. At least one runnable mini-lab or concrete architecture diagram/spec in `04_labs/`.
