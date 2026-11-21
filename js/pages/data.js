/* Backup & transfer: copy all stored data as one string, paste it into another copy of the site, or use a file. */
(function () {
  'use strict';
  var app = document.getElementById('app');

  function render() {
    var s = Store.summary(Store.snapshot());
    var str = Store.exportString();
    app.innerHTML =
      '<div class="page-head"><p class="eyebrow">Your data</p><h1>Backup &amp; transfer</h1>' +
      '<p class="lede">Your progress lives only in this browser. To move it to another device, browser or copy of this website: copy the transfer string below, open the <em>Backup &amp; transfer</em> page there, and paste it in.</p></div>' +

      '<section class="card"><h2>1 · Copy your data</h2>' +
      '<p class="muted">Contains: <strong>' + s.questions + '</strong> practised questions (' + s.correct + ' correct), <strong>' + s.exams + '</strong> exam results, flags, logged times and your theme. The string is about ' + Math.max(1, Math.round(str.length / 1024)) + ' kB.</p>' +
      '<label class="sr" for="out">Transfer string</label><textarea id="out" class="transfer" readonly rows="6" spellcheck="false">' + UI.esc(str) + '</textarea>' +
      '<div class="actions"><button class="btn btn--primary" id="copy">Copy to clipboard</button><button class="btn btn--ghost" id="download">Download as .json file</button><span class="muted small" id="copied" aria-live="polite"></span></div></section>' +

      '<section class="card"><h2>2 · Paste data from another device</h2>' +
      '<label class="sr" for="in">Paste a transfer string</label><textarea id="in" class="transfer" rows="6" spellcheck="false" placeholder="Paste a transfer string starting with CPT2: (or the contents of an exported .json file)"></textarea>' +
      '<div id="check" class="check" aria-live="polite"></div>' +
      '<fieldset class="radios"><legend>When importing</legend>' +
      '<label><input type="radio" name="mode" value="merge" checked> <strong>Merge</strong> — keep what is here and add the imported data (for each question the most recent result wins; exams are combined).</label>' +
      '<label><input type="radio" name="mode" value="replace"> <strong>Replace</strong> — make this browser an exact copy of the imported data.</label></fieldset>' +
      '<div class="actions"><button class="btn btn--primary" id="import" disabled>Import</button>' +
      '<label class="btn btn--ghost">Load a .json file<input type="file" id="file" accept="application/json,.json,.txt" hidden></label></div></section>' +

      '<section class="card danger-zone"><h2>Delete everything</h2><p class="muted">Removes all topic progress, logged times, flags and exam results from this browser. Copy your data first if you might want it back.</p>' +
      '<div class="actions"><button class="btn btn--danger" id="wipe">Delete all progress</button></div></section>';

    var out = document.getElementById('out'), inp = document.getElementById('in'), check = document.getElementById('check'), btn = document.getElementById('import');
    document.getElementById('copy').addEventListener('click', function () {
      var done = function () { document.getElementById('copied').textContent = 'Copied — paste it on the other device.'; UI.toast('Transfer string copied'); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(out.value).then(done, fallback);
      else fallback();
      function fallback() { out.focus(); out.select(); try { document.execCommand('copy'); done(); } catch (e) { UI.toast('Select the text and copy it manually'); } }
    });
    out.addEventListener('focus', function () { out.select(); });
    document.getElementById('download').addEventListener('click', function () {
      var blob = new Blob([Store.exportAll()], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'calc-practice-progress-' + new Date().toISOString().slice(0, 10) + '.json';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });

    var validate = function () {
      var v = inp.value.trim();
      if (!v) { check.innerHTML = ''; btn.disabled = true; return; }
      try {
        var d = Store.parseImport(v), s2 = Store.summary(d);
        check.innerHTML = '<span class="tag tag--ok">✓ Valid</span> ' + s2.questions + ' practised questions (' + s2.correct + ' correct), ' + s2.exams + ' exam results' +
          (s2.exported ? ', exported ' + UI.fmtDate(Date.parse(s2.exported)) : '') + '.';
        btn.disabled = false;
      } catch (e) {
        check.innerHTML = '<span class="tag tag--bad">✗</span> ' + UI.esc(e.message);
        btn.disabled = true;
      }
    };
    inp.addEventListener('input', validate);
    document.getElementById('file').addEventListener('change', function (e) {
      var f = e.target.files[0]; if (!f) return;
      f.text().then(function (txt) { inp.value = txt; validate(); });
    });
    btn.addEventListener('click', function () {
      var mode = app.querySelector('input[name="mode"]:checked').value;
      UI.confirm(mode === 'replace' ? 'Replace all data?' : 'Merge data?', mode === 'replace'
        ? 'Everything stored in this browser will be replaced by the imported data.'
        : 'The imported progress and exams will be combined with what is stored here.', 'Import', mode === 'replace').then(function (ok) {
        if (!ok) return;
        try { Store.importAll(inp.value, mode); UI.toast('Data imported'); render(); }
        catch (err) { check.innerHTML = '<span class="tag tag--bad">✗</span> ' + UI.esc(err.message); }
      });
    });
    document.getElementById('wipe').addEventListener('click', function () {
      UI.confirm('Delete all progress?', 'This permanently removes all topic progress, logged times, flags and every exam result from this browser.', 'Delete everything', true).then(function (ok) {
        if (ok) { Store.wipe(); UI.toast('All progress deleted'); render(); }
      });
    });
  }
  render();
})();
