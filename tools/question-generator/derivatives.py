"""Derivatives: rules, L'Hopital, implicit/tangent, partials, concavity, function analysis."""
from common import *
from sympy import sqrt, exp, log, sin, cos, tan, atan, pi, E, Abs

dfrac = lambda a, b: r'\dfrac{%s}{%s}' % (a, b)
POS = {'x': [0.4, 3]}


def nice(e):
    e = sp.nsimplify(sp.simplify(e))
    return e


# =====================================================================
def derivative_rules(B):
    r = B.rng
    cyc = Cycle()

    def product():
        k = cyc('p', 3)
        n_ = r.randint(1, 4); a = r.choice([1, 2, 3, -1, -2])
        if k == 0:
            U, V = x ** n_, exp(a * x)
        elif k == 1:
            U, V = x ** n_, sin(a * x)
        else:
            U, V = x ** n_, log(x)
        f = U * V; Up, Vp = sp.diff(U, x), sp.diff(V, x)
        fp = sp.factor(Up * V + U * Vp) if k != 1 else Up * V + U * Vp
        P = P_expr("$f'(x) =$", fp, sample=POS)
        st = [r'Product rule with $u = %s$, $v = %s$: $u^{\prime} = %s$, $v^{\prime} = %s$.' % (L(U), L(V), L(Up), L(Vp)),
              r"$f'(x) = u^{\prime}v + uv^{\prime} = %s + %s$." % (L(Up * V), L(U * Vp)),
              r'Simplified: $%s$.' % L(fp)]
        B.add(r'Differentiate $f(x) = %s$.' % L(f), [P], st, 3, mcq(P['latex'], [L(Up * Vp), L(Up * V), L(U * Vp), L(Up * V - U * Vp)]))

    def quotient():
        k = cyc('q', 3)
        if k == 0:
            a, b, c = r.choice([1, 2, 3]), r.randint(-4, 4), r.randint(1, 5)
            U, V = a * x + b, x ** 2 + c
        elif k == 1:
            a = r.randint(1, 4); U, V = exp(x), x + a
        else:
            n_ = r.randint(1, 3); U, V = log(x), x ** n_
        Up, Vp = sp.diff(U, x), sp.diff(V, x)
        fp = sp.factor(sp.simplify((Up * V - U * Vp) / V ** 2))
        P = P_expr("$f'(x) =$", fp, sample=POS)
        st = [r'Quotient rule with $u = %s$, $v = %s$: $u^{\prime} = %s$, $v^{\prime} = %s$.' % (L(U), L(V), L(Up), L(Vp)),
              r"$f'(x) = \dfrac{u^{\prime}v - uv^{\prime}}{v^2} = \dfrac{%s - %s}{%s}$." % (L(Up * V), L(U * Vp) if (U * Vp).could_extract_minus_sign() is False else '(' + L(U * Vp) + ')', L(V ** 2)),
              r'Simplified: $%s$.' % L(fp)]
        B.add(r'Differentiate $f(x) = %s$.' % L(U / V), [P], st, 3,
              mcq(P['latex'], [L(sp.factor((U * Vp - Up * V) / V ** 2)), L(Up / Vp), L(sp.factor((Up * V - U * Vp) / V))]))

    def chain():
        k = cyc('c', 6)
        a = r.choice([1, 2, 3, 4]); b = r.randint(1, 5); n_ = r.randint(2, 5)
        outer, inner = [(sin(u), a * x ** 2 + b), (log(u), x ** 2 + b), (sqrt(u), a * x ** 2 + b),
                        (exp(u), sin(a * x)), (u ** n_, x ** 2 + b), (tan(u), a * x)][k]
        f = outer.subs(u, inner)
        do = sp.diff(outer, u); di = sp.diff(inner, x)
        fp = sp.simplify(do.subs(u, inner) * di)
        P = P_expr("$f'(x) =$", fp, sample={'x': [0.2, 1.2]})
        st = [r'Chain rule: outer function $g(u) = %s$ with $g^{\prime}(u) = %s$, inner function $u = %s$ with $u^{\prime} = %s$.' % (L(outer), L(do), L(inner), L(di)),
              r"$f'(x) = g^{\prime}(u)\cdot u^{\prime} = %s$." % L(fp)]
        B.add(r'Differentiate $f(x) = %s$.' % L(f), [P], st, 3, mcq(P['latex'], [L(do.subs(u, inner)), L(do.subs(u, di)), L(sp.simplify(-fp)), L(sp.simplify(fp * 2))]))

    def logdiff():
        k = cyc('l', 5); a = r.choice([1, 2, 3])
        base, ex = [(x, a * x), (x, sin(x)), (x ** 2 + 1, x), (x, log(x)), (x, x ** 2 * a)][k]
        if k == 2:
            base = x ** 2 + a
        f = base ** ex
        lnf = ex * log(base)
        dl = sp.diff(lnf, x)
        fp = f * dl
        P = P_expr("$f'(x) =$", fp, sample={'x': [0.5, 2.5]})
        st = [r'Take logarithms: $\ln f(x) = %s$.' % L(lnf),
              r"Differentiate both sides: $\dfrac{f'(x)}{f(x)} = %s$." % L(dl),
              r"Multiply by $f(x)$: $f'(x) = %s\left(%s\right)$." % (L(f), L(dl))]
        B.add(r'Use logarithmic differentiation to find the derivative of $f(x) = %s$ (for $x > 0$).' % L(f), [P], st, 4,
              mcq(P['latex'], [L(ex * base ** (ex - 1)), L(f * log(base)), L(f * sp.diff(ex, x)), L(dl)]))

    def evaluate():
        k = cyc('e', 3)
        if k == 0:
            a = r.choice([3, 4, 5, 8, 12]); trip = {3: (4, 5), 4: (3, 5), 5: (12, 13), 8: (6, 10), 12: (5, 13)}[a]
            f = x ** 2 * sqrt(x ** 2 + trip[0] ** 2 if False else x ** 2 + (trip[1] ** 2 - a ** 2)); c = a
        elif k == 1:
            a = r.randint(1, 4); c = 0; f = (x + a) * exp(r.choice([1, 2, -1]) * x) * cos(x)
        else:
            a = r.randint(2, 5); c = 1; f = log(x ** 2 + a) * x ** r.randint(1, 3)
        fp = sp.diff(f, x); v = sp.simplify(fp.subs(x, c))
        P = P_num("$f'(%d) =$" % c, v)
        st = [r"$f'(x) = %s$ (product and chain rules)." % L(sp.simplify(fp)),
              r"Substitute $x = %d$: $f'(%d) = %s$." % (c, c, L(v))]
        B.add(r"Let $f(x) = %s$. Compute $f'(%d)$." % (L(f), c), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    def second():
        a = r.choice([1, 2, 3, -1, -2, 4]); k = cyc('s', 3)
        if k == 0:
            f = x * exp(a * x); c = 0
        elif k == 1:
            f = x ** 2 * log(x) * a; c = 1
        else:
            f = sin(a * x) * x; c = 0
        f2 = sp.diff(f, x, 2); v = sp.simplify(f2.subs(x, c))
        P = P_num("$f''(%d) =$" % c, v)
        st = [r"$f'(x) = %s$." % L(sp.simplify(sp.diff(f, x))), r"$f''(x) = %s$." % L(sp.simplify(f2)), r"$f''(%d) = %s$." % (c, L(v))]
        B.add(r"Let $f(x) = %s$. Compute $f''(%d)$." % (L(f), c), [P], st, 4, mcq(P['latex'], num_distractors(v)))

    B.fill(product, 6); B.fill(quotient, 6); B.fill(chain, 7); B.fill(logdiff, 5); B.fill(evaluate, 4); B.fill(second, 4)


# =====================================================================
def lhopital(B):
    r = B.rng
    cyc = Cycle()

    def zero_zero():
        k = cyc('z', 6); a = r.randint(1, 5); b = r.randint(1, 5)
        if k == 0:
            f = (exp(a * x) - 1 - a * x) / x ** 2; ans = Q(a * a, 2)
            st = [r'Form $\tfrac{0}{0}$. L\'Hôpital: $\lim \dfrac{%s - %d}{2x}$, still $\tfrac{0}{0}$.' % (L(a * exp(a * x)), a),
                  r'Again: $\lim \dfrac{%s}{2} = \dfrac{%d}{2}$.' % (L(a * a * exp(a * x)), a * a)]
        elif k == 1:
            f = (1 - cos(a * x)) / x ** 2; ans = Q(a * a, 2)
            st = [r'Form $\tfrac{0}{0}$. L\'Hôpital: $\lim \dfrac{%s}{2x}$ (still $\tfrac00$).' % L(a * sin(a * x)),
                  r'Again: $\lim \dfrac{%s}{2} = \dfrac{%d}{2}$.' % (L(a * a * cos(a * x)), a * a)]
        elif k == 2:
            if a == b:
                raise ValueError
            f = log(1 + a * x) / (b * x); ans = Q(a, b)
            st = [r'Form $\tfrac{0}{0}$. L\'Hôpital: $\lim_{x\to0} \dfrac{%d/(1+%dx)}{%d} = \dfrac{%d}{%d}$.' % (a, a, b, a, b)]
        elif k == 3:
            a, b = r.sample([2, 3, 5, 7, 10], 2)
            f = (sp.Integer(a) ** x - sp.Integer(b) ** x) / x; ans = log(a) - log(b)
            st = [r'Form $\tfrac{0}{0}$. Using $(c^x)^{\prime} = c^x\ln c$: $\lim_{x\to0} (%d^x\ln %d - %d^x\ln %d) = \ln %d - \ln %d = \ln\tfrac{%d}{%d}$.' % (a, a, b, b, a, b, a, b)]
        elif k == 4:
            f = (a * x - sin(a * x)) / x ** 3; ans = Q(a ** 3, 6)
            st = [r'Form $\tfrac00$; apply L\'Hôpital three times.',
                  r'$\lim \dfrac{%d - %s}{3x^2} = \lim\dfrac{%s}{6x} = \lim\dfrac{%s}{6} = %s$.' % (a, L(a * cos(a * x)), L(a * a * sin(a * x)), L(a ** 3 * cos(a * x)), L(ans))]
        else:
            f = (exp(a * x) - exp(-b * x)) / x; ans = a + b
            st = [r'Form $\tfrac00$. L\'Hôpital: $\lim_{x\to0}(%s + %s) = %d + %d = %d$.' % (L(a * exp(a * x)), L(b * exp(-b * x)), a, b, a + b)]
        ans = sp.simplify(ans)
        assert sp.simplify(sp.limit(f, x, 0) - ans) == 0
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to 0} %s$.' % L(f), [P], st, 4, mcq(P['latex'], num_distractors(ans, [0, oo])))

    def one_inf():
        k = cyc('o', 5); a = r.choice([1, 2, 3, -1, -2]); b = r.choice([1, 2, 3, 4])
        if k == 0:
            f = (1 + sp.Integer(a) / x) ** (b * x); pt = oo; lnL = a * b
            st = [r'Form $1^\infty$. Take logs: $\ln L = \lim_{x\to\infty} %dx\ln(1 + \tfrac{%d}{x})$, form $\infty\cdot0$.' % (b, a),
                  r'Rewrite as $\lim \dfrac{\ln(1 + %d/x)}{1/(%dx)}$ and apply L\'Hôpital: $\lim \dfrac{\frac{-%d/x^2}{1+%d/x}}{-1/(%dx^2)} = \lim \dfrac{%d}{1 + %d/x} = %d$.' % (a, b, a, a, b, a * b, a, a * b)]
        elif k == 1:
            f = (1 + a * x) ** (1 / (b * x)); pt = 0; lnL = Q(a, b)
            st = [r'Form $1^\infty$. $\ln L = \lim_{x\to0}\dfrac{\ln(1+%dx)}{%dx}$, form $\tfrac00$.' % (a, b),
                  r'L\'Hôpital: $\lim \dfrac{%d/(1+%dx)}{%d} = %s$.' % (a, a, b, L(Q(a, b)))]
        elif k == 2:
            c = r.choice([1, 2]) * pi
            f = (x / c) ** (1 / sin(x)); pt = c; lnL = 1 / (c * cos(c))
            st = [r'Form $1^\infty$. $\ln L = \lim_{x\to%s}\dfrac{\ln(x/%s)}{\sin x}$, form $\tfrac00$.' % (L(c), L(c)),
                  r'L\'Hôpital: $\lim \dfrac{1/x}{\cos x} = \dfrac{1/%s}{%s} = %s$.' % (L(c), L(cos(c)), L(lnL))]
        elif k == 3:
            f = cos(b * x) ** (1 / x ** 2); pt = 0; lnL = -Q(b * b, 2)
            flat = r'\left(\cos(%s)\right)^{1/x^2}' % L(b * x)
            st = [r'Form $1^\infty$. $\ln L = \lim_{x\to0}\dfrac{\ln\cos(%dx)}{x^2}$, form $\tfrac00$.' % b,
                  r'L\'Hôpital: $\lim\dfrac{-%d\tan(%dx)}{2x}$; again: $\lim\dfrac{-%d/\cos^2(%dx)}{2} = %s$.' % (b, b, b * b, b, L(lnL))]
        else:
            c = r.randint(1, 5)
            f = (x / c) ** (1 / (x - c)); pt = c; lnL = Q(1, c)
            st = [r'Form $1^\infty$. $\ln L = \lim_{x\to%d}\dfrac{\ln(x/%d)}{x-%d}$, form $\tfrac00$.' % (c, c, c),
                  r'L\'Hôpital: $\lim \dfrac{1/x}{1} = %s$.' % L(Q(1, c))]
        ans = exp(lnL)
        st.append(r'Hence $L = e^{\ln L} = %s$.' % L(ans))
        P = P_num('$L =$', ans)
        pl = r'\infty' if pt == oo else L(pt)
        dis = [L(exp(-lnL)), '1', 'e', L(exp(2 * lnL)), r'\text{does not exist}', L(lnL), L(exp(1 / lnL)) if lnL != 0 else '0']
        B.add(r'Compute $L = \lim_{x\to %s} %s$.' % (pl, flat if k == 3 else L(f)), [P], st, 5, mcq(P['latex'], dis))

    def zero_inf():
        k = cyc('i', 3); a = r.randint(1, 7)
        if k == 0:
            fl = r'x\sin\!\left(\dfrac{%d}{x}\right)' % a; pl = r'\infty'; ans = a
            st = [r'Form $\infty\cdot 0$. Write as $\dfrac{\sin(%d/x)}{1/x}$ (form $\tfrac00$).' % a,
                  r'L\'Hôpital: $\dfrac{\cos(%d/x)\cdot(-%d/x^2)}{-1/x^2} = %d\cos(%d/x) \to %d$.' % (a, a, a, a, a)]
        elif k == 1:
            fl = r'x\left(e^{%d/x} - 1\right)' % a; pl = r'\infty'; ans = a
            st = [r'Form $\infty\cdot0$. Write as $\dfrac{e^{%d/x}-1}{1/x}$.' % a,
                  r'L\'Hôpital: $\dfrac{e^{%d/x}(-%d/x^2)}{-1/x^2} = %d e^{%d/x}\to %d$.' % (a, a, a, a, a)]
        else:
            b = r.choice([2, 3, 4, 6]); fl = r't^{%d}\ln(%dt^2)' % (r.choice([1, 2]), b); pl = '0^+'; ans = 0
            st = [r'Form $0\cdot(-\infty)$. Write as $\dfrac{\ln(%dt^2)}{t^{-n}}$ (form $\tfrac{-\infty}{\infty}$).' % b,
                  r'L\'Hôpital: $\dfrac{2/t}{-n t^{-n-1}} = -\dfrac{2}{n}t^{n} \to 0$.']
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{%s\to %s} %s$.' % ('t' if k == 2 else 'x', pl, fl), [P], st, 4, mcq(P['latex'], num_distractors(ans, [0, oo, 1])))

    def inf_minus_inf():
        k = cyc('m', 2); a = r.randint(1, 8)
        if k == 0:
            f = a / log(x) - a / (x - 1); pt = 1
            st = [r'Form $\infty-\infty$. Combine: $%d\cdot\dfrac{x - 1 - \ln x}{(x-1)\ln x}$, form $\tfrac00$.' % a,
                  r'L\'Hôpital: $%d\cdot\dfrac{1 - 1/x}{\ln x + (x-1)/x} = %d\cdot\dfrac{x-1}{x\ln x + x - 1}$, still $\tfrac00$.' % (a, a),
                  r'Again: $%d\cdot\dfrac{1}{\ln x + 1 + 1} \to \dfrac{%d}{2}$.' % (a, a)]
        else:
            f = a / x - a / (exp(x) - 1); pt = 0
            st = [r'Form $\infty-\infty$. Combine: $%d\cdot\dfrac{e^x - 1 - x}{x(e^x-1)}$, form $\tfrac00$.' % a,
                  r'L\'Hôpital: $%d\cdot\dfrac{e^x - 1}{e^x - 1 + xe^x}$, still $\tfrac00$.' % a,
                  r'Again: $%d\cdot\dfrac{e^x}{2e^x + xe^x} \to \dfrac{%d}{2}$.' % (a, a)]
        ans = Q(a, 2)
        assert sp.simplify(sp.limit(f, x, pt) - ans) == 0
        P = P_num('$L =$', ans)
        B.add(r'Compute $L = \lim_{x\to %d}\left(%s\right)$.' % (pt, L(f)), [P], st, 5, mcq(P['latex'], num_distractors(ans, [0, oo])))

    def param():
        k = cyc('pa', 3); kk = r.randint(1, 5)
        if k == 0:
            f = (exp(kk * x) - 1 - sp.Symbol('a') * x) / x ** 2; aval = kk; Lv = Q(kk * kk, 2)
            st = [r'Numerator and denominator both $\to0$. After one L\'Hôpital step: $\dfrac{%s - a}{2x}$.' % L(kk * exp(kk * x)),
                  r'For a finite limit the new numerator must vanish at $0$: $%d - a = 0$, so $a = %d$.' % (kk, kk),
                  r'Then once more: $\lim\dfrac{%s}{2} = %s$.' % (L(kk * kk * exp(kk * x)), L(Lv))]
        elif k == 1:
            f = (sin(kk * x) - sp.Symbol('a') * x) / x ** 3; aval = kk; Lv = -Q(kk ** 3, 6)
            st = [r'L\'Hôpital once: $\dfrac{%s - a}{3x^2}$; finiteness forces $%d - a = 0$, so $a=%d$.' % (L(kk * cos(kk * x)), kk, kk),
                  r'Then $\lim\dfrac{%s}{6x} = \lim\dfrac{%s}{6} = %s$.' % (L(-kk ** 2 * sin(kk * x)), L(-kk ** 3 * cos(kk * x)), L(Lv))]
        else:
            f = (log(1 + kk * x) - sp.Symbol('a') * x) / x ** 2; aval = kk; Lv = -Q(kk * kk, 2)
            st = [r'L\'Hôpital once: $\dfrac{\frac{%d}{1+%dx} - a}{2x}$; finiteness forces $%d - a = 0$, so $a = %d$.' % (kk, kk, kk, kk),
                  r'Then $\lim\dfrac{-%d/(1+%dx)^2}{2} = %s$.' % (kk * kk, kk, L(Lv))]
        assert sp.simplify(sp.limit(f.subs(sp.Symbol('a'), aval), x, 0) - Lv) == 0
        B.add(r'For which value of $a$ is $L = \lim_{x\to0} %s$ finite? Give $a$ and the value of $L$.' % L(f),
              [P_num('$a =$', aval), P_num('$L =$', Lv)], st, 6)

    def abc():
        d0 = r.randint(1, 5); Lt = r.randint(1, 4)
        A = 2 * Lt - d0; Bv = -A; C = d0
        if A == 0:
            raise ValueError
        expr = (A * pi * tan(pi * x) + Bv * pi ** 2 * log(x) + C * cos(pi * x) + d0) / (pi ** 2 * (x - 1) ** 2)
        assert sp.simplify(sp.limit(expr, x, 1) - Lt) == 0
        st = [r'The denominator $\to 0$, so the numerator must $\to 0$ too: $C\cos\pi + %d = 0 \Rightarrow C = %d$.' % (d0, d0),
              r"L'Hôpital: $\dfrac{\frac{A\pi^2}{\cos^2(\pi x)} + \frac{B\pi^2}{x} - C\pi\sin(\pi x)}{2\pi^2(x-1)}$; the numerator must vanish at $x=1$: $A\pi^2 + B\pi^2 = 0 \Rightarrow B = -A$.",
              r"L'Hôpital again and evaluate at $x = 1$: $\dfrac{0 - B\pi^2 + C\pi^2}{2\pi^2} = \dfrac{C - B}{2} = \dfrac{%d + A}{2}$." % d0,
              r'Setting this equal to $%d$: $A = %d$, $B = %d$, $C = %d$.' % (Lt, A, Bv, C)]
        B.add(r'If $\displaystyle\lim_{x\to1} \dfrac{A\pi\tan(\pi x) + B\pi^2\ln(x) + C\cos(\pi x) + %d}{\pi^2(x-1)^2} = %d$, what are $A, B, C \in \mathbb{Z}$?' % (d0, Lt),
              [P_num('$A =$', A), P_num('$B =$', Bv), P_num('$C =$', C)], st, 6)

    B.fill(zero_zero, 9); B.fill(one_inf, 9); B.fill(zero_inf, 4); B.fill(inf_minus_inf, 3); B.fill(param, 4); B.fill(abc, 3)


