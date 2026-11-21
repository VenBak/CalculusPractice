/* Reference page: static formula sheet + extended reference. Renders the maths and lets you filter which sections show. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var btns = app.querySelectorAll('[data-show]');
  function show(what) {
    app.querySelectorAll('.ref-official').forEach(function (s) { s.hidden = what === 'extra'; });
    app.querySelectorAll('.ref-extra').forEach(function (s) { s.hidden = what === 'sheet'; });
    btns.forEach(function (b) {
      var on = b.getAttribute('data-show') === what;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  btns.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-show')); }); });
  UI.math(app);
})();
