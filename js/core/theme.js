/*
 * Theme — loaded in <head> (not deferred) so the right colours are applied before the page paints.
 * The choice is stored in localStorage ("cpt.theme" = "light" | "dark"); without a choice the system setting is used.
 */
(function () {
  'use strict';
  var KEY = 'cpt.theme';
  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function system() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function apply(t) {
    document.documentElement.setAttribute('data-theme', t);
  }
  var s = stored();
  apply(s === 'light' || s === 'dark' ? s : system());

  window.CalcTheme = {
    get: function () { return document.documentElement.getAttribute('data-theme') || 'light'; },
    set: function (t) {
      apply(t);
      try { localStorage.setItem(KEY, t); } catch (e) { /* private mode */ }
    },
    toggle: function () { this.set(this.get() === 'dark' ? 'light' : 'dark'); return this.get(); }
  };
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var follow = function () { var c = stored(); if (c !== 'light' && c !== 'dark') apply(system()); };
    if (mq.addEventListener) mq.addEventListener('change', follow);
  }
})();
