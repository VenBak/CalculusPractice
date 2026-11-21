/* Progress: exam history (practice + past exams) with score chart, weak topics, time per topic and practice coverage. */
(function () {
  'use strict';
  var app = document.getElementById('app');

  function render() {
    var exams = Store.exams();
    var topics = Bank.topics();
    var html = '<div class="page-head"><h1>Progress</h1><p class="muted">Every exam you submit is stored here, together with your topic practice. <a href="data.html">Back up or transfer your data →</a></p></div>';

    if (exams.length) {
      var best = exams.reduce(function (m, e) { return Math.max(m, e.score); }, 0);
      var last3 = exams.slice(-3), avg3 = last3.reduce(function (s, e) { return s + e.score; }, 0) / last3.length;
      var last = exams[exams.length - 1];
      var nPast = exams.filter(function (e) { return e.kind === 'past'; }).length;
      html += '<section class="tiles">' +
        tile(exams.length, 'exams taken' + (nPast ? ' (' + nPast + ' past)' : '')) + tile(UI.num(best) + '<small>/90</small>', 'best score') +
        tile(UI.num(avg3) + '<small>/90</small>', 'average of last ' + last3.length) +
        tile('<span class="' + (last.grade >= 5.5 ? 'good' : 'bad') + '">' + last.grade.toFixed(1) + '</span>', 'latest grade') + '</section>';
      html += '<section class="card"><h2>Exam scores over time</h2><div class="chart" id="chart"></div></section>';
      html += '<section class="card"><h2>All exams</h2><div class="table-wrap"><table class="table"><thead><tr><th>Date</th><th>Paper</th><th class="num">Score</th><th class="num">Grade</th><th class="num">Time</th><th class="num">Hints</th><th></th></tr></thead><tbody>' +
        exams.slice().reverse().map(function (e) {
          var hintsUsed = e.items.reduce(function (a, i) { return a + (i.hints || 0); }, 0);
          return '<tr><td><a href="results.html?id=' + encodeURIComponent(e.id) + '">' + UI.fmtDate(e.submittedAt) + '</a>' + (e.auto ? ' <span class="tag">timed out</span>' : '') + '</td>' +
            '<td>' + (e.kind === 'past' ? '<span class="tag tag--exam">past</span> ' : '') + UI.esc(e.title || 'Practice exam') + '</td>' +
            '<td class="num"><strong>' + UI.num(e.score) + '</strong></td><td class="num ' + (e.grade >= 5.5 ? 'good' : 'bad') + '">' + e.grade.toFixed(1) + '</td>' +
            '<td class="num">' + UI.fmtDur(e.duration) + '</td><td class="num">' + hintsUsed + '</td>' +
            '<td class="num"><button class="btn btn--link btn--sm" data-del="' + UI.esc(e.id) + '">Delete</button></td></tr>';
        }).join('') + '</tbody></table></div></section>';

      var area = {}, top = {};
      exams.forEach(function (e) {
        e.items.forEach(function (it) {
          (area[it.area] = area[it.area] || { e: 0, p: 0 }); area[it.area].e += it.earned; area[it.area].p += it.points;
          (top[it.topic] = top[it.topic] || { e: 0, p: 0, n: 0 }); top[it.topic].e += it.earned; top[it.topic].p += it.points; top[it.topic].n++;
        });
      });
      var weak = Object.keys(top).map(function (t) { return { t: t, r: top[t].e / top[t].p, s: top[t] }; })
        .sort(function (a, b) { return a.r - b.r; }).slice(0, 6);
      html += '<section class="two-col"><div class="card"><h2>Exam points by area</h2><div class="area-bars">' +
        Bank.areas().map(function (a) {
          var s = area[a.id]; if (!s) return '';
          return '<div class="area-bar"><div class="area-bar__label"><span>' + UI.esc(a.name) + '</span><span>' + Math.round(100 * s.e / s.p) + '%</span></div>' + UI.bar(s.e / s.p, { label: a.name }) + '</div>';
        }).join('') + '</div></div>' +
        '<div class="card"><h2>Weakest topics in exams</h2><ol class="weak">' +
        weak.map(function (w) {
          var t = Bank.topic(w.t);
          return '<li><a href="practice.html?topic=' + t.id + '">' + UI.esc(t.name) + '</a><span>' + Math.round(100 * w.r) + '% of ' + UI.num(w.s.p) + ' pt</span></li>';
        }).join('') + '</ol></div></section>';
    } else {
      html += '<section class="card empty"><h2>No exams yet</h2><p>Sit a <a href="exam.html">practice exam</a> or a <a href="past-exams.html">past exam</a>: your score, grade and the topics you missed will be logged here.</p></section>';
    }

    html += '<section class="card"><h2>Topic practice</h2><div class="table-wrap"><table class="table"><thead><tr><th>Topic</th><th>Progress</th><th class="num">Correct</th><th class="num">Wrong</th><th class="num">Not tried</th><th class="num" title="Average time per answered attempt">Avg time</th><th class="num">Total time</th></tr></thead><tbody>' +
      topics.map(function (t) {
        var s = Store.topicStats(t.id, t.count);
        return '<tr><td><a href="practice.html?topic=' + t.id + '">' + UI.esc(t.name) + '</a></td><td class="cell-bar">' + UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, size: 'sm', label: t.name }) + '</td>' +
          '<td class="num">' + s.correct + '</td><td class="num' + (s.wrong ? ' bad' : '') + '">' + s.wrong + '</td><td class="num">' + (s.total - s.attempted) + '</td>' +
          '<td class="num">' + (s.timed ? UI.fmtShort(s.avgTime) : '—') + '</td><td class="num">' + (s.time ? UI.fmtShort(s.time) : '—') + '</td></tr>';
      }).join('') + '</tbody></table></div></section>';

    app.innerHTML = html;
    if (exams.length) chart(document.getElementById('chart'), exams);

    app.querySelectorAll('[data-del]').forEach(function (b) {
      b.addEventListener('click', function () {
        UI.confirm('Delete this exam?', 'It will be removed from your history. Topic progress is not changed.', 'Delete', true).then(function (ok) {
          if (ok) { Store.deleteExam(b.getAttribute('data-del')); render(); }
        });
      });
    });
  }

  function tile(v, l) { return '<div class="tile card"><span class="tile__num">' + v + '</span><span class="tile__label">' + l + '</span></div>'; }

  /* Single-series line chart of all exams in order; y fixed to 0–90 with the pass threshold (45 pt = grade 5.5). */
  function chart(el, exams) {
    var W = 760, H = 260, m = { l: 40, r: 20, t: 16, b: 34 };
    var iw = W - m.l - m.r, ih = H - m.t - m.b;
    var n = exams.length;
    var X = function (i) { return m.l + (n === 1 ? iw / 2 : i * iw / (n - 1)); };
    var Y = function (v) { return m.t + ih - v / 90 * ih; };
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Exam scores over time, out of 90">';
    [0, 30, 60, 90].forEach(function (v) {
      svg += '<line class="grid" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/><text class="axis" x="' + (m.l - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + v + '</text>';
    });
    svg += '<line class="pass" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(45) + '" y2="' + Y(45) + '"/><text class="pass-label" x="' + (W - m.r) + '" y="' + (Y(45) - 6) + '" text-anchor="end">pass line · 45 pt = 5.5</text>';
    var pts = exams.map(function (e, i) { return [X(i), Y(e.score)]; });
    if (n > 1) svg += '<polyline class="line" points="' + pts.map(function (p) { return p.join(','); }).join(' ') + '"/>';
    var step = Math.max(1, Math.ceil(n / 8));
    exams.forEach(function (e, i) {
      if (i % step === 0 || i === n - 1) svg += '<text class="axis" x="' + X(i) + '" y="' + (H - 10) + '" text-anchor="middle">#' + (i + 1) + '</text>';
    });
    exams.forEach(function (e, i) {
      svg += '<g class="pt" data-i="' + i + '" tabindex="0"><circle class="hit" cx="' + pts[i][0] + '" cy="' + pts[i][1] + '" r="14"/><circle class="mark' + (e.kind === 'past' ? ' mark--past' : '') + '" cx="' + pts[i][0] + '" cy="' + pts[i][1] + '" r="5"/></g>';
    });
    svg += '</svg>';
    el.innerHTML = svg + '<div class="tip" hidden></div><p class="muted small chart__note">Filled dots: practice exams · ringed dots: past exams. Hover or focus a dot for details; click to open the results.</p>';
    var tip = el.querySelector('.tip');
    el.querySelectorAll('.pt').forEach(function (g) {
      var i = Number(g.getAttribute('data-i')), e = exams[i];
      var showTip = function () {
        tip.hidden = false;
        tip.innerHTML = '<strong>#' + (i + 1) + ' · ' + UI.esc(e.title || 'Practice exam') + '</strong><span>' + UI.fmtDate(e.submittedAt) + '</span><span>' + UI.num(e.score) + ' / 90 · grade ' + e.grade.toFixed(1) + '</span>';
        var r = el.getBoundingClientRect(), c = g.querySelector('.mark').getBoundingClientRect();
        tip.style.left = Math.min(r.width - 190, Math.max(0, c.left - r.left - 90)) + 'px';
        tip.style.top = (c.top - r.top - 78) + 'px';
        g.classList.add('is-hover');
      };
      var hideTip = function () { tip.hidden = true; g.classList.remove('is-hover'); };
      g.addEventListener('mouseenter', showTip); g.addEventListener('mouseleave', hideTip);
      g.addEventListener('focus', showTip); g.addEventListener('blur', hideTip);
      g.addEventListener('click', function () { location.href = 'results.html?id=' + encodeURIComponent(e.id); });
    });
  }

  render();
})();