# =====================================================================
def implicit_tangent(B):
    r = B.rng
    cyc = Cycle()

    def implicit_line():
        k = cyc('f', 5)
        x0, y0 = r.choice([-2, -1, 1, 2]), r.choice([-2, -1, 1, 2]); a = r.choice([1, 2, 3, -1])
        G = [x * (a + 1 - x ** 2 - y ** 2), x ** 2 + a * x * y + y ** 2, x ** 3 + y ** 3 - a * x * y, y ** 2 - x ** 3 - a * x, x ** 2 * y + a * y ** 3][k]
        C = G.subs({x: x0, y: y0})
        F = G - C
        Fx, Fy = sp.diff(F, x), sp.diff(F, y)
        fy0 = Fy.subs({x: x0, y: y0})
        if fy0 == 0:
            raise ValueError
        mm = -Fx.subs({x: x0, y: y0}) / fy0; b = y0 - mm * x0
        eq = r'%s = %s' % (L(G), L(C))
        st = [r"Differentiate both sides with respect to $x$, treating $y$ as $y(x)$: $%s + \left(%s\right)\dfrac{dy}{dx} = 0$." % (L(Fx), L(Fy)),
              r'So $\dfrac{dy}{dx} = -\dfrac{%s}{%s}$.' % (L(Fx), L(Fy)),
              r'At $(%d, %d)$: $m = -\dfrac{%s}{%s} = %s$.' % (x0, y0, L(Fx.subs({x: x0, y: y0})), L(fy0), L(mm)),
              r'Slope-point form: $y - (%d) = %s(x - (%d))$, so $b = %d - %s\cdot(%d) = %s$.' % (y0, L(mm), x0, y0, L(mm), x0, L(b))]
        B.add(r'Given is the implicit equation $%s$. Compute the slope $m$ and intercept $b$ of the tangent line $y = mx + b$ through the point $(x, y) = (%d, %d)$.' % (eq, x0, y0),
              [P_num('$m =$', mm), P_num('$b =$', b)], st, 6)

    def explicit_line():
        k = cyc('e', 5)
        n_ = r.randint(1, 3); a = r.randint(1, 4)
        f, c = [(x ** n_ * exp(x - 1), 1), (x ** n_ * log(x) + a * x, 1), pyth(r),
                (dfrac_e(a, n_), 0), (x ** 3 - a * x ** 2 + n_, r.randint(-2, 2))][k]
        if not f.has(x) or sp.simplify(sp.diff(f, x)) == 0:
            raise ValueError
        fp = sp.diff(f, x); mm = sp.simplify(fp.subs(x, c)); fc = sp.simplify(f.subs(x, c)); b = sp.simplify(fc - mm * c)
        st = [r"$f'(x) = %s$." % L(sp.simplify(fp)),
              r"Slope: $m = f'(%d) = %s$; point: $f(%d) = %s$." % (c, L(mm), c, L(fc)),
              r'Tangent: $y - %s = %s(x - %d)$, so $b = %s - %s\cdot %d = %s$.' % (L(fc), L(mm), c, L(fc), L(mm), c, L(b))]
        B.add(r'Determine the tangent line $y = mx + b$ to the graph of $f(x) = %s$ at $x = %d$.' % (L(f), c),
              [P_num('$m =$', mm), P_num('$b =$', b)], st, 4)

    def dydx():
        k = cyc('d', 4); a = r.choice([1, 3, 4, 5]); c = r.randint(1, 9)
        G = [x ** 2 + a * x * y + y ** 2, x ** 3 + y ** 3 - a * x * y, x * y ** 2 + a * x ** 2, sin(x * y) + a * y][k]
        Fx, Fy = sp.diff(G, x), sp.diff(G, y)
        der = sp.simplify(-Fx / Fy)
        P = P_expr(r'$\dfrac{dy}{dx} =$', der, vars=('x', 'y'), sample={'x': [0.3, 1.5], 'y': [0.3, 1.5]})
        st = [r"Differentiate implicitly: $%s + \left(%s\right) y^{\prime} = 0$." % (L(Fx), L(Fy)),
              r"Solve for $y^{\prime}$: $\dfrac{dy}{dx} = %s$." % L(der)]
        B.add(r'The curve $%s = %d$ defines $y$ implicitly as a function of $x$. Find $\dfrac{dy}{dx}$ in terms of $x$ and $y$.' % (L(G), c),
              [P], st, 4, mcq(P['latex'], [L(sp.simplify(Fx / Fy)), L(sp.simplify(-Fy / Fx)), L(sp.simplify(-Fx)), L(sp.simplify(Fx / Fy + 1))]))

    B.fill(implicit_line, 13); B.fill(explicit_line, 9); B.fill(dydx, 8)


