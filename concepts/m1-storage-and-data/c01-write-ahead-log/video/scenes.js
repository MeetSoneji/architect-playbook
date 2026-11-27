// c01 video scenes. Each key matches a scene id in script.json.
// html: the scene's markup. init(ctx): one-time setup (ctx.beat(word) -> 0..1 position of a spoken word,
// ctx.bolt(word) fires the lightning effect on that word). fx(p, ctx): draw the scene at progress p (0..1).

// --- the same crash simulation as lab/wal.py, used to colour the crash-point grids truthfully ---
const SIM = (() => {
  const OPS = [0, 1, 2, 3, 4, 5].map(i => [`user:${i}`, `balance=${i * 100}`]).concat([["user:0", "balance=999"]]);
  const pyDict = m => "{" + [...m].map(([k, v]) => `"${k}": "${v}"`).join(", ") + "}";
  function naiveLoses(budget) {
    let file = "", written = 0; const st = new Map(), acked = [];
    try {
      for (const [k, v] of OPS) {
        st.set(k, v);
        if (written >= budget) throw 0; file = "";
        const d = pyDict(st), ok = Math.max(0, Math.min(d.length, budget - written)); written += ok; file += d.slice(0, ok);
        if (ok < d.length) throw 0; acked.push([k, v]);
      }
    } catch (e) {}
    let after = {}; try { after = file ? JSON.parse(file) : {}; } catch (e) { after = {}; }
    return [...new Map(acked)].some(([k, v]) => after[k] !== v);
  }
  let total = 0; { const st = new Map(); for (const [k, v] of OPS) { st.set(k, v); total += pyDict(st).length; } }
  const naive = Array.from({ length: total + 1 }, (_, n) => naiveLoses(n));
  return { naive, walPoints: 230 };
})();

function gridHTML(id, n, cols) { return `<div id="${id}" style="display:grid;grid-template-columns:repeat(${cols},1fr);gap:3px;width:100%">${Array.from({ length: n }, () => `<i style="display:block;aspect-ratio:1;border-radius:2px;background:var(--rule)"></i>`).join("")}</div>`; }

