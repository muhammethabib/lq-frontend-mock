/* Metin parçalarını, ekran görüntülerindeki ile aynı motor (Chromium) ve
   aynı fontlarla, saydam zemin üzerinde PNG olarak basar.
   Girdi: JSON [{out, text, family, weight, size, color, ls, style, transform, lh, dsf, html}] */
const fs = require('fs');
const { launch, fontCss } = require('./lib');

(async () => {
  const CSS = fontCss();
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await launch();
  const byDsf = {};
  for (const j of jobs) { (byDsf[j.dsf || 2] = byDsf[j.dsf || 2] || []).push(j); }
  for (const dsf of Object.keys(byDsf)) {
    const p = await b.newPage({ viewport: { width: 1400, height: 400 }, deviceScaleFactor: Number(dsf) });
    await p.setContent(`<!doctype html><html><head><style>${CSS}
      html,body{margin:0;padding:0;background:transparent}
      #t{display:inline-block;white-space:pre;padding:0 0 0 0}
    </style></head><body><span id="t"></span></body></html>`);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    for (const j of byDsf[dsf]) {
      await p.evaluate(j => {
        const t = document.getElementById('t');
        if (j.html) { t.innerHTML = j.html; } else { t.textContent = j.text; }
        t.style.fontFamily = j.family || 'Inter, sans-serif';
        t.style.fontWeight = j.weight || '400';
        t.style.fontSize = j.size + 'px';
        t.style.color = j.color || '#000';
        t.style.letterSpacing = (j.ls !== undefined ? j.ls : 0) + 'em';
        t.style.fontStyle = j.style || 'normal';
        t.style.textTransform = j.transform || 'none';
        t.style.lineHeight = (j.lh || 1.2);
      }, j);
      await p.waitForTimeout(20);
      const el = await p.$('#t');
      await el.screenshot({ path: j.out, omitBackground: true });
    }
    await p.close();
  }
  await b.close();
  console.log('rendered', jobs.length);
})();
