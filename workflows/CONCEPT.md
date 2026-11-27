# CONCEPT <id>

Goal: one concept, end to end, in **one run and one PR**: the notes, the blog post and the narrated video.
Stage: `queued → published`. This is what every scheduled run does (see [WEEKLY.md](WEEKLY.md)).

## Steps

1. **Branch.** From an up-to-date `main`, create `concept/<id>-<slug>` and push it right away
   (`git push -u origin concept/<id>-<slug>`). The open branch tells the next scheduled run that this concept
   is taken, so two runs never write the same concept.
2. **Notes.** Run [DEEP_DIVE.md](DEEP_DIVE.md) steps 1–7. Result: `notes.md`, `stage = "drafted"`, `validate` clean.
   If the concept is a case study (`kind = "case-study"`), use the case-study variant in `EXPLAINING.md`.
3. **Post and video.** Run [PUBLISH.md](PUBLISH.md) steps 1–6 on the same branch. Result: `post.md`,
   `video.md`, `video/script.json`, `video/scenes.js`, the rendered MP4, `stage = "published"`.
4. **Gate.** `python3 tools/playbook.py validate` (0 errors), then `python3 tools/playbook.py status`.
5. **Store the video.** Upload the MP4 as described in PUBLISH step 7.
6. **PR** from `concept/<id>-<slug>`, title `<id>: <title>`. Body:
   - "After reading you should be able to explain…" (3 bullets).
   - The two incidents, one line each.
   - Links: the video file, `post.md`, `video.md`.
   - Open questions for Meet.
   If a step could not be finished (a source was unreachable, the render failed), say so at the top and leave
   the stage at the last gate that passed.

One concept per run. Never start a second concept in the same run, and never push to `main`.
