# How we explain a concept

This is the style guide every concept page follows. DEEP_DIVE and PUBLISH read it before writing.
The goal is a reader who understands the idea in five minutes **and wants to keep going**.

## What goes wrong with most technical explanations

1. **They start with the definition.** "A write-ahead log is an append-only file in which…" The reader has
   no reason to care yet, so nothing sticks.
2. **They hand over the finished design.** The reader sees seven mechanisms at once and has to take each on
   faith. They never learn *why* each piece exists, so they can't rebuild it or spot a fake one.
3. **They are abstract all the way down.** No moment the reader recognizes, no real system, no number.
4. **They are one flat depth.** Too deep for a newcomer on page one, too shallow for a veteran by the end,
   so both leave.
5. **Proof replaces understanding.** Code, benchmarks or a lab come before the reader has the mental model,
   so they read as noise.

## What keeps people reading (the principles behind the format)

| Principle | What it means for a page | Where it comes from |
|---|---|---|
| **Open a curiosity gap** | Start with a situation and a question the reader can't answer yet. Close it only after they've wanted the answer. | Loewenstein's information-gap theory of curiosity (1994) |
| **Concrete before abstract** | A moment the reader has lived first, the general idea second, the jargon last. | "Concreteness fading" research in maths and science teaching (Fyfe et al., 2014) |
| **Let them invent it** | Build the design through naive attempts that each break in a specific way. Every piece of the real design arrives as the fix for a failure the reader just saw. | How good teachers and writers like Julia Evans, Bartosz Ciechanowski and 3Blue1Brown structure explanations: motivate each step before giving it |
| **Predict, then reveal** | Before showing what happens, ask "what do you think happens?" Being wrong for a moment makes the answer memorable. | The generation and testing effects in learning research (Roediger & Karpicke, 2006) |
| **One idea at a time** | Short sections, one new idea each, a picture next to the words that explain it. | Mayer's multimedia learning principles (segmenting, signaling, coherence) |
| **Show it in the wild** | Point to things the reader already uses (their phone, their bank statement, Redis) that run on this idea. Familiar becomes interesting. | Transfer: ideas stick when tied to many concrete cases |
| **Layered depth** | Level 1 for everyone, Level 2 for how it really works, Level 3 for architects. Each level ends with an open question that pulls into the next. | Progressive disclosure (interface design); the inverted pyramid (journalism) |
| **Stories for failure** | Incidents told as short stories: who, what they believed, what was actually true, what changed. | Narrative is remembered far better than lists |
| **Proof is optional and after** | The lab or simulation is a "try it yourself" box placed where the story needs evidence, never the headline. | Worked examples help once the schema exists (Sweller's cognitive load theory) |

## The page format

Every concept uses the same nine parts in three levels. Readers learn the shape once and can skim
any page.

**Level 1 · The idea (5 minutes, everyone)**
1. **A moment you've lived.** An everyday moment (the "unsaved changes" dialog, a bank statement) and the
   AI-era version of the same problem. End on the question the page answers.
2. **The big idea.** One sentence and one picture. If the reader stops here, they still have the right
   mental model.
3. **Invent it yourself.** Three or four attempts at solving the problem, each simple, each breaking in a
   way the reader can predict. The real design is the last attempt. Put the interactive demo here, at the
   moment the naive attempt breaks.
4. **You've already used it.** Four to six real systems or everyday things that run on this idea, one line
   each, with the detail that makes each surprising.

**Level 2 · How it really works (10 minutes)**
5. **How it really works.** The real mechanism, step by step, now that every step has a reason. Jargon is
   introduced here, each term attached to something from part 3.
6. **When it goes wrong.** Two or more real incidents told as stories, linked to their postmortems.
7. **The price you pay.** Tradeoffs and alternatives, and when this is the wrong tool.

**Level 3 · The architect's view**
8. **The AI connection.** A concrete design for the AI problem from part 1, built from this mechanism.
9. **Remember and check.** Three things to remember, prediction questions with hidden answers, and one
   design challenge for `/challenge`.

Then two optional boxes: **Prove it yourself** (the lab: what it shows and how to run it) and **Going
deeper** (veteran's corner, open questions, self-review), followed by **Sources**.

## Writing rules

- **First 100 words:** a scene and a question. No definitions.
- **Every new term** arrives after the reader has seen the thing it names, and is defined in one plain
  sentence.
- **Every mechanism** is introduced as the fix for something the reader just watched break.
- **At least two predict-then-reveal moments** per page (a collapsed answer under a question).
- **At least four real-world examples** in part 4, including one from everyday life and one AI system.
- **Analogies** must be mechanically faithful, and the page says where each one stops working.
- **Numbers** are concrete and cited, or explicitly marked "measure it yourself".
- **End every level** with a question that makes the next level feel necessary.
- **Plain words.** Short sentences. No "simply", "just" or "obviously".

## From page to video

Every concept also becomes two videos, made from the **same story in the same order**, so watching and
reading are interchangeable. PUBLISH writes them as `video.md` next to `post.md`.

- **Short (90–120 s, vertical, narrated, captions burned in).** Level 1 plus the AI payoff: the hook (part 1), one attempt that
  breaks and the one that holds (part 3), the catch, the AI payoff (part 8) and a closing line that is the
  next concept's open question. One idea per scene, a 5–10 second scene each, with every number shown on
  screen. Most people watch muted, so the captions carry the narration.
- **Long (8–12 min, horizontal).** Levels 1 to 3. One chapter per post part, with the same names. The
  "Invent it yourself" chapter is a screen recording of the blog's interactive demo, pausing to ask the
  viewer to predict before each reveal.

**Linking:** the post opens with "Watch first?" and each part has a "watch this part" link to the long
video's chapter. The video descriptions link back to the post and to each part's anchor. The interactive
demo lives only on the blog, which gives viewers a reason to click through.

**How videos are made.** Nobody records anything. For each concept, PUBLISH writes `video/script.json` (the
narration and captions per scene) and `video/scenes.js` (the visuals for each scene, keyed to spoken words).
Then `python tools/video/make_video.py <id>` produces the MP4. It generates the voice with Kokoro, an open
text-to-speech model that runs locally, times every scene to the narration, lights up caption words as
they are spoken, mixes in a generated music bed that ducks under the voice, and renders 1080×1920 frames.
Every concept's video shares the same look, voice, captions and music, because they all come from
`tools/video/engine.html`.
