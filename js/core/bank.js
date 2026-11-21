/*
 * Bank — loads the question files in data/bank/ and builds practice exams.
 * Files are plain <script>s (not fetch/JSON) so the site also works when opened from disk.
 */
(function (root) {
  'use strict';
  var loaded = {};

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  function topics() { return root.CalcTopics.topics; }
  function areas() { return root.CalcTopics.areas; }
  function topic(id) { return topics().filter(function (t) { return t.id === id; })[0] || null; }
  function area(id) { return areas().filter(function (a) { return a.id === id; })[0] || null; }

  function load(ids) {
    ids = ids || topics().map(function (t) { return t.id; });
    return Promise.all(ids.map(function (id) {
      if (!loaded[id]) loaded[id] = loadScript('data/bank/' + id + '.js');
      return loaded[id];
    })).then(function () { return root.CalcBank; });
  }

  function question(id) {
    var tid = id.slice(0, -4);
    var list = (root.CalcBank || {})[tid] || [];
    return list.filter(function (q) { return q.id === id; })[0] || null;
  }

  /* ---------------- past exams ---------------- */
  var pastLoaded = {};
  function pastIndex() { return root.CalcPastIndex || []; }
  function loadPast(ids) {
    ids = ids || pastIndex().map(function (e) { return e.id; });
    return Promise.all(ids.map(function (id) {
      if (!pastLoaded[id]) pastLoaded[id] = loadScript('data/past-exams/' + id + '.js');
      return pastLoaded[id];
    })).then(function () { return root.CalcPast; });
  }
  function pastExam(id) { return (root.CalcPast || {})[id] || null; }
  function pastMeta(id) { return pastIndex().filter(function (e) { return e.id === id; })[0] || null; }
  function pastTitle(meta) {
    if (!meta) return 'Past exam';
    var d = meta.date.replace(/^(\w+) \d+, (\d+)$/, '$1 $2');
    return d + ' · ' + meta.kind;
  }

  /* Flatten an exam into its answerable items (sub-questions). */
  var flatCache = {};
  function pastItems(id) {
    if (flatCache[id]) return flatCache[id];
    var ex = pastExam(id), out = [];
    if (!ex) return out;
    ex.questions.forEach(function (q, gi) {
      q.items.forEach(function (it, ii) {
        out.push({
          ref: 'past:' + id + ':' + out.length, gi: gi, ii: ii, group: q, first: ii === 0, single: q.items.length === 1,
          label: q.no + (it.label ? ' ' + it.label : ''), prompt: it.prompt || q.intro, parts: it.parts, points: it.points,
          topic: it.topic, hints: it.hints, solution: it.solution
        });
      });
    });
    flatCache[id] = out;
    return out;
  }

  /*
   * Resolve any stored reference (a bank question id, or "past:<exam>:<n>") to a displayable item:
   * { prompt, parts, mcq, hints, solution, topic, label? }
   */
  function resolve(ref) {
    if (!ref) return null;
    if (ref.indexOf('past:') === 0) {
      var bits = ref.split(':');
      return pastItems(bits[1])[Number(bits[2])] || null;
    }
    return question(ref);
  }

  /* -------- seeded RNG so an exam can be rebuilt from its seed -------- */
  function mulberry(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, rnd) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  /*
   * Exam blueprint (matches the old exams: 90 points, 36 of them multiple choice).
   *  Part 1: 12 multiple-choice items × 3 pt  (Foundations 3, Derivatives 4, Integrals 3, Probability 2)
   *  Part 2: 54 pt of open questions worth 3–6 pt (Foundations 8, Derivatives 21, Integrals 15, Probability 10)
   */
  var MCQ_QUOTA = { foundations: 3, derivatives: 4, integrals: 3, probability: 2 };
  var OPEN_QUOTA = { foundations: 8, derivatives: 21, integrals: 15, probability: 10 };

  function buildExam(seed) {
    var rnd = mulberry(seed);
    var used = {}, mcq = [], open = [];
    var progress = root.Store ? root.Store.progress() : {};

    function pool(areaId, filter) {
      return topics().filter(function (t) { return t.area === areaId; }).map(function (t) {
        return shuffle((root.CalcBank[t.id] || []).filter(function (q) { return !used[q.id] && filter(q); }), rnd)
          // questions you have not yet solved come first
          .sort(function (a, b) { return ((progress[a.id] || {}).status === 'correct') - ((progress[b.id] || {}).status === 'correct'); });
      });
    }

    Object.keys(MCQ_QUOTA).forEach(function (areaId) {
      var lists = shuffle(pool(areaId, function (q) { return !!q.mcq; }), rnd), k = 0, guard = 0;
      while (k < MCQ_QUOTA[areaId] && guard++ < 50) {
        var list = lists[guard % lists.length];
        var q = list.filter(function (x) { return !used[x.id]; })[0];
        if (!q) continue;
        used[q.id] = true; k++;
        var n = q.mcq.options.length, order;
        if (q.mcq.native) order = q.mcq.options.map(function (_, i) { return i; });
        else order = shuffle(q.mcq.options.map(function (_, i) { return i; }).slice(0, Math.min(n, 6)), rnd);
        mcq.push({ ref: q.id, qid: q.id, mode: 'mcq', points: 3, order: order });
      }
    });

    Object.keys(OPEN_QUOTA).forEach(function (areaId) {
      var remaining = OPEN_QUOTA[areaId];
      var lists = shuffle(pool(areaId, function (q) { return !(q.mcq && q.mcq.native); }), rnd);
      var guard = 0, ti = 0;
      while (remaining > 0 && guard++ < 200) {
        var list = lists[ti++ % lists.length];
        var fits = list.filter(function (x) {
          if (used[x.id]) return false;
          var left = remaining - x.points;
          return left === 0 || left >= 3;
        });
        var q = fits[0];
        if (!q) {
          if (guard < 40) continue;
          q = list.filter(function (x) { return !used[x.id]; })[0];
          if (!q) continue;
        }
        used[q.id] = true;
        var pts = Math.min(q.points, remaining);
        if (remaining - pts > 0 && remaining - pts < 3) pts = remaining;
        open.push({ ref: q.id, qid: q.id, mode: 'open', points: pts });
        remaining -= pts;
      }
    });

    open = shuffle(open, rnd);
    return mcq.concat(open);
  }

  /* -------- grading -------- */
  function filled(a) {
    if (a == null) return false;
    if (Array.isArray(a)) return a.length > 0;
    return String(a).trim() !== '';
  }

  function gradeItem(item, answers) {
    var q = resolve(item.ref || item.qid);
    if (item.mode === 'mcq') {
      var pick = answers == null || answers === '' ? null : Number(answers);
      var ok = pick !== null && item.order[pick] === q.mcq.correct;
      return { earned: ok ? item.points : 0, parts: [ok], answered: pick !== null };
    }
    answers = answers || [];
    var per = q.parts.map(function (p, i) { return root.MathCheck.checkPart(answers[i] == null ? '' : answers[i], p).ok; });
    // parts with their own points (past exams) keep them; otherwise the item's points are split evenly
    var pts = root.MathCheck.partPoints(q.parts, item.points);
    var earned = 0;
    per.forEach(function (ok, i) { if (ok) earned += pts[i]; });
    earned = Math.round(earned * 100) / 100;
    return { earned: earned, parts: per, answered: answers.some(filled) };
  }

  function grade(score) { return Math.round((1 + score / 10) * 10) / 10; }

  root.Bank = { load: load, topics: topics, areas: areas, topic: topic, area: area, question: question, resolve: resolve,
    pastIndex: pastIndex, loadPast: loadPast, pastExam: pastExam, pastMeta: pastMeta, pastItems: pastItems, pastTitle: pastTitle,
    buildExam: buildExam, gradeItem: gradeItem, grade: grade, MCQ_QUOTA: MCQ_QUOTA, OPEN_QUOTA: OPEN_QUOTA };
})(window);