def pyth(r):
    c, k = r.choice([(3, 16), (4, 9), (5, 144), (6, 64), (8, 36), (12, 25)])
    return (sqrt(x ** 2 + k), c)


def dfrac_e(a, n_):
    return (a * x + n_) / (x + 1)


# =====================================================================
def partial_derivatives(B):
    r = B.rng
    cyc = Cycle()

    def exam_style():
        nn = r.randint(1, 5)
        f = x ** y / E ** (nn - 1)
        fxy = sp.diff(f, x, y)
        v = sp.simplify(fxy.subs({x: E, y: nn}))
        st = [r'Write $x^y = e^{y\ln x}$. Then $\dfrac{\partial}{\partial y} x^y = x^y\ln x$.',
              r'$\dfrac{\partial}{\partial x}\left(x^y\ln x\right) = yx^{y-1}\ln x + x^y\cdot\dfrac1x = x^{y-1}(y\ln x + 1)$.',
              r'So $\dfrac{\partial^2 f}{\partial x\partial y} = \dfrac{x^{y-1}(y\ln x + 1)}{e^{%d}}$.' % (nn - 1),
              r'At $(e, %d)$: $\dfrac{e^{%d}(%d + 1)}{e^{%d}} = %s$.' % (nn, nn - 1, nn, nn - 1, L(v))]
        P1 = P_expr(r'$\dfrac{\partial^2 f}{\partial x\,\partial y} =$', fxy, vars=('x', 'y'), sample={'x': [0.5, 3], 'y': [0.5, 3]})
        B.add(r'Let $f(x, y) = %s$. Determine $\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y} f(x, y)$ and use it to compute its value at $(e, %d)$.' % (L(f), nn),
              [P1, P_num('Value at $(e,%d)$:' % nn, v)], st, 5)

    def mixed():
        k = cyc('m', 6); a = r.randint(1, 4); b = r.randint(1, 3)
        f = [x ** 2 * y ** 3 + a * x * y, exp(a * x * y), sin(a * x + b * y), log(x ** 2 + y ** 2), x * exp(b * y) + y * exp(a * x), x ** a * y ** (b + 1)][k]
        x0, y0 = r.choice([1, 2, -1]), r.choice([1, 2, 0, -1])
        if k == 3 and x0 == 0 and y0 == 0:
            raise ValueError
        fx = sp.diff(f, x); fxy = sp.diff(fx, y)
        v = sp.simplify(fxy.subs({x: x0, y: y0}))
        st = [r'$\dfrac{\partial f}{\partial x} = %s$ (treat $y$ as a constant).' % L(sp.simplify(fx)),
              r'$\dfrac{\partial^2 f}{\partial y\,\partial x} = %s$ (by Schwarz the order does not matter).' % L(sp.simplify(fxy)),
              r'At $(%d, %d)$: $%s$.' % (x0, y0, L(v))]
        B.add(r'Let $f(x, y) = %s$. Compute $\dfrac{\partial f}{\partial x}$ and $\dfrac{\partial^2 f}{\partial x\,\partial y}(%d, %d)$.' % (L(f), x0, y0),
              [P_expr(r'$\dfrac{\partial f}{\partial x} =$', fx, vars=('x', 'y'), sample={'x': [0.5, 2], 'y': [0.5, 2]}), P_num('Mixed partial at the point:', v)], st, 5)

    def grad():
        k = cyc('g', 5); a = r.randint(1, 4)
        f = [x ** 3 * y - a * x * y ** 2, x * log(y) + y ** 2, exp(x) * cos(y) + a * x, sqrt(x ** 2 + y ** 2), x / (y + a)][k]
        pts = [(1, 2), (2, 1), (0, 0), (3, 4), (2, 1)]
        x0, y0 = pts[k] if k != 1 else (r.randint(1, 3), 1)
        if k == 0:
            x0, y0 = r.choice([(1, 2), (2, 1), (-1, 1), (1, -1)])
        fx, fy = sp.diff(f, x), sp.diff(f, y)
        vx, vy = sp.simplify(fx.subs({x: x0, y: y0})), sp.simplify(fy.subs({x: x0, y: y0}))
        st = [r'$f_x = %s$, so $f_x(%d,%d) = %s$.' % (L(fx), x0, y0, L(vx)), r'$f_y = %s$, so $f_y(%d,%d) = %s$.' % (L(fy), x0, y0, L(vy))]
        B.add(r'Let $f(x,y) = %s$. Compute both first-order partial derivatives at $(%d, %d)$.' % (L(f), x0, y0),
              [P_num(r'$\dfrac{\partial f}{\partial x}(%d,%d) =$' % (x0, y0), vx), P_num(r'$\dfrac{\partial f}{\partial y}(%d,%d) =$' % (x0, y0), vy)], st, 4)

    def pde():
        k = cyc('p', 2); c = r.randint(2, 6); a = r.randint(1, 4)
        if k == 0:
            f = sin(x - c * t) + (x + c * t) ** 2; ans = c * c
            st = [r'$f_{xx} = -\sin(x - %dt) + 2$.' % c, r'$f_{tt} = -%d\sin(x-%dt) + %d$.' % (c * c, c, 2 * c * c), r'So $f_{tt} = %d\,f_{xx}$, i.e. $k = %d$.' % (c * c, c * c)]
            prm = r'f_{tt} = k\,f_{xx}'
        else:
            f = exp(-c * t) * sin(a * x); ans = Q(c, a * a)
            st = [r'$f_t = -%d e^{-%dt}\sin(%dx)$.' % (c, c, a), r'$f_{xx} = -%d e^{-%dt}\sin(%dx)$.' % (a * a, c, a), r'So $f_t = %s f_{xx}$, i.e. $k = %s$.' % (L(Q(c, a * a)), L(Q(c, a * a)))]
            prm = r'f_t = k\,f_{xx}'
        B.add(r'Let $f(x,t) = %s$. Find the constant $k$ such that $%s$ for all $x, t$.' % (L(f), prm), [P_num('$k =$', ans)], st, 4, mcq(L(ans), num_distractors(ans, [c, a])))

    B.fill(exam_style, 5); B.fill(mixed, 11); B.fill(grad, 8); B.fill(pde, 6)


