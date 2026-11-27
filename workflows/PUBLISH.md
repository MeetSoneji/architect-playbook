# PUBLISH <id>

Goal: a channel-neutral, publish-ready deep dive in `post.md`. Stage: `mastered → published`.
Channels (blog, video, newsletter) are decided later; this draft must be easy to adapt to any.

## Steps

1. Read `notes.md`, `lab/`, and `review.md`. The *Gaps found* and *Attacks* in the review tell you
   which parts confused a real learner: those get the most care in the post.
2. Structure: the **same nine parts and three levels as `notes.md`** (see `EXPLAINING.md`), made tighter
   and more vivid. Keep the strongest two incidents, keep every predict-then-reveal moment, fold *Going
   deeper* into one "for veterans" box, and put the interactive demo or lab output inside part 3 at the
   moment the naive attempt breaks.
3. Rules: no claim without a source in `notes.md`; every term defined on first use; code excerpts come
   from the lab and are runnable; 1,800–3,500 words; no channel-specific formatting.
4. Fill frontmatter `two_audience_check` with one line for the newcomer and one for the veteran.
   Set `status: ready` only when both lines are true.
5. Make the video, following `EXPLAINING.md` → *From page to video*:
   - `video/script.json`: 8–12 scenes, each with `say` (narration, spelled for the voice), `cap` (caption) and
     `part`. Aim for about 300 words.
   - `video/scenes.js`: one visual per scene, built from the engine's classes and helpers. Key the animations
     to spoken words with `ctx.beat("word")`. Show real numbers from the lab, never invented ones.
   - `video.md`: the scene table, description text, the long video's chapters, and the links to the post.
   - Run `python tools/video/make_video.py <id> --preview` and check the page, then render the MP4 without
     `--preview`. Attach the MP4 to the PR conversation; `build/` is not committed.
6. Set `stage = "published"` (meaning *publish-ready*), `validate`, `status`, PR `publish/<id>-<slug>`.
