# How the playbook runs itself

Two halves, deliberately separated:

- **`tools/playbook.py` decides what is true and what runs next.** Deterministic, testable, runs in CI.
- **Claude runs the workflows** in `workflows/` and opens one PR per concept.

## The rhythm: two concepts a week, in order

`curriculum.toml` is one ordered list (`seq` 1 to 38). Every run takes the next item and produces all of
it: the notes, the blog post and the narrated video.

| When | Who | What | Result |
|---|---|---|---|
| Monday ~07:00 IST | Scheduled `/weekly` | `next` picks the next item by `seq`; [CONCEPT](workflows/CONCEPT.md) writes notes, post and video | One PR on `concept/<id>-<slug>`, the MP4 in the project's shared files |
| Thursday ~07:00 IST | Scheduled `/weekly` | Same, for the following item | One PR |
| Any time | **You** | Read the post, watch the video, comment on the PR, merge | The concept is `published` on `main` |
| Sunday 18:00 IST | Scheduled INGEST | `feeds` pulls whitelisted posts into the inbox; INGEST sharpens existing notes | PR: `inbox/reports/YYYY-Www.md` + note edits |
| When you want | **You + Claude, live** | `/challenge <id>`: teach-back, then a Staff-engineer design review | `review.md`, and ★ `mastered = true` if you pass |

**Your merges are not the clock, the calendar is.** Each run opens the next concept even if the previous PR
is still open (the open `concept/*` branch tells the next run to skip that one). If four concept PRs are
waiting for you, automation pauses until you merge, so unread work never piles up. If a run fails, the
next run picks the same concept up again. Behind schedule? Each run catches up by one.

CI (`.github/workflows/validate.yml`) runs on every PR: tool self-tests, structure and depth gates.

## Where the outputs go

| Output | Where | Ready for |
|---|---|---|
| Notes | `concepts/<module>/<id>-<slug>/notes.md` | You, and INGEST to keep sharpening |
| Blog post | `post.md` (channel-neutral Markdown) | Substack and Medium |
| Video (1080×1920 MP4, captions burned in) | Project files: `architect-playbook/videos/<id>-video.mp4`, attached to the run's reply | Instagram Reels and YouTube Shorts |
| Video description, chapters, hashtags | `video.md` | The same uploads |

Posting to Instagram, YouTube, Substack and Medium is a later step, once the accounts exist.

## Running it

**Manually (any time):** open the repo in Claude Code and use the slash commands:
`/weekly`, `/concept c23`, `/challenge c01`, `/ingest <url>`. `/deep-dive` and `/publish` run the two
halves of `/concept` separately. `/build-lab` adds an optional runnable lab.
Drop links into `inbox/drops.md` whenever you find something; Sunday's run picks them up.

**On a schedule: Claude Code scheduled tasks** on this repo, each with a one-line prompt:

| Task | Schedule (IST) | Cron (UTC) | Prompt |
|---|---|---|---|
| playbook-mon | Mondays 07:00 | `30 1 * * 1` | `Run /weekly for the architect-playbook repo. Open PRs, never push to main.` |
| playbook-thu | Thursdays 07:00 | `30 1 * * 4` | same as above |
| playbook-ingest | Sundays 18:00 | `30 12 * * 0` | `Run python3 tools/playbook.py feeds, then /ingest for the whole inbox. Open one PR.` |

They need the repo connected with push access, and a cloud environment whose network allows the research
and feed domains (the default list blocks most engineering blogs). The video renderer downloads its voice
model from GitHub releases and Python packages from PyPI, which the default list allows.

**Alternative: GitHub Actions.** Use `anthropics/claude-code-action` on a `schedule:` trigger with the same
prompts. It needs an `ANTHROPIC_API_KEY` (or Claude OAuth token) repository secret, ffmpeg and Playwright
on the runner, and bills that account per run.

## Claude Project (web/desktop) as a reading companion

If you also use a Claude Project for reading and asking questions:
1. Attach the GitHub repo as Project knowledge and press **Sync** after merges.
2. Sync `concepts/`, `curriculum.toml`, `CLAUDE.md`, `EXPLAINING.md`, `workflows/`, `sources/MASTER_SOURCES.md`.
   Skip `sources/bedrock/` PDFs: they are gitignored anyway.
3. Ask it to "run CHALLENGE on c01" there too; save the result as `review.md` via a PR.
