/*
 * UI — shared rendering helpers: escaping, KaTeX, progress bars, answer fields, modal dialogs.
 */
(function (root) {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* Generated question text: escape, then allow **bold**. Math stays in $…$ for KaTeX. */
  function rich(s) {
    return esc(s).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
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
    set: 'All values separated by commas, e.g. <code>{0, 1/7}</code>',
    prob: 'Exact fraction or a decimal with at least 3 decimals, e.g. <code>3/8</code> or <code>0.375</code>'
  };

  function hintFor(part) {
    if (part.kind === 'expr') return (part.upToConstant ? HINTS.exprC : HINTS.expr).replace('{vars}', part.vars.map(function (v) { return '<code>' + v + '</code>'; }).join(', '));
    if (part.kind === 'number' && part.tol && part.tol.abs) return HINTS.prob;
    return HINTS[part.kind] || '';
  }

  /*
   * Answer field for one part. Returns { el, get(), set(v), lock(), mark(result) }.
   */
  function answerField(part, idx, value, onInput) {
    var wrap = h('div', { class: 'part' });
    var id = 'ans-' + idx + '-' + Math.random().toString(36).slice(2, 7);
    var lab0 = h('label', { class: 'part__label', for: id }, rich(part.label));
    wrap.appendChild(lab0);
    math(lab0);
    var api = { el: wrap };

    if (part.kind === 'choice') {
      var list = h('div', { class: 'choices', role: 'radiogroup' });
      part.options.forEach(function (opt, i) {
        var lab = h('label', { class: 'choice' });
        var inp = h('input', { type: 'radio', name: id, value: String(i) });
        if (String(value) === String(i)) inp.checked = true;
        inp.addEventListener('change', function () { onInput && onInput(); });
        lab.appendChild(inp);
        lab.appendChild(h('span', { class: 'choice__letter' }, String.fromCharCode(65 + i)));
        lab.appendChild(h('span', { class: 'choice__text' }, rich(opt)));
        list.appendChild(lab);
      });
      wrap.appendChild(list);
      math(list);
      api.get = function () { var c = list.querySelector('input:checked'); return c ? c.value : ''; };
      api.lock = function () { list.querySelectorAll('input').forEach(function (i) { i.disabled = true; }); };
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
      if (!res.ok && showAnswer !== false) html += '<div class="part__correct">Correct answer: ' + (part.kind === 'choice' ? rich(part.options[part.answer]) : tex(part.latex)) + '</div>';
      fb.innerHTML = html;
      math(fb);
    };
    return api;
  }

  function solutionBlock(q) {
    var d = h('details', { class: 'solution' });
    d.innerHTML = '<summary>Worked solution</summary><ol>' + q.solution.map(function (s) { return '<li>' + rich(s) + '</li>'; }).join('') + '</ol>';
    math(d);
    return d;
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
  function num(x) { return (Math.round(x * 10) / 10).toString(); }

  root.UI = { esc: esc, rich: rich, math: math, tex: tex, h: h, bar: bar, answerField: answerField, solutionBlock: solutionBlock,
    confirm: confirmBox, toast: toast, param: param, fmtDate: fmtDate, fmtDur: fmtDur, num: num };
})(window);