# =====================================================================
TF = [
    (r'If $f$ has an inflection point at $a$ and $f^{\prime\prime}$ exists near $a$, then $f^{\prime\prime}(a) = 0$.', True, r'At an inflection point $f^{\prime\prime}$ changes sign; if it exists and is continuous it must pass through $0$.'),
    (r'If $f^{\prime\prime}(a) = 0$, then $f$ has an inflection point at $a$.', False, r'Counterexample: $f(x) = x^4$ has $f^{\prime\prime}(0) = 0$ but is convex everywhere — no change of concavity.'),
    (r'If $f^{\prime\prime}(x) > 0$ for all $x\in(a,b)$, then $f$ is convex on $(a,b)$.', True, r'This is exactly the second-derivative test for convexity.'),
    (r'$f(x) = x^3$ has an inflection point at $x = 0$.', True, r'$f^{\prime\prime}(x) = 6x$ changes sign at $0$.'),
    (r'$f(x) = x^4$ has an inflection point at $x = 0$.', False, r'$f^{\prime\prime}(x) = 12x^2 \ge 0$ never changes sign.'),
    (r'$f(x) = e^x$ is concave on $\mathbb{R}$.', False, r'$f^{\prime\prime}(x) = e^x > 0$, so it is convex.'),
    (r'$f(x) = \ln x$ is concave on $(0,\infty)$.', True, r'$f^{\prime\prime}(x) = -1/x^2 < 0$.'),
    (r'If $f$ and $g$ are convex on $(a,b)$ (and twice differentiable), then $f + g$ is convex on $(a,b)$.', True, r'$(f+g)^{\prime\prime} = f^{\prime\prime} + g^{\prime\prime} \ge 0$.'),
    (r'If $f^{\prime}(a) = 0$ and $f^{\prime\prime}(a) < 0$, then $f$ has a local maximum at $a$.', True, r'Second-derivative test for extrema.'),
    (r'If $f$ is concave and differentiable on $(a,b)$, then $f^{\prime}$ is decreasing on $(a,b)$.', True, r'Concave means $f^{\prime\prime}\le0$, i.e. $f^{\prime}$ decreasing.'),
    (r'$f(x) = \sin x$ has an inflection point at $x = \pi$.', True, r'$f^{\prime\prime}(x) = -\sin x$ changes sign at $\pi$.'),
    (r'$f(x) = \dfrac{1}{x}$ has an inflection point at $x = 0$.', False, r'Concavity changes at $0$, but $0$ is not in the domain, so it is not an inflection point.'),
]


