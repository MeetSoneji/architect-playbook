# Video pipeline

`python tools/video/make_video.py <concept id>` turns a concept's `video/script.json` and `video/scenes.js`
into a narrated 1080×1920 MP4 in `build/<id>/`. Add `--preview` to build only the silent, auto-playing HTML
page, which is quick for checking visuals.

| File | Role |
|---|---|
| `engine.html` | Shared look: background, top bar, chapter progress, word-by-word captions, lightning effect, scene timing |
| `make_video.py` | Narration (Kokoro TTS) → timing → page → frames → music → MP4 |
| `frames.js` | Renders every frame with Playwright (deterministic: the page draws itself from a time `t`) |

**Setup, once per machine:** ffmpeg, Node with Playwright, and a Python venv with
`pip install kokoro-onnx soundfile numpy`. The Kokoro model (about 330 MB) downloads on first run to
`~/.cache/playbook-tts`. The default voice is `af_heart`, set in each `script.json`.

**Writing scenes:** each scene in `scenes.js` has `html`, an optional `init(ctx)`, and `fx(p, ctx)`, which
draws the scene at progress `p` (0 to 1). `ctx.beat("word")` returns when that caption word is spoken, and
`ctx.bolt("word")` fires the lightning effect on it. Helpers: `ease`, `easeInOut`, `seg`, `show`, `$`.
The engine's CSS classes (`big`, `huge`, `mid`, `small`, `tag`, `card`, `row`, `stack`, `accent`, `danger`,
`ok`) keep every concept's video consistent.
