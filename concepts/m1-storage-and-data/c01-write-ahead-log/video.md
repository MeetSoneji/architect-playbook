---
concept: c01
status: draft
short_seconds: 76
long_minutes: 9
blog: post.md
---

# c01 video · The Log Is the Truth

Both videos tell the **same story as `post.md`**, in the same order, so a viewer can switch between
watching and reading at any point. The short covers Level 1 only. The long video covers Levels 1 to 3.

## Short (vertical 9:16, 76 s, captions burned in)

Rendered preview: `c01-short.mp4`. Animated storyboard page: see the PR description.

| Time | On screen | Narration / caption | Post part |
|---|---|---|---|
| 0:00 | "Your AI agent just refunded a customer **twice**." Two refund receipts drop in. | Your AI agent just refunded a customer twice. | 1 |
| 0:06 | The four agent steps. Step 2 turns red: *pod evicted*. Then back to step 1: *refund #2*. | It crashed mid-refund. On restart it remembered nothing, so it started over. | 1 |
| 0:15 | "After a crash, how does a program know what it already did?" | That's a 50-year-old database problem: what did I already do before the crash? | 1 |
| 0:21 | Attempt 1: a file is truncated, half rewritten, then struck by lightning. "Half a file. Unreadable." | First idea: rewrite the whole file on every save. Then the power fails mid-write. | 3 |
| 0:31 | A counter rolls up to **634**: "of 664 crash moments lose saved data". | 634 out of 664 crash moments lose data the user was told was saved. | 3 |
| 0:36 | Attempt 2: log lines append one by one. Lightning tears the last one: *torn → skip*. "0 of 230." | Real fix: never overwrite. Append a note of what you're about to do. A crash only tears the last line. | 3 |
| 0:47 | Memory box and disk box. A record chip sits in memory, then moves to disk on `fsync`. | Catch: write() leaves data in memory. Only after fsync is it on disk. Say "saved" only then. | 5 |
| 0:55 | Agent journal rows: intent → call → crash → restart → retry with same key → "already done". "Refunds: 1." | For agents: log the intent, do the step, log the result. On restart, skip what's done. Retry the rest with the same key. | 8 |
| 1:06 | "The log is the truth." Three rules. | That's a write-ahead log. The log is the truth. | 9 |
| 1:11 | "Full story + crash demo: link in description." Teaser: "Next: idempotency keys." | Full story and a live crash demo: link below. | → |

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
