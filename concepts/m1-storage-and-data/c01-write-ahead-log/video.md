---
concept: c01
status: draft
short_seconds: 113
long_minutes: 9
blog: post.md
---

# c01 video · The Log Is the Truth

Both videos tell the **same story as `post.md`**, in the same order, so a viewer can switch between
watching and reading at any point. The short covers Level 1 only. The long video covers Levels 1 to 3.

## Short (vertical 9:16, about 2 minutes, narrated)

The short is generated, not hand-edited. Its source is in [`video/`](video/):

- [`video/script.json`](video/script.json) holds the scenes in order. For each one, `say` is the narration
  (spelled for the voice, e.g. "eff-sync") and `cap` is the on-screen caption.
- [`video/scenes.js`](video/scenes.js) holds the visuals for each scene. Animations are keyed to spoken
  words, so a lightning strike lands exactly on "power fails".
- `python tools/video/make_video.py c01` renders `build/c01/c01-video.mp4`: Kokoro narration, word-by-word
  captions, a generated music bed ducked under the voice, and 1080×1920 frames.

| Scene | Post part | Beat |
|---|---|---|
| hook | 1 | "Your AI agent just refunded a customer. Twice." |
| what | 1 | The four steps, the server shut down mid-refund, the restart that refunds again |
| old | 1 | 2026 rolls back to 1976: "how do you know what you already did?" |
| try1 | 3 | Rewrite the whole file; lightning on "power fails"; half a file |
| count | 3 | A 664-square grid fills in: 634 red, coloured from the real simulation |
| wal | 3 | Log lines append; lightning tears the last; a 230-square grid fills green |
| fsync | 5 | A record sits in memory until fsync moves it to disk |
| agent | 8 | The step journal: intent, done, crash, restart, retry with the same key, already done → 1 refund |
| truth | 9 | Three rules, then "The log is the truth." |
| outro | → | Link to the full story; next: idempotency keys |

**Description text:**

> Your AI agent refunded a customer twice. Here's the 50-year-old database idea that prevents it.
> Full write-up with a live crash demo: <blog link>
> Long version (9 min): <long video link>
> Part 1 of 30 · System design for the AI era

## Long video (horizontal 16:9, about 9 minutes)

Chapters map 1:1 to the post's parts, with the same names, so each chapter timestamp can link to the
matching anchor in the blog post (`#invent-it-yourself` and so on).

| Chapter | Time | Post part | What's on screen |
|---|---|---|---|
| A moment you've lived | 0:00 | 1 | The laptop that dies mid-paragraph, then the double refund as a timeline |
| The big idea | 0:50 | 2 | One sentence and the flow diagram. The bank teller's journal |
| Invent it yourself | 1:40 | 3 | Screen recording of the blog's crash slider: Try 1 → Try 4, pausing to ask "what happens if the power fails here?" before each reveal |
| You've already used it | 3:30 | 4 | Quick cuts: phone apps (SQLite WAL), a bank statement, Redis `appendfsync everysec`, Postgres, Kafka, Temporal |
| How it really works | 4:20 | 5 | The sequence diagram built step by step: append, fsync, ack, lazy pages, checkpoint, recovery |
| When it goes wrong | 5:50 | 6 | fsyncgate and GitLab 2017 told as 45-second stories over the postmortem headlines |
| The price you pay | 7:10 | 7 | The alternatives table, with one sentence on when each wins |
| The AI connection | 7:50 | 8 | The step journal, and the lab run showing refunds=2 vs refunds=1 |
| Remember and check | 8:40 | 9 | Three things to remember, then the design challenge as the closing question |

## How the pieces link

- **Blog → video:** the post opens with "Watch first?" linking both videos. Each part heading has a
  "watch this part" link to the long video's chapter timestamp.
- **Video → blog:** the short's description links the post and the long video. Each long-video chapter in
  the description links to the post's matching anchor. The interactive demo only exists on the blog,
  which gives viewers a reason to click.
- **Series:** every short ends on the next concept's open question ("Next: idempotency keys").
