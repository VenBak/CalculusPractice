/* Home: overview of all topics with progress, plus the practice-exam call to action. */
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

  var html = '';
  html += '<section class="hero">' +
    '<div class="hero__text"><p class="eyebrow">IBC017 · Calculus and Probability</p>' +
    '<h1>Practise one topic at a time, then sit a full exam.</h1>' +
    '<p class="lede">' + total + ' questions across ' + topics.length + ' topics, each with an exact answer checker and a worked solution. ' +
    'Practice exams follow the real format: 90 points in 3 hours, with 36 points of multiple choice.</p>' +
    '<div class="hero__actions">' +
    (active ? '<a class="btn btn--primary" href="exam.html">Resume exam in progress</a>' : '<a class="btn btn--primary" href="exam.html">Start a practice exam</a>') +
    '<a class="btn btn--ghost" href="reference.html">Reference page</a></div></div>' +
    '<div class="hero__stats card">' +
    '<div class="stat"><span class="stat__num">' + correct + '<small>/' + total + '</small></span><span class="stat__label">questions solved</span></div>' +
    UI.bar(correct / total, { wrong: wrong / total, size: 'lg', label: 'Overall progress' }) +
    '<div class="legend"><span><i class="dot dot--ok"></i>correct</span><span><i class="dot dot--bad"></i>wrong on last attempt</span><span><i class="dot"></i>not tried</span></div>' +
    (last ? '<a class="last-exam" href="results.html?id=' + encodeURIComponent(last.id) + '"><span>Last exam</span><strong>' + UI.num(last.score) + ' / 90</strong><span class="grade ' + (last.grade >= 5.5 ? 'grade--pass' : 'grade--fail') + '">grade ' + last.grade.toFixed(1) + '</span></a>'
      : '<p class="muted small">No practice exams yet — your scores will appear here.</p>') +
    '</div></section>';

  areas.forEach(function (a) {
    var ts = topics.filter(function (t) { return t.area === a.id; });
    var ac = 0, at = 0;
    ts.forEach(function (t) { ac += stats[t.id].correct; at += stats[t.id].total; });
    html += '<section class="area"><div class="area__head"><h2>' + UI.esc(a.name) + '</h2>' +
      '<span class="area__meta">' + a.lecture + ' · ≈' + a.weight + ' of 90 exam points · ' + ac + '/' + at + ' solved</span></div><div class="topic-grid">';
    ts.forEach(function (t) {
      var s = stats[t.id];
      var done = s.correct === s.total;
      html += '<a class="topic card' + (done ? ' topic--done' : '') + '" href="practice.html?topic=' + t.id + '">' +
        '<div class="topic__top"><h3>' + UI.esc(t.name) + '</h3>' + (done ? '<span class="tag tag--ok">complete</span>' : '') + '</div>' +
        '<p class="topic__desc">' + UI.esc(t.description) + '</p>' +
        UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, label: t.name + ' progress' }) +
        '<div class="topic__counts"><span>' + s.correct + '/' + s.total + ' correct</span>' + (s.wrong ? '<span class="bad">' + s.wrong + ' to retry</span>' : '') + '</div></a>';
    });
    html += '</div></section>';
  });

  app.innerHTML = html;
})();