const SCENES = {
  hook: {
    html: `<div class="big">Your AI agent just refunded a customer. <span class="danger" id="h-twice">Twice.</span></div>
      <div class="card row" id="h-r1"><span>REFUND #rf_881</span><span>$40.00</span></div>
      <div class="card row bad" id="h-r2"><span>REFUND #rf_882</span><span>$40.00</span></div>`,
    fx(p, c) { show($("h-r1"), ease(seg(p, c.beat("refunded"), c.beat("refunded") + 0.12))); show($("h-r2"), ease(seg(p, c.beat("Twice"), c.beat("Twice") + 0.1))); $("h-twice").style.opacity = p > c.beat("Twice") ? 1 : 0.15; },
  },

  what: {
    html: `<div class="tag">What happened</div>
      <div class="stack">
        <div class="row" id="w-1"><span>1 · plan</span><span>LLM</span></div>
        <div class="row" id="w-2"><span>2 · refund $40</span><span>payment API</span></div>
        <div class="row" id="w-3"><span>3 · email customer</span><span>tool</span></div>
        <div class="row" id="w-4"><span>4 · summarize</span><span>LLM</span></div>
      </div>
      <div class="card row good" id="w-bank"><span>BANK</span><span class="ok">refund sent ✓</span></div>
      <div class="mid" id="w-note">&nbsp;</div>`,
    init(c) { c.bolt("shut"); },
    fx(p, c) {
      const rows = [1, 2, 3, 4].map(i => $("w-" + i));
      const bStep = c.beat("step"), bShut = c.beat("shut"), bPaid = c.beat("paid"), bNothing = c.beat("nothing"), bAgain = c.beat("again");
      rows.forEach(r => r.className = "row");
      rows.forEach(r => r.style.opacity = 1);
      if (p < bStep) rows[0].classList.add("hot");
      else if (p < bShut) rows[1].classList.add("hot");
      else if (p < bNothing) rows[1].classList.add("bad");
      else if (p < bAgain) rows.forEach(r => r.style.opacity = 0.25);
      else rows[p < bAgain + 0.06 ? 0 : 1].classList.add("hot");
      show($("w-bank"), ease(seg(p, bPaid, bPaid + 0.06)));
      $("w-note").innerHTML = p < bShut ? "&nbsp;" : p < bNothing ? '<span class="danger">server shut down</span> mid-refund' : p < bAgain ? "restart: memory empty" : 'starts over → <span class="danger">refund #2</span>';
    },
  },

  old: {
    html: `<div class="tag">Not a new problem</div>
      <div class="huge accent mono" id="o-year" style="font-size:120px">2026</div>
      <div class="big" id="o-q" style="font-size:46px">After a crash, how do you know what you <span class="accent">already did?</span></div>`,
    fx(p, c) { const k = easeInOut(seg(p, 0.12, c.beat("After"))); $("o-year").textContent = Math.round(2026 - 50 * k); show($("o-q"), ease(seg(p, c.beat("After"), c.beat("After") + 0.12))); },
  },

  try1: {
    html: `<div class="tag">Obvious fix</div>
      <div class="mid">Save the whole file on every change.</div>
      <div class="card mono" id="t-file" style="font-size:19px;line-height:1.5;min-height:200px;word-break:break-all"></div>
      <div class="mid danger" id="t-out">&nbsp;</div>`,
    init(c) { c.bolt("power"); },
    fx(p, c) {
      const S = '{"user:0": "$0", "user:1": "$100", "user:2": "$200", "user:3": "$300"}';
      const bPow = c.beat("power"), bGone = c.beat("gone"), bHalf = c.beat("half");
      const f = $("t-file");
      if (p < c.beat("save") + 0.05) f.innerHTML = `<span style="color:var(--ink)">${S}</span>`;
      else if (p < bPow - 0.05) { const k = seg(p, c.beat("save") + 0.05, bPow - 0.05); f.innerHTML = k < 0.25 ? '<span class="small">(truncated… rewriting)</span>' : `<span class="accent">${S.slice(0, Math.floor(S.length * (k - 0.25) / 0.75 * 0.6))}</span>`; }
      else f.innerHTML = `<span class="danger">${S.slice(0, Math.floor(S.length * 0.42))}</span><span class="danger" style="opacity:.5">▌</span>`;
      $("t-out").innerHTML = p < bGone ? "&nbsp;" : p < bHalf ? "Old data: gone." : "Old data: gone. New data: half. Unreadable.";
    },
  },

  count: {
    html: `<div style="display:flex;align-items:baseline;gap:14px"><div class="huge danger" id="c-n">0</div><div class="mid" style="color:var(--muted)">/ 664</div></div>
      <div class="mid">crash moments lose data the user was told was <span class="accent">saved</span>.</div>
      ${gridHTML("c-grid", 664, 32)}
      <div class="small">Each square is one byte where the power could fail. Red = saved data lost.</div>`,
    fx(p) {
      const k = ease(seg(p, 0.08, 0.75)); const upto = Math.floor(664 * k); let bad = 0;
      [...$("c-grid").children].forEach((cell, i) => { const on = i < upto; if (on && SIM.naive[i]) bad++; cell.style.background = !on ? "var(--rule)" : SIM.naive[i] ? "var(--danger)" : "var(--muted)"; });
      $("c-n").textContent = bad;
    },
  },

  wal: {
    html: `<style>#scene-wal{gap:16px}#scene-wal .row{padding:9px 14px;font-size:18px}#scene-wal .stack{gap:8px}#l-gridwrap{width:78%}</style>
      <div class="tag">The real fix</div>
      <div class="mid">Never overwrite. <span class="accent">Append</span> a note first.</div>
      <div class="stack" id="l-log"></div>
      <div id="l-gridwrap" style="opacity:0">${gridHTML("l-grid", 230, 23)}</div>
      <div class="mid ok" id="l-out">&nbsp;</div>`,
    init(c) {
      const L = ["set user:0 $0", "set user:1 $100", "set user:2 $200", "set user:3 $300", "set user:4 $400"];
      $("l-log").innerHTML = L.map((l, i) => `<div class="row" id="l-${i}" style="border-left:4px solid var(--accent)"><span>${l}</span><span>✓</span></div>`).join("");
      c.bolt("power");
    },
    fx(p, c) {
      const bApp = c.beat("append"), bPow = c.beat("power"), bTear = c.beat("tear"), bZero = c.beat("0");
      for (let i = 0; i < 5; i++) {
        const e = $("l-" + i);
        if (i < 4) { show(e, ease(seg(p, bApp + i * 0.04, bApp + i * 0.04 + 0.04)), 10); e.className = "row"; }
        else { e.style.opacity = p > bPow - 0.06 ? 1 : 0; e.style.transform = "none";
          const torn = p > bPow; e.className = torn ? "row bad" : "row"; e.firstChild.textContent = torn ? "set user:4 $4" : "set user:4 $400"; e.lastChild.textContent = p > bTear ? "torn → skipped" : torn ? "⚡" : ""; e.style.textDecoration = p > bTear ? "line-through" : "none"; }
      }
      const g = seg(p, bZero - 0.04, bZero + 0.12);
      $("l-gridwrap").style.opacity = g > 0 ? 1 : 0;
      [...$("l-grid").children].forEach((cell, i) => cell.style.background = i < Math.floor(230 * ease(g)) ? "var(--ok)" : "var(--rule)");
      $("l-out").innerHTML = p > bZero ? "0 / 230 crash points lose saved data." : "&nbsp;";
    },
  },

  fsync: {
    html: `<div class="tag">One catch</div>
      <div class="mid">“Written” isn’t saved until <span class="accent mono">fsync</span> says so.</div>
      <div style="position:relative;display:grid;grid-template-columns:1fr 1fr;gap:18px">
        <div class="card" style="height:230px;border-style:dashed"><div class="tag" style="color:var(--muted)">Memory</div><div class="small">page cache</div></div>
        <div class="card" style="height:230px;border-style:dashed"><div class="tag" style="color:var(--muted)">Disk</div><div class="small">survives power loss</div></div>
        <div id="f-chip" style="position:absolute;top:110px;left:18px;width:190px;padding:14px;border-radius:10px;background:var(--accent);color:#04262A;font:700 19px var(--f-mono);text-align:center">LSN 101</div>
      </div>
      <div class="mid" id="f-out">&nbsp;</div>`,
    fx(p, c) {
      const bMem = c.beat("memory"), bConf = c.beat("confirms"), bSaved = c.beat("Say");
      const chip = $("f-chip"); chip.style.opacity = ease(seg(p, bMem - 0.08, bMem));
      const mv = easeInOut(seg(p, bConf, bConf + 0.12)); chip.style.left = `${18 + 239 * mv}px`;
      chip.style.boxShadow = p > bMem && p < bConf ? `0 0 ${12 + 10 * Math.sin(p * 40)}px rgba(63,193,203,.7)` : "none";
      $("f-out").innerHTML = p < bMem ? "&nbsp;" : p < bConf ? 'write() returned. Saved? <span class="danger">Not yet.</span>' : p < bSaved ? "fsync() … on disk." : 'Now say <span class="ok">“saved”</span>.';
    },
  },

  agent: {
    html: `<div class="tag">For agents: a step journal</div>
      <div class="stack" id="a-j"></div>
      <div style="display:flex;align-items:baseline;gap:16px" id="a-res"><div class="huge ok" style="font-size:110px">1</div><div class="mid">refund. LLM calls repeated: <span class="ok">0</span></div></div>`,
    init(c) {
      const J = [["intent", "step 2 · key run-42:2", "accent"], ["done", "result: rf_881", "ok"], ["crash", "server shut down", "danger"], ["restart", "skip done steps", "accent"], ["retry", "same key run-42:2", "accent"], ["API", "already done ✓", "ok"]];
      $("a-j").innerHTML = J.map(([k, v, col], i) => `<div class="row" id="a-${i}" style="border-left:4px solid var(--${col})"><span>${k}</span><span>${v}</span></div>`).join("");
    },
    fx(p, c) {
      const beats = [c.beat("Before"), c.beat("result"), c.beat("restart"), c.beat("skip"), c.beat("idempotency"), c.beat("replies")];
      beats.forEach((b, i) => show($("a-" + i), ease(seg(p, b - 0.02, b + 0.05)), 10));
      show($("a-res"), ease(seg(p, c.beat("One") - 0.02, c.beat("One") + 0.05)));
    },
  },

  truth: {
    html: `<div class="tag">Write-ahead log</div>
      <div class="stack">
        <div class="row" id="r-1"><span>1</span><span>Append, never overwrite.</span></div>
        <div class="row" id="r-2"><span>2</span><span>Saved = fsync returned.</span></div>
        <div class="row" id="r-3"><span>3</span><span>Agents: journal the results.</span></div>
      </div>
      <div class="big" id="r-big" style="font-size:64px">The log is <span class="accent">the truth.</span></div>`,
    fx(p, c) { show($("r-1"), ease(seg(p, c.beat("Append") - 0.02, c.beat("Append") + 0.06))); show($("r-2"), ease(seg(p, c.beat("Saved") - 0.02, c.beat("Saved") + 0.06))); show($("r-3"), ease(seg(p, c.beat("journal") - 0.02, c.beat("journal") + 0.06))); show($("r-big"), ease(seg(p, c.beat("truth.") - 0.12, c.beat("truth.")))); },
  },

};