def concavity(B):
    r = B.rng
    cyc = Cycle()

    def quartic():
        p, q = sorted(r.sample(range(-4, 5), 2)); c1 = r.randint(-5, 5)
        f = x ** 4 - 2 * (p + q) * x ** 3 + 6 * p * q * x ** 2 + c1 * x
        f2 = sp.factor(sp.diff(f, x, 2))
        ask_concave = r.random() < 0.5
        s = Interval.open(p, q) if ask_concave else Union(Interval.open(-oo, p), Interval.open(q, oo))
        P1 = P_int('%s on:' % ('Concave' if ask_concave else 'Convex'), s); P2 = P_set('Inflection points ($x$-values):', [p, q])
        st = [r"$f'(x) = %s$, $f''(x) = %s = %s$." % (L(sp.diff(f, x)), L(sp.expand(f2)), L(f2)),
              r"$f'' < 0$ between the zeros $%d$ and $%d$ (concave there) and $f'' > 0$ outside (convex)." % (p, q),
              r'$f^{\prime\prime}$ changes sign at both zeros, so the inflection points are at $x = %d$ and $x = %d$.' % (p, q)]
        B.add(r'Let $f(x) = %s$. On which (largest open) set is $f$ %s, and where are its inflection points?' % (L(f), 'concave' if ask_concave else 'convex'),
              [P1, P2], st, 5)

    def xexp():
        a = r.choice([1, 2, 3, 4, Q(1, 2)])
        f = x * exp(-a * x); ip = 2 / sp.sympify(a)
        st = [r"$f'(x) = %s$." % L(sp.factor(sp.diff(f, x))), r"$f''(x) = %s$." % L(sp.factor(sp.diff(f, x, 2))),
              r"$f''(x) = 0 \iff x = %s$; $f'' < 0$ for $x < %s$ and $f'' > 0$ for $x > %s$." % (L(ip), L(ip), L(ip))]
        B.add(r'Let $f(x) = %s$. Give the largest open interval on which $f$ is convex, and the inflection point.' % L(f),
              [P_int('Convex on:', Interval.open(ip, oo)), P_num('Inflection at $x =$', ip)], st, 4)

    def lnquad():
        a = r.randint(1, 6)
        f = log(x ** 2 + a * a)
        st = [r"$f'(x) = \dfrac{2x}{x^2 + %d}$." % (a * a), r"$f''(x) = \dfrac{2(x^2 + %d) - 4x^2}{(x^2+%d)^2} = \dfrac{2(%d - x^2)}{(x^2+%d)^2}$." % (a * a, a * a, a * a, a * a),
              r"$f'' > 0 \iff x^2 < %d \iff -%d < x < %d$: convex there, concave outside; inflection points at $x = \pm %d$." % (a * a, a, a, a)]
        B.add(r'Let $f(x) = %s$. On which (largest open) interval is $f$ convex, and what are the $x$-coordinates of its inflection points?' % L(f),
              [P_int('Convex on:', Interval.open(-a, a)), P_set('Inflection points:', [-a, a])], st, 5)

    def recip():
        a = r.randint(1, 5)
        f = 1 / (x ** 2 + a * a); ipv = a / sqrt(3)
        f2 = sp.factor(sp.diff(f, x, 2))
        st = [r"$f''(x) = %s$." % L(f2), r"$f''(x) = 0 \iff 3x^2 = %d \iff x = \pm %s$, and $f''$ changes sign there." % (a * a, L(ipv))]
        B.add(r'Determine the $x$-coordinates of the inflection points of $f(x) = %s$.' % L(f), [P_set('Inflection points:', [-ipv, ipv])], st, 4)

    def cubic():
        p = r.randint(-3, 4); c1 = r.randint(-6, 6); sgn = r.choice([1, -1])
        f = sgn * (x ** 3 - 3 * p * x ** 2) + c1 * x
        f2 = sp.diff(f, x, 2)
        s = Interval.open(-oo, p) if sgn == 1 else Interval.open(p, oo)
        st = [r"$f''(x) = %s$, zero at $x = %d$." % (L(sp.factor(f2)), p), r"$f'' < 0$ on $%s$, so $f$ is concave there; the sign change makes $x = %d$ an inflection point." % (interval_latex(set_to_intervals(s)), p)]
        B.add(r'Let $f(x) = %s$. On which (largest open) interval is $f$ concave, and where is the inflection point?' % L(f),
              [P_int('Concave on:', s), P_num('Inflection at $x =$', p)], st, 4)

    def gauss():
        s_ = r.choice([1, 2, 3, 4, 9]); f = exp(-x ** 2 / (2 * s_))
        st = [r"$f''(x) = %s$." % L(sp.factor(sp.diff(f, x, 2))), r'This vanishes and changes sign at $x^2 = %d$, i.e. $x = \pm %s$.' % (s_, L(sqrt(s_)))]
        B.add(r'Give the $x$-coordinates of the inflection points of $f(x) = %s$.' % L(f), [P_set('Inflection points:', [-sqrt(s_), sqrt(s_)])], st, 4)

    i = [0]

    def tf():
        stt, truth, why = TF[i[0] % len(TF)]; i[0] += 1
        B.add(r'True or false? %s' % stt, [P_choice('Statement is:', ['True', 'False'], 0 if truth else 1)], [why], 3)

    B.fill(quartic, 8); B.fill(xexp, 4); B.fill(lnquad, 3); B.fill(recip, 3); B.fill(cubic, 3); B.fill(gauss, 3); B.fill(tf, len(TF))


