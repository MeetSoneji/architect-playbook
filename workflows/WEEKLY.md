# WEEKLY — the scheduler entry point

This is the only prompt a schedule needs. It asks the deterministic tool what to do, then runs it.

1. `git checkout main && git pull`.
2. `python3 tools/playbook.py feeds` (pulls new whitelisted posts into `inbox/drops.md`;
   unreachable feeds are reported, not fatal). Commit that change on the INGEST branch if INGEST runs.
3. `python3 tools/playbook.py next --json`.
4. For each item, in order, run its workflow file from a fresh branch off `main`:
   - `PUBLISH` → [PUBLISH.md](PUBLISH.md)
   - `BUILD_LAB` → [BUILD_LAB.md](BUILD_LAB.md)
   - `DEEP_DIVE` → [DEEP_DIVE.md](DEEP_DIVE.md)
   - `INGEST` → [INGEST.md](INGEST.md) (whole inbox)
   - `WAITING_ON_MEET` / `BLOCKED_BY_WIP` → do nothing; list them in the run summary.
5. Never run more than **3** workflows in one scheduled run. Leave the rest for the next run.
6. Finish with a run summary: PRs opened (links), items waiting on Meet, feeds that failed.

Why a tool decides instead of the agent: the schedule must not race ahead of Meet's learning.
`next` enforces the WIP limit in `curriculum.toml` (default 2 concepts in flight), so if Meet is
behind, automation finishes and polishes existing work instead of piling up new notes.
