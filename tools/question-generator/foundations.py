"""Foundations: domain & range, inverse, parity, limits, asymptotes, continuity."""
from common import *
from sympy import sqrt, exp, log, sin, cos, tan, atan, pi, E, Abs

dfrac = lambda a, b: r'\dfrac{%s}{%s}' % (a, b)


# =====================================================================
def domain_range(B):
    r = B.rng

    def sqrt_over_quad():
        a = r.randint(-3, 5)
        p, q = sorted(r.sample(range(-5, 7), 2))
        sgn = r.choice([1, -1])
        rad = (a - x) if sgn == 1 else (x - a)
        den = sp.expand((x - p) * (x - q))
        base = Interval(-oo, a) if sgn == 1 else Interval(a, oo)
        dom = base - FiniteSet(p, q)
        f = dfrac(r'\sqrt{%s}' % L(rad), L(den))
        inside = [v for v in (p, q) if v in base]
        ineq = r'x \le %d' % a if sgn == 1 else r'x \ge %d' % a
        steps = [
            r'The square root needs a non-negative argument: $%s \ge 0 \iff %s$.' % (L(rad), ineq),
            r'The denominator factors as $%s = (x %s)(x %s)$, so we need $x \neq %d$ and $x \neq %d$.'
            % (L(den), '-' if p >= 0 else '+', abs(p) if p else '', p, q) if p != 0 else
            r'The denominator factors as $%s = %s$, so we need $x \neq %d$ and $x \neq %d$.' % (L(den), L(sp.factor(den)), p, q),
        ]
        if p != 0:
            steps[1] = r'The denominator factors as $%s = %s$, so we need $x \neq %d$ and $x \neq %d$.' % (L(den), L(sp.factor(den)), p, q)
        if len(inside) == 2:
            steps.append(r'Both excluded points lie in $%s$, so both are removed.' % L(base).replace(r'\left', '').replace(r'\right', ''))
        elif len(inside) == 1:
            steps.append(r'Only $x = %d$ lies in the set where the root is defined, so only that point is removed.' % inside[0])
        else:
            steps.append(r'Neither $%d$ nor $%d$ satisfies $%s$, so nothing extra is removed.' % (p, q, ineq))
        P = P_int('$D_f =$', dom)
        steps.append(r'Hence $D_f = %s$.' % P['latex'])
        dis = iv_distractors(dom, [base, r'\mathbb{R} \setminus \{%d, %d\}' % (p, q),
                                   (Interval(a, oo) if sgn == 1 else Interval(-oo, a)) - FiniteSet(p, q)])
        B.add(r'Determine the domain $D_f$ of $f(x) = %s$.' % f, [P], steps, 4, mcq(P['latex'], dis))

    def log_quad():
        p, q = sorted(r.sample(range(-5, 7), 2))
        kind = r.choice(['out', 'in', 'frac_sqrt', 'frac_sqrt2'])
        fac = (x - p) * (x - q)
        if kind == 'out':
            g = sp.expand(fac); f = r'\ln\left(%s\right)' % L(g)
            dom = Union(Interval.open(-oo, p), Interval.open(q, oo))
            st = [r'The logarithm needs a strictly positive argument: $%s > 0$.' % L(g),
                  r'Factor: $%s = %s$, with zeros $x = %d$ and $x = %d$.' % (L(g), L(sp.factor(g)), p, q),
                  r'An upward parabola is positive outside its zeros: $x < %d$ or $x > %d$.' % (p, q)]
            alt = [Interval.open(p, q), Union(Interval(-oo, p), Interval(q, oo))]
        elif kind == 'in':
            g = sp.expand(-fac); f = r'\ln\left(%s\right)' % L(g)
            dom = Interval.open(p, q)
            st = [r'The logarithm needs a strictly positive argument: $%s > 0$.' % L(g),
                  r'Factor: $%s = -(%s)(%s)$, zeros at $x=%d$ and $x=%d$.' % (L(g), lin(p), lin(q), p, q),
                  r'A downward parabola is positive strictly between its zeros: $%d < x < %d$.' % (p, q)]
            alt = [Interval(p, q), Union(Interval.open(-oo, p), Interval.open(q, oo))]
        elif kind == 'frac_sqrt':
            f = r'\sqrt{\dfrac{%s}{%s}}' % (L(x - p), L(x - q))
            dom = Union(Interval(-oo, p), Interval.open(q, oo))
            st = [r'We need $\dfrac{%s}{%s} \ge 0$ and $x \neq %d$ (denominator).' % (L(x - p), L(x - q), q),
                  r'Sign chart with critical points $%d$ (numerator zero) and $%d$ (denominator zero): the quotient is $\ge 0$ for $x \le %d$ and for $x > %d$.' % (p, q, p, q),
                  r'$x = %d$ is allowed (value $0$), $x = %d$ is not (division by zero).' % (p, q)]
            alt = [Union(Interval(-oo, p), Interval(q, oo)), Interval.open(p, q), Union(Interval.open(-oo, p), Interval.open(q, oo))]
        else:
            f = r'\sqrt{\dfrac{%s}{%s}}' % (L(x - q), L(x - p))
            dom = Union(Interval.open(-oo, p), Interval(q, oo))
            st = [r'We need $\dfrac{%s}{%s} \ge 0$ and $x \neq %d$ (denominator).' % (L(x - q), L(x - p), p),
                  r'Sign chart with critical points $%d$ (denominator zero) and $%d$ (numerator zero): the quotient is $\ge 0$ for $x < %d$ and for $x \ge %d$.' % (p, q, p, q),
                  r'$x = %d$ is allowed (value $0$), $x = %d$ is not.' % (q, p)]
            alt = [Union(Interval(-oo, p), Interval(q, oo)), Interval.Lopen(p, q), Union(Interval.open(-oo, p), Interval.open(q, oo))]
        P = P_int('$D_f =$', dom)
        st.append(r'Hence $D_f = %s$.' % P['latex'])
        B.add(r'Determine the domain $D_f$ of $f(x) = %s$.' % f, [P], st, 4, mcq(P['latex'], iv_distractors(dom, alt)))

    def log_log():
        k = r.choice([1, 2, 3, Q(1, 2), Q(1, 3)])
        mm = r.choice([1, 2, 3, E, E ** 2, Q(1, 2)])
        ub = sp.simplify(exp(1 / sp.sympify(k)) / mm)
        inner = L(mm * x) if mm != 1 else 'x'
        f = r'\ln\left(1 - %s\ln(%s)\right)' % (L(k) if k != 1 else '', inner)
        dom = Interval.open(0, ub)
        P = P_int('$D_f =$', dom)
        st = [r'Inner logarithm: $%s > 0 \iff x > 0$.' % inner,
              r'Outer logarithm: $1 - %s\ln(%s) > 0 \iff \ln(%s) < %s$.' % (L(k) if k != 1 else '', inner, inner, L(1 / sp.sympify(k))),
              r'Since $e^{(\cdot)}$ is increasing: $%s < e^{%s} \iff x < %s$.' % (inner, L(1 / sp.sympify(k)), L(ub)),
              r'Combining both conditions: $D_f = %s$.' % P['latex']]
        cands = [exp(sp.sympify(k)) / mm, mm * exp(1 / sp.sympify(k)), exp(-1 / sp.sympify(k)) / mm,
                 exp(1 / sp.sympify(k)), 1 / (sp.sympify(k) * mm), exp(1 / sp.sympify(k)) / (2 * mm)]
        dis = []
        for c in cands:
            c = sp.simplify(c)
            if sp.simplify(c - ub) != 0:
                dis.append(interval_latex([(0, c, False, False)]))
        dis.append(interval_latex([(0, ub, False, True)]))
        B.add(r'Determine the domain $D_f$ of $f(x) = %s$.' % f, [P], st, 3, mcq(P['latex'], dis))

    def root_forms():
        k = r.randint(1, 6)
        form = r.randrange(4)
        if form == 0:
            f = r'\dfrac{\sqrt{%d - x^2}}{x}' % (k * k); dom = Union(Interval.Ropen(-k, 0), Interval.Lopen(0, k))
            st = [r'Root: $%d - x^2 \ge 0 \iff -%d \le x \le %d$.' % (k * k, k, k), r'Denominator: $x \neq 0$.']
        elif form == 1:
            f = r'\dfrac{1}{\sqrt{x^2 - %d}}' % (k * k); dom = Union(Interval.open(-oo, -k), Interval.open(k, oo))
            st = [r'Root in the denominator must be strictly positive: $x^2 - %d > 0 \iff |x| > %d$.' % (k * k, k)]
        elif form == 2:
            f = r'\ln(%d - x^2)' % (k * k); dom = Interval.open(-k, k)
            st = [r'Logarithm: $%d - x^2 > 0 \iff x^2 < %d \iff -%d < x < %d$.' % (k * k, k * k, k, k)]
        else:
            f = r'\sqrt{x^2 - %d}' % (k * k); dom = Union(Interval(-oo, -k), Interval(k, oo))
            st = [r'Root: $x^2 - %d \ge 0 \iff |x| \ge %d$.' % (k * k, k)]
        P = P_int('$D_f =$', dom)
        st.append(r'Hence $D_f = %s$.' % P['latex'])
        B.add(r'Determine the domain $D_f$ of $f(x) = %s$.' % f, [P], st, 3, mcq(P['latex'], iv_distractors(dom, [Interval(-k, k), S.Reals])))

    cyc = Cycle()

    def ranges():
        form = cyc('r', 10)
        if form == 0:
            a = r.choice([1, 2, 3, -1, -2]); h = r.randint(-4, 4); k = r.randint(-5, 5)
            f = sp.expand(a * (x - h) ** 2 + k)
            rng = Interval(k, oo) if a > 0 else Interval(-oo, k)
            st = [r'Complete the square: $f(x) = %s$.' % L(a * sp.UnevaluatedExpr(x - h) ** 2 + k),
                  r'$(x %s)^2$ takes every value in $[0,\infty)$, so $%s(x-%d)^2$ takes every value in $%s$.' % (('-' if h >= 0 else '+') + str(abs(h)), L(a), h, '[0,\\infty)' if a > 0 else '(-\\infty,0]'),
                  r'Adding $%d$ shifts this to $%s$.' % (k, interval_latex(set_to_intervals(rng)))]
            fl = L(f)
        elif form == 1:
            c = r.randint(-4, 4); b = r.choice([1, 2, 3, -1, -2, -3]); s = r.choice([1, -1, 2])
            fl = L(c + b * exp(s * x)); rng = Interval.open(c, oo) if b > 0 else Interval.open(-oo, c)
            st = [r'$e^{%s}$ takes every value in $(0,\infty)$ (never $0$).' % L(s * x),
                  r'Multiplying by $%d$ gives $%s$, and adding $%d$ gives $%s$.' % (b, '(0,\\infty)' if b > 0 else '(-\\infty,0)', c, interval_latex(set_to_intervals(rng)))]
        elif form == 2:
            rr = r.randint(1, 5); c = r.randint(-3, 4)
            fl = r'%s\sqrt{%d - x^2}' % ((str(c) + ' + ') if c else '', rr * rr); rng = Interval(c, c + rr)
            st = [r'On the domain $[-%d,%d]$, $%d - x^2$ takes all values in $[0, %d]$.' % (rr, rr, rr * rr, rr * rr),
                  r'So $\sqrt{%d - x^2} \in [0, %d]$ (minimum at $x=\pm%d$, maximum at $x=0$).' % (rr * rr, rr, rr),
                  r'Adding $%d$: range $[%d, %d]$.' % (c, c, c + rr)]
        elif form == 3:
            a = r.randint(1, 9); b = r.randint(1, 5)
            fl = dfrac(a, L(x ** 2 + b)); rng = Interval.Lopen(0, Q(a, b))
            st = [r'$x^2 + %d$ takes every value in $[%d, \infty)$.' % (b, b),
                  r'The reciprocal map $s \mapsto %d/s$ is decreasing on $[%d,\infty)$: largest value $%s$ at $s=%d$, tending to $0$ (never reached) as $s\to\infty$.' % (a, b, L(Q(a, b)), b),
                  r'Range: $%s$.' % interval_latex(set_to_intervals(rng))]
        elif form == 4:
            c = r.randint(-3, 4); b = r.choice([1, 2, 3, -2, -3]); w = r.choice([1, 2, 3])
            fl = L(c + b * sin(w * x)); rng = Interval(c - abs(b), c + abs(b))
            st = [r'$\sin(%s)$ takes every value in $[-1,1]$.' % L(w * x),
                  r'So $%s\sin(%s) \in [%d, %d]$ and adding $%d$ gives $[%d, %d]$.' % (L(b), L(w * x), -abs(b), abs(b), c, c - abs(b), c + abs(b))]
        elif form == 5:
            k = r.randint(1, 9)
            fl = r'\ln(x^2 + %d)' % k; rng = Interval(log(k), oo)
            st = [r'$x^2 + %d$ takes every value in $[%d,\infty)$.' % (k, k),
                  r'$\ln$ is increasing and unbounded, so the range is $[\ln %d, \infty)%s$.' % (k, ' = [0,\\infty)' if k == 1 else '')]
        elif form == 6:
            a, b, c, dd = [r.choice([1, 2, 3, -1, -2, 4]) for _ in range(4)]
            if a * dd - b * c == 0:
                raise ValueError
            fl = dfrac(L(a * x + b), L(c * x + dd)); h = Q(a, c)
            rng = Union(Interval.open(-oo, h), Interval.open(h, oo))
            st = [r'Solve $y = %s$ for $x$: $x = %s$.' % (fl, L((b - dd * y) / (c * y - a))),
                  r'This is possible for every $y$ except $y = %s$ (division by zero); equivalently $y = %s$ is the horizontal asymptote.' % (L(h), L(h)),
                  r'Range: $\mathbb{R}\setminus\{%s\}$.' % L(h)]
        elif form == 7:
            a = r.randint(1, 6); c = r.randint(-3, 3)
            fl = L(a * exp(-x ** 2) + c); rng = Interval.Lopen(c, a + c)
            st = [r'$-x^2 \in (-\infty, 0]$, so $e^{-x^2} \in (0, 1]$ (maximum $1$ at $x=0$, tends to $0$).',
                  r'Hence $%d e^{-x^2} + %d \in (%d, %d]$.' % (a, c, c, a + c)]
        elif form == 8:
            h = r.randint(-4, 4); k = r.randint(-4, 5)
            fl = L(sqrt(x - h) + k); rng = Interval(k, oo)
            st = [r'Domain $x \ge %d$; there $\sqrt{x %s}$ takes every value in $[0,\infty)$.' % (h, ('-' if h >= 0 else '+') + str(abs(h))),
                  r'Adding $%d$: range $[%d,\infty)$.' % (k, k)]
        else:
            a = r.randint(1, 4); c = r.randint(-3, 3)
            fl = L(c + a * atan(x)); rng = Interval.open(c - a * pi / 2, c + a * pi / 2)
            st = [r'$\arctan(x)$ takes every value in $(-\frac{\pi}{2}, \frac{\pi}{2})$ (horizontal asymptotes, never reached).',
                  r'Hence the range is $%s$.' % interval_latex(set_to_intervals(rng))]
        P = P_int('$R(f) =$', rng)
        st.append(r'So $R(f) = %s$.' % P['latex'])
        B.add(r'Determine the range $R(f)$ of $f(x) = %s$ (on its largest possible domain).' % fl, [P], st, 3,
              mcq(P['latex'], iv_distractors(rng, [S.Reals])))

    B.fill(sqrt_over_quad, 8); B.fill(log_quad, 7); B.fill(log_log, 6); B.fill(root_forms, 5); B.fill(ranges, 12)


