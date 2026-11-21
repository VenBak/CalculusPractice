/*
 * Store — everything the site remembers lives in localStorage under "cpt.*" keys.
 *   cpt.progress   { [questionId]: { status, attempts, correctCount, last, source, times:[sec…], totalTime, hints } }
 *   cpt.exams      [ completed exam records (practice and past exams), oldest first ]
 *   cpt.activeExam the exam currently in progress (or absent)
 *   cpt.pending    { [questionId]: seconds spent on an unanswered attempt (kept while you are away/flagged) }
 *   cpt.flags      { [questionId]: true } flagged practice questions
 *   cpt.theme      "light" | "dark" (see theme.js)
 */
(function (root) {
  'use strict';
  var K = { progress: 'cpt.progress', exams: 'cpt.exams', active: 'cpt.activeExam', pending: 'cpt.pending', flags: 'cpt.flags', theme: 'cpt.theme' };
  var EXPORT_PREFIX = 'CPT2:';
  var memory = {};

  function read(key, fallback) {
    try {
      var raw = root.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return key in memory ? memory[key] : fallback;
    }
  }

  function write(key, value) {
    memory[key] = value;
    try { root.localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode: keep in memory */ }
  }

  function remove(key) {
    delete memory[key];
    try { root.localStorage.removeItem(key); } catch (e) { /* ignore */ }
  }

  function topicOf(id) { return id.slice(0, -4); }

  /* UTF-8 safe base64 for the copy/paste transfer string */
  function b64encode(str) {
    var bytes = new TextEncoder().encode(str), bin = '';
    for (var i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }
  function b64decode(b64) {
    var bin = atob(b64.replace(/\s+/g, '')), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }

  var Store = {
    /* ---------------- practice progress ---------------- */
    progress: function () { return read(K.progress, {}); },

    record: function (qid, correct, source, answer, seconds, hints) {
      var p = read(K.progress, {});
      var e = p[qid] || { attempts: 0, correctCount: 0 };
      e.attempts += 1;
      if (correct) e.correctCount += 1;
      e.status = correct ? 'correct' : 'wrong';
      e.last = Date.now();
      e.source = source || 'practice';
      if (answer !== undefined) e.answer = answer;
      if (seconds != null && seconds > 0) {
        e.times = (e.times || []).concat([Math.round(seconds)]).slice(-20);
        e.totalTime = (e.totalTime || 0) + Math.round(seconds);
      }
      if (hints) e.hints = (e.hints || 0) + hints;
      p[qid] = e;
      write(K.progress, p);
      return e;
    },

    override: function (qid) {
      var p = read(K.progress, {});
      if (!p[qid]) return;
      p[qid].status = 'correct';
      p[qid].correctCount = (p[qid].correctCount || 0) + 1;
      p[qid].overridden = true;
      write(K.progress, p);
    },

    resetTopic: function (topicId) {
      var p = read(K.progress, {}), pend = read(K.pending, {}), fl = read(K.flags, {});
      [p, pend, fl].forEach(function (obj) {
        Object.keys(obj).forEach(function (id) { if (topicOf(id) === topicId) delete obj[id]; });
      });
      write(K.progress, p); write(K.pending, pend); write(K.flags, fl);
    },

    topicStats: function (topicId, count) {
      var p = read(K.progress, {}), s = { total: count, correct: 0, wrong: 0, attempted: 0, time: 0, timed: 0 };
      for (var i = 1; i <= count; i++) {
        var id = topicId + '-' + ('00' + i).slice(-3), e = p[id];
        if (!e) continue;
        s.attempted++;
        if (e.status === 'correct') s.correct++; else s.wrong++;
        if (e.times && e.times.length) { s.time += e.totalTime || 0; s.timed += e.times.length; }
      }
      s.avgTime = s.timed ? s.time / s.timed : 0;
      return s;
    },

    /* ---------------- time spent on an unanswered attempt ---------------- */
    pending: function (qid) { return read(K.pending, {})[qid] || 0; },
    setPending: function (qid, sec) {
      var p = read(K.pending, {});
      if (sec > 0) p[qid] = Math.round(sec); else delete p[qid];
      write(K.pending, p);
    },

    /* ---------------- flagged practice questions ---------------- */
    flags: function () { return read(K.flags, {}); },
    isFlagged: function (qid) { return !!read(K.flags, {})[qid]; },
    setFlag: function (qid, on) {
      var f = read(K.flags, {});
      if (on) f[qid] = true; else delete f[qid];
      write(K.flags, f);
    },

    /* ---------------- exams ---------------- */
    exams: function () { return read(K.exams, []); },
    exam: function (id) { return this.exams().filter(function (e) { return e.id === id; })[0] || null; },
    saveExam: function (rec) {
      var list = read(K.exams, []).filter(function (e) { return e.id !== rec.id; });
      list.push(rec);
      list.sort(function (a, b) { return a.submittedAt - b.submittedAt; });
      write(K.exams, list);
    },
    deleteExam: function (id) { write(K.exams, read(K.exams, []).filter(function (e) { return e.id !== id; })); },

    active: function () { return read(K.active, null); },
    setActive: function (a) { write(K.active, a); },
    clearActive: function () { remove(K.active); },

    /* ---------------- export / import ---------------- */
    snapshot: function () {
      var theme = null;
      try { theme = root.localStorage.getItem(K.theme); } catch (e) { /* ignore */ }
      return { app: 'calc-exam-practice', version: 2, exported: new Date().toISOString(),
        progress: read(K.progress, {}), exams: read(K.exams, []), flags: read(K.flags, {}),
        pending: read(K.pending, {}), activeExam: read(K.active, null), theme: theme };
    },
    exportAll: function () { return JSON.stringify(this.snapshot(), null, 1); },
    exportString: function () { return EXPORT_PREFIX + b64encode(JSON.stringify(this.snapshot())); },

    parseImport: function (text) {
      var t = String(text || '').trim(), d;
      if (!t) throw new Error('Nothing to import — paste your transfer string first.');
      if (t.indexOf(EXPORT_PREFIX) === 0) {
        try { d = JSON.parse(b64decode(t.slice(EXPORT_PREFIX.length))); } catch (e) { throw new Error('The transfer string is damaged or incomplete. Copy it again in full.'); }
      } else {
        try { d = JSON.parse(t); } catch (e) { throw new Error('This is neither a transfer string (starting with CPT2:) nor an exported .json file.'); }
      }
      if (!d || d.app !== 'calc-exam-practice') throw new Error('This data does not come from this website.');
      return d;
    },

    summary: function (d) {
      var p = d.progress || {}, ids = Object.keys(p);
      return { questions: ids.length, correct: ids.filter(function (k) { return p[k].status === 'correct'; }).length,
        exams: (d.exams || []).length, exported: d.exported || null };
    },

    importAll: function (text, mode) {
      var d = this.parseImport(text);
      if (mode === 'merge') {
        var p = read(K.progress, {}), inP = d.progress || {};
        Object.keys(inP).forEach(function (id) {
          var a = p[id], b = inP[id];
          if (!a || (b.last || 0) > (a.last || 0)) p[id] = b;
        });
        var ex = read(K.exams, []), have = {};
        ex.forEach(function (e) { have[e.id] = true; });
        (d.exams || []).forEach(function (e) { if (!have[e.id]) ex.push(e); });
        ex.sort(function (a, b) { return a.submittedAt - b.submittedAt; });
        var fl = read(K.flags, {});
        Object.keys(d.flags || {}).forEach(function (k) { fl[k] = true; });
        write(K.progress, p); write(K.exams, ex); write(K.flags, fl);
      } else {
        write(K.progress, d.progress || {});
        write(K.exams, d.exams || []);
        write(K.flags, d.flags || {});
        write(K.pending, d.pending || {});
        if (d.activeExam) write(K.active, d.activeExam); else remove(K.active);
        if (d.theme && root.CalcTheme) root.CalcTheme.set(d.theme);
      }
      return d;
    },
    wipe: function () { [K.progress, K.exams, K.active, K.pending, K.flags].forEach(remove); }
  };

  root.Store = Store;
})(window);
