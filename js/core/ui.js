/*
 * UI — shared rendering helpers: escaping, KaTeX, icons, progress bars, answer fields, hints, dialogs, theme toggle.
 */
(function (root) {
  'use strict';

  /* ---------------- icons (inline SVG, inherit currentColor) ---------------- */
  var ICON = {
    bulb: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.4 1.1 2.2v.5h5V16c0-.8.4-1.6 1.1-2.2A6 6 0 0 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    flag: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4m0 0h11l-2 4 2 4H5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    dice: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="8.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.4" fill="currentColor"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/></svg>',
    book: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    sun: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    moon: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
  };

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /*
   * Question text: escape, then allow **bold**, *italic* and [[img:path|alt]] figures.
   * Math stays in $…$ / $$…$$ for KaTeX.
   */
  function rich(s) {
    var figs = [];
    var t = String(s == null ? '' : s).replace(/\[\[img:([^|\]]+)\|([^\]]*)\]\]/g, function (m, src, alt) {
      figs.push('<span class="qfig"><img src="' + esc(src) + '" alt="' + esc(alt) + '" loading="lazy"></span>');
      return '\u0000' + (figs.length - 1) + '\u0000';
    });
    t = esc(t).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s.,;:)]|$)/g, '$1<em>$2</em>');
    return t.replace(/\u0000(\d+)\u0000/g, function (m, i) { return figs[Number(i)]; });
  }

  function math(el) {
    if (!el || !root.renderMathInElement) return;
    root.renderMathInElement(el, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
        { left: '\\(', right: '\\)', display: false }
      ],
      throwOnError: false,
      strict: false
    });
  }

  function tex(latex, display) {
    try { return root.katex.renderToString(latex, { throwOnError: false, displayMode: !!display, strict: false }); }
    catch (e) { return esc(latex); }
  }

  function h(tag, attrs, html) {
    var el = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'class') el.className = attrs[k];
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
      else el.setAttribute(k, attrs[k]);
    });
    if (html != null) el.innerHTML = html;
    return el;
  }

  function bar(fraction, opts) {
    opts = opts || {};
    var pct = Math.max(0, Math.min(100, Math.round(fraction * 100)));
    var wrong = opts.wrong != null ? Math.max(0, Math.min(100 - pct, Math.round(opts.wrong * 100))) : 0;
    return '<div class="bar' + (opts.size ? ' bar--' + opts.size : '') + '" role="progressbar" aria-valuenow="' + pct + '" aria-valuemin="0" aria-valuemax="100"' +
      (opts.label ? ' aria-label="' + esc(opts.label) + '"' : '') + '>' +
      '<span class="bar__fill" style="width:' + pct + '%"></span>' +
      (wrong ? '<span class="bar__wrong" style="width:' + wrong + '%"></span>' : '') + '</div>';
  }

  var HINTS = {
    number: 'Exact value, e.g. <code>3/4</code>, <code>-2</code>, <code>sqrt(2)/2</code>, <code>e^(1/2)</code>, <code>ln(3)</code>, <code>pi/4</code>',
    expr: 'Expression in {vars}, e.g. <code>2x*e^(3x)</code>, <code>ln(x^2+1)</code>, <code>(x+1)/(x-2)</code>',
    exprC: 'Antiderivative in {vars}; adding <code>+ C</code> is optional',
    interval: 'Interval notation, e.g. <code>(-inf, 2) U [3, inf)</code> or <code>R \\ {1}</code>',
    intervalLoose: 'Interval notation, e.g. <code>(-inf, 2)</code> — open or closed endpoints are both accepted here',
    set: 'All values separated by commas, e.g. <code>{0, 1/7}</code>',
    setVars: 'All values separated by commas; you may use {vars}, e.g. <code>{0, b}</code>',
    prob: 'Exact fraction or a decimal with at least 3 decimals, e.g. <code>3/8</code> or <code>0.375</code>'
  };
  function varList(vars) { return vars.map(function (v) { return '<code>' + v + '</code>'; }).join(', '); }

  function hintFor(part) {
    if (part.kind === 'expr') return (part.upToConstant ? HINTS.exprC : HINTS.expr).replace('{vars}', varList(part.vars));
    if (part.kind === 'number' && part.tol && part.tol.abs) return HINTS.prob;
    if (part.kind === 'interval') return part.ignoreClosure ? HINTS.intervalLoose : HINTS.interval;
    if (part.kind === 'set' && part.vars) return HINTS.setVars.replace('{vars}', varList(part.vars));
    return HINTS[part.kind] || '';
  }

  /* text of the correct answer of a part */
  function answerHtml(part) {
    if (part.kind === 'choice') return rich(part.options[part.answer]);
    if (part.kind === 'multi') return part.answer.map(function (i) { return rich(part.options[i]); }).join(', ');
    return tex(part.latex);
  }

  /*
   * Answer field for one part. Returns { el, get(), lock(), mark(result), focus() }.
   */
  function answerField(part, idx, value, onInput) {
    var wrap = h('div', { class: 'part' });
    var id = 'ans-' + idx + '-' + Math.random().toString(36).slice(2, 7);
    if (part.label) {
      var lab0 = h(part.kind === 'choice' || part.kind === 'multi' ? 'div' : 'label', { class: 'part__label', for: id }, rich(part.label));
      wrap.appendChild(lab0);
      math(lab0);
    }
    var api = { el: wrap };

    if (part.kind === 'choice' || part.kind === 'multi') {
      var multi = part.kind === 'multi';
      var list = h('div', { class: 'choices' + (multi ? ' choices--multi' : ''), role: multi ? 'group' : 'radiogroup' });
      var picked = multi ? (Array.isArray(value) ? value.map(String) : String(value || '').split(',')) : [String(value)];
      part.options.forEach(function (opt, i) {
        var lab = h('label', { class: 'choice' });
        var inp = h('input', { type: multi ? 'checkbox' : 'radio', name: id, value: String(i) });
        if (picked.indexOf(String(i)) >= 0 && value !== '' && value != null) inp.checked = true;
        inp.addEventListener('change', function () { onInput && onInput(); });
        lab.appendChild(inp);
        lab.appendChild(h('span', { class: 'choice__letter' }, String.fromCharCode(65 + i)));
        lab.appendChild(h('span', { class: 'choice__text' }, rich(opt)));
        list.appendChild(lab);
      });
      wrap.appendChild(list);
      math(list);
      if (multi) wrap.appendChild(h('div', { class: 'part__hint' }, 'Select every option that applies.'));
      api.get = function () {
        if (multi) return Array.prototype.map.call(list.querySelectorAll('input:checked'), function (c) { return Number(c.value); });
        var c = list.querySelector('input:checked'); return c ? c.value : '';
      };
      api.lock = function () { list.querySelectorAll('input').forEach(function (i) { i.disabled = true; }); };
      api.unlock = function () { list.querySelectorAll('input').forEach(function (i) { i.disabled = false; }); };
      api.focus = function () { var f = list.querySelector('input'); if (f) f.focus(); };
    } else {
      var row = h('div', { class: 'part__row' });
      var input = h('input', { id: id, class: 'answer', type: 'text', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
        placeholder: part.kind === 'interval' ? '(-inf, 2) U [3, inf)' : part.kind === 'set' ? '{a, b}' : 'type your answer' });
      input.value = value || '';
      var prev = h('div', { class: 'preview', 'aria-live': 'polite' });
      var upd = function () {
        var t = root.MathCheck.preview(input.value, part.kind);
        if (t === '') prev.innerHTML = '<span class="muted">preview</span>';
        else if (t === null) prev.innerHTML = '<span class="muted">…</span>';
        else prev.innerHTML = tex(t);
      };
      input.addEventListener('input', function () { upd(); onInput && onInput(); });
      row.appendChild(input);
      row.appendChild(prev);
      wrap.appendChild(row);
      wrap.appendChild(h('div', { class: 'part__hint' }, hintFor(part)));
      upd();
      api.get = function () { return input.value; };
      api.lock = function () { input.readOnly = true; };
      api.unlock = function () { input.readOnly = false; };
      api.focus = function () { input.focus(); };
      api.input = input;
    }
    api.mark = function (res, showAnswer) {
      wrap.classList.remove('is-ok', 'is-bad');
      wrap.classList.add(res.ok ? 'is-ok' : 'is-bad');
      var fb = wrap.querySelector('.part__fb') || wrap.appendChild(h('div', { class: 'part__fb' }));
      var html = res.ok ? '<span class="tag tag--ok">✓ Correct</span>' : '<span class="tag tag--bad">✗ ' + (res.empty ? 'No answer' : 'Incorrect') + '</span>';
      if (res.error) html += ' <span class="muted">' + esc(res.error) + '</span>';
      if (res.hint) html += ' <span class="muted">' + esc(res.hint) + '</span>';
      if (!res.ok && showAnswer !== false) html += '<div class="part__correct">Correct answer: ' + answerHtml(part) + '</div>';
      fb.innerHTML = html;
      math(fb);
    };
    return api;
  }

  function solutionBlock(q, open) {
    var d = h('details', { class: 'solution' });
    if (open) d.open = true;
    d.innerHTML = '<summary>Worked solution</summary><ol>' + q.solution.map(function (s) { return '<li>' + rich(s) + '</li>'; }).join('') + '</ol>';
    math(d);
    return d;
  }

  /*
   * Hint box: a lightbulb button that reveals the hints one by one.
   * onReveal(count) is called each time a new hint is shown.
   */
  function hintBox(hints, onReveal, startShown) {
    hints = (hints || []).filter(Boolean);
    var box = h('div', { class: 'hintbox' });
    if (!hints.length) return box;
    var shown = 0;
    var list = h('ol', { class: 'hintbox__list' });
    var btn = h('button', { type: 'button', class: 'btn btn--hint' });
    var label = function () {
      btn.innerHTML = ICON.bulb + '<span>' + (shown === 0 ? 'Hint' : shown < hints.length ? 'Another hint' : 'No more hints') + '</span>' +
        '<span class="hintbox__count">' + shown + '/' + hints.length + '</span>';
      btn.disabled = shown >= hints.length;
      btn.setAttribute('aria-label', shown < hints.length ? 'Show hint ' + (shown + 1) + ' of ' + hints.length : 'All hints shown');
    };
    var reveal = function (silent) {
      if (shown >= hints.length) return;
      var li = h('li', { class: 'hintbox__item' }, '<span class="hintbox__tag">' + (shown === 0 ? 'Approach' : 'Answer shape') + '</span> ' + rich(hints[shown]));
      list.appendChild(li);
      math(li);
      shown++;
      label();
      if (!silent && onReveal) onReveal(shown);
    };
    btn.addEventListener('click', function () { reveal(false); });
    box.appendChild(btn);
    box.appendChild(list);
    for (var i = 0; i < (startShown || 0); i++) reveal(true);
    label();
    box.count = function () { return shown; };
    return box;
  }

  /* -------- modal confirm (no window.confirm) -------- */
  function confirmBox(title, body, okText, danger) {
    return new Promise(function (resolve) {
      var back = h('div', { class: 'modal-back' });
      var box = h('div', { class: 'modal', role: 'dialog', 'aria-modal': 'true', 'aria-label': title });
      box.innerHTML = '<h3>' + esc(title) + '</h3><p>' + body + '</p><div class="modal__actions">' +
        '<button class="btn btn--ghost" data-v="0">Cancel</button><button class="btn ' + (danger ? 'btn--danger' : 'btn--primary') + '" data-v="1">' + esc(okText || 'OK') + '</button></div>';
      back.appendChild(box);
      document.body.appendChild(back);
      var done = function (v) { document.removeEventListener('keydown', key); back.remove(); resolve(v); };
      var key = function (e) { if (e.key === 'Escape') done(false); };
      document.addEventListener('keydown', key);
      back.addEventListener('click', function (e) { if (e.target === back) done(false); });
      box.querySelectorAll('button').forEach(function (b) { b.addEventListener('click', function () { done(b.getAttribute('data-v') === '1'); }); });
      box.querySelector('[data-v="1"]').focus();
    });
  }

  function toast(msg) {
    var t = h('div', { class: 'toast', role: 'status' }, esc(msg));
    document.body.appendChild(t);
    setTimeout(function () { t.classList.add('toast--out'); }, 2200);
    setTimeout(function () { t.remove(); }, 2700);
  }

  function param(name) { return new URLSearchParams(root.location.search).get(name); }

  function fmtDate(ts) {
    var d = new Date(ts);
    return d.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) + ', ' +
      d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
  }
  function fmtDur(sec) {
    sec = Math.max(0, Math.round(sec));
    var hh = Math.floor(sec / 3600), mm = Math.floor(sec % 3600 / 60), ss = sec % 60;
    return hh + ':' + ('0' + mm).slice(-2) + ':' + ('0' + ss).slice(-2);
  }
  /* short "m:ss" (or "h:mm:ss") for per-question times */
  function fmtShort(sec) {
    sec = Math.max(0, Math.round(sec || 0));
    if (sec >= 3600) return fmtDur(sec);
    return Math.floor(sec / 60) + ':' + ('0' + sec % 60).slice(-2);
  }
  function num(x) { return (Math.round(x * 10) / 10).toString(); }

  /* -------- theme toggle in the header -------- */
  function themeToggle() {
    var nav = document.querySelector('.site-header__inner');
    if (!nav || !root.CalcTheme || document.getElementById('theme-toggle')) return;
    var b = h('button', { type: 'button', id: 'theme-toggle', class: 'theme-toggle' });
    var paint = function () {
      var dark = root.CalcTheme.get() === 'dark';
      b.innerHTML = dark ? ICON.sun : ICON.moon;
      b.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      b.title = dark ? 'Light mode' : 'Dark mode';
    };
    b.addEventListener('click', function () { root.CalcTheme.toggle(); paint(); });
    paint();
    nav.appendChild(b);
  }
  themeToggle();

  /* -------- highlight the nav link that matches the full URL (e.g. practice.html?mode=random) -------- */
  (function markNav() {
    var here = (location.pathname.split('/').pop() || 'index.html') + location.search;
    var links = document.querySelectorAll('.site-nav a'), hit = null;
    for (var i = 0; i < links.length; i++) if (links[i].getAttribute('href') === here) hit = links[i];
    if (!hit) return;
    for (var j = 0; j < links.length; j++) links[j].removeAttribute('aria-current');
    hit.setAttribute('aria-current', 'page');
  })();

  root.UI = { ICON: ICON, esc: esc, rich: rich, math: math, tex: tex, h: h, bar: bar, answerField: answerField, answerHtml: answerHtml,
    solutionBlock: solutionBlock, hintBox: hintBox, confirm: confirmBox, toast: toast, param: param, fmtDate: fmtDate, fmtDur: fmtDur,
    fmtShort: fmtShort, num: num };
})(window);