# =====================================================================
def inverse(B):
    r = B.rng

    def mobius():
        a, b, c, dd = [r.choice([1, 2, 3, -1, -2, 4, 5]) for _ in range(4)]
        if a * dd - b * c == 0:
            raise ValueError
        f = (a * x + b) / (c * x + dd)
        inv = (b - dd * x) / (c * x - a)
        s0 = Q(a, c)
        P = P_expr('$f^{-1}(x) =$', inv, sample={'x': [float(s0) + 0.4, float(s0) + 4]})
        st = [r'Write $y = %s$ and solve for $x$.' % L(f),
              r'Cross-multiply: $y(%s) = %s$.' % (L(c * x + dd), L(a * x + b)),
              r'Collect the $x$-terms: $x(%s) = %s$.' % (L(c * y - a), L(b - dd * y)),
              r'So $x = %s$. Swapping the names of $x$ and $y$: $f^{-1}(x) = %s$.' % (L((b - dd * y) / (c * y - a)), L(inv))]
        dis = [L((b + dd * x) / (c * x - a)), L((c * x + dd) / (a * x + b)), L((b - a * x) / (c * x - dd)), L((dd * x + b) / (a - c * x))]
        B.add(r'The function $f(x) = %s$ is injective on its domain. Determine $f^{-1}(x)$.' % L(f), [P], st, 4, mcq(P['latex'], dis))

    def expo():
        a = r.randint(-3, 4); b = r.choice([1, 2, 3, 5]); c = r.choice([1, 2, 3, -1, Q(1, 2)])
        f = a + b * exp(c * x)
        inv = log((x - a) / b) / c
        P = P_expr('$f^{-1}(x) =$', inv, sample={'x': [a + 0.3, a + 6]})
        st = [r'Set $y = %s$, so $%s = %s$.' % (L(f), L(b * exp(c * x)), L(y - a)),
              r'%s take $\ln$: $%s = \ln\left(%s\right)$.' % (('Divide by $%d$ and' % b) if b != 1 else 'Now', L(c * x), L((y - a) / b)),
              r'So $x = %s$; renaming gives $f^{-1}(x) = %s$, defined for $x > %d$ (the range of $f$).' % (L(log((y - a) / b) / c), L(inv), a)]
        dis = [L(log((x + a) / b) / c), L(log(x - a) / (b * c)), L(c * log((x - a) / b)), L(exp((x - a) / b) / c)]
        B.add(r'Determine the inverse of $f(x) = %s$.' % L(f), [P], st, 4, mcq(P['latex'], dis))

    def logf():
        a = r.choice([1, 2, 3, 4]); b = r.randint(-3, 3); c = r.randint(-3, 3)
        f = log(a * x + b) + c
        inv = (exp(x - c) - b) / a
        P = P_expr('$f^{-1}(x) =$', inv, sample={'x': [-2, 2]})
        st = [r'Set $y = %s$, so $\ln(%s) = %s$.' % (L(f), L(a * x + b), L(y - c)),
              r'Exponentiate: $%s = e^{%s}$.' % (L(a * x + b), L(y - c)),
              r'So $x = %s$, i.e. $f^{-1}(x) = %s$.' % (L((exp(y - c) - b) / a), L(inv))]
        dis = [L((exp(x + c) - b) / a), L(exp(x - c) / a - b), L((exp(x) - b - c) / a), L((log(x - c) - b) / a)]
        B.add(r'Determine the inverse of $f(x) = %s$.' % L(f), [P], st, 4, mcq(P['latex'], dis))

    def cubic():
        a = r.randint(-3, 3); b = r.randint(-4, 4); k = r.choice([1, 2, 8])
        f = k * (x - a) ** 3 + b
        inv = ((x - b) / k) ** Q(1, 3) + a
        P = P_expr('$f^{-1}(x) =$', inv, sample={'x': [b + 0.2, b + 9]})
        st = [r'Set $y = %s$: $(x - %d)^3 = %s$.' % (L(f), a, L((y - b) / k)),
              r'Take the (real) cube root: $x = %s$.' % L(((y - b) / k) ** Q(1, 3) + a),
              r'So $f^{-1}(x) = %s$ (enter a cube root as cbrt(...) or (...)^(1/3)).' % L(inv)]
        B.add(r'Determine the inverse of the bijection $f(x) = %s$.' % L(f), [P], st, 4)

    def deriv_inv():
        form = r.randrange(3)
        if form == 0:
            a = r.randint(1, 5); b = r.randint(-4, 4); c = r.choice([-2, -1, 1, 2])
            f = x ** 3 + a * x + b
        elif form == 1:
            a = r.randint(1, 4); b = r.randint(-3, 3); c = r.choice([-1, 1])
            f = x ** 5 + a * x + b
        else:
            a = r.randint(1, 6); b = 0; c = 1
            f = a * x + log(x)
        y0 = f.subs(x, c); fp = sp.diff(f, x); slope = fp.subs(x, c)
        ans = 1 / slope
        P = P_num(r"$(f^{-1})'(%s) =$" % L(y0), ans)
        st = [r"$f'(x) = %s > 0$ on the domain, so $f$ is strictly increasing and has an inverse." % L(fp),
              r'Since $f(%d) = %s$, we have $f^{-1}(%s) = %d$.' % (c, L(y0), L(y0), c),
              r"By the inverse-function rule: $(f^{-1})'(%s) = \dfrac{1}{f'(f^{-1}(%s))} = \dfrac{1}{f'(%d)} = \dfrac{1}{%s} = %s$." % (L(y0), L(y0), c, L(slope), L(ans))]
        dis = num_distractors(ans, [slope, 1 / fp.subs(x, y0) if fp.subs(x, y0) != 0 else 7, -ans])
        B.add(r'Let $f(x) = %s$. Compute $(f^{-1})^{\prime}(%s)$.' % (L(f), L(y0)), [P], st, 4, mcq(P['latex'], dis))

    def root_inv():
        a = r.choice([1, 2, 3]); b = r.randint(-4, 6); c = r.randint(-3, 4)
        f = sqrt(a * x - b) + c
        inv = ((x - c) ** 2 + b) / a
        P1 = P_expr('$f^{-1}(x) =$', inv, sample={'x': [c + 0.1, c + 5]})
        P2 = P_int('Domain of $f^{-1}$:', Interval(c, oo))
        st = [r'The range of $f$ is $[%d, \infty)$ since the square root takes all values $\ge 0$; this is the domain of $f^{-1}$.' % c,
              r'Solve $y = %s$: $\sqrt{%s} = %s \Rightarrow %s = (%s)^2$.' % (L(f), L(a * x - b), L(y - c), L(a * x - b), L(y - c)),
              r'So $x = %s$ and $f^{-1}(x) = %s$ for $x \ge %d$.' % (L(((y - c) ** 2 + b) / a), L(inv), c)]
        B.add(r'Let $f(x) = %s$ on $[%s, \infty)$. Determine $f^{-1}(x)$ and the domain of $f^{-1}$.' % (L(f), L(Q(b, a))), [P1, P2], st, 5)

    B.fill(mobius, 8); B.fill(expo, 5); B.fill(logf, 4); B.fill(cubic, 4); B.fill(deriv_inv, 7); B.fill(root_inv, 4)


