# PUBLISH <id>

Goal: a channel-neutral, publish-ready deep dive in `post.md`. Stage: `mastered → published`.
Channels (blog, video, newsletter) are decided later; this draft must be easy to adapt to any.

## Steps

1. Read `notes.md`, `lab/`, and `review.md`. The *Gaps found* and *Attacks* in the review tell you
   which parts confused a real learner: those get the most care in the post.
2. Structure:
   1. Hook: the incident or story from §0/§3.
   2. The mental model in one diagram.
   3. Mechanics, step by step (from §1), with the lab output as the proof.
   4. How it fails, with one real incident.
   5. Tradeoffs and when to choose something else.
   6. The AI-agent bridge.
   7. "If you remember three things".
   8. Sources.
3. Rules: no claim without a source in `notes.md`; every term defined on first use; code excerpts come
   from the lab and are runnable; 1,800–3,500 words; no channel-specific formatting.
4. Fill frontmatter `two_audience_check` with one line for the newcomer and one for the veteran.
   Set `status: ready` only when both lines are true.
5. Add a `video_outline` section at the end: 6–10 beats with the diagram or lab output to show at each.
6. Set `stage = "published"` (meaning *publish-ready*), `validate`, `status`, PR `publish/<id>-<slug>`.
