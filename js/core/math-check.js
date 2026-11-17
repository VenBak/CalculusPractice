/*
 * MathCheck — parses typed answers and compares them with stored answers.
 * Answer kinds: number, expr, interval, set, choice.
 * Depends on math.js (global `math`, or require('mathjs') under Node for tests).
 */
(function (root) {
  'use strict';
  var M = root.math || (typeof require !== 'undefined' ? require('mathjs') : null);

  var REL = 1e-6;

  /* ------------------------------------------------------------ normalise */
  function normalize(str) {
    var s = String(str == null ? '' : str).trim();
    s = s.replace(/[−–—]/g, '-').replace(/[×·⋅∙]/g, '*').replace(/÷/g, '/')
      .replace(/π/g, 'pi').replace(/∞/g, 'Infinity').replace(/√/g, 'sqrt')
      .replace(/²/g, '^2').replace(/³/g, '^3').replace(/\*\*/g, '^')
      .replace(/\\cdot/g, '*').replace(/\\pi/g, 'pi').replace(/\\infty/g, 'Infinity')
      .replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, '(($1)/($2))')
      .replace(/\\sqrt\{([^{}]*)\}/g, 'sqrt($1)').replace(/[{}]/g, function (c) { return c === '{' ? '(' : ')'; })
      .replace(/\\left|\\right|\\,|\\!/g, '').replace(/\\/g, '');
    s = s.replace(/\barc(sin|cos|tan)\b/g, 'a$1');
    s = s.replace(/(^|[^a-zA-Z])ln/g, '$1log');
    // "ln 3", "2ln2", "sin x" -> function call
    s = s.replace(/(^|[^a-zA-Z])(log|sin|cos|tan|sqrt|exp)\s*(\d+(?:\.\d+)?|[a-z])(?![\w(])/g, '$1$2($3)');
    s = s.replace(/\b(inf|infty|infinity)\b/gi, 'Infinity');
    s = s.replace(/\bE\b/g, 'e');
    // sin^2(x) -> (sin(x))^2  (non-nested argument)
    s = s.replace(/\b(sin|cos|tan|log)\^(\d+)\s*\(([^()]*)\)/g, '($1($3))^$2');
    // |x| -> abs(x)
    for (var i = 0; i < 3; i++) s = s.replace(/\|([^|]+)\|/g, 'abs($1)');
    // trailing percent
    s = s.replace(/(\d+(?:\.\d+)?)\s*%/g, '($1/100)');
    // decimal comma "0,25" only when it is the whole string
    if (/^-?\d+,\d+$/.test(s)) s = s.replace(',', '.');
    return s.trim();
  }

  function stripLhs(s) {
    // "y = 2x+1", "f'(x) = ...", "L = 3" -> right-hand side
    var idx = s.lastIndexOf('=');
    if (idx >= 0) s = s.slice(idx + 1);
    return s.trim();
  }

  function toReal(v) {
    if (v == null) return NaN;
    if (typeof v === 'number') return v;
    if (typeof v === 'boolean') return NaN;
    if (v.isComplex) return Math.abs(v.im) < 1e-9 * Math.max(1, Math.abs(v.re)) ? v.re : NaN;
    if (v.isFraction || v.isBigNumber) return Number(v.valueOf());
    if (typeof v.valueOf === 'function' && typeof v.valueOf() === 'number') return v.valueOf();
    return NaN;
  }

  var compiled = {};
  function compile(expr) {
    if (compiled[expr]) return compiled[expr];
    var c = M.compile(expr);
    compiled[expr] = c;
    return c;
  }

  function evalNum(expr, scope) {
    var v = compile(expr).evaluate(Object.assign({}, scope || {}));
    return toReal(v);
  }

  function close(a, b, tol) {
    if (!isFinite(a) || !isFinite(b)) return a === b;
    tol = tol || {};
    var lim = tol.abs != null ? tol.abs : REL * Math.max(1, Math.abs(b));
    if (tol.abs != null && tol.rel != null) lim = Math.max(lim, tol.rel * Math.abs(b));
    return Math.abs(a - b) <= lim + 1e-12;
  }

  /* ------------------------------------------------------------ number */
  function checkNumber(input, part) {
    var s = stripLhs(normalize(input));
    if (!s) return { ok: false, empty: true };
    var u, a;
    try { u = evalNum(s); } catch (e) { return { ok: false, error: 'Could not read “' + input + '” as a number.' }; }
    if (isNaN(u)) return { ok: false, error: 'That does not evaluate to a real number.' };
    a = evalNum(part.answer);
    return { ok: close(u, a, part.tol) };
  }

  /* ------------------------------------------------------------ expression */
  function rng(seed) {
    var x = seed || 123456789;
    return function () { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return ((x >>> 0) % 1e6) / 1e6; };
  }

  function checkExpr(input, part) {
    var s = stripLhs(normalize(input));
    if (part.upToConstant) s = s.replace(/\+\s*C\s*$/, '').replace(/^C\s*\+/, '');
    if (!s) return { ok: false, empty: true };
    try { M.parse(s); } catch (e) { return { ok: false, error: 'Syntax error: ' + e.message }; }
    var vars = part.vars || ['x'];
    var R = rng(987654321), valid = 0, diffs = [], fail = false, unknown = null;
    for (var i = 0; i < 24 && valid < 10; i++) {
      var scope = { C: 0 };
      vars.forEach(function (v) {
        var b = (part.sample && part.sample[v]) || [-2, 2];
        scope[v] = b[0] + (b[1] - b[0]) * (0.03 + 0.94 * R());
      });
      var uv, av;
      try { uv = evalNum(s, scope); } catch (e) {
        var m = /Undefined symbol (\w+)/.exec(e.message);
        if (m) { unknown = m[1]; break; }
        continue;
      }
      try { av = evalNum(part.answer, scope); } catch (e) { continue; }
      if (!isFinite(uv) || !isFinite(av)) {
        if (isFinite(av) && !isFinite(uv) && !isNaN(uv)) { fail = true; break; }
        continue;
      }
      valid++;
      if (part.upToConstant) diffs.push({ d: uv - av, a: av });
      else if (!close(uv, av, { rel: 1e-6, abs: 1e-7 * Math.max(1, Math.abs(av)) })) { fail = true; break; }
    }
    if (unknown) return { ok: false, error: 'Unknown symbol “' + unknown + '”. Use the variable' + (vars.length > 1 ? 's ' : ' ') + vars.join(', ') + '.' };
    if (fail) return { ok: false };
    if (valid < 4) return { ok: false, error: 'Could not evaluate your expression on the domain of the question.' };
    if (part.upToConstant) {
      var d0 = diffs[0].d;
      for (var j = 1; j < diffs.length; j++) {
        if (Math.abs(diffs[j].d - d0) > 1e-6 * Math.max(1, Math.abs(diffs[j].a))) return { ok: false };
      }
    }
    return { ok: true };
  }

  /* ------------------------------------------------------------ intervals */
  function parseEndpoint(txt) {
    var t = txt.trim();
    if (/^[-+]?\s*Infinity$/.test(t)) return /^-/.test(t) ? -Infinity : Infinity;
    var v = evalNum(t);
    if (isNaN(v)) throw new Error('bad endpoint ' + txt);
    return v;
  }

  function splitTop(str, seps) {
    var out = [], depth = 0, cur = '';
    for (var i = 0; i < str.length; i++) {
      var c = str[i];
      if (c === '(' || c === '[') depth++;
      if (c === ')' || c === ']') depth--;
      if (depth === 0 && seps.indexOf(c) >= 0) { out.push(cur); cur = ''; continue; }
      cur += c;
    }
    out.push(cur);
    return out;
  }

  function parseIntervals(input) {
    var raw = String(input).trim().replace(/^\s*(D_?f?|R\(f\)|[A-Za-z]\w*)\s*=/, '');
    // pull out removed points first (before braces are normalised): "\ {a,b}", "- {a}", "minus {..}"
    var removed = [];
    raw = raw.replace(/(?:\\setminus|\\|∖|-|minus|except|excluding|without)\s*\{([^{}]*)\}\s*$/i, function (m, inner) {
      splitTop(normalize(inner), [',', ';']).forEach(function (p) { if (p.trim()) removed.push(evalNum(p.trim())); });
      return '';
    });
    var s = normalize(raw);
    var ivs = [];
    if (/^(R|ℝ|reals?|all\s*reals?|\(-Infinity,\s*Infinity\))$/i.test(s)) {
      ivs.push({ lo: -Infinity, hi: Infinity, lc: false, hc: false });
    } else {
      var i = 0;
      while (i < s.length) {
        var c = s[i];
        if (c === '(' || c === '[') {
          var depth = 0, j = i, comma = -1;
          for (; j < s.length; j++) {
            var d = s[j];
            if (d === '(' || d === '[') depth++;
            else if (d === ')' || d === ']') { depth--; if (depth === 0) break; }
            else if (d === ',' && depth === 1 && comma < 0) comma = j;
          }
          if (j >= s.length || comma < 0) throw new Error('Unclosed interval');
          ivs.push({ lo: parseEndpoint(s.slice(i + 1, comma)), hi: parseEndpoint(s.slice(comma + 1, j)), lc: c === '[', hc: s[j] === ']' });
          i = j + 1;
        } else if (/^R\b|^ℝ/.test(s.slice(i)) && ivs.length === 0) {
          ivs.push({ lo: -Infinity, hi: Infinity, lc: false, hc: false });
          i++;
        } else {
          i++;
        }
      }
    }
    if (!ivs.length) throw new Error('No interval found');
    return canon(ivs, removed);
  }

  function canon(ivs, removed) {
    ivs = ivs.map(function (v) {
      return { lo: v.lo, hi: v.hi, lc: v.lc && isFinite(v.lo), hc: v.hc && isFinite(v.hi) };
    });
    (removed || []).forEach(function (p) {
      var next = [];
      ivs.forEach(function (v) {
        if (p > v.lo && p < v.hi) {
          next.push({ lo: v.lo, hi: p, lc: v.lc, hc: false });
          next.push({ lo: p, hi: v.hi, lc: false, hc: v.hc });
        } else {
          if (p === v.lo) v.lc = false;
          if (p === v.hi) v.hc = false;
          next.push(v);
        }
      });
      ivs = next;
    });
    ivs = ivs.filter(function (v) { return v.lo < v.hi || (v.lo === v.hi && v.lc && v.hc); });
    ivs.sort(function (a, b) { return a.lo - b.lo; });
    var out = [];
    ivs.forEach(function (v) {
      var last = out[out.length - 1];
      if (last && (v.lo < last.hi || (Math.abs(v.lo - last.hi) < 1e-12 && (last.hc || v.lc)))) {
        if (v.hi > last.hi) { last.hi = v.hi; last.hc = v.hc; }
        else if (v.hi === last.hi) last.hc = last.hc || v.hc;
      } else out.push(Object.assign({}, v));
    });
    return out;
  }

  function sameEnd(a, b) { return (!isFinite(a) || !isFinite(b)) ? a === b : close(a, b, { rel: 1e-6 }); }

  function checkInterval(input, part) {
    if (!String(input || '').trim()) return { ok: false, empty: true };
    var mine;
    try { mine = parseIntervals(input); } catch (e) { return { ok: false, error: 'Use interval notation, e.g. (-inf, 2) U [3, inf) or R \\ {1}.' }; }
    var ans = canon(part.answer.map(function (a) { return { lo: evalNum(a[0]), hi: evalNum(a[1]), lc: a[2], hc: a[3] }; }), []);
    if (mine.length !== ans.length) return { ok: false };
    for (var i = 0; i < ans.length; i++) {
      var m = mine[i], a = ans[i];
      if (!sameEnd(m.lo, a.lo) || !sameEnd(m.hi, a.hi)) return { ok: false };
      if (isFinite(a.lo) && m.lc !== a.lc) return { ok: false, hint: 'Check whether the endpoints are included.' };
      if (isFinite(a.hi) && m.hc !== a.hc) return { ok: false, hint: 'Check whether the endpoints are included.' };
    }
    return { ok: true };
  }

  /* ------------------------------------------------------------ finite sets */
  function parseSet(input) {
    var s = normalize(input).replace(/^[^=]*=\s*(?=[({])/, '');
    if (/^(∅|\(\s*\)|none|empty)$/i.test(s)) return [];
    s = s.replace(/^\(\s*/, '').replace(/\s*\)$/, '');
    var bits = splitTop(s, [',', ';']);
    var vals = [];
    bits.forEach(function (b) {
      b = b.replace(/\band\b/g, '').trim();
      if (!b) return;
      b = stripLhs(b);
      var v = evalNum(b);
      if (isNaN(v)) throw new Error('bad');
      vals.push(v);
    });
    return vals.sort(function (a, b) { return a - b; });
  }

  function checkSet(input, part) {
    if (!String(input || '').trim()) return { ok: false, empty: true };
    var mine;
    try { mine = parseSet(input); } catch (e) { return { ok: false, error: 'List the values separated by commas, e.g. {0, 1/7}.' }; }
    var ans = part.answer.map(function (a) { return evalNum(a); }).sort(function (a, b) { return a - b; });
    // remove duplicates the user may have typed
    mine = mine.filter(function (v, i) { return i === 0 || !close(v, mine[i - 1], { rel: 1e-9 }); });
    if (mine.length !== ans.length) return { ok: false, hint: ans.length > mine.length ? 'You are missing at least one value.' : 'You listed too many values.' };
    for (var i = 0; i < ans.length; i++) if (!close(mine[i], ans[i])) return { ok: false };
    return { ok: true };
  }

  /* ------------------------------------------------------------ dispatch */
  function checkPart(input, part) {
    try {
      switch (part.kind) {
        case 'number': return checkNumber(input, part);
        case 'expr': return checkExpr(input, part);
        case 'interval': return checkInterval(input, part);
        case 'set': return checkSet(input, part);
        case 'choice':
          if (input === '' || input == null) return { ok: false, empty: true };
          return { ok: Number(input) === part.answer };
      }
    } catch (e) {
      return { ok: false, error: 'Could not read your answer (' + e.message + ').' };
    }
    return { ok: false, error: 'Unknown answer type' };
  }

  /* ------------------------------------------------------------ preview */
  function texOf(expr) {
    return M.parse(expr).toTex({ parenthesis: 'keep', implicit: 'hide' });
  }

  function preview(input, kind) {
    var raw = String(input || '').trim();
    if (!raw) return '';
    try {
      if (kind === 'interval') {
        var ivs = parseIntervals(raw);
        return ivs.map(function (v) {
          var f = function (n) { return n === Infinity ? '\\infty' : n === -Infinity ? '-\\infty' : fmt(n); };
          return (v.lc ? '[' : '(') + f(v.lo) + ', ' + f(v.hi) + (v.hc ? ']' : ')');
        }).join(' \\cup ');
      }
      if (kind === 'set') {
        var s = normalize(raw).replace(/^[^=]*=\s*(?=[({])/, '').replace(/^\(\s*/, '').replace(/\s*\)$/, '');
        return '\\{' + splitTop(s, [',', ';']).filter(function (b) { return b.trim(); })
          .map(function (b) { return texOf(stripLhs(b.trim())); }).join(',\\ ') + '\\}';
      }
      var n = stripLhs(normalize(raw));
      return texOf(n);
    } catch (e) {
      return null;
    }
  }

  function fmt(n) {
    if (Math.abs(n - Math.round(n)) < 1e-12) return String(Math.round(n));
    var f = M.fraction(n);
    if (f && Math.abs(f.d) <= 1000 && Math.abs(Number(f.n) / Number(f.d) * (f.s || 1) - n) < 1e-12) return (n < 0 ? '-' : '') + '\\tfrac{' + Number(f.n) + '}{' + Number(f.d) + '}';
    return String(+n.toPrecision(6));
  }

  var MC = { normalize: normalize, checkPart: checkPart, preview: preview, parseIntervals: parseIntervals, parseSet: parseSet, evalNum: evalNum };
  root.MathCheck = MC;
  if (typeof module !== 'undefined' && module.exports) module.exports = MC;
})(typeof window !== 'undefined' ? window : globalThis);
