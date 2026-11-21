/* Results of one exam (practice or past): score, grade, breakdown by area/topic, time per question, solutions. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var exams = Store.exams();
  var id = UI.param('id');
  var rec = id ? Store.exam(id) : exams[exams.length - 1];
  if (!rec) {
    app.innerHTML = '<div class="card empty"><h1>No results yet</h1><p>Finish a <a href="exam.html">practice exam</a> or a <a href="past-exams.html">past exam</a> to see your results here.</p></div>';
    return;
  }
  var kind = rec.kind || 'random';
  rec.items.forEach(function (it) { it.ref = it.ref || it.qid; });
  var topicIds = rec.items.filter(function (it) { return it.ref.indexOf('past:') !== 0; }).map(function (it) { return it.topic; })
    .filter(function (t, i, a) { return a.indexOf(t) === i; });

  Promise.all([Bank.load(topicIds), kind === 'past' ? Bank.loadPast([rec.pastId]) : null]).then(render)
    .catch(function (e) { app.innerHTML = '<div class="card empty"><p>' + UI.esc(e.message) + '</p></div>'; });

  function render() {
    var same = exams.filter(function (e) { return (e.kind || 'random') === kind && (kind !== 'past' || e.pastId === rec.pastId); });
    var idx = same.map(function (e) { return e.id; }).indexOf(rec.id);
    var prevRec = idx > 0 ? same[idx - 1] : null;
    var pass = rec.grade >= 5.5;
    var sum = function (l, k) { return l.reduce(function (s, it) { return s + (it[k] || 0); }, 0); };
    var mcq = rec.items.filter(function (it) { return it.mode === 'mcq'; });
    var open = rec.items.filter(function (it) { return it.mode !== 'mcq'; });
    var title = rec.title || 'Practice exam';
    var timeTotal = sum(rec.items, 'time'), hintsTotal = sum(rec.items, 'hints');

    var html = '<nav class="crumbs"><a href="history.html">Progress</a><span>/</span><span aria-current="page">' + UI.esc(title) + ' · ' + UI.fmtDate(rec.submittedAt) + '</span></nav>';
    if (UI.param('auto')) html += '<div class="verdict verdict--bad">Time was up — the exam was submitted automatically.</div>';
    html += '<section class="result-hero card">' +
      '<div class="result-score"><span class="result-score__label">' + UI.esc(title) + '</span><span class="result-score__num">' + UI.num(rec.score) + '</span><span class="result-score__max">/ 90 points</span></div>' +
      '<div class="result-grade ' + (pass ? 'grade--pass' : 'grade--fail') + '"><span>Grade</span><strong>' + rec.grade.toFixed(1) + '</strong><em>' + (pass ? 'pass' : 'below 5.5') + '</em></div>' +
      '<dl class="result-facts">' +
      (mcq.length ? '<div><dt>Multiple choice</dt><dd>' + UI.num(sum(mcq, 'earned')) + ' / ' + sum(mcq, 'points') + '</dd></div><div><dt>Open questions</dt><dd>' + UI.num(sum(open, 'earned')) + ' / ' + sum(open, 'points') + '</dd></div>' : '') +
      '<div><dt>Time used</dt><dd>' + UI.fmtDur(rec.duration) + (rec.minutes ? ' <span class="muted small">of ' + rec.minutes + ' min</span>' : '') + '</dd></div>' +
      '<div><dt>Hints used</dt><dd>' + hintsTotal + '</dd></div>' +
      (prevRec ? '<div><dt>vs. previous attempt</dt><dd class="' + (rec.score >= prevRec.score ? 'good' : 'bad') + '">' + (rec.score >= prevRec.score ? '+' : '') + UI.num(rec.score - prevRec.score) + ' pt</dd></div>' : '') +
      '</dl>' +
      '<div class="result-hero__actions">' + (kind === 'past' ? '<a class="btn btn--primary" href="past-exam.html?id=' + encodeURIComponent(rec.pastId) + '">Retake this exam</a><a class="btn btn--ghost" href="past-exams.html">Other past exams</a>'
        : '<a class="btn btn--primary" href="exam.html">New practice exam</a>') + '<a class="btn btn--ghost" href="history.html">All results</a></div></section>';

    // breakdown by area and topic
    var byArea = {}, byTopic = {};
    rec.items.forEach(function (it) {
      (byArea[it.area] = byArea[it.area] || { e: 0, p: 0 });
      byArea[it.area].e += it.earned; byArea[it.area].p += it.points;
      (byTopic[it.topic] = byTopic[it.topic] || { e: 0, p: 0, n: 0, wrong: 0, time: 0 });
      var t = byTopic[it.topic];
      t.e += it.earned; t.p += it.points; t.n++; t.time += it.time || 0;
      if (it.earned < it.points) t.wrong++;
    });
    html += '<section class="breakdown"><div class="card"><h2>By area</h2><div class="area-bars">' +
      Bank.areas().map(function (a) {
        var s = byArea[a.id];
        if (!s || !s.p) return '';
        return '<div class="area-bar"><div class="area-bar__label"><span>' + UI.esc(a.name) + '</span><span>' + UI.num(s.e) + ' / ' + UI.num(s.p) + '</span></div>' + UI.bar(s.e / s.p, { label: a.name }) + '</div>';
      }).join('') + '</div></div>';

    var trows = Object.keys(byTopic).map(function (t) { return { t: t, s: byTopic[t] }; })
      .sort(function (a, b) { return a.s.e / a.s.p - b.s.e / b.s.p; });
    html += '<div class="card"><h2>By topic <span class="muted small">— weakest first</span></h2><div class="table-wrap"><table class="table"><thead><tr><th>Topic</th><th class="num">Points</th><th class="num">Missed</th><th class="num">Time</th><th></th></tr></thead><tbody>' +
      trows.map(function (r) {
        var t = Bank.topic(r.t);
        var full = r.s.e >= r.s.p;
        return '<tr><td>' + UI.esc(t.name) + '</td><td class="num">' + UI.num(r.s.e) + '/' + UI.num(r.s.p) + '</td><td class="num">' + (full ? '<span class="good">—</span>' : '<span class="bad">' + r.s.wrong + '</span>') + '</td>' +
          '<td class="num">' + UI.fmtShort(r.s.time) + '</td><td class="num">' + (full ? '' : '<a href="practice.html?topic=' + t.id + '">Practise →</a>') + '</td></tr>';
      }).join('') + '</tbody></table></div></div></section>';

    html += '<section class="review"><div class="review__head"><h2>Question review</h2><div class="seg" role="tablist"><button data-f="missed" aria-selected="true">Missed only</button><button data-f="all" aria-selected="false">All questions</button></div></div>' +
      '<p class="muted small">Total time on questions: ' + UI.fmtDur(timeTotal) + '. The clock shows the time logged per question (flagged questions were paused).</p><div id="review-list"></div></section>';
    app.innerHTML = html;

    var list = document.getElementById('review-list');
    rec.items.forEach(function (it, i) {
      var q = Bank.resolve(it.ref);
      if (!q) return;
      var t = Bank.topic(it.topic);
      var label = it.label || (it.mode === 'mcq' ? '1' + 'abcdefghijkl'[mcq.indexOf(it)] : String(open.indexOf(it) + 2));
      var full = it.earned >= it.points;
      var card = UI.h('article', { class: 'rq card' + (full ? ' rq--ok' : it.earned > 0 ? ' rq--part' : ' rq--bad'), 'data-ok': full ? '1' : '0' });
      var head = '<header class="rq__head"><span class="rq__no">' + UI.esc(label) + '</span><span class="rq__topic">' + UI.esc(t ? t.name : '') + '</span>' +
        '<span class="qtime" title="Time spent">' + UI.ICON.clock + '<span>' + UI.fmtShort(it.time || 0) + '</span></span>' +
        (it.hints ? '<span class="tag tag--hint" title="Hints used">' + UI.ICON.bulb + it.hints + '</span>' : '') +
        '<span class="rq__pts ' + (full ? 'good' : it.earned > 0 ? 'warn' : 'bad') + '">' + UI.num(it.earned) + ' / ' + UI.num(it.points) + ' pt</span></header>';
      var body = '';
      if (q.group && !q.single && q.group.intro) {
        var intro = q.group.intro;
        body += intro.length < 140 && intro.indexOf('[[img:') < 0 ? '<div class="prompt rq__intro">' + UI.rich(intro) + '</div>'
          : '<details class="stem"><summary>Question ' + UI.esc(q.group.no) + ' — shared text</summary><div class="prompt">' + UI.rich(intro) + '</div></details>';
      }
      body += '<div class="prompt">' + UI.rich(q.prompt) + '</div>';
      if (it.mode === 'mcq') {
        var pick = it.answer == null || it.answer === '' ? null : Number(it.answer);
        body += '<div class="choices choices--review">' + it.order.map(function (oi, j) {
          var txt = q.mcq.native ? UI.rich(q.mcq.options[oi]) : UI.tex(q.mcq.options[oi]);
          var cls = oi === q.mcq.correct ? ' is-correct' : (pick === j ? ' is-picked-wrong' : '');
          return '<div class="choice' + cls + '"><span class="choice__letter">' + String.fromCharCode(65 + j) + '</span><span class="choice__text">' + txt + '</span>' +
            (pick === j ? '<span class="choice__you">your answer</span>' : '') + '</div>';
        }).join('') + '</div>' + (pick === null ? '<p class="bad small">Not answered.</p>' : '');
      } else {
        body += '<div class="table-wrap"><table class="table answers-table"><thead><tr><th>Part</th><th>Your answer</th><th>Correct answer</th><th></th></tr></thead><tbody>' +
          q.parts.map(function (p, j) {
            var mine = (it.answer || [])[j];
            var mineHtml;
            var empty = mine == null || (Array.isArray(mine) ? !mine.length : String(mine).trim() === '');
            if (empty) mineHtml = '<span class="muted">—</span>';
            else if (p.kind === 'choice') mineHtml = UI.rich(p.options[Number(mine)]);
            else if (p.kind === 'multi') mineHtml = (Array.isArray(mine) ? mine : String(mine).split(',')).map(function (k) { return UI.rich(p.options[Number(k)]); }).join(', ');
            else { var pv = MathCheck.preview(mine, p.kind); mineHtml = pv ? UI.tex(pv) : '<code>' + UI.esc(mine) + '</code>'; }
            return '<tr><td>' + (p.label ? UI.rich(p.label) : '—') + '</td><td>' + mineHtml + '</td><td>' + UI.answerHtml(p) + '</td><td>' + (it.parts[j] ? '<span class="tag tag--ok">✓</span>' : '<span class="tag tag--bad">✗</span>') + '</td></tr>';
          }).join('') + '</tbody></table></div>';
      }
      card.innerHTML = head + body;
      UI.math(card);
      card.appendChild(UI.solutionBlock(q));
      if (!full && it.ref.indexOf('past:') !== 0) card.appendChild(UI.h('a', { class: 'btn btn--link', href: 'practice.html?topic=' + t.id + '&q=' + Number(it.ref.slice(-3)) }, 'Retry this question in practice →'));
      if (!full && it.ref.indexOf('past:') === 0) card.appendChild(UI.h('a', { class: 'btn btn--link', href: 'practice.html?topic=' + t.id }, 'Practise “' + UI.esc(t.name) + '” →'));
      list.appendChild(card);
    });

    var applyFilter = function (f) {
      list.querySelectorAll('.rq').forEach(function (c) { c.hidden = f === 'missed' && c.getAttribute('data-ok') === '1'; });
      if (f === 'missed' && !list.querySelector('.rq:not([hidden])')) list.insertAdjacentHTML('afterbegin', '<p class="card empty-inline">Full marks — nothing missed.</p>');
    };
    app.querySelectorAll('.review .seg button').forEach(function (b) {
      b.addEventListener('click', function () {
        app.querySelectorAll('.review .seg button').forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
        var e = list.querySelector('.empty-inline'); if (e) e.remove();
        applyFilter(b.getAttribute('data-f'));
      });
    });
    applyFilter('missed');
  }
})();
