# How the playbook runs itself

Two halves, deliberately separated:

- **`tools/playbook.py` decides what is true and what runs next.** Deterministic, testable, runs in CI.
- **Claude runs the workflows** in `workflows/` and opens one PR per step.

Your merges are the clock. A scheduled run only sees what is on `main`, so a concept moves forward when
you merge its PR. If you don't merge for a week, automation doesn't pile up unread notes: the WIP limit
(`curriculum.toml` → `wip_limit = 2`) stops new deep dives until you master one.

## The weekly rhythm (one concept per week, pipelined)

| When | Who | What | Result |
|---|---|---|---|
| Monday morning | Scheduled `/weekly` | `next` usually says DEEP_DIVE for this week's concept, plus PUBLISH for anything mastered | PR: `notes.md` (and `post.md`) |
| Mon–Wed | **You** | Read the notes PR, leave questions as PR comments, merge | concept is `drafted` |
| Thursday morning | Scheduled `/weekly` | `next` says BUILD_LAB for the drafted concept | PR: `lab/` with the failure proof; CI runs it |
| Thu–Sat | **You** | Run the lab, break it on purpose, merge | concept is `proven` |
| Weekend, ~45 min | **You + Claude, live** | `/challenge <id>`: teach-back, then a Staff-engineer design review | PR: `review.md`; you decide `mastered` |
| Sunday evening | Scheduled INGEST | `feeds` pulls whitelisted posts into the inbox, INGEST distills inbox into notes | PR: `inbox/reports/YYYY-Www.md` + note edits |

CI (`.github/workflows/validate.yml`) runs on every PR: tool self-tests, structure and depth gates, and every
lab's negative control and recovery test. A PR that would mark a concept `drafted` with thin notes fails.

## Running it

**Manually (any time):** open the repo in Claude Code and use the slash commands:
`/weekly`, `/deep-dive c01`, `/build-lab c01`, `/challenge c01`, `/publish c01`, `/ingest <url>`.
Drop links into `inbox/drops.md` whenever you find something; Sunday's run picks them up.

**On a schedule (recommended: Claude Code scheduled tasks).** Three scheduled cloud tasks on this repo,
each with a one-line prompt:

| Task | Schedule | Prompt |
|---|---|---|
| weekly-mon | Mondays 07:00 local | `Run /weekly for the architect-playbook repo. Open PRs, never push to main.` |
| weekly-thu | Thursdays 07:00 local | same as above |
| ingest-sun | Sundays 18:00 local | `Run python3 tools/playbook.py feeds, then /ingest for the whole inbox. Open one PR.` |

These need the repo connected to Claude with push access, and a network setting that allows the feed and
source domains (the default trusted list blocks most blogs; INGEST and DEEP_DIVE need web access).

**Alternative: GitHub Actions.** If you prefer the schedule to live in the repo, use
`anthropics/claude-code-action` on a `schedule:` trigger with the same prompts. It needs an
`ANTHROPIC_API_KEY` (or Claude OAuth token) repository secret and bills that account per run.

## Claude Project (web/desktop) as a reading companion

If you also use a Claude Project for reading and asking questions:
1. Attach the GitHub repo as Project knowledge and press **Sync** after merges.
2. Sync `concepts/`, `curriculum.toml`, `CLAUDE.md`, `workflows/`, `sources/MASTER_SOURCES.md`.
   Skip `sources/bedrock/` PDFs: they are gitignored anyway, and whole textbooks crowd out retrieval.
   Commit short chapter notes (`sources/bedrock/<source>__<chapter>.md`) instead.
3. Ask it to "run CHALLENGE on c01" there too; save the result as `review.md` via a PR.
