/*
 * ExamRunner — runs a timed exam (random practice exam or real past exam).
 *
 * state (persisted as cpt.activeExam):
 *   { id, kind: 'random'|'past', pastId?, title, startedAt, endsAt,
 *     items: [{ ref, mode: 'mcq'|'open', points, order? }],
 *     answers: { idx: value }, flags: { idx: true }, times: { idx: seconds }, hints: { idx: count } }
 * paper: { groups: [{ no, title, points, intro, items: [idx…], labels: [label…] }] }
 *
 * Time per question: the question you last clicked/typed in (or the one in view) collects time every second,
 * unless it is flagged — flagging pauses its clock until you unflag it.
 */
(function (root) {
  'use strict';
  var UI = root.UI, Bank = root.Bank, Store = root.Store;

  function mount(opts) {
    var app = opts.app, state = opts.state, paper = opts.paper;
    state.answers = state.answers || {};
    state.flags = state.flags || {};
    state.times = state.times || {};
    state.hints = state.hints || {};
    var timer = null, saveTimer = null, submitting = false, dirty = false, active = null, lastSave = Date.now();
    var itemEls = {};

    document.body.classList.add('in-exam');
    app.innerHTML =
      '<div class="exam-bar" id="exam-bar"><div class="exam-bar__inner">' +
      '<div class="timer" id="timer" role="timer" aria-live="off"><span class="timer__label">Time left</span><span class="timer__value" id="timer-value">–</span></div>' +
      '<div class="exam-bar__title"><strong>' + UI.esc(state.title) + '</strong><span id="answered-count"></span><div id="answered-bar"></div></div>' +
      '<div class="exam-bar__actions"><button class="btn btn--ghost btn--sm" id="abandon">Abandon</button><button class="btn btn--primary" id="submit">Submit exam</button></div>' +
      '</div></div>' +
      '<div class="exam-layout"><aside class="exam-nav card" aria-label="Question overview"><h3>Overview</h3><div id="exam-nav"></div></aside>' +
      '<div class="exam-paper" id="paper"></div></div>';
    var paperEl = document.getElementById('paper');

    paper.groups.forEach(function (g) {
      var sec = UI.h('section', { class: 'exam-q card', id: 'g' + g.no });
      var multi = g.items.length > 1;
      sec.innerHTML = '<header class="exam-q__head"><h2>' + UI.esc(g.no) + '. ' + (g.title ? UI.rich(g.title) : '') + '</h2><span class="pts">' + UI.num(g.points) + ' pt</span></header>' +
        (g.intro ? '<div class="prompt exam-q__intro">' + UI.rich(g.intro) + '</div>' : '');
      UI.math(sec.querySelector('.exam-q__head'));
      if (g.intro) UI.math(sec.querySelector('.exam-q__intro'));
      g.items.forEach(function (idx, k) {
        var el = renderItem(idx, multi ? g.labels[k] : '', multi);
        sec.appendChild(el);
      });
      paperEl.appendChild(sec);
    });
    paperEl.appendChild(UI.h('div', { class: 'exam-end card' }, '<p>End of the exam. Check your answers, then submit.</p><button class="btn btn--primary" id="submit2">Submit exam</button>'));

    function renderItem(idx, label, multi) {
      var it = state.items[idx], q = Bank.resolve(it.ref);
      var el = UI.h('div', { class: 'exam-item' + (multi ? ' exam-item--sub' : ''), id: 'item-' + idx, 'data-i': String(idx) });
      itemEls[idx] = el;
      var head = UI.h('div', { class: 'exam-item__head' });
      head.innerHTML = (label ? '<span class="exam-item__label">' + UI.esc(label) + '</span>' : '') +
        (multi ? '<span class="pts pts--sm">' + UI.num(it.points) + ' pt</span>' : '') +
        '<span class="qtime" id="qtime-' + idx + '" title="Time spent on this question">' + UI.ICON.clock + '<span>' + UI.fmtShort(state.times[idx]) + '</span></span>' +
        '<button type="button" class="flag" data-i="' + idx + '" aria-pressed="' + (!!state.flags[idx]) + '" title="Flag to come back later — pauses this question’s clock">' + UI.ICON.flag + '<span class="sr">Flag</span></button>';
      el.appendChild(head);
      if (q.prompt && !(opts.skipPrompt && opts.skipPrompt(idx))) {
        var pr = UI.h('div', { class: 'prompt' }, UI.rich(q.prompt));
        el.appendChild(pr);
        UI.math(pr);
      }
      var hb = UI.hintBox(q.hints, function (n) { state.hints[idx] = n; setActive(idx); changed(); }, state.hints[idx] || 0);
      if (it.mode === 'mcq') {
        var list = UI.h('div', { class: 'choices' });
        it.order.forEach(function (oi, j) {
          var txt = q.mcq.native ? UI.rich(q.mcq.options[oi]) : UI.tex(q.mcq.options[oi]);
          var lab = UI.h('label', { class: 'choice' });
          lab.innerHTML = '<input type="radio" name="m' + idx + '" value="' + j + '"' + (String(state.answers[idx]) === String(j) ? ' checked' : '') + '>' +
            '<span class="choice__letter">' + String.fromCharCode(65 + j) + '</span><span class="choice__text">' + txt + '</span>';
          lab.querySelector('input').addEventListener('change', function (e) { state.answers[idx] = e.target.value; changed(); });
          list.appendChild(lab);
        });
        UI.math(list);
        el.appendChild(list);
      } else {
        var saved = state.answers[idx] || [];
        var fields = q.parts.map(function (p, j) {
          var f = UI.answerField(p, idx + '-' + j, saved[j] == null ? '' : saved[j], function () {
            state.answers[idx] = fields.map(function (x) { return x.get(); });
            changed();
          });
          el.appendChild(f.el);
          return f;
        });
      }
      el.appendChild(hb);
      return el;
    }

    /* ---------------- interaction ---------------- */
    paperEl.addEventListener('click', function (e) {
      var b = e.target.closest('.flag');
      if (!b) return;
      var i = b.getAttribute('data-i');
      state.flags[i] = !state.flags[i];
      if (!state.flags[i]) delete state.flags[i];
      b.setAttribute('aria-pressed', String(!!state.flags[i]));
      paintTime(Number(i));
      changed();
    });
    var pick = function (e) {
      var el = e.target.closest && e.target.closest('.exam-item');
      if (el) setActive(Number(el.getAttribute('data-i')));
    };
    paperEl.addEventListener('focusin', pick);
    paperEl.addEventListener('pointerdown', pick);
    var scrollT = null;
    window.addEventListener('scroll', function () {
      clearTimeout(scrollT);
      scrollT = setTimeout(followScroll, 250);
    }, { passive: true });

    function inView(el) {
      var r = el.getBoundingClientRect();
      return r.bottom > 90 && r.top < window.innerHeight;
    }
    function followScroll() {
      if (active !== null && itemEls[active] && inView(itemEls[active])) return;
      var best = null, bestD = Infinity, target = window.innerHeight * 0.35;
      Object.keys(itemEls).forEach(function (k) {
        var r = itemEls[k].getBoundingClientRect();
        if (r.bottom < 90 || r.top > window.innerHeight) return;
        var d = Math.abs(r.top - target);
        if (d < bestD) { bestD = d; best = Number(k); }
      });
      if (best !== null) setActive(best);
    }
    function setActive(i) {
      if (active === i) return;
      if (active !== null && itemEls[active]) itemEls[active].classList.remove('is-active');
      active = i;
      if (itemEls[i]) itemEls[i].classList.add('is-active');
      drawNav();
    }
    function paintTime(i) {
      var chip = document.getElementById('qtime-' + i);
      if (!chip) return;
      chip.querySelector('span').textContent = UI.fmtShort(state.times[i]) + (state.flags[i] ? ' · paused' : '');
      chip.classList.toggle('qtime--paused', !!state.flags[i]);
      chip.classList.toggle('qtime--running', i === active && !state.flags[i]);
    }

    document.getElementById('submit').addEventListener('click', askSubmit);
    document.getElementById('submit2').addEventListener('click', askSubmit);
    document.getElementById('abandon').addEventListener('click', function () {
      UI.confirm('Abandon this exam?', 'Your answers will be discarded and nothing is saved to your history.', 'Abandon exam', true).then(function (ok) {
        if (!ok) return;
        submitting = true;
        Store.clearActive(); clearInterval(timer); document.body.classList.remove('in-exam');
        if (opts.onAbandon) opts.onAbandon();
      });
    });
    window.addEventListener('beforeunload', function () { if (!submitting && dirty) Store.setActive(state); });

    function isAnswered(i) {
      var a = state.answers[i];
      if (state.items[i].mode === 'mcq') return a != null && a !== '';
      return Array.isArray(a) && a.some(function (v) { return Array.isArray(v) ? v.length > 0 : String(v).trim() !== ''; });
    }

    function changed() {
      dirty = true;
      clearTimeout(saveTimer);
      saveTimer = setTimeout(save, 300);
      drawNav();
    }
    function save() { Store.setActive(state); dirty = false; lastSave = Date.now(); }

    function drawNav() {
      // multi-part questions get their own row; consecutive single questions share a row
      var blocks = [];
      paper.groups.forEach(function (g) {
        if (g.items.length > 1) {
          blocks.push({ title: g.navTitle || ('Question ' + g.no), cells: g.items.map(function (idx, k) { return [idx, g.short[k]]; }) });
        } else {
          var last = blocks[blocks.length - 1];
          if (last && last.singles) last.cells.push([g.items[0], g.no]);
          else blocks.push({ singles: true, title: g.navTitle || 'Questions', cells: [[g.items[0], g.no]] });
        }
      });
      var html = '';
      blocks.forEach(function (b) {
        html += '<div class="navgroup"><span>' + UI.esc(b.title) + '</span><div class="navcells">';
        b.cells.forEach(function (c) {
          var idx = c[0];
          html += '<a href="#item-' + idx + '" class="navcell' + (isAnswered(idx) ? ' is-done' : '') + (state.flags[idx] ? ' is-flag' : '') + (idx === active ? ' is-active' : '') + '">' + UI.esc(c[1]) + '</a>';
        });
        html += '</div></div>';
      });
      html += '<div class="legend small"><span><i class="dot dot--accent"></i>answered</span><span><i class="dot dot--flag"></i>flagged (clock paused)</span></div>';
      document.getElementById('exam-nav').innerHTML = html;
      var n = state.items.filter(function (_, i) { return isAnswered(i); }).length;
      document.getElementById('answered-count').textContent = n + ' of ' + state.items.length + ' answered';
      document.getElementById('answered-bar').innerHTML = UI.bar(n / state.items.length, { size: 'sm', label: 'Answered' });
    }

    function tick() {
      var left = Math.max(0, Math.round((state.endsAt - Date.now()) / 1000));
      var el = document.getElementById('timer-value');
      if (!el) return;
      el.textContent = UI.fmtDur(left);
      var t = document.getElementById('timer');
      t.classList.toggle('timer--warn', left <= 15 * 60 && left > 5 * 60);
      t.classList.toggle('timer--danger', left <= 5 * 60);
      if (left === 15 * 60 || left === 5 * 60) UI.toast((left / 60) + ' minutes left');
      if (!document.hidden && active !== null && !state.flags[active]) {
        state.times[active] = (state.times[active] || 0) + 1;
        if (Date.now() - lastSave > 10000) save();
      }
      Object.keys(itemEls).forEach(function (k) { paintTime(Number(k)); });
      if (left <= 0) submit(true);
    }

    function askSubmit() {
      var unanswered = state.items.filter(function (_, i) { return !isAnswered(i); }).length;
      var flagged = Object.keys(state.flags).filter(function (k) { return state.flags[k]; }).length;
      var msg = 'Time left: ' + UI.fmtDur((state.endsAt - Date.now()) / 1000) + '.';
      if (unanswered) msg += ' <strong>' + unanswered + ' question' + (unanswered > 1 ? 's are' : ' is') + ' unanswered.</strong>';
      if (flagged) msg += ' ' + flagged + ' flagged.';
      UI.confirm('Submit your exam?', msg + ' You cannot change your answers afterwards.', 'Submit and grade').then(function (ok) { if (ok) submit(false); });
    }

    function submit(auto) {
      if (submitting) return;
      submitting = true;
      clearInterval(timer);
      var now = Date.now();
      var items = state.items.map(function (it, i) {
        var q = Bank.resolve(it.ref);
        var g = Bank.gradeItem(it, state.answers[i]);
        var topic = q.topic;
        return { ref: it.ref, label: labelOf[i], topic: topic, area: Bank.topic(topic).area, mode: it.mode, points: it.points, order: it.order,
          answer: state.answers[i] == null ? null : state.answers[i], earned: g.earned, parts: g.parts, answered: g.answered,
          time: Math.round(state.times[i] || 0), hints: state.hints[i] || 0 };
      });
      var score = Math.round(items.reduce(function (s, it) { return s + it.earned; }, 0) * 100) / 100;
      var rec = { id: state.id, kind: state.kind, pastId: state.pastId, title: state.title, seed: state.seed,
        startedAt: state.startedAt, submittedAt: now, minutes: state.minutes,
        duration: Math.min(state.endsAt - state.startedAt, now - state.startedAt) / 1000, auto: !!auto, items: items,
        score: score, max: 90, grade: Bank.grade(score) };
      Store.saveExam(rec);
      // practice-exam questions also count towards topic progress
      items.forEach(function (it) {
        if (it.answered && it.ref.indexOf('past:') !== 0) Store.record(it.ref, it.earned >= it.points, 'exam', it.answer, it.time, it.hints);
      });
      Store.clearActive();
      document.body.classList.remove('in-exam');
      location.href = 'results.html?id=' + encodeURIComponent(rec.id) + (auto ? '&auto=1' : '');
    }

    var labelOf = {};
    paper.groups.forEach(function (g) {
      g.items.forEach(function (idx, k) { labelOf[idx] = g.items.length > 1 ? g.no + g.labels[k].replace(/[()]/g, '') : g.no; });
    });

    drawNav();
    tick();
    timer = setInterval(tick, 1000);
    setTimeout(followScroll, 50);
  }

  root.ExamRunner = { mount: mount };
})(window);
