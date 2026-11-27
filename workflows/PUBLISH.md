# PUBLISH <id>

Goal: the public versions of a drafted concept: the blog post (`post.md`) and the narrated video.
Stage: `drafted → published`. Normally step 3 of [CONCEPT.md](CONCEPT.md), on the same branch.

## Steps

1. Read `notes.md` (and `review.md` if Meet has challenged this concept: its *Gaps found* show which parts
   confused a real learner, so they get the most care).
2. **Post.** The **same nine parts and three levels as `notes.md`** (see `EXPLAINING.md`), tighter and more
   vivid. Keep the strongest two incidents and every predict-then-reveal moment, fold *Going deeper* into one
   "for veterans" box, and put the interactive demo inside part 3 at the moment the naive attempt breaks.
   No lab section in the post. Rules: no claim without a source in `notes.md`; every term defined on first
   use; 1,800–3,500 words; no channel-specific formatting (it must paste cleanly into Substack or Medium).
3. Fill frontmatter `two_audience_check` with one line for the newcomer and one for the veteran.
   Set `status: ready` only when both lines are true.
4. **Video script**, following `EXPLAINING.md` → *From page to video*. Start from `templates/video/`:
   - `video/script.json`: 8–11 scenes, each with `say` (narration, spelled for the voice), `cap` (caption)
     and `part`. About 280 words. **Do not write an outro or name the next concept**: every video ends with
     the standard closing scene from `tools/video/standard.json` ("The full story is linked below. See you
     in the next one."), added automatically.
   - `video/scenes.js`: one visual per scene, built from the engine's classes and helpers, keyed to spoken
     words with `ctx.beat("word")`. Every number on screen is a real, sourced one.
   - `video.md`: the scene table, description text (hook line, blog link placeholder, 3–5 hashtags), the long
     video's chapters, and the links to the post.
5. **Render.** `~/.cache/playbook-tts/venv/bin/python tools/video/make_video.py <id> --preview`, screenshot a frame from each scene and fix
   anything that overlaps or overflows. Then render without `--preview` (about 10 minutes, run it in the
   background). Output: `build/<id>/<id>-video.mp4` (1080×1920, captions burned in).
6. Set `stage = "published"` (meaning *ready to post*), `validate`, `status`.
7. **Store the MP4** (it is not committed; `build/` is gitignored): create or update a **draft** GitHub
   release tagged `video-<id>` and upload the MP4 as its asset:
   `gh release create video-<id> build/<id>/<id>-video.mp4 --draft --title "<id> video" --notes "Video for <id>. Not public."`
   (if it exists: `gh release upload video-<id> build/<id>/<id>-video.mp4 --clobber`). Drafts are invisible
   to the public. Link the release in the PR body. If the upload is refused, say so in the PR.
