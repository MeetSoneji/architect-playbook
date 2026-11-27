// Render every frame of a built video page to PNG. Usage: node frames.js page.html outdir fps
const { chromium } = require("playwright");
(async () => {
  const [page, out, fps] = [process.argv[2], process.argv[3], +process.argv[4] || 24];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  const errs = []; p.on("pageerror", e => errs.push(e.message));
  await p.addInitScript(() => { window.__export = true; });
  await p.goto("file://" + page); await p.waitForTimeout(1500);
  await p.evaluate(() => document.fonts.ready);
  if (errs.length) { console.error(errs); process.exit(1); }
  const total = await p.evaluate(() => window.__total);
  const stage = p.locator("#stage");
  const n = Math.ceil(total * fps);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.__render(t), i / fps);
    await stage.screenshot({ path: `${out}/f_${String(i).padStart(5, "0")}.png` });
    if (i % 240 === 0) console.log(`frame ${i}/${n}`);
  }
  await b.close();
})();
