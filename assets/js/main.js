// Меню, cookie, позиция прокрутки, «Назад», «Наверх», фильтр галереи
(function () {
  // ---------- Меню на телефоне ----------
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // ---------- Уведомление о cookie ----------
  var bar = document.getElementById('cookie');
  if (bar) {
    var accepted = false;
    try { accepted = localStorage.getItem('cookie-ok') === '1'; } catch (e) {}
    if (!accepted) bar.hidden = false;
    bar.querySelector('button').addEventListener('click', function () {
      bar.hidden = true;
      try { localStorage.setItem('cookie-ok', '1'); } catch (e) {}
    });
  }

  // ---------- Позиция прокрутки ----------
  // Новая страница открывается с начала. При возврате («Назад» в браузере
  // или на сайте) страница встаёт на то место, откуда человек ушёл.
  function keyNow() { return 'pos:' + location.pathname + location.search; }
  var key = keyNow();
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function jump(y) { window.scrollTo({ top: y, left: 0, behavior: 'instant' }); }
  function save() { try { sessionStorage.setItem(keyNow(), String(Math.round(window.pageYOffset))); } catch (e) {} }

  var navType = '';
  try { navType = (performance.getEntriesByType('navigation')[0] || {}).type || ''; } catch (e) {}
  var saved = null;
  try { saved = sessionStorage.getItem(key); } catch (e) {}

  if ((navType === 'back_forward' || navType === 'reload') && saved !== null) {
    var y = parseInt(saved, 10) || 0;
    jump(y);
    // шрифты и картинки могут догрузиться и сдвинуть вёрстку — повторяем
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { jump(y); });
    window.addEventListener('load', function () { jump(y); });
  } else {
    jump(0);
  }
  window.addEventListener('pagehide', save);
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (a && !a.hasAttribute('data-back')) save();
  });

  // ---------- Кнопка «Назад» ----------
  document.querySelectorAll('[data-back]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var fromSite = false;
      try { fromSite = document.referrer && new URL(document.referrer).origin === location.origin; } catch (err) {}
      if (fromSite && history.length > 1) { e.preventDefault(); history.back(); }
    });
  });

  // ---------- Кнопка «Наверх» ----------
  var up = document.querySelector('.to-top');
  if (up) {
    var onScroll = function () { up.hidden = window.pageYOffset < 900; };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    up.addEventListener('click', function () {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'instant' : 'smooth' });
    });
  }

  // ---------- Рубрики галереи: фильтр без прокрутки ----------
  var chips = document.querySelectorAll('.rubrics a[data-r]');
  var groups = document.querySelectorAll('[data-rubric]');
  function show(r) {
    var any = false;
    groups.forEach(function (g) { var on = r === 'all' || g.getAttribute('data-rubric') === r; g.hidden = !on; any = any || on; });
    if (!any) { r = 'all'; groups.forEach(function (g) { g.hidden = false; }); }
    chips.forEach(function (c) { if (c.getAttribute('data-r') === r) c.setAttribute('aria-current', 'true'); else c.removeAttribute('aria-current'); });
  }
  if (chips.length) {
    var start = 'all';
    try { start = new URLSearchParams(location.search).get('r') || 'all'; } catch (e) {}
    show(start);
    chips.forEach(function (c) {
      c.addEventListener('click', function (e) {
        e.preventDefault();
        var r = c.getAttribute('data-r');
        show(r);
        try { history.replaceState(null, '', r === 'all' ? 'galereya.html' : 'galereya.html?r=' + r); } catch (err) {}
      });
    });
  }
})();