# =====================================================================
PAR_OPTS = ['even', 'odd', 'neither even nor odd', 'both even and odd']


def parity(f):
    fn = sp.lambdify(x, f, 'math')
    pts = [0.37, 0.81, 1.3, 1.9, 2.6]
    ev = all(abs(fn(-p) - fn(p)) < 1e-9 for p in pts)
    od = all(abs(fn(-p) + fn(p)) < 1e-9 for p in pts)
    return 'both' if ev and od else 'even' if ev else 'odd' if od else 'neither'


def even_odd(B):
    r = B.rng
    EVEN = [x ** 2, x ** 4, cos(x), Abs(x), exp(-x ** 2), 1 / (1 + x ** 2), cos(2 * x), x ** 2 + 1, log(1 + x ** 2)]
    ODD = [x, x ** 3, sin(x), atan(x), x ** 5, sin(2 * x), x ** 3 - x]
    NEI = [exp(x), x + 1, (x - 1) ** 2, exp(x) + x, x ** 2 + x]

    def classify():
        form = r.randrange(5)
        if form == 0:
            f = r.choice(EVEN + ODD) * r.choice(EVEN + ODD)
        elif form == 1:
            f = r.choice(EVEN) + r.choice(ODD)
        elif form == 2:
            g = r.choice([sin, cos, exp, atan]); h = r.choice(EVEN + ODD)
            f = g(h)
        elif form == 3:
            f = r.choice(NEI) * r.choice(EVEN)
        else:
            f = r.choice(ODD) / r.choice([1 + x ** 2, 2 + cos(x), exp(x ** 2)])
        if f.has(sp.zoo) or f == 0:
            raise ValueError
        p = parity(f)
        if p == 'both':
            raise ValueError
        idx = {'even': 0, 'odd': 1, 'neither': 2}[p]
        fm = f.subs(x, -x)
        st = [r'Compute $f(-x) = %s$.' % L(fm)]
        if p == 'even':
            st.append(r'This equals $f(x)$ for every $x$ in the (symmetric) domain, so $f$ is **even**.')
        elif p == 'odd':
            st.append(r'This equals $-f(x)$ for every $x$ in the (symmetric) domain, so $f$ is **odd**.')
        else:
            f1, fm1 = sp.simplify(f.subs(x, 1)), sp.simplify(f.subs(x, -1))
            st.append(r'Counterexample: $f(1) = %s$ while $f(-1) = %s$, which is neither $f(1)$ nor $-f(1)$. So $f$ is **neither** even nor odd.' % (L(f1), L(fm1)))
        st.append(r'Useful rules: even·even and odd·odd are even, even·odd is odd; a composition with an even inner function is even.')
        P = P_choice('Parity of $f$:', PAR_OPTS, idx)
        B.add(r'Is $f(x) = %s$ even, odd, or neither?' % L(f), [P], st, 3)

    ODD_N = [sin(x), x ** 3, atan(x), x ** 5, x ** 3 + x]
    EVEN_N = [Abs(x), cos(x), x ** 2, exp(-x ** 2), x ** 4 + 1]
    NEI_N = [exp(x), x + 1, x ** 2 + x]

    def composition():
        fx = r.choice(ODD_N); gx = r.choice(EVEN_N); hx = r.choice(ODD_N + NEI_N)
        if hx == fx:
            raise ValueError
        F = {'f': fx, 'g': gx, 'h': hx}
        comp = lambda a, b: a.subs(x, b)
        cands = {
            'g': gx, 'f': fx, 'h': hx,
            r'g \circ h': comp(gx, hx), r'f \circ g': comp(fx, gx), r'f \circ h': comp(fx, hx),
            r'h \circ f': comp(hx, fx), r'f \circ g \circ h': comp(fx, comp(gx, hx)),
            r'h \circ g': comp(hx, gx), r'g \circ f': comp(gx, fx), r'f \cdot g': fx * gx,
            r'f \cdot h': fx * hx, r'h \circ h': comp(hx, hx),
        }
        target = r.choice(['odd', 'even'])
        par = {k: parity(v) for k, v in cands.items()}
        good = [k for k in cands if par[k] == target]
        bad = [k for k in cands if par[k] not in (target, 'both')]
        if not good or len(bad) < 4:
            raise ValueError
        c = r.choice(good); wrong = r.sample(bad, 4)
        opts = [c] + wrong
        r.shuffle(opts)
        st = []
        for o in opts:
            st.append(r'$%s$: $%s$ is %s.' % (o, L(cands[o]), {'even': 'even', 'odd': 'odd', 'neither': 'neither even nor odd'}[par[o]]))
        st.append(r'So the %s function is $%s$.' % (target, c))
        P = P_choice('Which function is %s?' % target, ['$%s$' % o for o in opts], opts.index(c))
        B.add(r'Consider $f(x) = %s$, $g(x) = %s$ and $h(x) = %s$. Which of the following functions is %s (in terms of parity)?'
              % (L(fx), L(gx), L(hx), target), [P], st, 3)

    def rules():
        pf, pg = r.choice([('odd', 'even'), ('odd', 'odd'), ('even', 'odd'), ('even', 'even')])
        P_ = {'f': pf, 'g': pg}
        exprs = [('f∘g', 'comp', 'f', 'g'), ('g∘f', 'comp', 'g', 'f'), ('f∘f', 'comp', 'f', 'f'), ('g∘g', 'comp', 'g', 'g'),
                 ('f·g', 'prod', 'f', 'g'), ('f·f', 'prod', 'f', 'f'), ('g·g', 'prod', 'g', 'g')]
        e1, e2 = r.sample(exprs, 2)

        def par_of(e):
            _, kind, a, b = e
            if kind == 'comp':
                return 'even' if P_[b] == 'even' else P_[a]
            return 'even' if P_[a] == P_[b] else 'odd'

        def why(e):
            name, kind, a, b = e
            nm = name.replace('∘', r' \circ ').replace('·', r' \cdot ')
            if kind == 'comp':
                if P_[b] == 'even':
                    return r'$(%s)(-x) = %s(%s(-x)) = %s(%s(x))$, so $%s$ is even.' % (nm, a, b, a, b, nm)
                if P_[a] == 'odd':
                    return r'$(%s)(-x) = %s(%s(-x)) = %s(-%s(x)) = -%s(%s(x))$, so $%s$ is odd.' % (nm, a, b, a, b, a, b, nm)
                return r'$(%s)(-x) = %s(%s(-x)) = %s(-%s(x)) = %s(%s(x))$, so $%s$ is even.' % (nm, a, b, a, b, a, b, nm)
            sa = '' if P_[a] == 'even' else '-'; sb = '' if P_[b] == 'even' else '-'
            res = par_of(e)
            return r'$(%s)(-x) = %s(-x)\,%s(-x) = (%s%s(x))(%s%s(x))$, so $%s$ is %s.' % (nm, a, b, sa, a, sb, b, nm, res)

        p1, p2 = par_of(e1), par_of(e2)
        n1 = e1[0].replace('∘', r' \circ ').replace('·', r' \cdot '); n2 = e2[0].replace('∘', r' \circ ').replace('·', r' \cdot ')
        combos = [('even', 'even'), ('odd', 'even'), ('even', 'odd'), ('odd', 'odd')]
        opts = [r'$(%s)(x)$ is %s, and $(%s)(x)$ is %s.' % (n1, a, n2, b) for a, b in combos]
        P = P_choice('Choose:', opts, combos.index((p1, p2)))
        B.add(r'Let $f(x)$ be an %s function and $g(x)$ be an %s function (defined on all of $\mathbb{R}$). Then which statement is true?' % (pf, pg),
              [P], [why(e1), why(e2)], 3)

    B.fill(classify, 18); B.fill(composition, 7); B.fill(rules, 8)


