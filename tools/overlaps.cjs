// Flags painted text in a figure that overlaps other painted text, at the animation's end state.
//   node tools/overlaps.cjs assets/*.svg
const fs = require("fs");
const pw = require(process.env.PLAYWRIGHT_DIR || "playwright");
(async () => {
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  let bad = 0;
  for (const file of process.argv.slice(2)) {
    await page.setContent(`<body style="margin:0">${fs.readFileSync(file, "utf8")}</body>`);
    await page.evaluate(() => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = 60000; }));
    const hits = await page.evaluate(() => {
      const painted = (el) => { for (let e = el; e && e.tagName !== "svg"; e = e.parentElement) { const s = getComputedStyle(e); if (+s.opacity < 0.05 || s.display === "none" || s.visibility === "hidden") return false; } return true; };
      // a run of text = a <g fill> whose children are glyph groups of <use>; the looping highlight
      // (.scan) deliberately redraws a label over itself, so it is left out
      const runs = [...document.querySelectorAll("g[fill]")].filter((g) => g.querySelector(":scope > g > use") && !g.closest(".scan") && painted(g));
      // compare glyph by glyph: a rotated label's axis-aligned box is far bigger than its letters
      const glyphs = runs.map((g, k) => [...g.querySelectorAll("use")].map((u) => ({ k, r: u.getBoundingClientRect() })).filter((x) => x.r.width > 0.5));
      const flat = glyphs.flat();
      const out = [];
      for (let i = 0; i < flat.length; i++) for (let j = i + 1; j < flat.length; j++) {
        if (flat[i].k === flat[j].k) continue;
        const a = flat[i].r, b = flat[j].r;
        const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left), iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (ix > 0.5 && iy > 0.5) out.push(`runs ${flat[i].k} and ${flat[j].k} at ${Math.round(a.x)},${Math.round(a.y)} (${ix.toFixed(1)}x${iy.toFixed(1)}px)`);
      }
      const boxes = runs;
      return { n: boxes.length, out };
    });
    bad += hits.out.length;
    console.log(`${file}: ${hits.n} text runs, ${hits.out.length} overlaps${hits.out.length ? "\n  " + hits.out.join("\n  ") : ""}`);
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