# =====================================================================
def function_analysis(B):
    r = B.rng
    cyc = Cycle()

    def crit_sqrt():
        k = r.randint(2, 9); form = cyc('c', 2)
        if form == 0:
            f = sqrt(x) / (1 + k * x); cp = [0, Q(1, k)]
            st = [r"$f'(x) = \dfrac{\frac{1}{2\sqrt x}(1 + %dx) - \sqrt x\cdot %d}{(1+%dx)^2} = \dfrac{1 - %dx}{2\sqrt{x}(1+%dx)^2}$." % (k, k, k, k, k),
                  r"$f'(x) = 0 \iff x = %s$; $f'$ does not exist at $x = 0$ (it tends to $\infty$)." % L(Q(1, k))]
        else:
            f = sqrt(x) / (k + x); cp = [0, k]
            st = [r"$f'(x) = \dfrac{\frac{1}{2\sqrt x}(%d + x) - \sqrt x}{(%d+x)^2} = \dfrac{%d - x}{2\sqrt{x}(%d+x)^2}$." % (k, k, k, k),
                  r"$f'(x) = 0 \iff x = %d$; $f'$ does not exist at $x = 0$." % k]
        st.append(r'Critical points: $%s$.' % set_latex(cp))
        P = P_set('Critical points:', cp)
        B.add(r'Give all critical points of $f(x) = %s$ on the domain $D_f = [0, \infty)$, i.e. all points where $f^{\prime}(x) = 0$ or where the derivative does not exist.' % L(f),
              [P], st, 5, mcq(P['latex'], [set_latex([cp[1]]), set_latex([0]), set_latex([0, 2 * cp[1]]), set_latex([0, 1 / cp[1]]) if cp[1] != 1 else r'\{0, 2\}']))

    def cubic_ext():
        p, q = sorted(r.sample(range(-4, 5), 2)); c = r.randint(-5, 5); sgn = r.choice([1, -1])
        f = sgn * (2 * x ** 3 - 3 * (p + q) * x ** 2 + 6 * p * q * x) + c
        fp = sp.factor(sp.diff(f, x))
        mx, mn = (p, q) if sgn == 1 else (q, p)
        st = [r"$f'(x) = %s$, zero at $x = %d$ and $x = %d$." % (L(fp), p, q),
              r"$f''(x) = %s$: $f''(%d) = %s$ and $f''(%d) = %s$." % (L(sp.diff(f, x, 2)), p, L(sp.diff(f, x, 2).subs(x, p)), q, L(sp.diff(f, x, 2).subs(x, q))),
              r'Negative second derivative ⇒ local maximum, positive ⇒ local minimum: max at $x = %d$, min at $x = %d$.' % (mx, mn)]
        B.add(r'Let $f(x) = %s$. Determine the $x$-coordinates of the local maximum and the local minimum.' % L(f),
              [P_num('Local max at $x =$', mx), P_num('Local min at $x =$', mn)], st, 4)

    def abs_ext():
        p, q = sorted(r.sample(range(-2, 4), 2)); a = p - r.randint(1, 2); b = q + r.randint(1, 2); c = r.randint(-3, 3)
        f = 2 * x ** 3 - 3 * (p + q) * x ** 2 + 6 * p * q * x + c
        cand = {v: f.subs(x, v) for v in (a, p, q, b)}
        mxv, mnv = max(cand.values()), min(cand.values())
        st = [r"$f'(x) = %s$: critical points $%d, %d$ (both in $[%d, %d]$)." % (L(sp.factor(sp.diff(f, x))), p, q, a, b),
              r'Evaluate at critical points and endpoints: ' + ', '.join(r'$f(%d) = %s$' % (v, L(cand[v])) for v in (a, p, q, b)) + '.',
              r'Absolute maximum $%s$, absolute minimum $%s$.' % (L(mxv), L(mnv))]
        B.add(r'Determine the absolute maximum and minimum values of $f(x) = %s$ on $[%d, %d]$.' % (L(f), a, b),
              [P_num('Absolute max value:', mxv), P_num('Absolute min value:', mnv)], st, 5)

    def xexp():
        a = r.choice([1, 2, 3, 4, 5, Q(1, 2), Q(1, 3)]); a = sp.sympify(a)
        f = x * exp(-a * x)
        st = [r"$f'(x) = %s$." % L(sp.factor(sp.diff(f, x))), r"$f'(x) = 0 \iff x = %s$; $f'$ changes from $+$ to $-$: maximum." % L(1 / a),
              r'Value: $f(%s) = %s$.' % (L(1 / a), L(sp.simplify(f.subs(x, 1 / a))))]
        B.add(r'Find the location and value of the global maximum of $f(x) = %s$.' % L(f),
              [P_num('Maximum at $x =$', 1 / a), P_num('Maximum value:', sp.simplify(f.subs(x, 1 / a)))], st, 4)

    def xnln():
        n_ = r.randint(1, 4); f = x ** n_ * log(x); xm = exp(-Q(1, n_)); v = sp.simplify(f.subs(x, xm))
        st = [r"$f'(x) = %s = x^{%d}(%d\ln x + 1)$." % (L(sp.diff(f, x)), n_ - 1, n_) if n_ > 1 else r"$f'(x) = \ln x + 1$.",
              r"$f'(x) = 0 \iff \ln x = -\tfrac{1}{%d} \iff x = %s$; $f'$ goes from $-$ to $+$: minimum." % (n_, L(xm)),
              r'Value: $f(%s) = %s$.' % (L(xm), L(v))]
        B.add(r'Find the location and value of the minimum of $f(x) = %s$ on $(0,\infty)$.' % L(f),
              [P_num('Minimum at $x =$', xm), P_num('Minimum value:', v)], st, 5)

    def mono():
        a = r.randint(1, 5); form = cyc('m', 2)
        if form == 0:
            f = x ** 3 - 3 * a * a * x; s = Interval.open(-a, a); what = 'strictly decreasing'
            st = [r"$f'(x) = 3x^2 - %d = 3(x-%d)(x+%d)$, negative exactly for $-%d < x < %d$." % (3 * a * a, a, a, a, a)]
        else:
            f = x / (x ** 2 + a * a); s = Interval.open(-a, a); what = 'strictly increasing'
            st = [r"$f'(x) = \dfrac{%d - x^2}{(x^2+%d)^2}$, positive exactly for $-%d < x < %d$." % (a * a, a * a, a, a)]
        B.add(r'Give the largest open interval on which $f(x) = %s$ is %s.' % (L(f), what), [P_int('Interval:', s)], st, 3,
              mcq(interval_latex(set_to_intervals(s)), iv_distractors(s, [Union(Interval.open(-oo, -a), Interval.open(a, oo)), Interval.open(0, a), Interval.open(-a * a, a * a)])))

    def optim():
        k = cyc('o', 5); v = r.choice([4, 8, 12, 16, 20, 24, 36, 40])
        if k == 0:
            q, ans = r'A rectangle has perimeter $%d$. What is the largest possible area?' % v, Q(v * v, 16)
            st = [r'Sides $x$ and $%s - x$: $A(x) = x(%s - x)$.' % (L(Q(v, 2)), L(Q(v, 2))), r"$A'(x) = %s - 2x = 0 \Rightarrow x = %s$ (a square)." % (L(Q(v, 2)), L(Q(v, 4))), r'$A_{max} = %s$.' % L(ans)]
        elif k == 1:
            q, ans = r'A farmer has $%d$ m of fence to enclose a rectangle along a straight river (no fence on the river side). What is the maximal area (m$^2$)?' % v, Q(v * v, 8)
            st = [r'Width $x$ (two sides), length $%d - 2x$: $A(x) = x(%d - 2x)$.' % (v, v), r"$A'(x) = %d - 4x = 0 \Rightarrow x = %s$." % (v, L(Q(v, 4))), r'$A_{max} = %s\cdot%s = %s$.' % (L(Q(v, 4)), L(Q(v, 2)), L(ans))]
        elif k == 2:
            kk = r.choice([4, 9, 16, 25, 2, 3]); q, ans = r'Find the minimum value of $f(x) = x + \dfrac{%d}{x}$ for $x > 0$.' % kk, 2 * sqrt(kk)
            st = [r"$f'(x) = 1 - \dfrac{%d}{x^2} = 0 \Rightarrow x = %s$." % (kk, L(sqrt(kk))), r"$f''(x) = %d/x^3 > 0$, so it is a minimum: $f(%s) = %s$." % (2 * kk, L(sqrt(kk)), L(ans))]
        elif k == 3:
            s_ = r.choice([6, 12, 18, 24, 30]); q, ans = r'From a square sheet of side $%d$ we cut equal squares of side $x$ from the corners and fold up an open box. For which $x$ is the volume maximal?' % s_, Q(s_, 6)
            st = [r'$V(x) = x(%d - 2x)^2$ for $0 < x < %d$.' % (s_, s_ // 2), r"$V'(x) = (%d - 2x)(%d - 6x) = 0 \Rightarrow x = %d$ (gives $V = 0$) or $x = %s$." % (s_, s_, s_ // 2, L(ans)), r'So $x = %s$.' % L(ans)]
        else:
            q, ans = r'Two non-negative numbers sum to $%d$. What is the maximal value of their product?' % v, Q(v * v, 4)
            st = [r'$P(x) = x(%d - x)$, $P^{\prime}(x) = %d - 2x = 0 \Rightarrow x = %s$.' % (v, v, L(Q(v, 2))), r'$P_{max} = %s$.' % L(ans)]
        P = P_num('Answer:', ans)
        B.add(q, [P], st, 4, mcq(P['latex'], num_distractors(ans)))

    B.fill(crit_sqrt, 6); B.fill(cubic_ext, 6); B.fill(abs_ext, 5); B.fill(xexp, 4); B.fill(xnln, 4); B.fill(mono, 4); B.fill(optim, 8)
