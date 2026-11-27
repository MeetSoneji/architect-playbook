# DEEP_DIVE <id>

Goal: a `notes.md` that teaches the concept from "a bit above basics" to production depth, passes
the Two-Audience Test, and survives an adversarial reviewer. Stage: `queued → drafted`.

## Steps

1. **Load context.** Read `CLAUDE.md`, the concept's entry in `curriculum.toml`, the module's
   `_module.md`, and the `notes.md` of every concept in `requires`. Link to them instead of re-explaining.
2. **Scaffold.** `python3 tools/playbook.py scaffold <id>`.
3. **Research, bedrock first.** Read the `bedrock` sources listed for the concept (local copies in
   `sources/bedrock/` when present, otherwise the official free URL in `sources/MASTER_SOURCES.md`).
   Then whitelisted engineering blogs and papers. Then search for **public incident reports and
   postmortems** involving the mechanism (vendor status pages, engineering blogs, `danluu/post-mortems`).
   Record every claim's source as you go. Any number (latency, throughput, cost) needs a citation.
4. **Write each part** of the template, in order. Every concept uses the same eight parts:
   1. *The AI problem it prevents*: a concrete story, then "this is an old problem called X".
   2. *Intuition*: a mechanically faithful analogy (say where it breaks down) and one mermaid diagram.
   3. *Mechanics, step by step*: one operation end to end, numbered. Define every term on first use.
   4. *Break it*: the failure modes, then the lab spec (BUILD_LAB fills in real output later).
   5. *Real incidents*: at least 2, linked, each with the exact mechanism that failed.
   6. *Tradeoffs and where it is used*: alternatives, named systems, one wrong-tool case.
   7. *Apply it to agents*: a concrete design (records, fields, write order, restart behaviour).
   8. *Check yourself*: 5–8 understanding questions with collapsed answers, plus one design challenge.
   Then *Going deeper* (veteran's corner, open questions, self-review) and *Sources*.
5. **Two-Audience pass.** Re-read as (a) an engineer with 1 year of experience: is every step
   followable without outside reading? (b) a 25-year distributed-systems veteran: is anything hand-wavy,
   outdated, or wrong? Fix both.
6. **Adversarial self-review.** Switch roles to a Staff/Principal reviewer whose job is to find what
   is wrong or missing: incorrect mechanics, missing failure modes, unsupported numbers, incidents that
   don't actually involve the mechanism, a weak AI bridge. Write the attacks and resolutions under *Going deeper → Self-review*.
   If you have a subagent tool, run this as a separate reviewer agent given only the notes and sources.
7. **Gate.** Set `stage = "drafted"` in `curriculum.toml`, run `validate`, fix until 0 errors, run `status`.
8. **PR** `deep-dive/<id>-<slug>`. Body: "After reading you should be able to explain…" (3 bullets),
   the diagram, the two incidents in one line each, open questions.
