// Меню на телефоне, уведомление о cookie, точный переход к блоку по ссылке
(function () {
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

  // Любая страница открывается с самого начала
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function toTop() { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  toTop();
  window.addEventListener('pageshow', toTop);

  // Рубрики галереи: показываем выбранную рубрику без прокрутки страницы
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
