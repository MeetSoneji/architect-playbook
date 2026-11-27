// {{id}} video scenes. Each key matches a scene id in script.json. Do NOT write an `outro`:
// every video ends with the standard closing scene from tools/video/standard.json + engine.html.
// html: markup using the engine classes (big, huge, mid, small, tag, card, row, stack, accent, danger, ok).
// init(ctx): one-time setup. fx(p, ctx): draw at progress p (0..1). ctx.beat("word") = when that caption
// word is spoken (0..1); ctx.bolt("word") fires the lightning effect on it. Every number shown must be real.
const SCENES = {
  hook: {
    html: `<div class="tag">{{title}}</div><div class="big" id="h-1">FILL</div>`,
    fx(p, c) { show($("h-1"), ease(seg(p, 0, 0.15))); },
  },
  // what, old, try1, fix, catch, agent, truth ... one idea per scene, 5-10 s each
};
