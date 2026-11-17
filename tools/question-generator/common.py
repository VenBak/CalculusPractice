"""Shared helpers for the question-bank generator."""
import random
import sympy as sp
from sympy import Rational as Q, S, oo, Interval, Union, FiniteSet
from sympy.printing.str import StrPrinter

x, y, t, u = sp.symbols('x y t u', real=True)


_OPN = {r'\operatorname{atan}': r'\arctan', r'\operatorname{asin}': r'\arcsin', r'\operatorname{acos}': r'\arccos'}


def L(e):
    """LaTeX for a sympy expression, using ln for natural log."""
    s = sp.latex(sp.sympify(e), ln_notation=True)
    for k, v in _OPN.items():
        s = s.replace(k, v)
    return s


def lin(p, var='x'):
    """'x - p' with correct sign handling."""
    return L(sp.Symbol(var) - p)


class Cycle:
    def __init__(self):
        self.i = {}

    def __call__(self, key, n):
        k = self.i.get(key, -1) + 1
        self.i[key] = k
        return k % n


class _JS(StrPrinter):
    def _print_Exp1(self, e):
        return 'e'

    def _print_Abs(self, e):
        return 'abs(%s)' % self._print(e.args[0])

    def _print_Infinity(self, e):
        return 'Infinity'

    def _print_NegativeInfinity(self, e):
        return '-Infinity'

    def _print_ImaginaryUnit(self, e):
        raise ValueError('complex value')


def js(e):
    """math.js-parsable string for a sympy expression."""
    return _JS().doprint(sp.sympify(e)).replace('**', '^')


def val(e):
    return float(sp.N(e))


# ---------------------------------------------------------------- parts

def P_num(label, value, tol=None, approx=False):
    value = sp.sympify(value)
    d = {'kind': 'number', 'label': label, 'answer': js(value), 'latex': L(value)}
    if approx and not value.is_Rational:
        d['latex'] = L(value) + r' \approx ' + ('%.4f' % val(value))
    if tol:
        d['tol'] = tol
    return d


def P_prob(label, value):
    """Probability answers: exact value stored, decimals within 0.0005 accepted."""
    value = sp.nsimplify(value) if not isinstance(value, sp.Basic) else value
    d = P_num(label, value, tol={'abs': 5e-4})
    if not value.is_Integer:
        d['latex'] = L(value) + r' \approx ' + ('%.4f' % val(value))
    return d


def P_approx(label, value, digits=4):
    """Numeric answers that only make sense as decimals (e.g. binomial tails)."""
    v = val(value)
    return {'kind': 'number', 'label': label, 'answer': repr(round(v, 10)),
            'latex': r'\approx %.*f' % (digits, v), 'tol': {'abs': 5e-4}}


def P_expr(label, e, vars=('x',), sample=None, upc=False):
    e = sp.sympify(e)
    sample = sample or {v: [-2, 2] for v in vars}
    d = {'kind': 'expr', 'label': label, 'answer': js(e), 'latex': L(e),
         'vars': list(vars), 'sample': {k: [float(a), float(b)] for k, (a, b) in sample.items()}}
    if upc:
        d['upToConstant'] = True
        d['latex'] = L(e) + ' + C'
    return d


def set_to_intervals(s):
    if s == S.Reals:
        return [(-oo, oo, False, False)]
    if isinstance(s, Interval):
        return [(s.start, s.end, (not s.left_open) and s.start != -oo, (not s.right_open) and s.end != oo)]
    if isinstance(s, Union):
        out = []
        for a in s.args:
            out += set_to_intervals(a)
        return sorted(out, key=lambda r: val(r[0]) if r[0] != -oo else -1e300)
    raise ValueError('unsupported set %r' % (s,))


def interval_latex(ivs):
    parts = []
    for lo, hi, lc, hc in ivs:
        parts.append('%s%s, %s%s' % ('[' if lc else '(', L(lo), L(hi), ']' if hc else ')'))
    return r' \cup '.join(parts)


