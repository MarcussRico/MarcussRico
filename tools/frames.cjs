// Renders an SVG figure at chosen moments of its animation, in Chromium (and WebKit with --webkit).
//   node tools/frames.cjs assets/hero.svg 0,400,1200,6000 out-dir [--webkit] [--reduced]
const path = require("path");
const fs = require("fs");
const pw = require(process.env.PLAYWRIGHT_DIR || "playwright");
const [file, times, outDir, ...flags] = process.argv.slice(2);
(async () => {
  const engine = flags.includes("--webkit") ? pw.webkit : pw.chromium;
  const browser = await engine.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2, reducedMotion: flags.includes("--reduced") ? "reduce" : "no-preference" });
  const svg = fs.readFileSync(file, "utf8");
  await page.setContent(`<body style="margin:0;background:#0d1117">${svg}</body>`);
  fs.mkdirSync(outDir, { recursive: true });
  const name = path.basename(file, ".svg");
  for (const t of times.split(",").map(Number)) {
    await page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);
    await page.locator("svg").first().screenshot({ path: `${outDir}/${name}-${t}.png` });
  }
  const count = await page.evaluate(() => document.getAnimations().length);
  console.log(`${name}: ${count} animations, frames at ${times}`);
  await browser.close();
})();
