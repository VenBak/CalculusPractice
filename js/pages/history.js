/* Progress: exam history with score chart, weak topics, practice coverage and data export/import. */
(function () {
  'use strict';
  var app = document.getElementById('app');

  function render() {
    var exams = Store.exams();
    var topics = Bank.topics();
    var html = '<div class="page-head"><h1>Progress</h1><p class="muted">Every practice exam you submit is stored here, together with your topic practice.</p></div>';

    if (exams.length) {
      var best = exams.reduce(function (m, e) { return Math.max(m, e.score); }, 0);
      var last3 = exams.slice(-3), avg3 = last3.reduce(function (s, e) { return s + e.score; }, 0) / last3.length;
      var last = exams[exams.length - 1];
      html += '<section class="tiles">' +
        tile(exams.length, 'exams taken') + tile(UI.num(best) + '<small>/90</small>', 'best score') +
        tile(UI.num(avg3) + '<small>/90</small>', 'average of last ' + last3.length) +
        tile('<span class="' + (last.grade >= 5.5 ? 'good' : 'bad') + '">' + last.grade.toFixed(1) + '</span>', 'latest grade') + '</section>';
      html += '<section class="card"><h2>Exam scores over time</h2><div class="chart" id="chart"></div></section>';
      html += '<section class="card"><h2>All exams</h2><div class="table-wrap"><table class="table"><thead><tr><th>Date</th><th class="num">Score</th><th class="num">Grade</th><th class="num">Multiple choice</th><th class="num">Open</th><th class="num">Time</th><th></th></tr></thead><tbody>' +
        exams.slice().reverse().map(function (e) {
          var mc = e.items.filter(function (i) { return i.mode === 'mcq'; }), op = e.items.filter(function (i) { return i.mode === 'open'; });
          var s = function (l) { return UI.num(l.reduce(function (a, i) { return a + i.earned; }, 0)) + '/' + l.reduce(function (a, i) { return a + i.points; }, 0); };
          return '<tr><td><a href="results.html?id=' + encodeURIComponent(e.id) + '">' + UI.fmtDate(e.submittedAt) + '</a>' + (e.auto ? ' <span class="tag">timed out</span>' : '') + '</td>' +
            '<td class="num"><strong>' + UI.num(e.score) + '</strong></td><td class="num ' + (e.grade >= 5.5 ? 'good' : 'bad') + '">' + e.grade.toFixed(1) + '</td>' +
            '<td class="num">' + s(mc) + '</td><td class="num">' + s(op) + '</td><td class="num">' + UI.fmtDur(e.duration) + '</td>' +
            '<td class="num"><button class="btn btn--link btn--sm" data-del="' + UI.esc(e.id) + '">Delete</button></td></tr>';
        }).join('') + '</tbody></table></div></section>';

      // performance per area and per topic across all exams
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
          return '<li><a href="practice.html?topic=' + t.id + '">' + UI.esc(t.name) + '</a><span>' + Math.round(100 * w.r) + '% of ' + w.s.p + ' pt</span></li>';
        }).join('') + '</ol></div></section>';
    } else {
      html += '<section class="card empty"><h2>No exams yet</h2><p>Sit a <a href="exam.html">practice exam</a>: your score, grade and the topics you missed will be logged here.</p></section>';
    }

    // practice coverage
    html += '<section class="card"><h2>Topic practice</h2><div class="table-wrap"><table class="table"><thead><tr><th>Topic</th><th>Progress</th><th class="num">Correct</th><th class="num">Wrong</th><th class="num">Not tried</th></tr></thead><tbody>' +
      topics.map(function (t) {
        var s = Store.topicStats(t.id, t.count);
        return '<tr><td><a href="practice.html?topic=' + t.id + '">' + UI.esc(t.name) + '</a></td><td class="cell-bar">' + UI.bar(s.correct / s.total, { wrong: s.wrong / s.total, size: 'sm', label: t.name }) + '</td>' +
          '<td class="num">' + s.correct + '</td><td class="num' + (s.wrong ? ' bad' : '') + '">' + s.wrong + '</td><td class="num">' + (s.total - s.attempted) + '</td></tr>';
      }).join('') + '</tbody></table></div></section>';

    html += '<section class="card" id="data"><h2>Your data</h2><p class="muted">Everything is stored in this browser only. Export a backup to move it to another device or browser.</p>' +
      '<div class="actions"><button class="btn btn--ghost" id="export">Export progress (.json)</button>' +
      '<label class="btn btn--ghost">Import progress<input type="file" id="import" accept="application/json,.json" hidden></label>' +
      '<button class="btn btn--danger" id="wipe">Delete all progress</button></div></section>';

    app.innerHTML = html;
    if (exams.length) chart(document.getElementById('chart'), exams);

    app.querySelectorAll('[data-del]').forEach(function (b) {
      b.addEventListener('click', function () {
        UI.confirm('Delete this exam?', 'It will be removed from your history. Topic progress is not changed.', 'Delete', true).then(function (ok) {
          if (ok) { Store.deleteExam(b.getAttribute('data-del')); render(); }
        });
      });
    });
    document.getElementById('export').addEventListener('click', function () {
      var blob = new Blob([Store.exportAll()], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'calc-practice-progress-' + new Date().toISOString().slice(0, 10) + '.json';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    document.getElementById('import').addEventListener('change', function (e) {
      var f = e.target.files[0]; if (!f) return;
      f.text().then(function (txt) {
        return UI.confirm('Import progress?', 'This replaces the progress and exam history in this browser with the contents of “' + UI.esc(f.name) + '”.', 'Import').then(function (ok) {
          if (!ok) return;
          Store.importAll(txt); UI.toast('Progress imported'); render();
        });
      }).catch(function (err) { UI.toast('Import failed: ' + err.message); });
    });
    document.getElementById('wipe').addEventListener('click', function () {
      UI.confirm('Delete all progress?', 'This permanently removes all topic progress and every exam result from this browser.', 'Delete everything', true).then(function (ok) {
        if (ok) { Store.wipe(); UI.toast('All progress deleted'); render(); }
      });
    });
  }

  function tile(v, l) { return '<div class="tile card"><span class="tile__num">' + v + '</span><span class="tile__label">' + l + '</span></div>'; }

  /* Single-series line chart, y fixed to 0–90 with the pass threshold (45 pt = grade 5.5). */
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
      svg += '<g class="pt" data-i="' + i + '"><circle class="hit" cx="' + pts[i][0] + '" cy="' + pts[i][1] + '" r="14"/><circle class="mark" cx="' + pts[i][0] + '" cy="' + pts[i][1] + '" r="5"/></g>';
    });
    svg += '</svg>';
    el.innerHTML = svg + '<div class="tip" hidden></div>';
    var tip = el.querySelector('.tip');
    el.querySelectorAll('.pt').forEach(function (g) {
      var i = Number(g.getAttribute('data-i')), e = exams[i];
      var showTip = function () {
        tip.hidden = false;
        tip.innerHTML = '<strong>Exam #' + (i + 1) + '</strong><span>' + UI.fmtDate(e.submittedAt) + '</span><span>' + UI.num(e.score) + ' / 90 · grade ' + e.grade.toFixed(1) + '</span>';
        var r = el.getBoundingClientRect(), c = g.querySelector('.mark').getBoundingClientRect();
        tip.style.left = Math.min(r.width - 170, Math.max(0, c.left - r.left - 80)) + 'px';
        tip.style.top = (c.top - r.top - 74) + 'px';
        g.classList.add('is-hover');
      };
      var hideTip = function () { tip.hidden = true; g.classList.remove('is-hover'); };
      g.addEventListener('mouseenter', showTip); g.addEventListener('mouseleave', hideTip);
      g.addEventListener('click', function () { location.href = 'results.html?id=' + encodeURIComponent(e.id); });
    });
  }

  render();
})();
