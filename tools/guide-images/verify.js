/* Sayfa denetimi: kırık görsel, kırık iç bağlantı, konsol hatası.
   Kullanım: node verify.js pages/user-guide-en.html [çıktı.png] */
const path = require('path');
const { launch, openPage } = require('./lib');

const REPO = path.resolve(__dirname, '..', '..');
const rel = process.argv[2] || 'pages/user-guide-en.html';
const shot = process.argv[3];

(async () => {
  const b = await launch();
  const errs = [];
  const url = 'file://' + path.join(REPO, rel);
  const p = await openPage(b, url, { w: 1280, h: 1000 });
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(2500);
  const info = await p.evaluate(() => {
    const imgs = [...document.images];
    const bad = [...document.querySelectorAll('a[href^="#"]')]
      .map(a => a.getAttribute('href').slice(1))
      .filter(h => h && !document.getElementById(decodeURIComponent(h)));
    return {
      title: document.title,
      lang: document.documentElement.lang,
      imgTotal: imgs.length,
      imgBroken: imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')),
      brokenAnchors: [...new Set(bad)]
    };
  });
  console.log(JSON.stringify(info, null, 1));
  console.log('CONSOLE ERRORS:', errs.length ? errs : 'none');
  if (shot) { await p.screenshot({ path: shot, fullPage: false }); }
  await b.close();
})();
