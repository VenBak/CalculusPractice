/* Random practice exam: 90 points, 3 hours, 12 multiple-choice items (36 pt) + open questions (54 pt). */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var DURATION = 3 * 60 * 60 * 1000;
  var LETTERS = 'abcdefghijklmnopqrstuvwxyz';

  Bank.load().then(function () {
    var a = Store.active();
    if (a && a.kind === 'past') { otherActive(a); return; }
    if (a && !a.items.every(function (it) { return Bank.resolve(it.ref || it.qid); })) { Store.clearActive(); a = null; }
    if (a) run(upgrade(a)); else intro();
  }).catch(function (e) { app.innerHTML = '<div class="card empty"><p>' + UI.esc(e.message) + '</p></div>'; });

  /* exams started with the previous version of the site */
  function upgrade(a) {
    a.kind = 'random';
    a.title = a.title || 'Practice exam';
    a.items.forEach(function (it) { it.ref = it.ref || it.qid; });
    return a;
  }

  function otherActive(a) {
    app.innerHTML = '<section class="card empty"><h1>A past exam is in progress</h1><p>You are in the middle of <strong>' + UI.esc(a.title) + '</strong>. Finish or abandon it before starting a practice exam.</p>' +
      '<div class="actions actions--center"><a class="btn btn--primary" href="past-exam.html?id=' + encodeURIComponent(a.pastId) + '">Go to that exam</a></div></section>';
  }

  function intro() {
    var past = Store.exams().filter(function (e) { return (e.kind || 'random') === 'random'; });
    app.innerHTML =
      '<section class="exam-intro card">' +
      '<p class="eyebrow">Practice exam · randomly generated</p><h1>Calculus and Probability</h1>' +
      '<div class="exam-intro__facts"><div><strong>3:00:00</strong><span>time</span></div><div><strong>90</strong><span>points</span></div><div><strong>36</strong><span>points multiple choice</span></div><div><strong>3–6</strong><span>points per open question</span></div></div>' +
      '<h2>Read these instructions carefully</h2><ul class="rules">' +
      '<li>Question 1 consists of 12 multiple-choice items worth 3 points each. Select the best fitting answer.</li>' +
      '<li>The remaining 54 points are open questions worth 3 to 6 points. Questions with several answer boxes give partial credit per box.</li>' +
      '<li>Give exact answers where possible: fractions, roots, <code>e</code>, <code>ln</code>, <code>pi</code> — not rounded decimals (probabilities may be given to 3 decimals).</li>' +
      '<li>Your answers are saved as you type. You can close the tab and resume; the exam clock keeps running.</li>' +
      '<li>The time you spend on each question is logged. Flag a question to pause its clock until you unflag it.</li>' +
      '<li>Hints are available behind the lightbulb; their use is shown in your results.</li>' +
      '<li>When the timer reaches 0:00:00 the exam is submitted automatically. Your grade is (points + 10) / 10, as on the real exam.</li></ul>' +
      '<p class="muted small">Questions are drawn from all ' + Bank.topics().length + ' topics, weighted like the real exam (Foundations ≈20, Derivatives ≈35, Integrals ≈22, Probability ≈13 points). Questions you have not solved yet in practice are preferred. Want the real thing? Try a <a href="past-exams.html">past exam</a>.</p>' +
      '<div class="actions"><button class="btn btn--primary btn--lg" id="start">Start exam — the clock starts now</button>' +
      '<a class="btn btn--ghost" href="reference.html" target="_blank" rel="noopener">Open reference page in a new tab</a></div>' +
      (past.length ? '<p class="small muted">You have completed ' + past.length + ' practice exam' + (past.length > 1 ? 's' : '') + '. <a href="history.html">See your progress</a>.</p>' : '') +
      '</section>';
    document.getElementById('start').addEventListener('click', start);
  }

  function start() {
    var seed = (Date.now() ^ Math.floor(Math.random() * 1e9)) >>> 0;
    var now = Date.now();
    var state = { id: 'exam-' + now.toString(36), kind: 'random', title: 'Practice exam', seed: seed, minutes: 180,
      startedAt: now, endsAt: now + DURATION, items: Bank.buildExam(seed), answers: {}, flags: {}, times: {}, hints: {} };
    Store.setActive(state);
    run(state);
    window.scrollTo(0, 0);
  }

  function run(state) {
    var mcq = [], open = [];
    state.items.forEach(function (it, i) { (it.mode === 'mcq' ? mcq : open).push(i); });
    var groups = [{ no: '1', title: 'Select the best fitting answer', points: mcq.length * 3, items: mcq, navTitle: 'Question 1 · multiple choice',
      labels: mcq.map(function (_, k) { return '(' + LETTERS[k] + ')'; }), short: mcq.map(function (_, k) { return LETTERS[k]; }) }];
    open.forEach(function (i, k) {
      groups.push({ no: String(k + 2), title: '', points: state.items[i].points, items: [i], labels: [''], short: [String(k + 2)], navTitle: k === 0 ? 'Open questions' : '' });
    });
    ExamRunner.mount({ app: app, state: state, paper: { groups: groups }, onAbandon: intro });
  }
})();