def P_int(label, s):
    ivs = set_to_intervals(s)
    return {'kind': 'interval', 'label': label,
            'answer': [[js(a), js(b), lc, hc] for a, b, lc, hc in ivs],
            'latex': interval_latex(ivs)}


def set_latex(vals):
    vals = sorted(vals, key=val)
    return r'\{' + ', '.join(L(v) for v in vals) + r'\}'


def P_set(label, vals):
    vals = sorted([sp.sympify(v) for v in vals], key=val)
    return {'kind': 'set', 'label': label, 'answer': [js(v) for v in vals],
            'latex': set_latex(vals)}


def P_choice(label, options, correct):
    return {'kind': 'choice', 'label': label, 'options': options, 'answer': correct,
            'latex': options[correct]}


# ---------------------------------------------------------------- distractors

def num_distractors(v, extra=()):
    v = sp.nsimplify(sp.sympify(v))
    cands = list(extra) + [-v, 2 * v, v / 2, v + 1, v - 1, v + Q(1, 2), 3 * v, v ** 2]
    if v != 0:
        cands.append(1 / v)
    out, seen = [], {round(val(v), 9)}
    for c in cands:
        try:
            c = sp.nsimplify(sp.sympify(c))
            k = round(val(c), 9)
        except Exception:
            continue
        if k in seen:
            continue
        seen.add(k)
        out.append(L(c))
    return out


def iv_distractors(s, extra=()):
    """Mutations of an interval answer."""
    ivs = set_to_intervals(s)
    out = []
    for e in extra:
        out.append(e if isinstance(e, str) else interval_latex(set_to_intervals(e)))
    # flip closedness of each finite endpoint
    for i, (lo, hi, lc, hc) in enumerate(ivs):
        if lo != -oo:
            m = list(ivs); m[i] = (lo, hi, not lc, hc); out.append(interval_latex(m))
        if hi != oo:
            m = list(ivs); m[i] = (lo, hi, lc, not hc); out.append(interval_latex(m))
    if len(ivs) > 1:
        out.append(interval_latex([(ivs[0][0], ivs[-1][1], ivs[0][2], ivs[-1][3])]))
    return out


def mcq(correct_latex, distractors, max_opts=6):
    opts, seen = [correct_latex], {correct_latex}
    for d in distractors:
        if d not in seen:
            seen.add(d)
            opts.append(d)
        if len(opts) >= max_opts:
            break
    if len(opts) < 4:
        return None
    return {'options': opts, 'correct': 0}


# ---------------------------------------------------------------- bank

class Bank:
    def __init__(self, topic, seed):
        self.topic = topic
        self.items = []
        self.seen = set()
        self.rng = random.Random(seed)

    def add(self, prompt, parts, solution, points=4, mcq_=None, diff=2):
        if prompt in self.seen:
            return False
        self.seen.add(prompt)
        q = {'id': '%s-%03d' % (self.topic, len(self.items) + 1), 'topic': self.topic,
             'prompt': prompt, 'parts': parts, 'solution': solution,
             'points': points, 'difficulty': diff}
        if mcq_:
            q['mcq'] = mcq_
        elif len(parts) == 1 and parts[0]['kind'] == 'choice':
            q['mcq'] = {'options': parts[0]['options'], 'correct': parts[0]['answer'], 'native': True}
        self.items.append(q)
        return True

    def fill(self, fn, n, tries=400):
        """Call fn() (which calls self.add) until n new items were added from it."""
        start = len(self.items)
        for _ in range(tries):
            if len(self.items) - start >= n:
                break
            try:
                fn()
            except (ValueError, ZeroDivisionError, sp.PolynomialError):
                continue
        return len(self.items) - start


def d(expr_latex):
    """Display-math helper."""
    return '$$' + expr_latex + '$$'


def m(expr_latex):
    return '$' + expr_latex + '$'
