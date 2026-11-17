/*
 * Store — everything the site remembers lives in localStorage under "cpt.*" keys.
 *   cpt.progress   { [questionId]: { status, attempts, correctCount, last, source } }
 *   cpt.exams      [ completed exam records, oldest first ]
 *   cpt.activeExam the exam currently in progress (or absent)
 */
(function (root) {
  'use strict';
  var K = { progress: 'cpt.progress', exams: 'cpt.exams', active: 'cpt.activeExam' };
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

  var Store = {
    progress: function () { return read(K.progress, {}); },

    record: function (qid, correct, source, answer) {
      var p = read(K.progress, {});
      var e = p[qid] || { attempts: 0, correctCount: 0 };
      e.attempts += 1;
      if (correct) e.correctCount += 1;
      e.status = correct ? 'correct' : 'wrong';
      e.last = Date.now();
      e.source = source || 'practice';
      if (answer !== undefined) e.answer = answer;
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
      var p = read(K.progress, {});
      Object.keys(p).forEach(function (id) { if (id.indexOf(topicId + '-') === 0 && /-\d{3}$/.test(id) && id.slice(0, -4) === topicId) delete p[id]; });
      write(K.progress, p);
    },

    topicStats: function (topicId, count) {
      var p = read(K.progress, {}), s = { total: count, correct: 0, wrong: 0, attempted: 0 };
      for (var i = 1; i <= count; i++) {
        var id = topicId + '-' + ('00' + i).slice(-3), e = p[id];
        if (!e) continue;
        s.attempted++;
        if (e.status === 'correct') s.correct++; else s.wrong++;
      }
      return s;
    },

    exams: function () { return read(K.exams, []); },
    exam: function (id) { return this.exams().filter(function (e) { return e.id === id; })[0] || null; },
    saveExam: function (rec) {
      var list = read(K.exams, []).filter(function (e) { return e.id !== rec.id; });
      list.push(rec);
      write(K.exams, list);
    },
    deleteExam: function (id) { write(K.exams, read(K.exams, []).filter(function (e) { return e.id !== id; })); },

    active: function () { return read(K.active, null); },
    setActive: function (a) { write(K.active, a); },
    clearActive: function () { remove(K.active); },

    exportAll: function () {
      return JSON.stringify({ app: 'calc-exam-practice', version: 1, exported: new Date().toISOString(),
        progress: read(K.progress, {}), exams: read(K.exams, []) }, null, 1);
    },
    importAll: function (text) {
      var d = JSON.parse(text);
      if (!d || d.app !== 'calc-exam-practice') throw new Error('This file is not an export of this site.');
      write(K.progress, d.progress || {});
      write(K.exams, d.exams || []);
    },
    wipe: function () { remove(K.progress); remove(K.exams); remove(K.active); }
  };

  root.Store = Store;
})(window);
