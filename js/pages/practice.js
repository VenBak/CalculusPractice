/* Practice: one topic, one question at a time, instant feedback, saved progress. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var topicId = UI.param('topic');
  var topic = topicId && Bank.topic(topicId);
  if (!topic) {
    app.innerHTML = '<div class="card empty"><h1>Choose a topic</h1><p>That topic does not exist. <a href="index.html">Back to all topics</a>.</p></div>';
    return;
  }
  var area = Bank.area(topic.area);
  document.title = topic.name + ' — Practice';

  var filter = sessionStorage.getItem('cpt.filter') || 'all';
  var questions = [], current = 0, fields = [], answered = false;

  Bank.load([topic.id]).then(function (bank) {
    questions = bank[topic.id];
    var want = parseInt(UI.param('q'), 10);
    if (want >= 1 && want <= questions.length) current = want - 1;
    else current = firstOpen();
    layout();
    show(current);
  }).catch(function (e) {
    app.innerHTML = '<div class="card empty"><p>Could not load the questions: ' + UI.esc(e.message) + '</p></div>';
  });

  function status(q) { var e = Store.progress()[q.id]; return e ? e.status : 'new'; }
  function firstOpen() {
    for (var i = 0; i < questions.length; i++) if (status(questions[i]) !== 'correct') return i;
    return 0;
  }
  function visible() {
    return questions.map(function (q, i) { return i; }).filter(function (i) {
      var s = status(questions[i]);
      return filter === 'all' || (filter === 'open' && s !== 'correct') || (filter === 'wrong' && s === 'wrong');
    });
  }

  function layout() {
    app.innerHTML =
      '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Topics</a><span>/</span><span>' + UI.esc(area.name) + '</span><span>/</span><span aria-current="page">' + UI.esc(topic.name) + '</span></nav>' +
      '<div class="practice-head"><div><h1>' + UI.esc(topic.name) + '</h1><p class="muted">' + UI.esc(topic.description) + '</p></div>' +
      '<div class="practice-head__progress" id="topic-progress"></div></div>' +
      '<div class="practice-layout">' +
      '<aside class="qnav card" aria-label="Questions in this topic">' +
      '<div class="seg" role="tablist" aria-label="Filter">' +
      ['all', 'open', 'wrong'].map(function (f) {
        return '<button role="tab" data-f="' + f + '" aria-selected="' + (f === filter) + '">' + { all: 'All', open: 'Not solved', wrong: 'Wrong' }[f] + '</button>';
      }).join('') + '</div>' +
      '<div class="qnav__grid" id="qgrid"></div>' +
      '<div class="legend small"><span><i class="dot dot--ok"></i>correct</span><span><i class="dot dot--bad"></i>wrong</span><span><i class="dot"></i>new</span></div>' +
      '<button class="btn btn--ghost btn--sm" id="reset">Reset this topic</button>' +
      '</aside>' +
      '<section class="qcard card" id="qcard" aria-live="polite"></section>' +
      '</div>' + helpBox();

    app.querySelectorAll('.seg button').forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.getAttribute('data-f');
        sessionStorage.setItem('cpt.filter', filter);
        app.querySelectorAll('.seg button').forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
        drawNav();
        var v = visible();
        if (v.length && v.indexOf(current) < 0) show(v[0]);
      });
    });
    document.getElementById('reset').addEventListener('click', function () {
      UI.confirm('Reset “' + topic.name + '”?', 'This clears your saved results for all ' + questions.length + ' questions in this topic. Exam history is kept.', 'Reset topic', true)
        .then(function (ok) { if (ok) { Store.resetTopic(topic.id); drawNav(); drawProgress(); show(0); UI.toast('Topic reset'); } });
    });
    UI.math(app.querySelector('.help'));
    drawProgress();
  }

  function drawProgress() {
    var s = Store.topicStats(topic.id, questions.length);
    document.getElementById('topic-progress').innerHTML =
      '<div class="pp__nums"><strong>' + s.correct + '</strong> of ' + s.total + ' correct' + (s.wrong ? ' · <span class="bad">' + s.wrong + ' wrong</span>' : '') + '</div>' +
      UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, size: 'lg', label: 'Topic progress' });
  }

  function drawNav() {
    var grid = document.getElementById('qgrid');
    var v = visible();
    if (!v.length) {
      grid.innerHTML = '<p class="muted small">' + (filter === 'wrong' ? 'Nothing wrong right now — nice.' : 'Every question in this topic is solved.') + '</p>';
      return;
    }
    grid.innerHTML = v.map(function (i) {
      var s = status(questions[i]);
      return '<button class="qbtn qbtn--' + s + (i === current ? ' is-current' : '') + '" data-i="' + i + '" aria-label="Question ' + (i + 1) + ', ' + s + '"' +
        (i === current ? ' aria-current="true"' : '') + '>' + (i + 1) + '</button>';
    }).join('');
    grid.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { show(Number(b.getAttribute('data-i'))); });
    });
  }

  function show(i) {
    current = i;
    answered = false;
    var q = questions[i];
    var prev = Store.progress()[q.id];
    history.replaceState(null, '', 'practice.html?topic=' + topic.id + '&q=' + (i + 1));
    var card = document.getElementById('qcard');
    card.innerHTML =
      '<div class="qcard__meta"><span>Question ' + (i + 1) + ' of ' + questions.length + '</span><span>' + q.points + ' pt</span>' +
      (prev ? '<span class="tag ' + (prev.status === 'correct' ? 'tag--ok' : 'tag--bad') + '">' + (prev.status === 'correct' ? 'solved before' : 'wrong last time') + '</span>' : '') + '</div>' +
      '<div class="prompt">' + UI.rich(q.prompt) + '</div>';
    UI.math(card.querySelector('.prompt'));
    var form = UI.h('form', { class: 'answers', novalidate: '' });
    fields = q.parts.map(function (p, k) {
      var f = UI.answerField(p, k, '', null);
      form.appendChild(f.el);
      return f;
    });
    var actions = UI.h('div', { class: 'actions' });
    actions.innerHTML = '<button type="submit" class="btn btn--primary">Check answer</button>' +
      '<button type="button" class="btn btn--ghost" id="skip">Skip</button>' +
      '<button type="button" class="btn btn--link" id="peek">Show solution without answering</button>';
    form.appendChild(actions);
    card.appendChild(form);
    var fb = UI.h('div', { class: 'feedback', id: 'feedback' });
    card.appendChild(fb);
    form.addEventListener('submit', function (e) { e.preventDefault(); if (!answered) check(q); });
    actions.querySelector('#skip').addEventListener('click', next);
    actions.querySelector('#peek').addEventListener('click', function () {
      if (fb.querySelector('.solution')) return;
      var s = UI.solutionBlock(q); s.open = true; fb.appendChild(s);
    });
    drawNav();
    if (fields[0] && fields[0].focus && window.matchMedia('(min-width: 800px)').matches) fields[0].focus();
  }

  function check(q) {
    var vals = fields.map(function (f) { return f.get(); });
    if (vals.every(function (v) { return String(v).trim() === ''; })) {
      UI.toast('Type an answer first (or press Skip)');
      return;
    }
    var res = q.parts.map(function (p, k) { return MathCheck.checkPart(vals[k], p); });
    // A parse error is not a wrong answer yet: let the student fix the syntax.
    var syntax = res.filter(function (r) { return r.error && !r.empty; });
    if (syntax.length) {
      res.forEach(function (r, k) { if (r.error) fields[k].mark(r, false); });
      return;
    }
    answered = true;
    var ok = res.every(function (r) { return r.ok; });
    res.forEach(function (r, k) { fields[k].mark(r); fields[k].lock(); });
    var formActions = document.querySelector('#qcard form .actions');
    if (formActions) formActions.hidden = true;
    Store.record(q.id, ok, 'practice', vals);
    var fb = document.getElementById('feedback');
    var nOk = res.filter(function (r) { return r.ok; }).length;
    fb.innerHTML = '<div class="verdict ' + (ok ? 'verdict--ok' : 'verdict--bad') + '">' +
      (ok ? '<strong>Correct.</strong> Saved to your progress.' : '<strong>Not quite' + (q.parts.length > 1 ? ' — ' + nOk + ' of ' + q.parts.length + ' parts right' : '') + '.</strong> Look through the worked solution, then try again later.') + '</div>';
    var sol = UI.solutionBlock(q);
    if (!ok) sol.open = true;
    fb.appendChild(sol);
    var act = UI.h('div', { class: 'actions' });
    act.innerHTML = '<button class="btn btn--primary" id="next">Next question →</button><button class="btn btn--ghost" id="retry">Try again</button>' +
      (ok ? '' : '<button class="btn btn--link" id="override" title="Use this if your answer is equivalent but the checker rejected it">My answer was right — count it</button>');
    fb.appendChild(act);
    act.querySelector('#next').addEventListener('click', next);
    act.querySelector('#retry').addEventListener('click', function () { show(current); });
    var ov = act.querySelector('#override');
    if (ov) ov.addEventListener('click', function () { Store.override(q.id); drawNav(); drawProgress(); ov.remove(); UI.toast('Counted as correct'); });
    act.querySelector('#next').focus({ preventScroll: true });
    drawNav();
    drawProgress();
  }

  function next() {
    var v = visible();
    if (!v.length) { show((current + 1) % questions.length); return; }
    var after = v.filter(function (i) { return i > current; });
    show(after.length ? after[0] : v[0]);
    document.getElementById('qcard').scrollIntoView({ block: 'nearest' });
  }

  function helpBox() {
    return '<details class="help card"><summary>How to type answers</summary><div class="help__grid">' +
      '<div><h4>Numbers & expressions</h4><ul>' +
      '<li>Fractions and powers: <code>3/4</code>, <code>x^2</code>, <code>e^(2x)</code>, <code>2^(1/3)</code></li>' +
      '<li>Functions: <code>sqrt(x)</code>, <code>ln(x)</code>, <code>sin(x)</code>, <code>arctan(x)</code>, <code>cbrt(x)</code>, <code>|x|</code></li>' +
      '<li>Constants: <code>pi</code>, <code>e</code>, <code>inf</code></li>' +
      '<li>Multiplication may be implicit (<code>2x</code>, <code>3pi</code>) but write <code>x*e^x</code>, not <code>xe^x</code>.</li>' +
      '<li>Any equivalent form is accepted: $\\tfrac{1}{\\sqrt e}$ = <code>e^(-1/2)</code>.</li></ul></div>' +
      '<div><h4>Intervals & sets</h4><ul>' +
      '<li>Intervals: <code>[0, 2)</code>, <code>(-inf, 1] U (3, inf)</code></li>' +
      '<li>All reals except points: <code>R \\ {-2, 3}</code></li>' +
      '<li>Lists of values: <code>{0, 1/7}</code> (order does not matter)</li>' +
      '<li>Probabilities: exact fraction, or a decimal to at least 3 decimals.</li></ul></div></div></details>';
  }
})();
