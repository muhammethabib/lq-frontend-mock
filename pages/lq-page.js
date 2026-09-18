/* =========================================================
   LexiQamus · ortak sayfa betiği
   1) Üst banttaki logonun soluna hamburger menü; ana sayfadaki
      yan menünün aynısı soldan açılır.
   2) Soldaki içindekiler: alt başlıklar, bölüm kodları (A, A1 ya
      da 7, 7.1), okunan yerin işaretlenmesi, dar ekranda yapışkan
      içindekiler çubuğu.
   ========================================================= */
(function () {
  'use strict';
  var doc = document;
  var LANG = (doc.documentElement.lang || 'en').slice(0, 2) === 'tr' ? 'tr' : 'en';
  var FILE = location.pathname.split('/').pop() || '';

  /* ---------------- 1. YAN MENÜ ---------------- */
  var T = {
    en: { signIn: 'Sign in', signUp: 'Sign up', about: 'About', team: 'Team', what: 'What is LexiQamus?', guide: 'Instructions',
          updates: 'History of Suggestions and Corrections', lq3: 'LexiQamus 3.0', v3about: 'Digitization and Data Model', v3brochure: "What's New",
          lq2: 'LexiQamus 2.0', newFeatures: "What's New", lq1: 'LexiQamus 1.0', firstRelease: 'First Release (2016)', lexicon: 'Lexicon Digitization Project',
          institutional: 'Institutional Subscribers', menu: 'Menu', backTop: 'Back to top' },
    tr: { signIn: 'Giriş Yap', signUp: 'Kaydol', about: 'Hakkımızda', team: 'Ekip', what: 'LexiQamus Nedir?', guide: 'Kullanım Kılavuzu',
          updates: 'Öneri ve Düzeltme Geçmişi', lq3: 'LexiQamus 3.0', v3about: 'Dijitalleştirme ve Veri Modeli', v3brochure: 'Yenilikler',
          lq2: 'LexiQamus 2.0', newFeatures: 'Yenilikler', lq1: 'LexiQamus 1.0', firstRelease: 'İlk Sürüm (2016)', lexicon: 'Lexicon Dijitalleştirme Projesi',
          institutional: 'Kurumsal Üyeler', menu: 'Menü', backTop: 'Başa dön' }
  }[LANG];

  /* [en dosyası, tr dosyası] */
  var P = {
    about: ['about-en.html', 'hakkimizda-tr.html'],
    what: ['what-is-lexiqamus-en.html', 'lexiqamus-nedir-tr.html'],
    guide: ['user-guide-en.html', 'kullanim-kilavuzu-tr.html'],
    updates: ['suggestions-corrections-history-en.html', 'oneri-duzeltme-gecmisi-tr.html'],
    v3about: ['data-model-en.html', 'veri-modeli-tr.html'],
    v3brochure: ['lq3-whats-new-en.html', 'lq3-yenilikler-tr.html'],
    newFeatures: ['lq2-new-features-en.html', 'lq2-yeni-ozellikler-tr.html'],
    firstRelease: ['lq1-first-version-en.html', 'lq1-ilk-surum-tr.html'],
    lexicon: ['lexicon-digitization-en.html', 'lexicon-dijitallestirme-tr.html'],
    institutional: ['institutional-subscribers-en.html', 'kurumsal-uyeler-tr.html'],
    _team: ['team-en.html', 'ekip-tr.html']
  };
  function href(key) { return P[key][LANG === 'tr' ? 1 : 0]; }
  function isHere(key) { return P[key][0] === FILE || P[key][1] === FILE; }
  function counterpart(lang) {
    for (var k in P) { if (isHere(k)) { var f = P[k][lang === 'tr' ? 1 : 0]; return f === FILE ? null : f; } }
    return null;
  }
  var HOME = '../index.html' + (LANG === 'tr' ? '?lang=tr' : '');
  function esc(t) { var d = doc.createElement('div'); d.textContent = t; return d.innerHTML; }

  var ICON = {
    about: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"></circle><circle cx="12" cy="7.6" r="1.5" fill="var(--cut)"></circle><path d="M12 11.2v6" fill="none" stroke="var(--cut)" stroke-width="2.4"></path></svg>',
    team: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8.2" r="3.6" fill="currentColor"></circle><path d="M2.4 20.2c0-3.4 2.9-5.6 6.6-5.6s6.6 2.2 6.6 5.6z" fill="currentColor"></path><circle cx="17.4" cy="7.4" r="2.7" fill="currentColor" opacity="0.55"></circle><path d="M17.4 12.6c2.9 0 4.7 1.8 4.7 4.4h-4.2" fill="currentColor" opacity="0.55"></path></svg>',
    what: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"></circle><path d="M9.3 9.1a2.8 2.8 0 0 1 5.4.9c0 1.9-2.7 2.3-2.7 4" fill="none" stroke="var(--cut)" stroke-width="2.1"></path><circle cx="12" cy="17.3" r="1.4" fill="var(--cut)"></circle></svg>',
    guide: '<svg viewBox="0 0 24 24"><path d="M5.5 3.8A1.8 1.8 0 0 1 7.3 2h6.9l4.3 4.3V20a1.8 1.8 0 0 1-1.8 1.8H7.3A1.8 1.8 0 0 1 5.5 20z" fill="currentColor"></path><path d="M14 2.4V7h4.4" fill="none" stroke="var(--cut)" stroke-width="1.5"></path><path d="M9 12.5h6M9 16h6" fill="none" stroke="var(--cut)" stroke-width="1.8"></path></svg>',
    updates: '<svg viewBox="0 0 24 24"><path d="M3 21l1.2-4.8L15.4 5l3.6 3.6L7.8 19.8 3 21z" fill="currentColor"></path><path d="M16.6 3.8l1-1a1.9 1.9 0 0 1 2.7 0l.9.9a1.9 1.9 0 0 1 0 2.7l-1 1z" fill="currentColor"></path><path d="M14.2 6.2l3.6 3.6" fill="none" stroke="var(--cut)" stroke-width="1.5"></path></svg>',
    gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="2.6" fill="currentColor"></circle><path d="M12 2.2v4.2M12 17.6v4.2M2.2 12h4.2M17.6 12h4.2M5.1 5.1l3 3M15.9 15.9l3 3M18.9 5.1l-3 3M8.1 15.9l-3 3" fill="none" stroke="currentColor" stroke-width="2.7"></path></svg>',
    institutional: '<svg viewBox="0 0 24 24"><path d="M4.3 20.4V8.4L12 3.6l7.7 4.8v12z" fill="currentColor"></path><path d="M9.9 20.4v-4.2a2.1 2.1 0 0 1 4.2 0v4.2" fill="none" stroke="var(--cut)" stroke-width="1.7"></path><circle cx="9.2" cy="11" r="1.1" fill="var(--cut)"></circle><circle cx="14.8" cy="11" r="1.1" fill="var(--cut)"></circle><path d="M2.4 21h19.2" fill="none" stroke="currentColor" stroke-width="2.3"></path></svg>',
    chev: '<span class="side-link-chev"><svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></span>',
    up: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>',
    burger: '<svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>'
  };

  function yearTag(y) { return y ? '<span class="side-year">' + y + '</span>' : ''; }
  function link(key, label, url, icon, year) {
    return '<a class="side-link' + (isHere(key) ? ' active' : '') + '" href="' + url + '"' + (isHere(key) ? ' aria-current="page"' : '') + '>' +
      icon + '<span>' + esc(label) + '</span>' + yearTag(year) + (year ? '<span class="side-link-chev" aria-hidden="true"></span>' : '') + '</a>';
  }
  function sublink(key, label, url) {
    return '<a class="side-sublink' + (key && isHere(key) ? ' active' : '') + '" href="' + url + '"' + (key && isHere(key) ? ' aria-current="page"' : '') + '><span>' + esc(label) + '</span></a>';
  }
  function group(id, label, items, keys, year) {
    var open = keys.some(isHere);
    return '<button type="button" class="side-link side-link-parent" id="' + id + 'Toggle" aria-expanded="' + open + '" aria-controls="' + id + '">' +
      ICON.gear + '<span>' + esc(label) + '</span>' + yearTag(year) + ICON.chev + '</button>' +
      '<div class="side-submenu' + (open ? ' open' : '') + '" id="' + id + '">' + items + '</div>';
  }

  function buildMenu() {
    var bar = doc.querySelector('.lqbar');
    if (!bar || doc.getElementById('sideMenu')) return;
    var enTarget = counterpart('en'), trTarget = counterpart('tr');
    var html =
      '<div class="menu-scrim"></div>' +
      '<nav class="side-menu" id="sideMenu" aria-label="' + T.menu + '" aria-hidden="true">' +
        '<div class="side-menu-top">' +
          '<a class="side-logo-link" href="' + HOME + '" aria-label="LexiQamus"><img class="side-logo" alt="LexiQamus" src="../assets/lexiqamus-logo.png"></a>' +
          '<div class="lang-switch side-lang' + (LANG === 'tr' ? ' tr-active' : '') + '">' +
            '<span class="lang-thumb"></span>' +
            '<button class="lang-btn' + (LANG === 'en' ? ' active' : '') + '" data-lang="en" data-go="' + (enTarget || '') + '">EN</button>' +
            '<button class="lang-btn' + (LANG === 'tr' ? ' active' : '') + '" data-lang="tr" data-go="' + (trTarget || '') + '">TR</button>' +
          '</div>' +
        '</div>' +
        '<div class="side-auth">' +
          '<a class="side-btn ghost" href="' + HOME + '">' + esc(T.signIn) + '</a>' +
          '<a class="side-btn primary" href="' + HOME + '">' + esc(T.signUp) + '</a>' +
        '</div>' +
        '<div class="side-nav">' +
          link('about', T.about, href('about'), ICON.about) +
          link('_team', T.team, href('_team'), ICON.team) +
          link('what', T.what, href('what'), ICON.what) +
          link('guide', T.guide, href('guide'), ICON.guide) +
          link('institutional', T.institutional, href('institutional'), ICON.institutional) +
          group('lqSub3', T.lq3, sublink('v3about', T.v3about, href('v3about')) + sublink('v3brochure', T.v3brochure, href('v3brochure')), ['v3about', 'v3brochure'], '2026') +
          group('lqSub2', T.lq2, sublink('lexicon', T.lexicon, href('lexicon')) + sublink('newFeatures', T.newFeatures, href('newFeatures')), ['newFeatures', 'lexicon'], '2020') +
          link('firstRelease', T.lq1, href('firstRelease'), ICON.gear, '2016') +
          link('updates', T.updates, href('updates'), ICON.updates) +
        '</div>' +
      '</nav>';
    doc.body.insertAdjacentHTML('beforeend', html);

    var btn = doc.createElement('button');
    btn.type = 'button'; btn.className = 'menu-btn lqbar-menu'; btn.id = 'menuBtn';
    btn.setAttribute('aria-label', T.menu); btn.setAttribute('aria-controls', 'sideMenu'); btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = ICON.burger;
    var left = doc.createElement('div'); left.className = 'lqbar-left';
    var brand = bar.querySelector('.lqbar-brand');
    bar.insertBefore(left, brand); left.appendChild(btn); left.appendChild(brand);

    /* Ust cubuktaki dil dugmesi: sitenin geri kalanindaki gibi ikili anahtar */
    var right = bar.querySelector('.lqbar-right');
    if (right && !right.querySelector('.lang-switch')) {     /* HTML'de yoksa kur (eski sayfalar) */
      right.innerHTML =
        '<div class="lang-switch bar-lang' + (LANG === 'tr' ? ' tr-active' : '') + '" role="group" aria-label="' + (LANG === 'tr' ? 'Dil' : 'Language') + '">' +
          '<span class="lang-thumb"></span>' +
          '<button type="button" class="lang-btn' + (LANG === 'en' ? ' active' : '') + '" data-lang="en" data-go="' + (enTarget || '') + '"' +
            (LANG === 'en' ? ' aria-current="true"' : '') + '>EN</button>' +
          '<button type="button" class="lang-btn' + (LANG === 'tr' ? ' active' : '') + '" data-lang="tr" data-go="' + (trTarget || '') + '"' +
            (LANG === 'tr' ? ' aria-current="true"' : '') + '>TR</button>' +
        '</div>';
      right.querySelectorAll('.lang-btn').forEach(function (b) {
        b.addEventListener('click', function () { if (b.dataset.go) location.href = b.dataset.go; });
        if (!b.classList.contains('active') && !b.dataset.go) {
          b.disabled = true;
          b.title = LANG === 'tr' ? 'Bu sayfanın İngilizcesi henüz yok' : 'Not available in this language yet';
        }
      });
    }

    var menu = doc.getElementById('sideMenu'), scrim = doc.querySelector('.menu-scrim');
    function resetSubmenus() {
      /* Menüden çıkınca alt başlıklar varsayılana döner: yalnızca bulunulan sayfanın grubu açık kalır */
      menu.querySelectorAll('.side-link-parent').forEach(function (b) {
        var sub = doc.getElementById(b.getAttribute('aria-controls'));
        var keep = !!(sub && sub.querySelector('[aria-current="page"]'));
        if (sub) sub.classList.toggle('open', keep);
        b.setAttribute('aria-expanded', keep ? 'true' : 'false');
      });
    }
    function setMenu(open) {
      doc.body.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) { var a = menu.querySelector('.side-link'); if (a) a.focus({ preventScroll: true }); }
      else resetSubmenus();
    }
    btn.addEventListener('click', function () { setMenu(!doc.body.classList.contains('menu-open')); });
    scrim.addEventListener('click', function () { setMenu(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && doc.body.classList.contains('menu-open')) { setMenu(false); btn.focus(); } });
    menu.querySelectorAll('.side-link-parent').forEach(function (b) {
      b.addEventListener('click', function () {
        var sub = doc.getElementById(b.getAttribute('aria-controls'));
        var open = sub.classList.toggle('open');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
    menu.querySelectorAll('a[aria-current="page"]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); setMenu(false); });
    });
    menu.querySelectorAll('.lang-btn').forEach(function (b) {
      b.addEventListener('click', function () { if (b.dataset.go) location.href = b.dataset.go; });
      if (!b.classList.contains('active') && !b.dataset.go) { b.disabled = true; b.title = LANG === 'tr' ? 'Bu sayfanın İngilizcesi henüz yok' : 'Not available in this language yet'; }
    });
  }

  /* ---------------- 2. İÇİNDEKİLER ---------------- */
  var LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var CHEV = '<svg class="toc-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"></polyline></svg>';

  function slug(t) {
    var s = t.toLowerCase().replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'bolum';
    var id = s, n = 2; while (doc.getElementById(id)) id = s + '-' + (n++);
    return id;
  }
  /* "7.1. Başlık" → ["7.1", "Başlık"] */
  function splitNum(t) { var m = t.match(/^\s*(\d+(?:\.\d+)*)\.?\s+(.+)$/); return m ? [m[1], m[2]] : [null, t.trim()]; }

  function buildToc() {
    var nav = doc.querySelector('.layout > nav.toc');
    if (!nav) return;
    var layout = nav.parentElement;
    var main = layout.querySelector(':scope > main, :scope > .article');
    if (!main) return;
    var mode = doc.body.getAttribute('data-toc') || 'plain';
    var titleEl = nav.querySelector('.toc-title');
    var tocTitle = titleEl ? titleEl.textContent.trim() : (LANG === 'tr' ? 'Bu sayfada' : 'On this page');

    var entries = [];
    nav.querySelectorAll(':scope > a[href^="#"]').forEach(function (a) {
      var target = doc.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
      if (target) entries.push({ label: a.textContent.trim(), target: target, subs: [] });
    });
    if (!entries.length) return;

    /* her h3, belgede kendisinden önce gelen son bölüme bağlanır */
    if (mode !== 'plain') {
      main.querySelectorAll('h3').forEach(function (h) {
        if (h.closest('.footnotes, figure, aside')) return;
        var owner = null;
        entries.forEach(function (e) { if (e.target === h || (e.target.compareDocumentPosition(h) & Node.DOCUMENT_POSITION_FOLLOWING)) owner = e; });
        if (owner) owner.subs.push({ el: h });
      });
      /* bölümün tek alt başlığı bölüm adıyla aynıysa içindekilerde tekrar etmesin */
      entries.forEach(function (e) {
        if (e.subs.length === 1 && e.subs[0].el.textContent.trim().toLocaleLowerCase(LANG) === e.label.toLocaleLowerCase(LANG)) e.subs[0].hideInToc = true;
      });
    }

    var hasCodes = false;
    var li = 0;
    entries.forEach(function (e) {
      var h2 = e.target.tagName === 'H2' ? e.target : e.target.querySelector('h2');
      if (mode === 'letters') {
        if (h2) {
          e.code = LETTERS[li++];
          var inner = doc.createElement('span'); inner.className = 'sec-title';
          while (h2.firstChild) inner.appendChild(h2.firstChild);
          h2.appendChild(inner);
          h2.insertAdjacentHTML('afterbegin', '<span class="sec-letter" aria-hidden="true">' + e.code + '</span>');
          h2.classList.add('has-letter');
        }
        e.subs.forEach(function (s, i) {
          s.label = s.el.textContent.trim();
          if (e.code) { s.code = e.code + (i + 1); s.el.setAttribute('data-code', s.code); }
        });
      } else if (mode === 'decimal') {
        var sp = splitNum(e.label); e.code = sp[0]; e.label = sp[1];
        e.subs.forEach(function (s) { var p = splitNum(s.el.textContent); s.code = p[0]; s.label = p[1]; });
      }
      if (e.code) hasCodes = true;
      e.subs.forEach(function (s) {
        if (s.code) hasCodes = true;
        var box = s.el.parentElement;
        if (box && box.classList.contains('block') && box.id && box.firstElementChild === s.el) s.id = box.id;
        else s.id = s.el.id || (s.el.id = slug(s.label));
      });
    });

    /* görsellerdeki etiketler (a.pin) bağlandıkları başlığın kodunu kendiliğinden alır */
    var codeOf = {};
    entries.forEach(function (e) { if (e.code) codeOf[e.target.id] = e.code; e.subs.forEach(function (x) { if (x.code) codeOf[x.id] = x.code; }); });
    doc.querySelectorAll('a.pin[href^="#"]').forEach(function (pin) {
      var c = codeOf[decodeURIComponent(pin.getAttribute('href').slice(1))];
      if (c) { pin.textContent = c; pin.setAttribute('aria-label', c); }
    });
    /* metin içi bölüm bağlantıları (a.xref) hedefin kodunu küçük bir etiketle gösterir */
    doc.querySelectorAll('a.xref[href^="#"]').forEach(function (a) {
      var c = codeOf[decodeURIComponent(a.getAttribute('href').slice(1))];
      if (c) a.setAttribute('data-code', c);
    });

    var out = '<button class="toc-toggle" type="button" aria-expanded="false" aria-controls="lqTocList"><span class="toc-title">' + esc(tocTitle) + '</span><span class="toc-now"></span>' + CHEV + '</button>' +
      '<p class="toc-title">' + esc(tocTitle) + '</p><ol class="toc-list" id="lqTocList">';
    entries.forEach(function (e) {
      out += '<li><a class="toc-sec" href="#' + e.target.id + '" data-code="' + (e.code || '') + '" data-t="' + esc(e.label) + '">' +
        (e.code ? '<span class="k" aria-hidden="true">' + e.code + '</span>' : '') + esc(e.label) + '</a>';
      var shown = e.subs.filter(function (s) { return !s.hideInToc; });
      if (shown.length) {
        out += '<ol>';
        shown.forEach(function (s) {
          out += '<li><a href="#' + s.id + '" data-code="' + (s.code || '') + '" data-t="' + esc(s.label) + '">' +
            (s.code ? '<span class="n">' + s.code + '</span>' : '') + esc(s.label) + '</a></li>';
        });
        out += '</ol>';
      }
      out += '</li>';
    });
    nav.innerHTML = out + '</ol>';
    nav.classList.add('lqtoc');
    nav.setAttribute('data-mode', mode);
    if (hasCodes) nav.classList.add('has-codes');
    layout.classList.add('lqtoc-layout');
    doc.body.classList.add('has-lqtoc');

    var btn = nav.querySelector('.toc-toggle'), now = nav.querySelector('.toc-now');
    var links = [].slice.call(nav.querySelectorAll('.toc-list a'));
    var targets = links.map(function (l) {
      var el = doc.getElementById(l.getAttribute('href').slice(1));
      return el && el.classList.contains('block') ? (el.querySelector('h3') || el) : el;
    });
    function setOpen(v) { nav.classList.toggle('open', v); btn.setAttribute('aria-expanded', v ? 'true' : 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!nav.classList.contains('open')); });
    links.forEach(function (l) { l.addEventListener('click', function () { setOpen(false); }); });
    doc.addEventListener('click', function (e) { if (!nav.contains(e.target)) setOpen(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });

    var current = -1, ticking = false;
    function update() {
      ticking = false;
      var line = Math.min(window.innerHeight * 0.3, 240), idx = 0;
      for (var i = 0; i < targets.length; i++) { if (targets[i] && targets[i].getBoundingClientRect().top <= line) idx = i; }
      if (idx === current) return;
      current = idx;
      links.forEach(function (l, i) { l.classList.toggle('active', i === idx); });
      var a = links[idx], secLi = a.closest('.toc-list > li');
      nav.querySelectorAll('.toc-list > li').forEach(function (x) { x.classList.toggle('open', x === secLi); });
      var sec = secLi.querySelector('.toc-sec'); sec.classList.add('active');
      var code = a.dataset.code ? '<span class="nk">' + a.dataset.code + '</span>' : '';
      now.innerHTML = code + (a !== sec
        ? '<b class="ns">' + esc(sec.dataset.t) + '</b><span class="nsub">' + esc(a.dataset.t) + '</span>'
        : '<b>' + esc(sec.dataset.t) + '</b>');
      if (window.innerWidth > 900 && nav.scrollHeight > nav.clientHeight + 2) {
        var r = a.getBoundingClientRect(), t = nav.getBoundingClientRect();
        if (r.top < t.top + 40 || r.bottom > t.bottom - 20) nav.scrollTop += (r.top - t.top) - nav.clientHeight / 3;
      }
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', function () { current = -1; update(); });
    update();
    /* sayfa bir alt başlık adresiyle açıldıysa (#...) oraya git */
    if (location.hash) { var h = doc.getElementById(decodeURIComponent(location.hash.slice(1))); if (h) setTimeout(function () { h.scrollIntoView(); }, 30); }
  }

  /* ---------------- 3. UZUN SAYFALARDA YÜZEN "BAŞA DÖN" ----------------
     Sağ altta, kullanıcı ~1.5 ekran kaydırınca belirir, tepeye dönünce kaybolur.
     Kısa sayfalarda (iki ekran boyundan az) hiç kurulmaz. */
  function buildBackTop() {
    if (doc.getElementById('lqBackTop')) return;
    if (doc.documentElement.scrollHeight < window.innerHeight * 2) return;
    var b = doc.createElement('button');
    b.type = 'button'; b.id = 'lqBackTop'; b.className = 'lq-backtop';
    b.setAttribute('aria-label', T.backTop); b.setAttribute('title', T.backTop);
    b.innerHTML = ICON.up + '<span>' + esc(T.backTop) + '</span>';
    b.setAttribute('aria-hidden', 'true'); b.tabIndex = -1;                /* tepedeyken gizli */
    b.addEventListener('click', function () {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      var brand = doc.querySelector('.lqbar-brand');
      if (brand) brand.focus({ preventScroll: true });          /* klavye odağı da başa dönsün */
    });
    doc.body.appendChild(b);
    var shown = false, ticking = false;
    function update() {
      ticking = false;
      var want = window.scrollY > window.innerHeight * 1.5;
      if (want !== shown) { shown = want; b.classList.toggle('show', shown); b.setAttribute('aria-hidden', shown ? 'false' : 'true'); b.tabIndex = shown ? 0 : -1; }
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------------- 4. OSMANLICA PARÇALAR ----------------
     Düz metin içinde işaretsiz kalan Arap harfli parçaları <span class="ota" lang="ota" dir="rtl">
     ile sarar: doğru font/boyut (CSS) ve ekran okuyucu için dil bilgisi (WCAG 3.1.2). */
  var AR = '؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿';
  var AR_RUN = new RegExp('[' + AR + '](?:[' + AR + '‌‍]|\\s+(?=[' + AR + ']))*', 'g');
  var SKIP = 'script,style,textarea,code,pre,[dir="rtl"],[lang^="ar"],[lang^="ota"],.ota,.lqbar,.side-menu,.seq,.kk,.bk';
  function wrapArabic() {
    var root = doc.querySelector('.page-shell') || doc.body;
    /* zaten [dir=rtl] işaretli parçalara dil bilgisi (kılavuz dahil) */
    root.querySelectorAll('[dir="rtl"]:not([lang])').forEach(function (el) { el.setAttribute('lang', 'ota'); });
    if (doc.body.classList.contains('lq-guide')) return;      /* kılavuzun özel düzenine dokunma */
    var walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !new RegExp('[' + AR + ']').test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
        return n.parentElement && n.parentElement.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      var text = node.nodeValue, frag = doc.createDocumentFragment(), last = 0, m;
      AR_RUN.lastIndex = 0;
      while ((m = AR_RUN.exec(text))) {
        if (m.index > last) frag.appendChild(doc.createTextNode(text.slice(last, m.index)));
        var s = doc.createElement('span');
        s.className = 'ota'; s.setAttribute('lang', 'ota'); s.setAttribute('dir', 'rtl');
        s.textContent = m[0];
        frag.appendChild(s);
        last = m.index + m[0].length;
      }
      if (last < text.length) frag.appendChild(doc.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }

  function init() { buildMenu(); buildToc(); buildBackTop(); wrapArabic(); }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init); else init();
})();
