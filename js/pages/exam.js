/* Practice exam: 90 points, 3 hours, 12 multiple-choice items (36 pt) + open questions (54 pt). */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var DURATION = 3 * 60 * 60 * 1000;
  var LETTERS = 'abcdefghijklmnopqrstuvwxyz';
  var exam = null, timer = null, saveTimer = null, submitting = false, dirty = false;

  Bank.load().then(function () {
    exam = Store.active();
    if (exam && !exam.items.every(function (it) { return Bank.question(it.qid); })) { Store.clearActive(); exam = null; }
    if (exam) run(); else intro();
  }).catch(function (e) { app.innerHTML = '<div class="card empty"><p>' + UI.esc(e.message) + '</p></div>'; });

  /* ------------------------------------------------------------ intro */
  function intro() {
    var past = Store.exams();
    app.innerHTML =
      '<section class="exam-intro card">' +
      '<p class="eyebrow">Practice exam</p><h1>Calculus and Probability</h1>' +
      '<div class="exam-intro__facts"><div><strong>3:00:00</strong><span>time</span></div><div><strong>90</strong><span>points</span></div><div><strong>36</strong><span>points multiple choice</span></div><div><strong>3–6</strong><span>points per open question</span></div></div>' +
      '<h2>Read these instructions carefully</h2><ul class="rules">' +
      '<li>Question 1 consists of 12 multiple-choice items worth 3 points each. Select the best fitting answer.</li>' +
      '<li>The remaining 54 points are open questions worth 3 to 6 points. Questions with several answer boxes give partial credit per box.</li>' +
      '<li>Give exact answers where possible: fractions, roots, <code>e</code>, <code>ln</code>, <code>pi</code> — not rounded decimals (probabilities may be given to 3 decimals).</li>' +
      '<li>Your answers are saved as you type. You can close the tab and resume; the clock keeps running.</li>' +
      '<li>When the timer reaches 0:00:00 the exam is submitted automatically.</li>' +
      '<li>Your grade is computed as on the real exam: (points + 10) / 10, where the 10 points are the free “name and student number” points.</li></ul>' +
      '<p class="muted small">Questions are drawn from all ' + Bank.topics().length + ' topics, weighted like the real exam (Foundations ≈20, Derivatives ≈35, Integrals ≈22, Probability ≈13 points). Questions you have not solved yet in practice are preferred.</p>' +
      '<div class="actions"><button class="btn btn--primary btn--lg" id="start">Start exam — the clock starts now</button>' +
      '<a class="btn btn--ghost" href="reference.html" target="_blank" rel="noopener">Open reference page in a new tab</a></div>' +
      (past.length ? '<p class="small muted">You have completed ' + past.length + ' practice exam' + (past.length > 1 ? 's' : '') + '. <a href="history.html">See your progress</a>.</p>' : '') +
      '</section>';
    document.getElementById('start').addEventListener('click', start);
  }

  function start() {
    var seed = (Date.now() ^ Math.floor(Math.random() * 1e9)) >>> 0;
    var items = Bank.buildExam(seed);
    var now = Date.now();
    exam = { id: 'exam-' + now.toString(36), seed: seed, startedAt: now, endsAt: now + DURATION, items: items, answers: {}, flags: {} };
    Store.setActive(exam);
    run();
    window.scrollTo(0, 0);
  }

  /* ------------------------------------------------------------ running exam */
  function run() {
    document.body.classList.add('in-exam');
    var mcq = exam.items.filter(function (it) { return it.mode === 'mcq'; });
    var open = exam.items.filter(function (it) { return it.mode === 'open'; });

    app.innerHTML =
      '<div class="exam-bar" id="exam-bar"><div class="wrap exam-bar__inner">' +
      '<div class="timer" id="timer" role="timer" aria-live="off"><span class="timer__label">Time left</span><span class="timer__value" id="timer-value">3:00:00</span></div>' +
      '<div class="exam-bar__progress"><span id="answered-count"></span>' + '<div id="answered-bar"></div></div>' +
      '<div class="exam-bar__actions"><button class="btn btn--ghost btn--sm" id="abandon">Abandon</button><button class="btn btn--primary" id="submit">Submit exam</button></div>' +
      '</div></div>' +
      '<div class="exam-layout"><aside class="exam-nav card" aria-label="Question overview"><h3>Overview</h3><div id="exam-nav"></div></aside>' +
      '<div class="exam-paper" id="paper"></div></div>';

    var paper = document.getElementById('paper');

    // Question 1: multiple choice
    var q1 = UI.h('section', { class: 'exam-q card', id: 'q1' });
    q1.innerHTML = '<header class="exam-q__head"><h2>1. Select the best fitting answer</h2><span class="pts">' + (mcq.length * 3) + ' pt</span></header>';
    mcq.forEach(function (it, k) {
      var q = Bank.question(it.qid);
      var sub = UI.h('div', { class: 'mcq', id: 'q1' + LETTERS[k] });
      var opts = it.order.map(function (oi, j) {
        var txt = q.mcq.native ? UI.rich(q.mcq.options[oi]) : UI.tex(q.mcq.options[oi]);
        var checked = String(exam.answers[itemIndex(it)]) === String(j) ? ' checked' : '';
        return '<label class="choice"><input type="radio" name="m' + k + '" value="' + j + '"' + checked + '><span class="choice__letter">' + String.fromCharCode(65 + j) + '</span><span class="choice__text">' + txt + '</span></label>';
      }).join('');
      sub.innerHTML = '<div class="mcq__head"><span class="mcq__letter">(' + LETTERS[k] + ')</span><div class="prompt">' + UI.rich(q.prompt) + '</div>' + flagBtn(it) + '</div><div class="choices">' + opts + '</div>';
      UI.math(sub);
      sub.querySelectorAll('input').forEach(function (inp) {
        inp.addEventListener('change', function () { exam.answers[itemIndex(it)] = inp.value; changed(); });
      });
      q1.appendChild(sub);
    });
    paper.appendChild(q1);

    // Open questions
    open.forEach(function (it, k) {
      var q = Bank.question(it.qid);
      var no = k + 2;
      var sec = UI.h('section', { class: 'exam-q card', id: 'q' + no });
      sec.innerHTML = '<header class="exam-q__head"><h2>' + no + '.</h2><span class="pts">' + it.points + ' pt</span>' + flagBtn(it) + '</header><div class="prompt">' + UI.rich(q.prompt) + '</div>';
      UI.math(sec.querySelector('.prompt'));
      var saved = exam.answers[itemIndex(it)] || [];
      var fs = q.parts.map(function (p, j) {
        var f = UI.answerField(p, j, saved[j] || '', function () {
          exam.answers[itemIndex(it)] = fs.map(function (x) { return x.get(); });
          changed();
        });
        sec.appendChild(f.el);
        return f;
      });
      paper.appendChild(sec);
    });

    paper.appendChild(UI.h('div', { class: 'exam-end card' }, '<p>End of the exam. Check your answers, then submit.</p><button class="btn btn--primary" id="submit2">Submit exam</button>'));

    paper.addEventListener('click', function (e) {
      var b = e.target.closest('.flag');
      if (!b) return;
      var i = b.getAttribute('data-i');
      exam.flags[i] = !exam.flags[i];
      b.setAttribute('aria-pressed', String(!!exam.flags[i]));
      changed();
    });
    document.getElementById('submit').addEventListener('click', askSubmit);
    document.getElementById('submit2').addEventListener('click', askSubmit);
    document.getElementById('abandon').addEventListener('click', function () {
      UI.confirm('Abandon this exam?', 'Your answers will be discarded and nothing is saved to your history.', 'Abandon exam', true).then(function (ok) {
        if (!ok) return;
        Store.clearActive(); clearInterval(timer); document.body.classList.remove('in-exam'); exam = null; intro();
      });
    });
    drawNav();
    tick();
    timer = setInterval(tick, 1000);
    window.addEventListener('beforeunload', function () { if (exam && dirty && !submitting) Store.setActive(exam); });
  }

  function itemIndex(it) { return exam.items.indexOf(it); }

  function flagBtn(it) {
    var i = itemIndex(it);
    return '<button type="button" class="flag" data-i="' + i + '" aria-pressed="' + (!!exam.flags[i]) + '" title="Flag to come back later">⚑<span class="sr">Flag</span></button>';
  }

  function isAnswered(it) {
    var a = exam.answers[itemIndex(it)];
    if (it.mode === 'mcq') return a != null && a !== '';
    return Array.isArray(a) && a.some(function (v) { return String(v).trim() !== ''; });
  }

  function changed() {
    dirty = true;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { Store.setActive(exam); dirty = false; }, 300);
    drawNav();
  }

  function drawNav() {
    var mcq = exam.items.filter(function (it) { return it.mode === 'mcq'; });
    var open = exam.items.filter(function (it) { return it.mode === 'open'; });
    var cell = function (it, label, target) {
      var i = itemIndex(it);
      return '<a href="#' + target + '" class="navcell' + (isAnswered(it) ? ' is-done' : '') + (exam.flags[i] ? ' is-flag' : '') + '">' + label + '</a>';
    };
    var html = '<div class="navgroup"><span>Question 1 · multiple choice</span><div class="navcells">' +
      mcq.map(function (it, k) { return cell(it, LETTERS[k], 'q1' + LETTERS[k]); }).join('') + '</div></div>' +
      '<div class="navgroup"><span>Open questions</span><div class="navcells">' +
      open.map(function (it, k) { return cell(it, String(k + 2), 'q' + (k + 2)); }).join('') + '</div></div>' +
      '<div class="legend small"><span><i class="dot dot--ok"></i>answered</span><span><i class="dot dot--flag"></i>flagged</span></div>';
    document.getElementById('exam-nav').innerHTML = html;
    var n = exam.items.filter(isAnswered).length;
    document.getElementById('answered-count').textContent = n + ' of ' + exam.items.length + ' answered';
    document.getElementById('answered-bar').innerHTML = UI.bar(n / exam.items.length, { size: 'sm', label: 'Answered' });
  }

  function tick() {
    var left = Math.max(0, Math.round((exam.endsAt - Date.now()) / 1000));
    var el = document.getElementById('timer-value');
    if (!el) return;
    el.textContent = UI.fmtDur(left);
    var t = document.getElementById('timer');
    t.classList.toggle('timer--warn', left <= 15 * 60 && left > 5 * 60);
    t.classList.toggle('timer--danger', left <= 5 * 60);
    if (left === 15 * 60 || left === 5 * 60) UI.toast((left / 60) + ' minutes left');
    if (left <= 0) submit(true);
  }

  function askSubmit() {
    var unanswered = exam.items.filter(function (it) { return !isAnswered(it); }).length;
    var flagged = Object.keys(exam.flags).filter(function (k) { return exam.flags[k]; }).length;
    var msg = 'Time left: ' + UI.fmtDur((exam.endsAt - Date.now()) / 1000) + '.';
    if (unanswered) msg += ' <strong>' + unanswered + ' question' + (unanswered > 1 ? 's are' : ' is') + ' unanswered.</strong>';
    if (flagged) msg += ' ' + flagged + ' flagged.';
    UI.confirm('Submit your exam?', msg + ' You cannot change your answers afterwards.', 'Submit and grade').then(function (ok) { if (ok) submit(false); });
  }

  /* ------------------------------------------------------------ grading */
  function submit(auto) {
    if (submitting) return;
    submitting = true;
    clearInterval(timer);
    var now = Date.now();
    var items = exam.items.map(function (it, i) {
      var q = Bank.question(it.qid);
      var g = Bank.gradeItem(it, exam.answers[i]);
      return { qid: it.qid, topic: q.topic, area: Bank.topic(q.topic).area, mode: it.mode, points: it.points, order: it.order,
        answer: exam.answers[i] == null ? null : exam.answers[i], earned: g.earned, parts: g.parts, answered: g.answered };
    });
    var score = items.reduce(function (s, it) { return s + it.earned; }, 0);
    var rec = { id: exam.id, seed: exam.seed, startedAt: exam.startedAt, submittedAt: now,
      duration: Math.min(DURATION, now - exam.startedAt) / 1000, auto: !!auto, items: items,
      score: score, max: 90, grade: Bank.grade(score) };
    Store.saveExam(rec);
    // feed results into topic progress (answered questions only)
    items.forEach(function (it) {
      if (it.answered) Store.record(it.qid, it.earned === it.points, 'exam', it.answer);
    });
    Store.clearActive();
    location.href = 'results.html?id=' + encodeURIComponent(rec.id) + (auto ? '&auto=1' : '');
  }
})();