# =====================================================================
def limits(B):
    r = B.rng

    def rat_inf():
        form = r.randrange(3)
        if form == 0:
            a, dd = r.choice([1, 2, 3, 4, 5, -2]), r.choice([1, 2, 3, 4, -1])
            num = a * x ** 2 + r.randint(-5, 5) * x + r.randint(-5, 5)
            den = dd * x ** 2 + r.randint(-5, 5) * x + r.randint(1, 6)
            ans = Q(a, dd)
            fl = dfrac(L(num), L(den))
            st = [r'Divide numerator and denominator by the highest power $x^2$.',
                  r'All terms with $1/x$ or $1/x^2$ tend to $0$, leaving $\dfrac{%d}{%d} = %s$.' % (a, dd, L(ans))]
        elif form == 1:
            a = r.choice([1, 2, 3, 4]); b = r.choice([1, 2, 3, 4])
            num = sqrt(a * a * x ** 4 + r.randint(1, 5)); den = b * x ** 2 + r.randint(-4, 4) * x + r.randint(1, 6)
            ans = Q(a, b)
            fl = dfrac(r'\sqrt{%s}' % L(a * a * x ** 4 + (num.args[0] - a * a * x ** 4)), L(den))
            st = [r'Divide numerator and denominator by $x^2 = \sqrt{x^4}$ (for $x>0$).',
                  r'Numerator: $\sqrt{%d + \tfrac{c}{x^4}} \to %d$; denominator $\to %d$.' % (a * a, a, b),
                  r'So the limit is $%s$.' % L(ans)]
        else:
            a = r.choice([2, 4, 6, -2, 3, 5]); b = r.randint(-3, 3)
            fl = r'\sqrt{x^2 %s %dx %s} - x' % ('+' if a > 0 else '-', abs(a), ('+ %d' % b) if b > 0 else ('- %d' % -b) if b < 0 else '')
            ans = Q(a, 2)
            st = [r'Multiply by the conjugate: $\dfrac{(x^2 %+dx %+d) - x^2}{\sqrt{x^2 %+dx %+d} + x} = \dfrac{%dx %+d}{\sqrt{x^2 %+dx %+d} + x}$.' % (a, b, a, b, a, b, a, b),
                  r'Divide by $x$: $\dfrac{%d + %d/x}{\sqrt{1 + %d/x + %d/x^2} + 1} \to \dfrac{%d}{2} = %s$.' % (a, b, a, b, a, L(ans))]
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to\infty} %s$.' % fl, [P], st, 3, mcq(P['latex'], num_distractors(ans, [0, oo])))

    def factor():
        p = r.choice([-3, -2, -1, 1, 2, 3, 4]); q = r.choice([-4, -2, -1, 0, 1, 3, 5])
        if p == q or p == -p:
            raise ValueError
        num = sp.expand((x - p) * (x - q)); den = sp.expand((x - p) * (x + p))
        ans = Q(p - q, 2 * p)
        st = [r'Substituting $x = %d$ gives $\tfrac{0}{0}$, so factor.' % p,
              r'$\dfrac{%s}{%s} = \dfrac{%s}{%s} = \dfrac{%s}{%s}$ for $x \neq %d$.' % (L(num), L(den), L(sp.factor(num)), L(sp.factor(den)), L(x - q), L(x + p), p),
              r'Now substitute: $\dfrac{%d %s}{%d %s} = %s$.' % (p, ('-' if q >= 0 else '+') + str(abs(q)), p, ('+' if p >= 0 else '-') + str(abs(p)), L(ans))]
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to %d} \dfrac{%s}{%s}$.' % (p, L(num), L(den)), [P], st, 3, mcq(P['latex'], num_distractors(ans, [0])))

    def rationalize():
        a = r.randint(2, 6); mm = r.randint(1, 5); c = a * a - mm * a
        k = r.choice([1, 2, 4, 8, 6])
        if mm * a + c <= 0:
            raise ValueError
        ans = k * (1 - Q(mm, 2 * a))
        rad = mm * t + c
        st = [r'At $t=%d$: $\sqrt{%d} = %d$, so the limit has the form $\tfrac{0}{0}$.' % (a, a * a, a),
              r'Multiply numerator and denominator by $t + \sqrt{%s}$: numerator becomes $%d(t^2 - (%s)) = %d(%s)$.' % (L(rad), k, L(rad), k, L(sp.expand(t ** 2 - rad))),
              r'Factor: $t^2 - (%s) = %s$, so the factor $(t-%d)$ cancels.' % (L(rad), L(sp.factor(t ** 2 - rad)), a),
              r'What remains: $\lim_{t\to%d} \dfrac{%d(%s)}{t + \sqrt{%s}} = \dfrac{%d \cdot %s}{%d + %d} = %s$.' % (a, k, L(sp.cancel((t ** 2 - rad) / (t - a))), L(rad), k, L(sp.cancel((t ** 2 - rad) / (t - a)).subs(t, a)), a, a, L(ans))]
        P = P_num('$L =$', ans)
        kk = '' if k == 1 else str(k)
        B.add(r'Compute $L = \lim_{t\to %d} \dfrac{%st - %s\sqrt{%s}}{t - %d}$.' % (a, kk, kk, L(rad), a), [P], st, 4,
              mcq(P['latex'], num_distractors(ans, [k, 0, k * Q(mm, 2 * a)])))

    def sqrt_simple():
        a = r.randint(1, 7); k = r.choice([1, 2, 3])
        ans = Q(1, 2 * a * k)
        st = [r'Form $\tfrac{0}{0}$. Multiply by the conjugate $\sqrt{x + %d} + %d$.' % (a * a, a),
              r'Numerator: $(x + %d) - %d = x$, so the expression equals $\dfrac{x}{%sx(\sqrt{x+%d} + %d)} = \dfrac{1}{%s(\sqrt{x+%d}+%d)}$.' % (a * a, a * a, '' if k == 1 else k, a * a, a, '' if k == 1 else k, a * a, a),
              r'Let $x\to0$: $\dfrac{1}{%d\cdot %d} = %s$.' % (k, 2 * a, L(ans))]
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to 0} \dfrac{\sqrt{x + %d} - %d}{%s x}$.' % (a * a, a, '' if k == 1 else k), [P], st, 3, mcq(P['latex'], num_distractors(ans, [0, Q(1, a)])))

    def squeeze():
        form = r.randrange(3); k = r.randint(1, 9); n_ = r.randint(1, 3)
        if form == 0:
            fl = r'\lim_{x\to 0} x^{%d}\sin\!\left(\dfrac{%d}{x}\right)' % (2 * n_, k) if n_ > 0 else ''
            st = [r'The limit of $\sin(%d/x)$ does not exist, so we cannot use the product rule for limits.' % k,
                  r'Squeeze: $-x^{%d} \le x^{%d}\sin(%d/x) \le x^{%d}$ for all $x\neq0$.' % (2 * n_, 2 * n_, k, 2 * n_),
                  r'Both bounds tend to $0$, so by the squeeze theorem the limit is $0$.']
        elif form == 1:
            fl = r'\lim_{x\to\infty} \dfrac{%d + \sin(%dx)}{x}' % (k, n_)
            st = [r'Since $-1 \le \sin(%dx) \le 1$: $\dfrac{%d}{x} \le \dfrac{%d+\sin(%dx)}{x} \le \dfrac{%d}{x}$ for $x > 0$.' % (n_, k - 1, k, n_, k + 1),
                  r'Both bounds tend to $0$, so the limit is $0$.']
        else:
            fl = r'\lim_{x\to 0} x^{%d}\cos\!\left(\dfrac{%d}{x^2}\right)' % (n_, k)
            st = [r'$|\cos(\cdot)| \le 1$ gives $-|x|^{%d} \le x^{%d}\cos(%d/x^2) \le |x|^{%d}$.' % (n_, n_, k, n_),
                  r'Both bounds tend to $0$; by the squeeze theorem the limit is $0$.']
        P = P_num('$L =$', 0)
        B.add(r'Compute $L = %s$.' % fl, [P], st, 3, mcq(P['latex'], [L(k), '1', r'\text{does not exist}', L(-1), r'\infty']))

    def sin_lin():
        a = r.randint(1, 9); b = r.randint(1, 9)
        if a == b:
            raise ValueError
        ans = Q(a, b)
        fn = r.choice(['sin', 'tan'])
        st = [r'Use $\lim_{u\to0} \dfrac{\%s u}{u} = 1$ with $u = %dx$.' % (fn, a),
              r'$\dfrac{\%s(%dx)}{%dx} = \dfrac{\%s(%dx)}{%dx}\cdot\dfrac{%d}{%d} \to 1 \cdot %s = %s$.' % (fn, a, b, fn, a, a, a, b, L(ans), L(ans))]
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to 0} \dfrac{\%s(%dx)}{%dx}$.' % (fn, a, b), [P], st, 3, mcq(P['latex'], num_distractors(ans, [Q(b, a), 1, 0])))

    def one_sided():
        c = r.randint(-2, 3); m1 = r.randint(-3, 3); m2 = r.randint(-3, 3); b1 = r.randint(-4, 4); b2 = r.randint(-4, 4)
        f1 = m1 * x + b1; f2 = x ** 2 + m2 * x + b2
        lft = f1.subs(x, c); rgt = f2.subs(x, c)
        P1 = P_num(r'$\lim_{x\to %d^-} f(x) =$' % c, lft); P2 = P_num(r'$\lim_{x\to %d^+} f(x) =$' % c, rgt)
        P3 = P_choice(r'Does $\lim_{x\to %d} f(x)$ exist?' % c, ['yes', 'no'], 0 if lft == rgt else 1)
        st = [r'Left of $%d$ we use $%s$: the left limit is $%s$.' % (c, L(f1), L(lft)),
              r'Right of $%d$ we use $%s$: the right limit is $%s$.' % (c, L(f2), L(rgt)),
              r'The two-sided limit exists iff both one-sided limits agree: %s.' % ('they do' if lft == rgt else 'they do not, so it does not exist')]
        B.add(r'Let $f(x) = \begin{cases} %s & x < %d \\ %s & x \ge %d \end{cases}$. Determine the one-sided limits at $x = %d$.' % (L(f1), c, L(f2), c, c),
              [P1, P2, P3], st, 4)

    B.fill(rat_inf, 7); B.fill(factor, 5); B.fill(rationalize, 6); B.fill(sqrt_simple, 4); B.fill(squeeze, 3); B.fill(sin_lin, 3); B.fill(one_sided, 4)


