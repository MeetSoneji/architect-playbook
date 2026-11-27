# WEEKLY — the scheduler entry point (runs Mon and Thu)

This is the only prompt a schedule needs. It asks the deterministic tool what to do, then runs it.
Two runs a week (Mon and Thu, 07:00 IST) means two concepts a week, in `seq` order from `curriculum.toml`.

1. `git checkout main && git pull`.
2. `bash tools/video/setup.sh` (sets up the video renderer; instant if it is already set up).
3. `python3 tools/playbook.py next --json`. It returns at most one production item:
   - `CONCEPT` → run [CONCEPT.md](CONCEPT.md) for that id: notes, post and video in one PR.
   - `PUBLISH` → a concept was left `drafted` on `main`: run [PUBLISH.md](PUBLISH.md) on `concept/<id>-<slug>`.
   - `NOT_YET` → the next release date has not arrived. Do nothing.
   - `WAITING_ON_MEET` → too many concept PRs are waiting to be merged. Do nothing, and list them.
   - `INGEST` → only on the Sunday run: [INGEST.md](INGEST.md) for the whole inbox.
4. Finish with a run summary: the PR opened (link), what is waiting on Meet, anything that failed.

Why a tool decides instead of the agent: `next` is a pure function of the registry, the date and the open
`concept/*` branches, and CI tests it. Behind schedule? Each run catches up by one concept. More than
four concept PRs unmerged? Automation pauses until Meet merges, so unread work never piles up.
