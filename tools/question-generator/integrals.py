"""Integrals: substitution, partial fractions, area, limit of a sum, by parts."""
from common import *
from sympy import sqrt, exp, log, sin, cos, tan, atan, pi, E, Abs, integrate

n = sp.Symbol('n', positive=True, integer=True)
rr_ = sp.Symbol('r', positive=True, integer=True)


def I(f, a, b, var=x):
    return sp.simplify(integrate(f, (var, a, b)))


# =====================================================================
def substitution(B):
    r = B.rng
    cyc = Cycle()

    def poly_power():
        a = r.randint(1, 5); nn = r.randint(1, 4); b = r.randint(1, 3)
        f = x * (x ** 2 + a) ** nn
        v = I(f, 0, b)
        st = [r'Substitute $u = x^2 + %d$, $du = 2x\,dx$; bounds $x=0 \mapsto u=%d$, $x=%d \mapsto u=%d$.' % (a, a, b, b * b + a),
              r'$\displaystyle\int_0^{%d} %s\,dx = \frac12\int_{%d}^{%d} u^{%d}\,du = \frac{1}{%d}\Big[u^{%d}\Big]_{%d}^{%d}$.' % (b, L(f), a, b * b + a, nn, 2 * (nn + 1), nn + 1, a, b * b + a),
              r'$= \dfrac{%d^{%d} - %d^{%d}}{%d} = %s$.' % (b * b + a, nn + 1, a, nn + 1, 2 * (nn + 1), L(v))]
        P = P_num('Value:', v)
        B.add(r'Compute $\displaystyle\int_0^{%d} %s\,dx$.' % (b, L(f)), [P], st, 4, mcq(P['latex'], num_distractors(v, [v * 2])))

    def anti():
        k = cyc('a', 7); a = r.randint(1, 4); nn = r.randint(2, 5); b = r.randint(1, 5)
        if k == 0:
            f = x * exp(a * x ** 2); F = exp(a * x ** 2) / (2 * a); sub = r'u = %s,\ du = %s\,dx' % (L(a * x ** 2), L(2 * a * x)); smp = [-1, 1]
        elif k == 1:
            f = cos(x) * sin(x) ** nn; F = sin(x) ** (nn + 1) / (nn + 1); sub = r'u = \sin x,\ du = \cos x\,dx'; smp = [-1.5, 1.5]
        elif k == 2:
            f = log(x) ** nn / x; F = log(x) ** (nn + 1) / (nn + 1); sub = r'u = \ln x,\ du = \tfrac{1}{x}dx'; smp = [1.2, 4]
        elif k == 3:
            g = a * x ** 2 + b * x + r.randint(1, 6); f = sp.diff(g, x) / g; F = log(g); sub = r'u = %s,\ du = (%s)\,dx' % (L(g), L(sp.diff(g, x))); smp = [0.2, 3]
        elif k == 4:
            f = x / sqrt(x ** 2 + b); F = sqrt(x ** 2 + b); sub = r'u = x^2 + %d,\ du = 2x\,dx' % b; smp = [-2, 2]
        elif k == 5:
            f = x ** 2 * cos(x ** 3 + b); F = sin(x ** 3 + b) / 3; sub = r'u = x^3 + %d,\ du = 3x^2\,dx' % b; smp = [-1, 1]
        else:
            f = exp(x) / (1 + exp(2 * x)); F = atan(exp(x)); sub = r'u = e^x,\ du = e^x\,dx'; smp = [-1, 1]
        assert sp.simplify(sp.diff(F, x) - f) == 0
        P = P_expr(r'$\displaystyle\int f(x)\,dx =$', F, sample={'x': smp}, upc=True)
        st = [r'Substitute $%s$.' % sub, r'The integral becomes a standard one in $u$; integrating and substituting back gives $%s + C$.' % L(F),
              r'Check: differentiating $%s$ gives back $%s$.' % (L(F), L(f))]
        B.add(r'Find an antiderivative: $\displaystyle\int %s\,dx$. (Enter the antiderivative; the constant $C$ may be omitted.)' % L(f), [P], st, 4,
              mcq(P['latex'], [L(F * 2) + ' + C', L(f * x) + ' + C', L(-F) + ' + C', L(sp.diff(f, x)) + ' + C']))

    def exam_transform():
        u1 = r.choice([2, 3]); c = r.choice([1, 2, 3, 5]); m_ = r.choice([1, 1, 2]); kk = r.choice([1, 1, 2])
        x1sq = u1 * u1 - c
        x2 = r.choice([2, 3, 4])
        if x2 * x2 <= x1sq:
            raise ValueError
        u2 = sqrt(x2 * x2 + c)
        p = sp.expand(u * (u ** 2 - c) ** m_); q = kk + u
        x1l = L(sqrt(x1sq))
        st = [r'With $u = \sqrt{x^2 + %d}$: $du = \dfrac{x}{\sqrt{x^2+%d}}dx = \dfrac{x}{u}dx$, so $x\,dx = u\,du$, and $x^2 = u^2 - %d$.' % (c, c, c),
              r'Write $x^{%d} = (x^2)^{%d}\cdot x$: the integrand becomes $(u^2 - %d)^{%d}\ln(%s)\,u\,du$.' % (2 * m_ + 1, m_, c, m_, L(q)),
              r'So $p(u) = %s$ and $q(u) = %s$.' % (L(p), L(q)),
              r'Bounds: $x = %s \mapsto u = \sqrt{%d + %d} = %d$ and $x = %d \mapsto u = %s$.' % (x1l, x1sq, c, u1, x2, L(u2))]
        B.add(r'Use $u$-substitution with $u = \sqrt{x^2 + %d}$ to show that $\displaystyle\int_{%s}^{%d} x^{%d}\ln\left(%s + \sqrt{x^2 + %d}\right)dx = \int_a^b p(u)\ln(q(u))\,du$ with $p, q$ polynomials. Give $p(u)$, $q(u)$, $a$ and $b$.'
              % (c, x1l, x2, 2 * m_ + 1, kk, c),
              [P_expr('$p(u) =$', p, vars=('u',), sample={'u': [0.5, 3]}), P_expr('$q(u) =$', q, vars=('u',), sample={'u': [0.5, 3]}),
               P_num('$a =$', u1), P_num('$b =$', u2)], st, 6)

    def exp_sin():
        nn = r.randint(1, 3); fn = r.choice([sin, cos]); a = r.choice([1, 2, 3])
        A = r.choice([pi, 2 * pi, pi / 2]) if fn == sin else r.choice([pi, pi / 2])
        p = u ** nn
        st = [r'Substitute $u = e^x$, $du = e^x\,dx$. Then $e^{%dx}\,dx = (e^x)^{%d} e^x\,dx = u^{%d}\,du$.' % (nn + 1, nn, nn),
              r'So $p(u) = %s$.' % L(p),
              r'Bounds: $x \to -\infty$ gives $u = e^x \to 0$; $x = \ln(%s)$ gives $u = %s$.' % (L(A), L(A))]
        B.add(r'Using the substitution $u = e^x$, $\displaystyle\int_{-\infty}^{\ln(%s)} e^{%dx}\%s(e^x)\,dx = \int_a^b p(u)\%s(u)\,du$. Give $p(u)$, $a$ and $b$.' % (L(A), nn + 1, fn.__name__, fn.__name__),
              [P_expr('$p(u) =$', p, vars=('u',), sample={'u': [0.5, 3]}), P_num('$a =$', 0), P_num('$b =$', A)], st, 4)

    def definite():
        k = cyc('d', 4); nn = r.randint(1, 5); a = r.randint(1, 3)
        if k == 0:
            f = sin(x) * cos(x) ** nn; lo, hi = 0, pi / 2; sub = r'u = \cos x,\ du = -\sin x\,dx'
        elif k == 1:
            f = log(x) ** nn / x; lo, hi = 1, E; sub = r'u = \ln x,\ du = dx/x'
        elif k == 2:
            f = x * exp(a * x ** 2); lo, hi = 0, 1; sub = r'u = %s' % L(a * x ** 2)
        else:
            f = x ** 2 / (x ** 3 + a); lo, hi = 0, 1; sub = r'u = x^3 + %d' % a
        v = I(f, lo, hi)
        st = [r'Substitute $%s$ and change the bounds accordingly.' % sub, r'Antiderivative: $%s$.' % L(sp.simplify(integrate(f, x))),
              r'Evaluate: $%s$.' % L(v)]
        P = P_num('Value:', v)
        B.add(r'Compute $\displaystyle\int_{%s}^{%s} %s\,dx$.' % (L(lo), L(hi), L(f)), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def primitive_tangent():
        k = cyc('pt', 3)
        if k == 0:
            c = r.choice([3, 2]); f = x ** 2 * sqrt(x ** 3 - (c ** 3 - {3: 25, 2: 4}[c]))
        elif k == 1:
            c = r.choice([1, 2, 3]); f = x * exp(x ** 2 - c * c)
        else:
            c = r.choice([2, 3, 4]); f = x * log(x - 1) + x ** 2
        y0 = r.randint(-30, 40)
        fc = sp.simplify(f.subs(x, c)); b = y0 - fc * c
        st = [r'The tangent line of $F$ at $P$ has slope $F^{\prime}(%d) = f(%d) = %s$ — no integration needed.' % (c, c, L(fc)),
              r'It passes through $(%d, %d)$: $%d = %s\cdot %d + b$, so $b = %s$.' % (c, y0, y0, L(fc), c, L(b))]
        P = P_num('$b =$', b)
        B.add(r'Given $f(x) = %s$, let $F$ be the primitive of $f$ through $P = (%d, %d)$. What is the $y$-intercept $b$ of the tangent line of $F$ at $P$?' % (L(f), c, y0),
              [P], st, 4, mcq(P['latex'], num_distractors(b, [y0 - fc, fc * c - y0])))

    B.fill(poly_power, 6); B.fill(anti, 9); B.fill(exam_transform, 5); B.fill(exp_sin, 4); B.fill(definite, 4); B.fill(primitive_tangent, 4)


# =====================================================================
FORMS = [
    ((x - 1) ** 2 * (x + 1), r'(x-1)(x^2-1)', r'\frac{A}{x-1} + \frac{B}{(x-1)^2} + \frac{C}{x+1}',
     [r'\frac{A}{x-1} + \frac{B}{x^2-1}', r'\frac{A}{x-1} + \frac{Bx+C}{x^2-1}', r'\frac{A}{x-1} + \frac{B}{x+1}', r'\frac{Ax+B}{x^2-1} + \frac{C}{x+1}'],
     r'$x^2 - 1 = (x-1)(x+1)$, so the denominator is $(x-1)^2(x+1)$: a repeated linear factor needs terms up to $(x-1)^2$.'),
    ((x ** 2 + 1) * (x - 2), r'(x^2+1)(x-2)', r'\frac{A}{x-2} + \frac{Bx+C}{x^2+1}',
     [r'\frac{A}{x-2} + \frac{B}{x^2+1}', r'\frac{A}{x-2} + \frac{B}{x+1} + \frac{C}{x-1}', r'\frac{Ax+B}{x-2} + \frac{C}{x^2+1}', r'\frac{A}{x-2} + \frac{B}{(x-2)^2} + \frac{C}{x^2+1}'],
     r'$x^2+1$ is irreducible (discriminant $<0$), so it gets a linear numerator $Bx + C$.'),
    (x ** 2 * (x + 3), r'x^2(x+3)', r'\frac{A}{x} + \frac{B}{x^2} + \frac{C}{x+3}',
     [r'\frac{A}{x^2} + \frac{B}{x+3}', r'\frac{A}{x} + \frac{B}{x^2}', r'\frac{A}{x} + \frac{B}{x+3}', r'\frac{A}{x} + \frac{B}{x+3} + \frac{C}{(x+3)^2}'],
     r'$x^2$ is the repeated linear factor $x$, which needs $\frac{A}{x} + \frac{B}{x^2}$.'),
    ((x ** 2 + 1) ** 2, r'(x^2+1)^2', r'\frac{Ax+B}{x^2+1} + \frac{Cx+D}{(x^2+1)^2}',
     [r'\frac{A}{x^2+1} + \frac{B}{(x^2+1)^2}', r'\frac{A}{x^2+1} + \frac{Bx+C}{(x^2+1)^2}', r'\frac{A}{x+1} + \frac{B}{(x+1)^2}', r'\frac{Ax+B}{x^2+1}'],
     r'A repeated irreducible quadratic factor needs linear numerators over $(x^2+1)$ and $(x^2+1)^2$.'),
    ((x - 1) * (x + 2) * (x - 3), r'(x-1)(x+2)(x-3)', r'\frac{A}{x-1} + \frac{B}{x+2} + \frac{C}{x-3}',
     [r'\frac{A}{x-1} + \frac{B}{x+2}', r'\frac{A}{(x-1)(x+2)} + \frac{B}{x-3}', r'\frac{A}{x-1} + \frac{B}{(x+2)^2} + \frac{C}{x-3}', r'\frac{A}{(x-1)(x+2)(x-3)}'],
     r'Three distinct linear factors: one constant over each.'),
    ((x - 2) * (x + 2) * (x ** 2 + 4), r'x^4 - 16', r'\frac{A}{x-2} + \frac{B}{x+2} + \frac{Cx+D}{x^2+4}',
     [r'\frac{A}{x^2-4} + \frac{B}{x^2+4}', r'\frac{A}{x-2} + \frac{B}{x+2} + \frac{C}{x^2+4}', r'\frac{A}{x^4-16}', r'\frac{A}{x-2} + \frac{B}{(x-2)^2} + \frac{C}{x+2}'],
     r'$x^4 - 16 = (x-2)(x+2)(x^2+4)$; $x^2+4$ is irreducible and gets a linear numerator.'),
    (x * (x ** 2 + x + 1), r'x(x^2+x+1)', r'\frac{A}{x} + \frac{Bx+C}{x^2+x+1}',
     [r'\frac{A}{x} + \frac{B}{x^2+x+1}', r'\frac{A}{x} + \frac{B}{x+1} + \frac{C}{x}', r'\frac{A}{x} + \frac{B}{x^2} + \frac{C}{x+1}', r'\frac{Ax + B}{x} + \frac{C}{x^2+x+1}'],
     r'$x^2+x+1$ has discriminant $1 - 4 < 0$, so it is irreducible and gets a linear numerator.'),
    ((x + 1) ** 3, r'(x+1)^3', r'\frac{A}{x+1} + \frac{B}{(x+1)^2} + \frac{C}{(x+1)^3}',
     [r'\frac{A}{(x+1)^3}', r'\frac{A}{x+1} + \frac{B}{(x+1)^3}', r'\frac{A}{(x+1)^2} + \frac{B}{(x+1)^3}', r'\frac{A}{x+1} + \frac{B}{(x+1)^2}'],
     r'A triple linear factor needs constants over $(x+1)$, $(x+1)^2$ and $(x+1)^3$.'),
]


def partial_fractions(B):
    r = B.rng
    cyc = Cycle()

    def AB():
        a, b = r.sample(range(-4, 5), 2); A = r.choice([1, 2, 3, -1, -2, 4]); Bv = r.choice([1, 2, -1, -3, 5])
        num = sp.expand(A * (x - b) + Bv * (x - a)); den = sp.expand((x - a) * (x - b))
        if num.is_number:
            raise ValueError
        st = [r'Factor the denominator: $%s = (%s)(%s)$.' % (L(den), lin(a), lin(b)),
              r'Write $\dfrac{%s}{(%s)(%s)} = \dfrac{A}{%s} + \dfrac{B}{%s}$, so $%s = A(%s) + B(%s)$.' % (L(num), lin(a), lin(b), lin(a), lin(b), L(num), lin(b), lin(a)),
              r'Put $x = %d$: $%s = A\cdot(%d)$, so $A = %d$.' % (a, L(num.subs(x, a)), a - b, A),
              r'Put $x = %d$: $%s = B\cdot(%d)$, so $B = %d$.' % (b, L(num.subs(x, b)), b - a, Bv)]
        B.add(r'Find $A$ and $B$ such that $\dfrac{%s}{%s} = \dfrac{A}{%s} + \dfrac{B}{%s}$.' % (L(num), L(den), lin(a), lin(b)),
              [P_num('$A =$', A), P_num('$B =$', Bv)], st, 4)

    def definite():
        a, b = r.sample(range(-3, 3), 2); A = r.choice([1, 2, 3, -1, 4]); Bv = r.choice([1, 2, -1, 3])
        lo = max(a, b) + r.randint(1, 2); hi = lo + r.randint(1, 3)
        num = sp.expand(A * (x - b) + Bv * (x - a)); den = sp.expand((x - a) * (x - b))
        if num.is_number:
            raise ValueError
        v = sp.simplify(sp.expand_log(A * log(sp.Integer(hi - a) / (lo - a)) + Bv * log(sp.Integer(hi - b) / (lo - b)), force=True))
        st = [r'Partial fractions: $\dfrac{%s}{%s} = \dfrac{%d}{%s} + \dfrac{%d}{%s}$ (cover-up: $x=%d$ gives $A$, $x=%d$ gives $B$).' % (L(num), L(den), A, lin(a), Bv, lin(b), a, b),
              r'Antiderivative: $%d\ln|%s| + %d\ln|%s|$.' % (A, lin(a), Bv, lin(b)),
              r'Evaluate from $%d$ to $%d$: $%d\ln\tfrac{%d}{%d} + %d\ln\tfrac{%d}{%d} = %s$.' % (lo, hi, A, hi - a, lo - a, Bv, hi - b, lo - b, L(v))]
        assert abs(val(v) - val(integrate(num / den, (x, lo, hi)))) < 1e-9
        P = P_num('Value:', v)
        B.add(r'Compute $\displaystyle\int_{%d}^{%d} \dfrac{%s}{%s}\,dx$.' % (lo, hi, L(num), L(den)), [P], st, 5, mcq(P['latex'], num_distractors(v)))

    def quad():
        A = r.randint(1, 6); Bv = r.choice([0, 2, 4, 6]); C = r.choice([0, 1, 2, 4])
        if Bv == 0 and C == 0:
            raise ValueError
        num = sp.expand(A * (1 + x ** 2) + (Bv * x + C) * (1 + x))
        v = sp.nsimplify(A * log(2) + Q(Bv, 2) * log(2) + C * pi / 4)
        v = sp.simplify(A * log(2) + sp.Rational(Bv, 2) * log(2) + C * pi / 4)
        st = [r'Decompose: $\dfrac{%s}{(1+x)(1+x^2)} = \dfrac{A}{1+x} + \dfrac{Bx + C}{1+x^2}$.' % L(num),
              r'Comparing coefficients of $A(1+x^2) + (Bx+C)(1+x)$: $A = %d$, $B = %d$, $C = %d$.' % (A, Bv, C),
              r'$\int_0^1 \frac{%d}{1+x}dx = %d\ln 2$, $\int_0^1\frac{%dx}{1+x^2}dx = %s\ln(1+x^2)\Big|_0^1 = %s\ln 2$, $\int_0^1\frac{%d}{1+x^2}dx = %d\arctan x\Big|_0^1 = %s$.' % (A, A, Bv, L(Q(Bv, 2)), L(Q(Bv, 2)), C, C, L(C * pi / 4)),
              r'Total: $%s$.' % L(v)]
        assert abs(val(v) - val(integrate(num / ((1 + x) * (1 + x ** 2)), (x, 0, 1)))) < 1e-9
        P = P_num('Value:', v)
        B.add(r'Compute $\displaystyle\int_0^1 \dfrac{%s}{(1+x)(1+x^2)}\,dx$.' % L(num), [P], st, 6, mcq(P['latex'], num_distractors(v, [A * log(2), (A + Bv) * log(2)])))

    i = [0]

    def form():
        den, dl, corr, wrong, why = FORMS[i[0] % len(FORMS)]; i[0] += 1
        deg = sp.degree(sp.expand(den), x)
        num = sp.expand(sum(r.randint(0, 3) * x ** kk for kk in range(deg - 1)) + 1)
        opts = ['$\\displaystyle\\int ' + corr + '\\,dx$'] + ['$\\displaystyle\\int ' + w + '\\,dx$' for w in wrong[:4]] + ['None of the above']
        perm = list(range(5)); r.shuffle(perm); opts2 = [opts[j] for j in perm] + [opts[5]]
        P = P_choice('Correct form:', opts2, perm.index(0))
        B.add(r'Using partial fractions, the integral $\displaystyle\int \dfrac{%s}{%s}\,dx$ can be rewritten as (for suitable constants):' % (L(num), dl), [P], [why], 3)

    def improper():
        a = r.randint(-3, 3); al = r.randint(-3, 3); be = r.randint(-4, 4)
        num = x ** 2 + al * x + be
        quo, rem = sp.div(num, x - a, x)
        if rem == 0:
            raise ValueError
        F = integrate(quo, x) + rem * log(x - a)
        st = [r'The degree of the numerator is not smaller than that of the denominator: divide first.',
              r'$\dfrac{%s}{%s} = %s + \dfrac{%s}{%s}$.' % (L(num), lin(a), L(quo), L(rem), lin(a)),
              r'Integrate term by term: $%s + %s\ln|%s| + C$.' % (L(integrate(quo, x)), L(rem), lin(a))]
        P = P_expr(r'$\displaystyle\int f\,dx =$', F, sample={'x': [a + 0.5, a + 4]}, upc=True)
        B.add(r'Compute $\displaystyle\int \dfrac{%s}{%s}\,dx$ (for $x > %d$; the constant may be omitted).' % (L(num), lin(a), a), [P], st, 4)

    def repeated():
        a = r.randint(-4, 4); al = r.choice([1, 2, 3, -1, -2]); be = r.randint(-5, 5)
        num = al * x + be
        A, Bv = al, al * a + be
        if Bv == 0:
            raise ValueError
        st = [r'Write $%s = A(%s) + B$.' % (L(num), lin(a)), r'Comparing the $x$-coefficient: $A = %d$; putting $x = %d$: $B = %d$.' % (al, a, Bv)]
        B.add(r'Find $A$ and $B$ with $\dfrac{%s}{(%s)^2} = \dfrac{A}{%s} + \dfrac{B}{(%s)^2}$.' % (L(num), lin(a), lin(a), lin(a)),
              [P_num('$A =$', A), P_num('$B =$', Bv)], st, 3)

    B.fill(AB, 6); B.fill(definite, 6); B.fill(quad, 6); B.fill(form, len(FORMS)); B.fill(improper, 3); B.fill(repeated, 3)


# =====================================================================
def area(B):
    r = B.rng
    cyc = Cycle()

    def par_line0():
        a = r.randint(1, 4); b = r.choice([1, 2, 3, 4, 6, -2, -3])
        v = Q(abs(b) ** 3, 6 * a * a)
        xi = Q(b, a)
        st = [r'Intersections: $%s = %s \iff x(%s) = 0$, so $x = 0$ and $x = %s$.' % (L(a * x ** 2), L(b * x), L(a * x - b), L(xi)),
              r'Between them the line lies above the parabola, so $A = \left|\displaystyle\int_0^{%s} (%s - %s)\,dx\right|$.' % (L(xi), L(b * x), L(a * x ** 2)),
              r'$= \left|\Big[%s - %s\Big]_0^{%s}\right| = %s$.' % (L(b * x ** 2 / 2), L(a * x ** 3 / 3), L(xi), L(v))]
        P = P_num('$A =$', v)
        B.add(r'Compute the area of the region enclosed by $y = %s$ and $y = %s$.' % (L(a * x ** 2), L(b * x)), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def par_line():
        r1, r2 = sorted(r.sample(range(-3, 4), 2)); p = r.randint(-3, 3); q = r.randint(-3, 3)
        f = x ** 2 + p * x + q; g = sp.expand(f - (x - r1) * (x - r2))
        g = sp.expand(-(x - r1) * (x - r2) + f)
        v = Q((r2 - r1) ** 3, 6)
        st = [r'Intersections: $%s = %s \iff %s = 0 \iff x \in \{%d, %d\}$.' % (L(f), L(g), L(sp.expand(f - g)), r1, r2),
              r'On $[%d, %d]$ the line is above the parabola: $A = \displaystyle\int_{%d}^{%d} \left(%s\right)dx$.' % (r1, r2, r1, r2, L(sp.expand(g - f))),
              r'$= %s$.' % L(v)]
        P = P_num('$A =$', v)
        B.add(r'Compute the area enclosed by the parabola $y = %s$ and the line $y = %s$.' % (L(f), L(g)), [P], st, 5, mcq(P['latex'], num_distractors(v)))

    def two_par():
        k = r.randint(1, 3); a = r.randint(0, 2 * k * k); b = 2 * k * k - a
        f = x ** 2 - a; g = b - x ** 2
        v = I(g - f, -k, k)
        st = [r'Intersections: $x^2 - %d = %d - x^2 \iff x^2 = %d \iff x = \pm %d$.' % (a, b, k * k, k),
              r'$A = \displaystyle\int_{-%d}^{%d} (%s)\,dx = \Big[%s\Big]_{-%d}^{%d} = %s$.' % (k, k, L(g - f), L(integrate(g - f, x)), k, k, L(v))]
        P = P_num('$A =$', v)
        B.add(r'Compute the area enclosed by $y = %s$ and $y = %s$.' % (L(f), L(g)), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def tangent_origin():
        a = r.choice([-8, -4, -2, 2, 4, -6]); p = r.choice([1, 2, Q(1, 2)]); c = r.randint(-6, 6)
        b = -2 * a * p
        f = a * x ** 3 + b * x ** 2 + c * x
        fp = sp.diff(f, x); m_ = fp.subs(x, p)
        v = sp.simplify(abs(a) * p ** 4 / 12)
        assert abs(val(v) - val(integrate(sp.Abs(m_ * x - f), (x, 0, p)))) < 1e-9
        st = [r"$f'(x) = %s$; a line through $(0,0)$ touching $f$ at $x = p$ is $l(x) = f'(p)\,x$." % L(fp),
              r"Touching means $l(p) = f(p)$: $f'(p)p = f(p)$, i.e. $(%s)p = %s$ which gives $p = %s$ (for $p > 0$)." % (L(fp.subs(x, sp.Symbol('p'))), L(f.subs(x, sp.Symbol('p'))), L(p)),
              r'So $l(x) = %s$.' % L(m_ * x),
              r'$A = \displaystyle\int_0^{%s} |l(x) - f(x)|\,dx = \int_0^{%s} \left|%s\right|dx = %s$.' % (L(p), L(p), L(sp.factor(m_ * x - f)), L(v))]
        P = P_num('$A =$', v)
        B.add(r'Compute the area $A$ of the region bounded by the function $f(x) = %s$ and the tangent line $l(x)$ to $f$ at $x = p$, $p > 0$, that goes through $(0, 0)$ (the region between $x=0$ and $x=p$).' % L(f),
              [P], st, 6, mcq(P['latex'], num_distractors(v)))

    def sqrt_line():
        k = r.randint(1, 4); v = Q(k ** 3, 6)
        st = [r'Intersections: $\sqrt{x} = x/%d \iff x = 0$ or $x = %d$.' % (k, k * k),
              r'$A = \displaystyle\int_0^{%d}\left(\sqrt x - \tfrac{x}{%d}\right)dx = \Big[\tfrac23 x^{3/2} - \tfrac{x^2}{%d}\Big]_0^{%d} = %s - %s = %s$.' % (k * k, k, 2 * k, k * k, L(Q(2, 3) * k ** 3), L(Q(k ** 3, 2)), L(v))]
        P = P_num('$A =$', v)
        B.add(r'Compute the area enclosed by $y = \sqrt{x}$ and $y = %s$.' % L(x / k), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def volume():
        H, c2 = r.choice([(8, 5), (27, 5), (27, 20), (1, 5), (8, 20), (64, 5)])
        V = sp.pi * c2 * Q(3, 5) * sp.Integer(H) ** Q(5, 3)
        a = sp.sqrt(3 * V / (sp.pi * H ** 3))
        a = sp.nsimplify(a)
        st = [r'$V = \pi\displaystyle\int_0^{%d} %d\,x^{2/3}\,dx = %d\pi\cdot\tfrac35\Big[x^{5/3}\Big]_0^{%d} = %s$.' % (H, c2, c2, H, L(V)),
              r'Cone: $\pi\displaystyle\int_0^{%d} a^2x^2\,dx = a^2\pi\dfrac{%d}{3}$.' % (H, H ** 3),
              r'Equal volumes: $a^2 = %s$, so $a = %s$.' % (L(a ** 2), L(a))]
        P = P_num('$a =$', a)
        B.add(r'A solid is formed by rotating $f(x) = \sqrt{%d}\,\sqrt[3]{x}$ around the $x$-axis over $[0, %d]$ (volume $\int_a^b \pi f(x)^2dx$). A cone of the same height and volume is formed by rotating $g(x) = ax$. Find $a > 0$.' % (c2, H),
              [P], st, 5, mcq(P['latex'], num_distractors(a)))

    def trig():
        k = cyc('t', 4)
        if k == 0:
            f, g, lo, hi = sin(x), cos(x), 0, pi / 4; desc = r'$y = \sin x$ and $y = \cos x$ for $0 \le x \le \frac{\pi}{4}$'
        elif k == 1:
            c = r.randint(1, 4); f, g, lo, hi = 0 * x, sin(c * x), 0, pi / c; desc = r'$y = \sin(%s)$ and the $x$-axis for $0 \le x \le %s$' % (L(c * x), L(pi / c))
        elif k == 2:
            kk = r.randint(1, 4); f, g, lo, hi = 0 * x, 1 / x, 1, exp(kk); desc = r'$y = \frac1x$ and the $x$-axis for $1 \le x \le e^{%d}$' % kk
        else:
            kk = r.randint(1, 3); f, g, lo, hi = 0 * x, x * exp(-x), 0, kk; desc = r'$y = xe^{-x}$ and the $x$-axis for $0 \le x \le %d$' % kk
        v = I(g - f, lo, hi)
        st = [r'The upper function is $%s$ on the whole interval.' % L(g), r'$A = \displaystyle\int_{%s}^{%s} (%s)\,dx = \Big[%s\Big]_{%s}^{%s} = %s$.' % (L(lo), L(hi), L(g - f), L(integrate(g - f, x)), L(lo), L(hi), L(v))]
        P = P_num('$A =$', v)
        B.add(r'Compute the area between %s.' % desc, [P], st, 4, mcq(P['latex'], num_distractors(v)))

    B.fill(par_line0, 6); B.fill(par_line, 6); B.fill(two_par, 4); B.fill(tangent_origin, 5); B.fill(sqrt_line, 3); B.fill(volume, 4); B.fill(trig, 5)


# =====================================================================
def riemann(B):
    r = B.rng
    cyc = Cycle()

    def add_sum(summand, f, lo, hi, intro_note='', expanded=None):
        v = I(f, lo, hi)
        st = [r'Write the sum as $\dfrac1n\sum f\!\left(\dfrac rn\right)$ with $f(x) = %s$%s.' % (L(f), intro_note),
              r'As $n\to\infty$, $x = \tfrac rn$ runs through $[%s, %s]$, so the limit is $\displaystyle\int_{%s}^{%s} %s\,dx$.' % (L(lo), L(hi), L(lo), L(hi), L(f)),
              r'Antiderivative: $%s$, giving $%s$.' % (L(sp.simplify(integrate(f, x))), L(v))]
        P = P_num('Limit:', v)
        top = '2n' if hi == 2 and lo == 0 else 'n'
        body = expanded if expanded else r'\lim_{n\to\infty} \sum_{r=1}^{%s} %s' % (top, L(summand))
        return B.add(r'Compute $\displaystyle %s$.' % body, [P], st, 5, mcq(P['latex'], num_distractors(v, [v * 2])))

    def basic():
        k = cyc('b', 10); a = r.choice([1, 2, 3, -1]); kk = r.randint(1, 4)
        rr, nn = rr_, n
        if k == 0:
            add_sum(rr ** kk / nn ** (kk + 1), x ** kk, 0, 1)
        elif k == 1:
            add_sum(exp(a * rr / nn) / nn, exp(a * x), 0, 1)
        elif k == 2:
            add_sum(1 / (nn + kk * rr), 1 / (1 + kk * x), 0, 1, r' (divide numerator and denominator by $n$)')
        elif k == 3:
            c = r.choice([1, 3]); add_sum(nn / (nn ** 2 + c * rr ** 2), 1 / (1 + c * x ** 2), 0, 1, r' (divide by $n^2$)')
        elif k == 4:
            add_sum(rr / (nn ** 2 + rr ** 2), x / (1 + x ** 2), 0, 1, r' (divide by $n^2$)')
        elif k == 5:
            add_sum(sin(pi * rr / nn) / nn, sin(pi * x), 0, 1)
        elif k == 6:
            add_sum(sqrt(rr) / nn ** Q(3, 2), sqrt(x), 0, 1)
        elif k == 7:
            add_sum((nn + rr) ** kk / nn ** (kk + 1), (1 + x) ** kk, 0, 1, r' (here $f(x) = (1+x)^{%d}$, equivalently $\int_1^2 x^{%d}dx$)' % (kk, kk))
        elif k == 8:
            add_sum(rr * exp(rr / nn) / nn ** 2, x * exp(x), 0, 1, r'; integrate by parts')
        else:
            add_sum(rr ** 2 / nn ** 3, x ** 2, 0, 2)

    def expanded():
        k = cyc('x', 3)
        if k == 0:
            body = r'\lim_{n\to\infty}\left(\frac{e^{1/n}}{n^2} + \frac{2e^{2/n}}{n^2} + \frac{3e^{3/n}}{n^2} + \dots + \frac{e}{n}\right)'
            add_sum(None, x * exp(x), 0, 1, r'; the $r$-th term is $\frac{r e^{r/n}}{n^2}$, integrate by parts', body)
        elif k == 1:
            kk = r.randint(2, 4)
            body = r'\lim_{n\to\infty}\left(\frac{1}{n^{%d}} + \frac{2^{%d}}{n^{%d}} + \frac{3^{%d}}{n^{%d}} + \dots + \frac{1}{n}\right)' % (kk + 1, kk, kk + 1, kk, kk + 1)
            add_sum(None, x ** kk, 0, 1, r'; the $r$-th term is $\frac{r^{%d}}{n^{%d}}$' % (kk, kk + 1), body)
        else:
            a = r.randint(2, 4)
            body = r'\lim_{n\to\infty}\left(\frac{1}{n+%d} + \frac{1}{n+%d} + \dots + \frac{1}{n + %dn}\right)' % (a, 2 * a, a)
            add_sum(None, 1 / (1 + a * x), 0, 1, r'; the $r$-th term is $\frac{1}{n + %dr}$' % a, body)

    def exam_ln2():
        A = r.randint(1, 9); Bv = r.choice([2, 4, 6, 8])
        num = sp.expand(A * (n ** 2 + rr_ ** 2) + Bv * rr_ * (n + rr_))
        K = A + Bv // 2
        num_l = L(sp.collect(num, rr_))
        st = [r'Divide numerator and denominator by $n^3$: the term equals $\dfrac1n\cdot\dfrac{%s}{(1 + x)(1 + x^2)}$ with $x = \tfrac rn$.' % L(sp.expand(A * (1 + x ** 2) + Bv * x * (1 + x))),
              r'So the limit is $\displaystyle\int_0^1 \dfrac{%s}{(1+x)(1+x^2)}\,dx$.' % L(sp.expand(A * (1 + x ** 2) + Bv * x * (1 + x))),
              r'Partial fractions: $\dfrac{%d}{1+x} + \dfrac{%dx}{1+x^2}$.' % (A, Bv),
              r'$= %d\ln|1+x|\Big|_0^1 + %d\ln(1+x^2)\Big|_0^1 = %d\ln 2 + %d\ln 2 = %d\ln 2$.' % (A, Bv // 2, A, Bv // 2, K)]
        P = P_num('$A =$', K)
        B.add(r'If $\displaystyle\lim_{n\to\infty}\sum_{r=1}^n \frac{%s}{(n+r)(n^2+r^2)} = A\ln(2)$, what is $A \in \mathbb{N}$?' % num_l, [P], st, 6,
              mcq(P['latex'], num_distractors(K, [A, A + Bv, Bv])))

    B.fill(basic, 18); B.fill(expanded, 5); B.fill(exam_ln2, 7)


# =====================================================================
def by_parts(B):
    r = B.rng
    cyc = Cycle()

    def definite():
        k = cyc('d', 6); a = r.choice([1, 2, -1, 3]); nn = r.randint(1, 4); c = r.choice([1, 2])
        if k == 0:
            f, lo, hi, fg = x * exp(a * x), 0, c, (r'f = x', r"g' = %s" % L(exp(a * x)))
        elif k == 1:
            f, lo, hi, fg = x ** nn * log(x), 1, E, (r'f = \ln x', r"g' = x^{%d}" % nn)
        elif k == 2:
            aa = r.randint(1, 3); f, lo, hi, fg = x * sin(aa * x), 0, pi / aa, (r'f = x', r"g' = \sin(%s)" % L(aa * x))
        elif k == 3:
            f, lo, hi, fg = x * cos(x), 0, pi / c, (r'f = x', r"g' = \cos x")
        elif k == 4:
            kk = r.randint(1, 3); f, lo, hi, fg = log(x), 1, exp(kk), (r'f = \ln x', r"g' = 1")
        else:
            f, lo, hi, fg = x ** 2 * exp(x), 0, 1, (r'f = x^2', r"g' = e^x \text{ (twice)}")
        F = sp.simplify(integrate(f, x)); v = I(f, lo, hi)
        st = [r'Integration by parts with $%s$, $%s$ ($\int fg^{\prime} = fg - \int f^{\prime}g$).' % fg,
              r'Antiderivative: $%s$.' % L(F), r'Evaluate between $%s$ and $%s$: $%s$.' % (L(lo), L(hi), L(v))]
        P = P_num('Value:', v)
        B.add(r'Compute $\displaystyle\int_{%s}^{%s} %s\,dx$.' % (L(lo), L(hi), L(f)), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def qr():
        nn = r.randint(1, 3); fn = r.choice(['sin', 'cos']); a = r.choice([1, 1, 2, 3])
        f = a * u ** nn * (sin(u) if fn == 'sin' else cos(u))
        F = sp.expand(integrate(f, u))
        q = sp.simplify(F.coeff(sin(u))); rr = sp.simplify(F.coeff(cos(u)))
        assert sp.simplify(q * sin(u) + rr * cos(u) - F) == 0
        st = [r'Integrate by parts %s with $f$ the polynomial part (it lowers the degree each time).' % ('once' if nn == 1 else '%d times' % nn),
              r'$\displaystyle\int %s\,du = %s + C$.' % (L(f), L(F)),
              r'Collecting: $q(u) = %s$ and $r(u) = %s$.' % (L(q), L(rr))]
        B.add(r'We have $\displaystyle\int %s\,du = q(u)\sin(u) + r(u)\cos(u) + C$ for polynomials $q, r$. Determine $q(u)$ and $r(u)$.' % L(f),
              [P_expr('$q(u) =$', q, vars=('u',), sample={'u': [-2, 2]}), P_expr('$r(u) =$', rr, vars=('u',), sample={'u': [-2, 2]})], st, 5)

    def exam_full():
        nn = 2; A = r.choice([pi, pi / 2, 2 * pi])
        v = I(u ** 2 * sin(u), 0, A, u)
        st = [r'Substitute $u = e^x$, $du = e^x dx$: $e^{3x}\sin(e^x)dx = u^2\sin u\,du$, bounds $0$ to $%s$.' % L(A),
              r'By parts twice: $\int u^2\sin u\,du = -u^2\cos u + 2\int u\cos u\,du = 2u\sin u + (2 - u^2)\cos u + C$.',
              r'Evaluate at $%s$ and $0$: $%s$.' % (L(A), L(v))]
        B.add(r'Compute $\displaystyle\int_{-\infty}^{\ln(%s)} e^{3x}\sin(e^x)\,dx$ (substitute, then integrate by parts).' % L(A), [P_num('Value:', v)], st, 6, mcq(L(v), num_distractors(v)))

    def poly_exp():
        kk = r.choice([1, 2, 3, -1, -2, Q(1, 2)]); kk = sp.sympify(kk); deg = r.choice([1, 1, 2])
        f = x ** deg * exp(kk * x)
        F = integrate(f, x); p = sp.simplify(F / exp(kk * x))
        st = [r'By parts with $f = %s$, $g^{\prime} = %s$, so $g = %s$.' % (L(x ** deg), L(exp(kk * x)), L(exp(kk * x) / kk)),
              r'$\displaystyle\int %s\,dx = %s + C$.' % (L(f), L(sp.factor(F))), r'So $p(x) = %s$.' % L(p)]
        B.add(r'Find the polynomial $p(x)$ such that $\displaystyle\int %s\,dx = p(x)\,e^{%s} + C$.' % (L(f), L(kk * x)),
              [P_expr('$p(x) =$', p, sample={'x': [-2, 2]})], st, 4)

    def anti():
        k = cyc('a', 5); a = r.randint(1, 4)
        f = [x * log(x), x * cos(a * x), x * exp(-a * x), log(x) * a, x ** 2 * log(x)][k]
        F = integrate(f, x)
        P = P_expr(r'$\displaystyle\int f\,dx =$', F, sample={'x': [0.5, 3]}, upc=True)
        st = [r'Choose $f$ to be the factor that simplifies when differentiated (%s).' % ('$\\ln x$' if f.has(log) else '$x$'),
              r'Result: $%s + C$.' % L(F)]
        B.add(r'Compute $\displaystyle\int %s\,dx$ (the constant may be omitted).' % L(f), [P], st, 4, mcq(P['latex'], [L(sp.diff(f, x)) + ' + C', L(-F) + ' + C', L(F * 2) + ' + C', L(f * x) + ' + C']))

    B.fill(definite, 10); B.fill(qr, 8); B.fill(exam_full, 3); B.fill(poly_exp, 5); B.fill(anti, 5)
