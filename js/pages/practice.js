/*
 * Practice: one topic (practice.html?topic=<id>) or random problems from all topics (practice.html?mode=random).
 * Instant feedback, hints, refresher guide, time per question (paused while flagged), saved progress.
 */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var random = UI.param('mode') === 'random';
  var topicId = UI.param('topic');
  var topic = topicId && Bank.topic(topicId);
  if (!random && !topic) {
    app.innerHTML = '<div class="card empty"><h1>Choose a topic</h1><p>That topic does not exist. <a href="index.html">Back to all topics</a> or try a <a href="practice.html?mode=random">random problem</a>.</p></div>';
    return;
  }

  var filter = sessionStorage.getItem('cpt.filter') || 'all';
  var rArea = sessionStorage.getItem('cpt.rArea') || 'all';
  var rOpen = sessionStorage.getItem('cpt.rOpen') === '1';
  var session = { n: 0, ok: 0 };
  var questions = [], current = 0, currentQ = null, fields = [], answered = false, sw = null, hints = null, hintCount = 0;

  window.addEventListener('pagehide', parkTime);

  if (random) {
    document.title = 'Random problem — Practice';
    Bank.load().then(function () { layoutRandom(); nextRandom(); });
  } else {
    var area = Bank.area(topic.area);
    document.title = topic.name + ' — Practice';
    Bank.load([topic.id]).then(function (bank) {
      questions = bank[topic.id];
      var want = parseInt(UI.param('q'), 10);
      current = want >= 1 && want <= questions.length ? want - 1 : firstOpen();
      layoutTopic(area);
      show(questions[current]);
    }).catch(function (e) {
      app.innerHTML = '<div class="card empty"><p>Could not load the questions: ' + UI.esc(e.message) + '</p></div>';
    });
  }

  function status(q) { var e = Store.progress()[q.id]; return e ? e.status : 'new'; }
  function firstOpen() {
    for (var i = 0; i < questions.length; i++) if (status(questions[i]) !== 'correct') return i;
    return 0;
  }
  function visible() {
    var flags = Store.flags();
    return questions.map(function (q, i) { return i; }).filter(function (i) {
      var q = questions[i], s = status(q);
      return filter === 'all' || (filter === 'open' && s !== 'correct') || (filter === 'wrong' && s === 'wrong') || (filter === 'flagged' && flags[q.id]);
    });
  }

  /* ------------------------------------------------------------ layouts */
  function layoutTopic(area) {
    app.innerHTML =
      '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Topics</a><span>/</span><span>' + UI.esc(area.name) + '</span><span>/</span><span aria-current="page">' + UI.esc(topic.name) + '</span></nav>' +
      '<div class="practice-head"><div><h1>' + UI.esc(topic.name) + '</h1><p class="muted">' + UI.esc(topic.description) + '</p></div>' +
      '<div class="practice-head__progress" id="topic-progress"></div></div>' +
      guidePanel(topic.id) +
      '<div class="practice-layout">' +
      '<aside class="qnav card" aria-label="Questions in this topic">' +
      '<div class="seg seg--wrap" role="tablist" aria-label="Filter">' +
      ['all', 'open', 'wrong', 'flagged'].map(function (f) {
        return '<button role="tab" data-f="' + f + '" aria-selected="' + (f === filter) + '">' + { all: 'All', open: 'Not solved', wrong: 'Wrong', flagged: 'Flagged' }[f] + '</button>';
      }).join('') + '</div>' +
      '<div class="qnav__grid" id="qgrid"></div>' +
      '<div class="legend small"><span><i class="dot dot--ok"></i>correct</span><span><i class="dot dot--bad"></i>wrong</span><span><i class="dot"></i>new</span><span><i class="dot dot--flag"></i>flagged</span></div>' +
      '<button class="btn btn--ghost btn--sm" id="rnd">' + UI.ICON.dice + ' Random question in this topic</button>' +
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
        if (v.length && v.indexOf(current) < 0) goto(v[0]);
      });
    });
    document.getElementById('rnd').addEventListener('click', function () {
      var v = visible().filter(function (i) { return i !== current; });
      if (!v.length) v = questions.map(function (_, i) { return i; }).filter(function (i) { return i !== current; });
      goto(v[Math.floor(Math.random() * v.length)]);
    });
    document.getElementById('reset').addEventListener('click', function () {
      UI.confirm('Reset “' + topic.name + '”?', 'This clears your saved results, logged times and flags for all ' + questions.length + ' questions in this topic. Exam history is kept.', 'Reset topic', true)
        .then(function (ok) { if (ok) { if (sw) sw.stop(); Store.resetTopic(topic.id); drawNav(); drawProgress(); goto(0, true); UI.toast('Topic reset'); } });
    });
    UI.math(app.querySelector('.help'));
    wireGuide();
    drawProgress();
  }

  function layoutRandom() {
    var areas = Bank.areas();
    app.innerHTML =
      '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Topics</a><span>/</span><span aria-current="page">Random problem</span></nav>' +
      '<div class="practice-head"><div><p class="eyebrow">Mixed practice</p><h1>Random problem</h1><p class="muted">A random question from any topic — the way exam questions arrive. Your answers count towards the topic progress as usual.</p></div>' +
      '<div class="practice-head__progress" id="session-stats"></div></div>' +
      '<div class="random-bar card"><div class="seg seg--wrap" role="tablist" aria-label="Area">' +
      [{ id: 'all', name: 'All areas' }].concat(areas).map(function (a) { return '<button role="tab" data-a="' + a.id + '" aria-selected="' + (a.id === rArea) + '">' + UI.esc(a.name) + '</button>'; }).join('') +
      '</div><label class="switch"><input type="checkbox" id="only-open"' + (rOpen ? ' checked' : '') + '><span>Only questions I have not solved yet</span></label>' +
      '<button class="btn btn--primary btn--sm" id="next-random">' + UI.ICON.dice + ' New random problem</button></div>' +
      '<section class="qcard card" id="qcard" aria-live="polite"></section>' + helpBox();
    app.querySelectorAll('.random-bar .seg button').forEach(function (b) {
      b.addEventListener('click', function () {
        rArea = b.getAttribute('data-a'); sessionStorage.setItem('cpt.rArea', rArea);
        app.querySelectorAll('.random-bar .seg button').forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
        nextRandom();
      });
    });
    document.getElementById('only-open').addEventListener('change', function (e) { rOpen = e.target.checked; sessionStorage.setItem('cpt.rOpen', rOpen ? '1' : '0'); nextRandom(); });
    document.getElementById('next-random').addEventListener('click', nextRandom);
    UI.math(app.querySelector('.help'));
    drawSession();
  }

  function pool() {
    var prog = Store.progress(), out = [];
    Bank.topics().forEach(function (t) {
      if (rArea !== 'all' && t.area !== rArea) return;
      (window.CalcBank[t.id] || []).forEach(function (q) {
        if (rOpen && prog[q.id] && prog[q.id].status === 'correct') return;
        out.push(q);
      });
    });
    return out;
  }
  function nextRandom() {
    var p = pool().filter(function (q) { return !currentQ || q.id !== currentQ.id; });
    if (!p.length) {
      parkTime();
      document.getElementById('qcard').innerHTML = '<div class="empty"><h2>Nothing left here</h2><p>You have solved every question in this selection. Switch off “only not solved” or pick another area.</p></div>';
      return;
    }
    show(p[Math.floor(Math.random() * p.length)]);
    document.getElementById('qcard').scrollIntoView({ block: 'nearest' });
  }
  function drawSession() {
    var el = document.getElementById('session-stats');
    if (!el) return;
    el.innerHTML = '<div class="pp__nums">This session: <strong>' + session.ok + '</strong> of ' + session.n + ' correct</div>' + UI.bar(session.n ? session.ok / session.n : 0, { size: 'lg', label: 'Session score' });
  }

  /* ------------------------------------------------------------ refresher guide */
  function guidePanel(tid) {
    var g = window.CalcGuides && window.CalcGuides[tid];
    if (!g) return '';
    return '<details class="guide-panel card" id="guide-panel"><summary>' + UI.ICON.book + '<span>Refresher: ' + UI.esc(g.title) + '</span><span class="muted small">theory, key formulas and a worked example</span></summary>' +
      '<div class="guide-body" id="guide-body"></div><p class="small"><a href="guide.html?topic=' + tid + '">Open the refresher as a page →</a></p></details>';
  }
  function wireGuide() {
    var panel = document.getElementById('guide-panel');
    if (!panel) return;
    panel.addEventListener('toggle', function () {
      var body = document.getElementById('guide-body');
      if (panel.open && !body.childNodes.length) { body.innerHTML = window.GuideView.html(topic.id); UI.math(body); }
    });
  }

  /* ------------------------------------------------------------ progress + navigator */
  function drawProgress() {
    var s = Store.topicStats(topic.id, questions.length);
    document.getElementById('topic-progress').innerHTML =
      '<div class="pp__nums"><strong>' + s.correct + '</strong> of ' + s.total + ' correct' + (s.wrong ? ' · <span class="bad">' + s.wrong + ' wrong</span>' : '') +
      (s.avgTime ? ' · <span title="Average time per answered attempt">avg ' + UI.fmtShort(s.avgTime) + '</span>' : '') + '</div>' +
      UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, size: 'lg', label: 'Topic progress' });
  }

  function drawNav() {
    var grid = document.getElementById('qgrid');
    if (!grid) return;
    var v = visible(), flags = Store.flags();
    if (!v.length) {
      grid.innerHTML = '<p class="muted small">' + ({ wrong: 'Nothing wrong right now — nice.', flagged: 'No flagged questions in this topic.' }[filter] || 'Every question in this topic is solved.') + '</p>';
      return;
    }
    grid.innerHTML = v.map(function (i) {
      var q = questions[i], s = status(q);
      return '<button class="qbtn qbtn--' + s + (flags[q.id] ? ' is-flag' : '') + (i === current ? ' is-current' : '') + '" data-i="' + i + '" aria-label="Question ' + (i + 1) + ', ' + s + (flags[q.id] ? ', flagged' : '') + '"' +
        (i === current ? ' aria-current="true"' : '') + '>' + (i + 1) + '</button>';
    }).join('');
    grid.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { goto(Number(b.getAttribute('data-i'))); });
    });
  }

  function goto(i, fresh) {
    current = i;
    if (fresh) currentQ = null;
    show(questions[i]);
  }

  /* ------------------------------------------------------------ time */
  function parkTime() {
    if (sw && currentQ && !answered) Store.setPending(currentQ.id, sw.elapsed());
    if (sw) { sw.destroy(); sw = null; }
  }
  function paintClock(sec) {
    var el = document.getElementById('qclock');
    if (!el) return;
    var flagged = currentQ && Store.isFlagged(currentQ.id);
    el.querySelector('span').textContent = UI.fmtShort(sec) + (flagged && !answered ? ' · paused' : '');
    el.classList.toggle('qtime--paused', !!flagged && !answered);
    el.classList.toggle('qtime--running', !flagged && !answered);
  }

  /* ------------------------------------------------------------ one question */
  function show(q) {
    parkTime();
    currentQ = q;
    answered = false;
    hintCount = 0;
    var t = Bank.topic(q.topic);
    var prev = Store.progress()[q.id];
    var flagged = Store.isFlagged(q.id);
    if (!random) history.replaceState(null, '', 'practice.html?topic=' + topic.id + '&q=' + (current + 1));
    var card = document.getElementById('qcard');
    card.innerHTML =
      '<div class="qcard__meta">' +
      (random ? '<a class="tag tag--topic" href="practice.html?topic=' + t.id + '">' + UI.esc(t.name) + '</a>' : '<span>Question ' + (current + 1) + ' of ' + questions.length + '</span>') +
      '<span>' + q.points + ' pt</span>' +
      (prev ? '<span class="tag ' + (prev.status === 'correct' ? 'tag--ok' : 'tag--bad') + '">' + (prev.status === 'correct' ? 'solved before' : 'wrong last time') + '</span>' : '') +
      '<span class="qcard__tools"><span class="qtime" id="qclock" title="Time spent on this question (paused while flagged)">' + UI.ICON.clock + '<span>0:00</span></span>' +
      '<button type="button" class="flag" id="qflag" aria-pressed="' + flagged + '" title="Flag this question — pauses its clock until you unflag it">' + UI.ICON.flag + '<span class="flag__txt">' + (flagged ? 'Flagged' : 'Flag') + '</span></button></span>' +
      '</div>' +
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
      '<button type="button" class="btn btn--ghost" id="skip">' + (random ? 'Skip' : 'Skip') + '</button>' +
      '<button type="button" class="btn btn--link" id="peek">Show solution without answering</button>';
    form.appendChild(actions);
    card.appendChild(form);
    hints = UI.hintBox(q.hints, function (n) { hintCount = n; });
    card.appendChild(hints);
    var fb = UI.h('div', { class: 'feedback', id: 'feedback' });
    card.appendChild(fb);
    form.addEventListener('submit', function (e) { e.preventDefault(); if (!answered) check(q); });
    actions.querySelector('#skip').addEventListener('click', next);
    actions.querySelector('#peek').addEventListener('click', function () {
      if (fb.querySelector('.solution')) return;
      fb.appendChild(UI.solutionBlock(q, true));
    });
    document.getElementById('qflag').addEventListener('click', function () {
      var on = !Store.isFlagged(q.id);
      Store.setFlag(q.id, on);
      this.setAttribute('aria-pressed', String(on));
      this.querySelector('.flag__txt').textContent = on ? 'Flagged' : 'Flag';
      if (!answered && sw) { if (on) sw.pause(); else sw.resume(); }
      paintClock(sw ? sw.elapsed() : 0);
      drawNav();
      UI.toast(on ? 'Flagged — the clock for this question is paused' : 'Unflagged — the clock runs again');
    });
    sw = new Stopwatch(Store.pending(q.id), paintClock);
    if (flagged) sw.paused = true;
    sw.start();
    drawNav();
    if (fields[0] && fields[0].focus && window.matchMedia('(min-width: 800px)').matches) fields[0].focus();
  }

  function check(q) {
    var vals = fields.map(function (f) { return f.get(); });
    if (vals.every(function (v) { return Array.isArray(v) ? !v.length : String(v).trim() === ''; })) {
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
    var secs = sw ? sw.stop() : 0;
    paintClock(secs);
    var ok = res.every(function (r) { return r.ok; });
    res.forEach(function (r, k) { fields[k].mark(r); fields[k].lock(); });
    var formActions = document.querySelector('#qcard form .actions');
    if (formActions) formActions.hidden = true;
    Store.record(q.id, ok, random ? 'random' : 'practice', vals, secs, hintCount);
    Store.setPending(q.id, 0);
    session.n++; if (ok) session.ok++;
    var fb = document.getElementById('feedback');
    var nOk = res.filter(function (r) { return r.ok; }).length;
    var ts = Store.topicStats(q.topic, Bank.topic(q.topic).count);
    fb.innerHTML = '<div class="verdict ' + (ok ? 'verdict--ok' : 'verdict--bad') + '">' +
      (ok ? '<strong>Correct.</strong> Saved to your progress.' : '<strong>Not quite' + (q.parts.length > 1 ? ' — ' + nOk + ' of ' + q.parts.length + ' parts right' : '') + '.</strong> Look through the worked solution, then try again later.') +
      '<span class="verdict__time">' + UI.ICON.clock + ' ' + UI.fmtShort(secs) + (ts.avgTime ? ' · your average in this topic: ' + UI.fmtShort(ts.avgTime) : '') + (hintCount ? ' · ' + hintCount + ' hint' + (hintCount > 1 ? 's' : '') + ' used' : '') + '</span></div>';
    fb.appendChild(UI.solutionBlock(q, !ok));
    var act = UI.h('div', { class: 'actions' });
    act.innerHTML = '<button class="btn btn--primary" id="next">' + (random ? 'Next random problem →' : 'Next question →') + '</button><button class="btn btn--ghost" id="retry">Try again</button>' +
      (ok ? '' : '<button class="btn btn--link" id="override" title="Use this if your answer is equivalent but the checker rejected it">My answer was right — count it</button>');
    fb.appendChild(act);
    act.querySelector('#next').addEventListener('click', next);
    act.querySelector('#retry').addEventListener('click', function () { show(q); });
    var ov = act.querySelector('#override');
    if (ov) ov.addEventListener('click', function () { Store.override(q.id); if (!random) { drawNav(); drawProgress(); } session.ok++; drawSession(); ov.remove(); UI.toast('Counted as correct'); });
    act.querySelector('#next').focus({ preventScroll: true });
    if (random) drawSession(); else { drawNav(); drawProgress(); }
  }

  function next() {
    if (random) { nextRandom(); return; }
    var v = visible();
    if (!v.length) { goto((current + 1) % questions.length); return; }
    var after = v.filter(function (i) { return i > current; });
    goto(after.length ? after[0] : v[0]);
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
      '<li>Probabilities: exact fraction, or a decimal to at least 3 decimals.</li></ul></div>' +
      '<div><h4>Hints, time and flags</h4><ul>' +
      '<li>The lightbulb shows a hint about the approach first, then one about the shape of the answer.</li>' +
      '<li>The clock logs your time per question. Flag a question to pause its clock; it continues when you unflag or come back.</li></ul></div></div></details>';
  }
})();
