/* One past exam: intro → timed run (shared ExamRunner), or browse mode with hints, answer checking and solutions. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var id = UI.param('id');
  var meta = id && Bank.pastMeta(id);
  if (!meta) {
    app.innerHTML = '<div class="card empty"><h1>Exam not found</h1><p><a href="past-exams.html">Back to all past exams</a></p></div>';
    return;
  }
  var title = Bank.pastTitle(meta);
  document.title = title + ' — Past exam';

  Promise.all([Bank.load(), Bank.loadPast([id])]).then(function () {
    var a = Store.active();
    if (UI.param('mode') === 'browse') { browse(); return; }
    if (a && a.kind === 'past' && a.pastId === id) { run(a); return; }
    if (a) { otherActive(a); return; }
    intro();
  }).catch(function (e) { app.innerHTML = '<div class="card empty"><p>' + UI.esc(e.message) + '</p></div>'; });

  function otherActive(a) {
    var href = a.kind === 'past' ? 'past-exam.html?id=' + encodeURIComponent(a.pastId) : 'exam.html';
    app.innerHTML = '<section class="card empty"><h1>Another exam is in progress</h1><p>You are in the middle of <strong>' + UI.esc(a.title || 'a practice exam') + '</strong>. Finish or abandon it first.</p>' +
      '<div class="actions actions--center"><a class="btn btn--primary" href="' + href + '">Go to that exam</a><a class="btn btn--ghost" href="past-exam.html?id=' + encodeURIComponent(id) + '&amp;mode=browse">Browse this exam instead</a></div></section>';
  }

  function intro() {
    var ex = Bank.pastExam(id);
    var h = Math.floor(meta.minutes / 60), m = meta.minutes % 60;
    app.innerHTML =
      '<nav class="crumbs"><a href="past-exams.html">Past exams</a><span>/</span><span aria-current="page">' + UI.esc(meta.date) + '</span></nav>' +
      '<section class="exam-intro card">' +
      '<p class="eyebrow">' + UI.esc(meta.year) + ' · ' + (meta.sitting === 1 ? 'first exam' : 'second exam') + ' · ' + UI.esc(meta.kind) + '</p>' +
      '<h1>IBC017 Calculus and Probability — ' + UI.esc(meta.kind) + '</h1><p class="lede">' + UI.esc(meta.date) + '</p>' +
      '<div class="exam-intro__facts"><div><strong>' + h + ':' + ('0' + m).slice(-2) + ':00</strong><span>time (as on the paper)</span></div><div><strong>90</strong><span>points + 10 free</span></div><div><strong>' + meta.questions + '</strong><span>questions</span></div><div><strong>' + meta.items + '</strong><span>answer items</span></div></div>' +
      '<h2>Instructions from the paper</h2><ul class="rules">' + ex.instructions.map(function (s) { return '<li>' + UI.esc(s) + '</li>'; }).join('') + '</ul>' +
      '<h2>On this site</h2><ul class="rules">' +
      '<li>The questions are exactly those of the paper; you type only the final answers, which are marked automatically against the official solutions.</li>' +
      '<li>Points of a question with several answer boxes are split over the boxes (the paper does not give the split), so your score approximates the official marking, which also rewards correct working.</li>' +
      '<li>Your time per question is logged. Flagging a question pauses its clock until you unflag it.</li>' +
      '<li>Hints (lightbulb) are available but their use is shown in the results — skip them for a realistic attempt.</li></ul>' +
      (meta.note ? '<p class="small muted">' + UI.esc(meta.note) + '</p>' : '') +
      '<div class="actions"><button class="btn btn--primary btn--lg" id="start">Start — the ' + meta.minutes + '-minute clock starts now</button>' +
      '<a class="btn btn--ghost" href="past-exam.html?id=' + encodeURIComponent(id) + '&amp;mode=browse">Browse questions instead</a></div>' +
      '</section>';
    document.getElementById('start').addEventListener('click', start);
  }

  function start() {
    var items = Bank.pastItems(id);
    var now = Date.now();
    var state = { id: 'past-' + id + '-' + now.toString(36), kind: 'past', pastId: id, title: title, minutes: meta.minutes,
      startedAt: now, endsAt: now + meta.minutes * 60000,
      items: items.map(function (it) { return { ref: it.ref, mode: 'open', points: it.points }; }),
      answers: {}, flags: {}, times: {}, hints: {} };
    Store.setActive(state);
    run(state);
    window.scrollTo(0, 0);
  }

  function groupsFor() {
    var items = Bank.pastItems(id), ex = Bank.pastExam(id), groups = [];
    ex.questions.forEach(function (q, gi) {
      var idxs = [], labels = [], short = [];
      items.forEach(function (it, k) {
        if (it.gi !== gi) return;
        idxs.push(k);
        labels.push(q.items[it.ii].label);
        short.push(q.items[it.ii].label.replace(/[()]/g, ''));
      });
      groups.push({ no: q.no, title: '', points: q.points, intro: idxs.length > 1 ? q.intro : '', items: idxs, labels: labels, short: short });
    });
    return groups;
  }

  function run(state) {
    ExamRunner.mount({ app: app, state: state, paper: { groups: groupsFor() }, onAbandon: intro });
  }

  /* ---------------- browse mode ---------------- */
  function browse() {
    var ex = Bank.pastExam(id), items = Bank.pastItems(id);
    app.innerHTML = '<nav class="crumbs"><a href="past-exams.html">Past exams</a><span>/</span><span aria-current="page">' + UI.esc(meta.date) + ' — browse</span></nav>' +
      '<div class="page-head"><p class="eyebrow">' + UI.esc(meta.year) + ' · ' + UI.esc(meta.kind) + ' · ' + meta.minutes + ' minutes</p><h1>' + UI.esc(meta.date) + '</h1>' +
      '<p class="muted">Study mode: no timer, nothing is logged. Check single answers, open hints or reveal the official solution.</p>' +
      '<div class="actions"><a class="btn btn--primary" href="past-exam.html?id=' + encodeURIComponent(id) + '">Sit this exam timed</a><button class="btn btn--ghost" id="expand">Show all solutions</button></div></div>' +
      '<div id="browse" class="browse"></div>';
    var list = document.getElementById('browse');
    ex.questions.forEach(function (q, gi) {
      var sec = UI.h('section', { class: 'exam-q card' });
      var multi = q.items.length > 1;
      sec.innerHTML = '<header class="exam-q__head"><h2>' + UI.esc(q.no) + '.</h2><span class="pts">' + UI.num(q.points) + ' pt</span></header>' +
        (multi && q.intro ? '<div class="prompt exam-q__intro">' + UI.rich(q.intro) + '</div>' : '');
      if (multi) UI.math(sec.querySelector('.exam-q__intro'));
      items.forEach(function (it) {
        if (it.gi !== gi) return;
        var box = UI.h('div', { class: 'exam-item' + (multi ? ' exam-item--sub' : '') });
        box.innerHTML = '<div class="exam-item__head">' + (multi ? '<span class="exam-item__label">' + UI.esc(q.items[it.ii].label) + '</span><span class="pts pts--sm">' + UI.num(it.points) + ' pt</span>' : '') +
          '<span class="tag">' + UI.esc((Bank.topic(it.topic) || {}).name || '') + '</span></div>';
        var pr = UI.h('div', { class: 'prompt' }, UI.rich(it.prompt));
        box.appendChild(pr); UI.math(pr);
        var fields = it.parts.map(function (p, j) { var f = UI.answerField(p, it.ref + j, '', null); box.appendChild(f.el); return f; });
        var act = UI.h('div', { class: 'actions' });
        act.innerHTML = '<button class="btn btn--primary btn--sm" type="button">Check</button>';
        box.appendChild(act);
        box.appendChild(UI.hintBox(it.hints));
        var sol = UI.solutionBlock(it);
        box.appendChild(sol);
        act.querySelector('button').addEventListener('click', function () {
          it.parts.forEach(function (p, j) { var r = MathCheck.checkPart(fields[j].get(), p); fields[j].mark(r); });
        });
        sec.appendChild(box);
      });
      list.appendChild(sec);
    });
    document.getElementById('expand').addEventListener('click', function (e) {
      var open = e.target.textContent.indexOf('Show') === 0;
      list.querySelectorAll('details.solution').forEach(function (d) { d.open = open; });
      e.target.textContent = open ? 'Hide all solutions' : 'Show all solutions';
    });
  }
})();
