/* Home: overview of all topics with progress, plus random practice, practice exams and past exams. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var topics = Bank.topics(), areas = Bank.areas();

  var total = 0, correct = 0, wrong = 0;
  var stats = {};
  topics.forEach(function (t) {
    var s = Store.topicStats(t.id, t.count);
    stats[t.id] = s;
    total += s.total; correct += s.correct; wrong += s.wrong;
  });
  var exams = Store.exams(), last = exams[exams.length - 1], active = Store.active();
  var pastIdx = Bank.pastIndex();
  var activeHref = active ? (active.kind === 'past' ? 'past-exam.html?id=' + encodeURIComponent(active.pastId) : 'exam.html') : null;

  var html = '';
  html += '<section class="hero">' +
    '<div class="hero__text"><p class="eyebrow">IBC017 · Calculus and Probability</p>' +
    '<h1>Practise one topic at a time, then sit a full exam.</h1>' +
    '<p class="lede">' + total + ' questions across ' + topics.length + ' topics with hints, refreshers and worked solutions, plus ' + pastIdx.length + ' real past exams. ' +
    'Practice exams follow the real format: 90 points, with 36 points of multiple choice.</p>' +
    '<div class="hero__actions">' +
    (active ? '<a class="btn btn--primary" href="' + activeHref + '">Resume ' + UI.esc(active.title || 'exam') + '</a>' : '<a class="btn btn--primary" href="exam.html">Start a practice exam</a>') +
    '<a class="btn btn--ghost" href="practice.html?mode=random">' + UI.ICON.dice + ' Random problem</a>' +
    '<a class="btn btn--ghost" href="past-exams.html">Past exams</a></div></div>' +
    '<div class="hero__stats card">' +
    '<div class="stat"><span class="stat__num">' + correct + '<small>/' + total + '</small></span><span class="stat__label">questions solved</span></div>' +
    UI.bar(correct / total, { wrong: wrong / total, size: 'lg', label: 'Overall progress' }) +
    '<div class="legend"><span><i class="dot dot--ok"></i>correct</span><span><i class="dot dot--bad"></i>wrong on last attempt</span><span><i class="dot"></i>not tried</span></div>' +
    (last ? '<a class="last-exam" href="results.html?id=' + encodeURIComponent(last.id) + '"><span>Last exam</span><strong>' + UI.num(last.score) + ' / 90</strong><span class="grade ' + (last.grade >= 5.5 ? 'grade--pass' : 'grade--fail') + '">grade ' + last.grade.toFixed(1) + '</span></a>'
      : '<p class="muted small">No exams yet — your scores will appear here.</p>') +
    '</div></section>';

  html += '<section class="quick">' +
    '<a class="quick__item card" href="practice.html?mode=random">' + UI.ICON.dice + '<span><strong>Random problem</strong><small>a surprise question from any topic</small></span></a>' +
    '<a class="quick__item card" href="past-exams.html">' + UI.ICON.clock + '<span><strong>Past exams</strong><small>' + pastIdx.length + ' real exams' + (pastIdx.length ? ', ' + pastIdx[0].year + ' to ' + pastIdx[pastIdx.length - 1].year : '') + '</small></span></a>' +
    '<a class="quick__item card" href="guide.html">' + UI.ICON.book + '<span><strong>Refreshers</strong><small>theory + worked example per topic</small></span></a>' +
    '</section>';

  areas.forEach(function (a) {
    var ts = topics.filter(function (t) { return t.area === a.id; });
    var ac = 0, at = 0;
    ts.forEach(function (t) { ac += stats[t.id].correct; at += stats[t.id].total; });
    html += '<section class="area"><div class="area__head"><h2>' + UI.esc(a.name) + '</h2>' +
      '<span class="area__meta">' + a.lecture + ' · ≈' + a.weight + ' of 90 exam points · ' + ac + '/' + at + ' solved</span></div><div class="topic-grid">';
    ts.forEach(function (t) {
      var s = stats[t.id];
      var done = s.correct === s.total;
      html += '<div class="topic card' + (done ? ' topic--done' : '') + '">' +
        '<a class="topic__main" href="practice.html?topic=' + t.id + '">' +
        '<div class="topic__top"><h3>' + UI.esc(t.name) + '</h3>' + (done ? '<span class="tag tag--ok">complete</span>' : '') + '</div>' +
        '<p class="topic__desc">' + UI.esc(t.description) + '</p>' +
        UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, label: t.name + ' progress' }) +
        '<div class="topic__counts"><span>' + s.correct + '/' + s.total + ' correct</span>' + (s.wrong ? '<span class="bad">' + s.wrong + ' to retry</span>' : '') + '</div></a>' +
        '<a class="topic__guide" href="guide.html?topic=' + t.id + '">' + UI.ICON.book + 'Refresher</a></div>';
    });
    html += '</div></section>';
  });

  app.innerHTML = html;
})();
