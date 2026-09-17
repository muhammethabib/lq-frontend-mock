/* Ortak yardımcılar: Chromium'u bulur, yerel Google Fonts CSS'ini okur.
   Görsellerdeki metinler siteyle aynı motorda ve aynı fontlarla basılsın diye
   ağ kapalıyken de çalışan yerel bir font paketi kullanılır (fonts/gf-local.css). */
const fs = require('fs');
const path = require('path');
/* playwright yerel ya da global kurulumdan yüklenir */
function loadPlaywright() {
  try { return require('playwright'); } catch (e) {
    try {
      const root = require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim();
      return require(path.join(root, 'playwright'));
    } catch (_) { throw e; }
  }
}
const { chromium } = loadPlaywright();

function chromePath() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (root && fs.existsSync(root)) {
    const direct = path.join(root, 'chromium');
    if (fs.existsSync(direct) && fs.statSync(direct).isFile()) return direct;
    for (const d of fs.readdirSync(root)) {
      if (!d.startsWith('chromium')) continue;
      const p = path.join(root, d, 'chrome-linux', 'chrome');
      if (fs.existsSync(p)) return p;
    }
  }
  return null; // playwright kendi indirdiği tarayıcıyı kullanır
}

function launch(opts = {}) {
  const exe = chromePath();
  return chromium.launch(exe ? Object.assign({ executablePath: exe }, opts) : opts);
}

function fontCss() {
  const p = path.join(__dirname, 'fonts', 'gf-local.css');
  if (!fs.existsSync(p)) {
    throw new Error('fonts/gf-local.css yok — önce `python3 fetch-fonts.py` çalıştırın.');
  }
  return fs.readFileSync(p, 'utf8');
}

/* Sayfayı, Google Fonts istekleri yerel pakete yönlendirilmiş olarak açar. */
async function openPage(browser, fileUrl, opts = {}) {
  const css = fontCss();
  const p = await browser.newPage({
    viewport: { width: opts.w || 1280, height: opts.h || 1000 },
    deviceScaleFactor: opts.dsf || 1
  });
  await p.route('**/fonts.googleapis.com/**', r => r.fulfill({ status: 200, contentType: 'text/css', body: css }));
  await p.route('**/fonts.gstatic.com/**', r => r.abort());
  await p.goto(fileUrl);
  await p.waitForTimeout(opts.wait || 1500);
  return p;
}

module.exports = { launch, chromePath, fontCss, openPage };
