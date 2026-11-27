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
4. **Read `EXPLAINING.md`, then write each part** of the template in order. Nine parts in three levels:
   Level 1 (a moment you've lived, the big idea, invent it yourself, you've already used it), Level 2
   (how it really works, when it goes wrong, the price you pay), Level 3 (the AI connection, remember
   and check), then Prove it yourself, Going deeper and Sources. Draft part 3 (*Invent it yourself*)
   first: if you cannot tell the concept as a chain of attempts that break, you don't understand it
   well enough yet.
5. **Two-Audience pass.** Read Level 1 alone: does it hook, and does it stand on its own in 5 minutes? Then re-read as (a) an engineer with 1 year of experience: is every step
   followable without outside reading? (b) a 25-year distributed-systems veteran: is anything hand-wavy,
   outdated, or wrong? Fix both.
6. **Adversarial self-review.** Switch roles to a Staff/Principal reviewer whose job is to find what
   is wrong or missing: incorrect mechanics, missing failure modes, unsupported numbers, incidents that
   don't actually involve the mechanism, a weak AI bridge. Write the attacks and resolutions under *Going deeper → Self-review*.
   If you have a subagent tool, run this as a separate reviewer agent given only the notes and sources.
7. **Gate.** Set `stage = "drafted"` in `curriculum.toml`, run `validate`, fix until 0 errors, run `status`.
8. **PR** `deep-dive/<id>-<slug>`. Body: "After reading you should be able to explain…" (3 bullets),
   the diagram, the two incidents in one line each, open questions.
