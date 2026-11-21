/* Past exams: the real exams of earlier years, grouped by academic year. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var idx = Bank.pastIndex();
  var exams = Store.exams();
  var active = Store.active();

  var byYear = {};
  idx.forEach(function (e) { (byYear[e.year] = byYear[e.year] || []).push(e); });
  var years = Object.keys(byYear).sort().reverse();

  var html = '<div class="page-head"><p class="eyebrow">Real exams</p><h1>Past exams</h1>' +
    '<p class="lede">Every question exactly as it appeared on the paper, with the official answers. Sit one under exam conditions with its original time limit, or browse the questions with hints and worked solutions.</p></div>';
  if (active && active.kind === 'past') {
    html += '<div class="verdict verdict--info">You have an exam in progress: <strong>' + UI.esc(active.title) + '</strong>. <a href="past-exam.html?id=' + encodeURIComponent(active.pastId) + '">Continue it →</a></div>';
  }
  years.forEach(function (y) {
    html += '<section class="area"><div class="area__head"><h2>' + UI.esc(y) + '</h2><span class="area__meta">academic year · ' + byYear[y].length + ' exam' + (byYear[y].length > 1 ? 's' : '') + '</span></div><div class="past-grid">';
    byYear[y].sort(function (a, b) { return a.sitting - b.sitting; }).forEach(function (e) {
      var mine = exams.filter(function (r) { return r.kind === 'past' && r.pastId === e.id; });
      var best = mine.reduce(function (m, r) { return Math.max(m, r.score); }, -1);
      var last = mine[mine.length - 1];
      html += '<article class="past card">' +
        '<div class="past__top"><span class="tag ' + (e.kind === 'Resit' ? 'tag--resit' : 'tag--exam') + '">' + (e.sitting === 1 ? '1st sitting · ' : '2nd sitting · ') + UI.esc(e.kind) + '</span>' +
        (best >= 0 ? '<span class="grade ' + (Bank.grade(best) >= 5.5 ? 'grade--pass' : 'grade--fail') + '">best ' + UI.num(best) + '/90</span>' : '') + '</div>' +
        '<h3>' + UI.esc(e.date) + '</h3>' +
        '<p class="past__meta">' + e.minutes + ' minutes · ' + e.questions + ' questions · ' + e.items + ' answer items · 90 points</p>' +
        (e.note ? '<p class="past__note small">' + UI.esc(e.note) + '</p>' : '') +
        (mine.length ? '<p class="small muted">Taken ' + mine.length + '× · last: <a href="results.html?id=' + encodeURIComponent(last.id) + '">' + UI.num(last.score) + '/90 (grade ' + last.grade.toFixed(1) + ')</a></p>' : '<p class="small muted">Not taken yet.</p>') +
        '<div class="past__actions"><a class="btn btn--primary btn--sm" href="past-exam.html?id=' + encodeURIComponent(e.id) + '">Sit this exam</a>' +
        '<a class="btn btn--ghost btn--sm" href="past-exam.html?id=' + encodeURIComponent(e.id) + '&amp;mode=browse">Browse questions</a></div>' +
        '</article>';
    });
    html += '</div></section>';
  });
  app.innerHTML = html;
})();
