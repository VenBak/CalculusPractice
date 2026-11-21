/* Refresher guide page: guide.html?topic=<id>, or an index of all guides without a topic. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var id = UI.param('topic');
  var t = id && Bank.topic(id);
  if (!t) {
    var html = '<div class="page-head"><p class="eyebrow">Refreshers</p><h1>Topic refreshers</h1><p class="lede">Short summaries of the theory, the rules you need and one worked example per topic. Read one before you practise.</p></div>';
    Bank.areas().forEach(function (a) {
      html += '<section class="area"><div class="area__head"><h2>' + UI.esc(a.name) + '</h2><span class="area__meta">' + a.lecture + '</span></div><div class="topic-grid">';
      Bank.topics().filter(function (x) { return x.area === a.id; }).forEach(function (x) {
        html += '<a class="topic card" href="guide.html?topic=' + x.id + '"><div class="topic__top"><h3>' + UI.esc((window.CalcGuides[x.id] || x).title || x.name) + '</h3></div><p class="topic__desc">' + UI.esc(x.description) + '</p></a>';
      });
      html += '</div></section>';
    });
    app.innerHTML = html;
    return;
  }
  var g = window.CalcGuides[id] || { title: t.name };
  var area = Bank.area(t.area);
  var list = Bank.topics(), i = list.indexOf(t), prev = list[i - 1], next = list[i + 1];
  document.title = g.title + ' — Refresher';
  app.innerHTML = '<nav class="crumbs"><a href="guide.html">Refreshers</a><span>/</span><span>' + UI.esc(area.name) + '</span><span>/</span><span aria-current="page">' + UI.esc(g.title) + '</span></nav>' +
    '<div class="page-head"><p class="eyebrow">Refresher · ' + UI.esc(area.name) + '</p><h1>' + UI.esc(g.title) + '</h1>' +
    '<div class="actions"><a class="btn btn--primary" href="practice.html?topic=' + id + '">Practise this topic (' + t.count + ' questions)</a><a class="btn btn--ghost" href="reference.html">Reference page</a></div></div>' +
    '<article class="card guide-page">' + GuideView.html(id) + '</article>' +
    '<nav class="pager">' + (prev ? '<a href="guide.html?topic=' + prev.id + '">← ' + UI.esc(prev.name) + '</a>' : '<span></span>') +
    (next ? '<a href="guide.html?topic=' + next.id + '">' + UI.esc(next.name) + ' →</a>' : '<span></span>') + '</nav>';
  UI.math(app);
})();