# =====================================================================
def asymptotes(B):
    r = B.rng

    def slant():
        a = r.choice([1, 2, 3, -1, -2]); p = r.randint(-4, 4); q = r.randint(-4, 4); rr = r.randint(-4, 5)
        num = a * (x - p) * (x + q)
        if sp.expand(num).subs(x, rr) == 0:
            raise ValueError
        quo, rem = sp.div(sp.expand(num), x - rr, x)
        P = P_expr('$y =$', quo)
        st = [r'Expand the numerator: $%s = %s$.' % (L(num), L(sp.expand(num))),
              r'Polynomial long division by $%s$: $\dfrac{%s}{%s} = %s + \dfrac{%s}{%s}$.' % (L(x - rr), L(sp.expand(num)), L(x - rr), L(quo), L(rem), L(x - rr)),
              r'The remainder term tends to $0$ as $x\to\pm\infty$, so the slant asymptote is $y = %s$.' % L(quo)]
        k = sp.factor(quo)
        dis = [L(quo + a), L(quo - a), L(a * x), L(quo + 2 * a), L(a * (x + rr)), L(quo - 2 * a)]
        B.add(r'Determine the slant asymptote of $f(x) = \dfrac{%s}{%s}$.' % (L(num), L(x - rr)), [P], st, 4, mcq(P['latex'], dis))

    def mobius():
        a, b, c, dd = [r.choice([1, 2, 3, -1, -2, 4, 5, -3]) for _ in range(4)]
        if a * dd - b * c == 0:
            raise ValueError
        P1 = P_num('Vertical asymptote $x =$', Q(-dd, c)); P2 = P_num('Horizontal asymptote $y =$', Q(a, c))
        st = [r'Vertical: the denominator $%s$ vanishes at $x = %s$ while the numerator does not (since $ad - bc = %d \neq 0$).' % (L(c * x + dd), L(Q(-dd, c)), a * dd - b * c),
              r'Horizontal: divide by $x$, $\dfrac{%d + %d/x}{%d + %d/x} \to \dfrac{%d}{%d} = %s$ as $x\to\pm\infty$.' % (a, b, c, dd, a, c, L(Q(a, c)))]
        B.add(r'Give the vertical and horizontal asymptotes of $f(x) = \dfrac{%s}{%s}$.' % (L(a * x + b), L(c * x + dd)), [P1, P2], st, 4)

    def rational_holes():
        p, q, rr = r.sample(range(-4, 5), 3)
        s = r.choice([q, r.randint(-4, 4)])
        num = sp.expand((x - p) * (x - s)); den = sp.expand((x - q) * (x - rr))
        if num == den or s == rr and s == q:
            raise ValueError
        va = [v for v in (q, rr) if v != s and v != p] + []
        va = sorted(set(v for v in (q, rr) if sp.cancel(num / den).as_numer_denom()[1].subs(x, v) == 0))
        if not va:
            raise ValueError
        P1 = P_set('Vertical asymptotes ($x$-values):', va); P2 = P_num('Horizontal asymptote $y =$', 1)
        red = sp.cancel(num / den)
        st = [r'Factor: $f(x) = \dfrac{%s}{%s}$.' % (L(sp.factor(num)), L(sp.factor(den)))]
        if red != num / den and sp.denom(red) != den:
            st.append(r'A common factor cancels: $f(x) = %s$ for $x$ in the domain. A cancelled zero of the denominator is a hole, not an asymptote.' % L(red))
        st += [r'The remaining zeros of the denominator give vertical asymptotes: $x \in %s$.' % P1['latex'],
               r'Numerator and denominator have equal degree with leading coefficients $1$ and $1$, so $y = 1$ is the horizontal asymptote.']
        B.add(r'Determine all vertical asymptotes and the horizontal asymptote of $f(x) = \dfrac{%s}{%s}$.' % (L(num), L(den)), [P1, P2], st, 4)

    def exp_h():
        a, b, c, dd = [r.choice([1, 2, 3, 4, 5, 6]) for _ in range(4)]
        if a * dd == b * c:
            raise ValueError
        f = dfrac(L(a * exp(x) + b), L(c * exp(x) + dd))
        P1 = P_num(r'As $x\to\infty$: $y =$', Q(a, c)); P2 = P_num(r'As $x\to-\infty$: $y =$', Q(b, dd))
        st = [r'As $x\to\infty$, $e^x\to\infty$: divide by $e^x$ to get $\dfrac{%d + %d e^{-x}}{%d + %d e^{-x}} \to %s$.' % (a, b, c, dd, L(Q(a, c))),
              r'As $x\to-\infty$, $e^x\to0$: the quotient tends to $\dfrac{%d}{%d} = %s$.' % (b, dd, L(Q(b, dd)))]
        B.add(r'Give the horizontal asymptotes of $f(x) = %s$.' % f, [P1, P2], st, 4)

    def count():
        k = r.randint(0, 4); p, q = r.sample([v for v in range(-4, 7) if v != k], 2)
        den = sp.expand((x - p) * (x - q))
        inside = [v for v in (p, q) if v < k]
        ans = len(inside) + 1
        st = [r'Domain: $%d - x \ge 0$ and $x \ne %d, %d$, so we live on $(-\infty, %d]$ minus those points.' % (k, p, q, k),
              r'Vertical asymptotes occur at zeros of the denominator inside the domain where the numerator is non-zero: %s.' % (', '.join('$x=%d$' % v for v in inside) if inside else 'none'),
              r'As $x\to-\infty$ the numerator grows like $\sqrt{|x|}$ and the denominator like $x^2$, so $f\to0$: horizontal asymptote $y = 0$ (there is no $+\infty$ side).',
              r'Total: $%d$ asymptote%s.' % (ans, 's' if ans > 1 else '')]
        P = P_num('Number of asymptotes:', ans)
        B.add(r'Let $f(x) = \dfrac{\sqrt{%s}}{%s}$. How many asymptotes (horizontal and vertical together) does $f$ have?' % (L(k - x), L(den)), [P], st, 3,
              mcq(P['latex'], [str(v) for v in range(1, 6) if v != ans]))

    def slant_sqrt():
        form = r.randrange(2)
        if form == 0:
            a = r.choice([2, 4, 6, -2, -4, 3]); P = P_expr(r'For $x\to\infty$: $y =$', x + Q(a, 2))
            fl = r'\sqrt{x^2 %s %dx}' % ('+' if a > 0 else '-', abs(a))
            st = [r'Slope: $a = \lim_{x\to\infty} f(x)/x = \lim \sqrt{1 + %d/x} = 1$.' % a,
                  r'Intercept: $b = \lim_{x\to\infty} (\sqrt{x^2 %+dx} - x) = \lim \dfrac{%dx}{\sqrt{x^2 %+dx}+x} = %s$.' % (a, a, a, L(Q(a, 2))),
                  r'So the slant asymptote for $x\to\infty$ is $y = %s$.' % L(x + Q(a, 2))]
        else:
            a = r.choice([1, 2, 3, -1, -2]); b = r.randint(-3, 3); c = r.randint(1, 4)
            num = a * x ** 3 + b * x ** 2 + r.randint(-3, 3) * x + r.randint(-3, 3); den = x ** 2 + c
            quo, rem = sp.div(num, den, x)
            P = P_expr('$y =$', quo); fl = dfrac(L(num), L(den))
            st = [r'Long division: $\dfrac{%s}{%s} = %s + \dfrac{%s}{%s}$.' % (L(num), L(den), L(quo), L(rem), L(den)),
                  r'The remainder fraction tends to $0$, so the slant asymptote is $y = %s$.' % L(quo)]
        B.add(r'Determine the slant asymptote of $f(x) = %s$.' % fl, [P], st, 4)

    B.fill(slant, 9); B.fill(mobius, 5); B.fill(rational_holes, 5); B.fill(exp_h, 4); B.fill(count, 5); B.fill(slant_sqrt, 4)


