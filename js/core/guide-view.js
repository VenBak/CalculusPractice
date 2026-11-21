/* GuideView — renders a topic's refresher guide (data/guides.js) as HTML. Content is trusted, authored HTML + LaTeX. */
(function (root) {
  'use strict';
  function html(topicId) {
    var g = (root.CalcGuides || {})[topicId];
    if (!g) return '<p class="muted">No refresher available for this topic yet.</p>';
    return '<div class="guide">' +
      '<section class="guide__sec"><h3>The idea</h3>' + g.idea + '</section>' +
      '<section class="guide__sec"><h3>Key rules</h3><ul class="guide__rules">' + g.rules.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ul></section>' +
      '<section class="guide__sec guide__example"><h3>Worked example</h3><p class="guide__q">' + g.example.question + '</p><ol>' +
      g.example.steps.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ol></section>' +
      '<section class="guide__sec"><h3>Common mistakes</h3><ul class="guide__pitfalls">' + g.pitfalls.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul></section>' +
      '</div>';
  }
  root.GuideView = { html: html };
})(window);