# =====================================================================
def continuity(B):
    r = B.rng

    def find_k():
        mm = r.randint(-3, 4); b = r.randint(-5, 5); c = r.randint(-3, 3)
        k = mm * c + b - c * c
        P = P_num('$k =$', k)
        st = [r'For $x \ne %d$ both pieces are polynomials, hence continuous.' % c,
              r'At $x = %d$: the left limit is $%s$ evaluated at $x=%d$, i.e. $%d$, and $f(%d) = (%d)^2 + k = %d + k$.' % (c, L(mm * x + b), c, mm * c + b, c, c, c * c),
              r'Continuity requires $%d + k = %d$, so $k = %d$.' % (c * c, mm * c + b, k)]
        B.add(r'For which $k$ is $f(x) = \begin{cases} %s & x < %d \\ x^2 + k & x \ge %d \end{cases}$ continuous on $\mathbb{R}$?' % (L(mm * x + b), c, c),
              [P], st, 3, mcq(P['latex'], num_distractors(k, [mm * c + b, k + 2 * c])))

    def removable():
        form = r.randrange(4); p = r.choice([1, 2, 3, 4, -1, -2, 9, 16]) if True else 1
        if form == 0:
            fl = dfrac(L(x ** 2 - p * p), L(x - p)); a = 2 * p
            st = [r'For $x\ne%d$: $\dfrac{(x-%d)(x+%d)}{x-%d} = x + %d$.' % (p, p, p, p, p) if p > 0 else r'For $x\ne%d$: factor $x^2 - %d = (x - (%d))(x + (%d))$ and cancel.' % (p, p * p, p, p)]
        elif form == 1:
            fl = dfrac(L(x ** 3 - p ** 3), L(x - p)); a = 3 * p * p
            st = [r'For $x\ne%d$: $x^3 - %s = (x - %s)(x^2 + %s x + %s)$, so $f(x) = x^2 + %sx + %s$.' % (p, L(p ** 3), L(p), L(p), L(p * p), L(p), L(p * p))]
        elif form == 2:
            if p not in (1, 4, 9, 16):
                raise ValueError
            sp_ = int(sp.sqrt(p)); fl = dfrac(r'\sqrt{x} - %d' % sp_, L(x - p)); a = Q(1, 2 * sp_)
            st = [r'Multiply by $\sqrt{x}+%d$: $\dfrac{x - %d}{(x-%d)(\sqrt{x}+%d)} = \dfrac{1}{\sqrt{x}+%d}$.' % (sp_, p, p, sp_, sp_)]
        else:
            k = abs(p) if abs(p) < 9 else 5; fl = dfrac(r'\sin(%dx)' % k, 'x'); a = k; p = 0
            st = [r'$\dfrac{\sin(%dx)}{x} = %d\cdot\dfrac{\sin(%dx)}{%dx} \to %d$ as $x\to 0$.' % (k, k, k, k, k)]
        st.append(r'Continuity at $x = %d$ requires $a = \lim_{x\to %d} f(x) = %s$.' % (p, p, L(a)))
        P = P_num('$a =$', a)
        B.add(r'Determine $a$ such that $f(x) = \begin{cases} %s & x \ne %d \\ a & x = %d\end{cases}$ is continuous at $x = %d$.' % (fl, p, p, p),
              [P], st, 3, mcq(P['latex'], num_distractors(a, [0])))

    def diffble():
        c = r.choice([-2, -1, 1, 2, 3]); n_ = r.choice([2, 3])
        a = n_ * c ** (n_ - 1); b = c ** n_ - a * c
        P1 = P_num('$a =$', a); P2 = P_num('$b =$', b)
        st = [r'Continuity at $x=%d$: $%d^{%d} = %d a + b$, i.e. $%d = %da + b$.' % (c, c, n_, c, c ** n_, c),
              r"Differentiability: the one-sided derivatives must match: $%d\cdot%d^{%d} = a$, so $a = %d$." % (n_, c, n_ - 1, a),
              r'Then $b = %d - %d\cdot%d = %d$.' % (c ** n_, c, a, b)]
        B.add(r'Find $a, b$ such that $f(x) = \begin{cases} x^{%d} & x \le %d \\ ax + b & x > %d \end{cases}$ is differentiable on $\mathbb{R}$.' % (n_, c, c),
              [P1, P2], st, 5)

    def statements():
        c = r.randint(1, 4); mm = r.choice([1, 2, 3, -1, -2]); b1 = r.randint(-4, 4); b2 = r.choice([b1, r.randint(-4, 4)])
        f1 = mm * x + b1; f2 = mm * x + b2
        cont = b1 == b2
        # I: left difference quotient using f(c)=f2(c); II: right difference quotient; III: f'(c)=mm
        I = cont; II = True; III = cont
        opts = ['None', 'I only', 'II only', 'III only', 'I and II only', 'I, II, and III']
        truth = (I, II, III)
        idx = {(False, False, False): 0, (True, False, False): 1, (False, True, False): 2, (False, False, True): 3,
               (True, True, False): 4, (True, True, True): 5}[truth]
        st = [r'$f(%d) = %s$ (second piece).' % (c, L(f2.subs(x, c))),
              r'II: for $h > 0$, $\dfrac{f(%d+h) - f(%d)}{h} = \dfrac{%d h}{h} = %d$, so II is true.' % (c, c, mm, mm)]
        if cont:
            st.append(r'The pieces agree at $x=%d$ (same line), so the left quotient is also $%d$ and $f^{\prime}(%d) = %d$: I and III are true.' % (c, mm, c, mm))
        else:
            st.append(r'For $h<0$: $\dfrac{(%s) - (%s)}{h} = %d + \dfrac{%d}{h} \to \pm\infty$, so I is false; $f$ is not even continuous at $%d$, so $f^{\prime}(%d)$ does not exist and III is false.' % (L(f1.subs(x, c + sp.Symbol('h'))), L(f2.subs(x, c)), mm, b1 - b2, c, c))
        P = P_choice('Which statements are true?', opts, idx)
        B.add(r'Let $f(x) = \begin{cases} %s & x < %d \\ %s & x \ge %d\end{cases}$. Which of the following are true? '
              r'I. $\lim_{h\to0^-} \frac{f(%d+h)-f(%d)}{h} = %d$. II. $\lim_{h\to0^+} \frac{f(%d+h)-f(%d)}{h} = %d$. III. $f^{\prime}(%d) = %d$.'
              % (L(f1), c, L(f2), c, c, c, mm, c, c, mm, c, mm), [P], st, 3)

    def disc_points():
        p, q = sorted(r.sample(range(-5, 6), 2)); a = r.randint(1, 4)
        den = sp.expand((x - p) * (x - q)); num = x ** 2 + a
        P = P_set('Points of discontinuity:', [p, q])
        st = [r'A rational function is continuous on its domain; it is undefined where $%s = %s = 0$.' % (L(den), L(sp.factor(den))),
              r'The numerator $x^2 + %d > 0$ never cancels these factors, so $f$ is discontinuous at $x \in \{%d, %d\}$ (vertical asymptotes).' % (a, p, q)]
        B.add(r'At which $x$-values is $f(x) = \dfrac{%s}{%s}$ discontinuous?' % (L(num), L(den)), [P], st, 3)

    B.fill(find_k, 7); B.fill(removable, 8); B.fill(diffble, 5); B.fill(statements, 6); B.fill(disc_points, 4)
