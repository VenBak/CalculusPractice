"""Probability: discrete, continuous, conditional / Bayes."""
from common import *
from sympy import sqrt, exp, log, binomial, integrate, pi, E

PCT = lambda p: r'%s\%%' % sp.nsimplify(p * 100)


# =====================================================================
def discrete(B):
    r = B.rng
    cyc = Cycle()

    def binom():
        n_ = r.choice([10, 12, 15, 20, 25]); p = r.choice([Q(1, 20), Q(1, 10), Q(1, 5), Q(3, 10), Q(1, 4)]); k = cyc('b', 3)
        kk = r.randint(1, 3)
        b = lambda j: binomial(n_, j) * p ** j * (1 - p) ** (n_ - j)
        ctx = r.choice([
            ('On a typical day, $%s$ of the vehicles passing through a tunnel have a German license plate. We observe $%d$ vehicles.' % (PCT(p), n_), 'German plates'),
            ('A machine produces defective items with probability $%s$, independently. We inspect $%d$ items.' % (PCT(p), n_), 'defective items'),
            ('Each of $%d$ students independently forgets their calculator with probability $%s$.' % (n_, PCT(p)), 'students who forget'),
        ])
        if k == 0:
            v = 1 - sum(b(j) for j in range(kk + 1)); q = 'at least %d %s' % (kk + 1, ctx[1])
            st = [r'Model: binomial with $n = %d$, $p = %s$: $b(k) = \binom{%d}{k}(%s)^k(%s)^{%d-k}$.' % (n_, L(p), n_, L(p), L(1 - p), n_),
                  r'Use the complement: $P(X \ge %d) = 1 - \sum_{k=0}^{%d} b(k)$.' % (kk + 1, kk),
                  r'$= 1 - ' + ' - '.join(r'\binom{%d}{%d}(%s)^{%d}(%s)^{%d}' % (n_, j, L(p), j, L(1 - p), n_ - j) for j in range(kk + 1)) + r' \approx %.4f$.' % val(v)]
        elif k == 1:
            v = b(kk); q = 'exactly %d %s' % (kk, ctx[1])
            st = [r'Binomial with $n = %d$, $p = %s$.' % (n_, L(p)), r'$P(X = %d) = \binom{%d}{%d}(%s)^{%d}(%s)^{%d} \approx %.4f$.' % (kk, n_, kk, L(p), kk, L(1 - p), n_ - kk, val(v))]
        else:
            v = sum(b(j) for j in range(kk + 1)); q = 'at most %d %s' % (kk, ctx[1])
            st = [r'Binomial with $n = %d$, $p = %s$.' % (n_, L(p)), r'$P(X \le %d) = \sum_{k=0}^{%d}\binom{%d}{k}(%s)^k(%s)^{%d-k} \approx %.4f$.' % (kk, kk, n_, L(p), L(1 - p), n_, val(v))]
        P = P_approx('$P \\approx$', v)
        dis = ['%.4f' % val(x_) for x_ in [1 - v, b(kk), v * 0.8, min(0.9999, v + 0.12), 1 - b(0)] if abs(val(x_) - val(v)) > 1e-3]
        B.add(r'%s What is the probability of %s? (Give a decimal with at least 3 digits.)' % (ctx[0], q), [P], st, 4,
              mcq(r'%.4f' % val(v), dis))

    def die():
        n_ = r.choice([4, 6, 8, 10, 12, 20, 41, 100]); k = cyc('d', 2)
        if k == 0:
            v = Q(n_ + 1, 2)
            st = [r'Each side has probability $\frac{1}{%d}$: $E(X) = \sum_{i=1}^{%d} \frac{i}{%d} = \frac{1}{%d}\cdot\frac{%d\cdot%d}{2} = %s$.' % (n_, n_, n_, n_, n_, n_ + 1, L(v))]
            P = P_num('$E(X) =$', v); qq = 'expectation'
        else:
            v = Q(n_ * n_ - 1, 12)
            st = [r'$E(X) = \frac{%d}{2}$, $E(X^2) = \frac{1}{%d}\sum i^2 = \frac{(%d)(%d)}{6}$.' % (n_ + 1, n_, n_ + 1, 2 * n_ + 1),
                  r'$Var(X) = E(X^2) - E(X)^2 = \frac{n^2 - 1}{12} = %s$.' % L(v)]
            P = P_num('$Var(X) =$', v); qq = 'variance'
        B.add(r'A fair $%d$-sided die has sides $1, 2, \dots, %d$. What is the %s of the number rolled?' % (n_, n_, qq), [P], st, 3, mcq(P['latex'], num_distractors(v, [Q(n_, 2)])))

    def table():
        xs = sorted(r.sample(range(-2, 6), 4)); w = [r.randint(1, 4) for _ in xs]
        c = Q(1, sum(w)); ps = [c * wi for wi in w]
        E_ = sum(p * xi for p, xi in zip(ps, xs)); V = sum(p * (xi - E_) ** 2 for p, xi in zip(ps, xs))
        rows = ' & '.join(str(v) for v in xs); prow = ' & '.join(('%dc' % wi) if wi > 1 else 'c' for wi in w)
        st = [r'Probabilities sum to $1$: $%dc = 1 \Rightarrow c = %s$.' % (sum(w), L(c)),
              r'$E(X) = \sum x_i P(X=x_i) = %s$.' % L(E_),
              r'$Var(X) = \sum P(X = x_i)(x_i - E(X))^2 = %s$.' % L(V)]
        B.add(r'A random variable $X$ has distribution $\begin{array}{c|cccc} x & %s \\ \hline P(X=x) & %s\end{array}$. Find $c$, $E(X)$ and $Var(X)$.' % (rows, prow),
              [P_num('$c =$', c), P_num('$E(X) =$', E_), P_num('$Var(X) =$', V)], st, 6)

    def dice2():
        k = cyc('t', 3)
        if k == 0:
            s = r.randint(3, 11); cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s); v = Q(cnt, 36)
            q = 'the sum of the two dice is exactly $%d$' % s; why = r'There are $%d$ favourable outcomes out of $36$ equally likely ones.' % cnt
        elif k == 1:
            s = r.randint(7, 11); cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= s); v = Q(cnt, 36)
            q = 'the sum is at least $%d$' % s; why = r'Count pairs with $a + b \ge %d$: $%d$ out of $36$.' % (s, cnt)
        else:
            m = r.randint(2, 6); cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if max(a, b) == m); v = Q(cnt, 36)
            q = 'the maximum of the two dice equals $%d$' % m; why = r'$P(\max = %d) = P(\max\le%d) - P(\max\le%d) = \frac{%d^2 - %d^2}{36} = %s$.' % (m, m, m - 1, m, m - 1, L(v))
        P = P_prob('$P =$', v)
        B.add(r'Two fair six-sided dice are rolled. What is the probability that %s?' % q, [P], [why, r'$P = %s$.' % L(v)], 3, mcq(L(v), num_distractors(v, [Q(cnt, 21)])))

    def urn():
        rd = r.randint(2, 7); bl = r.randint(2, 7); N = rd + bl; k = cyc('u', 2)
        if k == 0:
            v = Q(rd * (rd - 1), N * (N - 1)); q = 'both balls are red'
            st = [r'Without replacement: $P = \frac{%d}{%d}\cdot\frac{%d}{%d} = %s$.' % (rd, N, rd - 1, N - 1, L(v))]
        else:
            v = Q(2 * rd * bl, N * (N - 1)); q = 'the two balls have different colours'
            st = [r'Red then blue or blue then red: $\frac{%d}{%d}\cdot\frac{%d}{%d} + \frac{%d}{%d}\cdot\frac{%d}{%d} = %s$.' % (rd, N, bl, N - 1, bl, N, rd, N - 1, L(v))]
        P = P_prob('$P =$', v)
        B.add(r'An urn contains $%d$ red and $%d$ blue balls. Two balls are drawn without replacement. What is the probability that %s?' % (rd, bl, q), [P], st, 4,
              mcq(L(v), num_distractors(v, [Q(rd * rd, N * N)])))

    def incl_excl():
        pa = Q(r.randint(2, 7), 10); pb = Q(r.randint(2, 7), 10); pab = Q(r.randint(1, int(min(pa, pb) * 10)), 10)
        if pa + pb - pab > 1:
            raise ValueError
        k = cyc('i', 2)
        if k == 0:
            v = pa + pb - pab; q = r'P(A \cup B)'; st = [r'$P(A\cup B) = P(A) + P(B) - P(A\cap B) = %s + %s - %s = %s$.' % (L(pa), L(pb), L(pab), L(v))]
        else:
            v = 1 - (pa + pb - pab); q = r'P(\neg A \cap \neg B)'; st = [r'$\neg A\cap\neg B = \neg(A\cup B)$ (De Morgan).', r'$P = 1 - (P(A) + P(B) - P(A\cap B)) = 1 - %s = %s$.' % (L(pa + pb - pab), L(v))]
        P = P_prob('$%s =$' % q, v)
        B.add(r'Given $P(A) = %s$, $P(B) = %s$ and $P(A\cap B) = %s$. Compute $%s$.' % (L(pa), L(pb), L(pab), q), [P], st, 3, mcq(L(v), num_distractors(v, [pa + pb])))

    def game():
        w = r.randint(2, 20); l = r.randint(1, 5); p = Q(r.randint(1, 5), 12)
        v = p * w - (1 - p) * l
        st = [r'$E(X) = %s\cdot %d + %s\cdot(-%d) = %s$.' % (L(p), w, L(1 - p), l, L(v))]
        B.add(r'In a game you win $%d$ euro with probability $%s$ and otherwise lose $%d$ euro. What is your expected gain $E(X)$?' % (w, L(p), l), [P_num('$E(X) =$', v)], st, 3,
              mcq(L(v), num_distractors(v, [p * w])))

    B.fill(binom, 8); B.fill(die, 4); B.fill(table, 5); B.fill(dice2, 5); B.fill(urn, 3); B.fill(incl_excl, 3); B.fill(game, 3)


# =====================================================================
def continuous(B):
    r = B.rng
    cyc = Cycle()

    def recip():
        a, b = r.choice([(1, 2), (2, 4), (1, 3), (1, 4), (2, 6), (3, 9), (1, E), (2, 8)])
        c = log(sp.sympify(b) / a); c = sp.simplify(sp.expand_log(c, force=True))
        F = sp.simplify((log(x) - log(a)) / c)
        st = [r'Normalise: $\displaystyle\int_{%s}^{%s} \frac{1}{cx}dx = \frac{\ln %s - \ln %s}{c} = 1 \Rightarrow c = %s$.' % (L(a), L(b), L(b), L(a), L(c)),
              r'CDF: $F(x) = \displaystyle\int_{%s}^x \frac{1}{c\,t}dt = \frac{\ln x - \ln %s}{%s}$ for $x \in [%s, %s]$.' % (L(a), L(a), L(c), L(a), L(b))]
        B.add(r'Consider the reciprocal distribution on $[%s, %s]$ with pdf $p(x) = \dfrac{1}{cx}$ for $%s \le x \le %s$. Find $c$ such that $p$ is normalised, and the cdf $F(x)$ on $[%s, %s]$.' % (L(a), L(b), L(a), L(b), L(a), L(b)),
              [P_num('$c =$', c), P_expr('$F(x) =$', F, sample={'x': [val(a) + 0.1, val(b)]})], st, 6)

    def power():
        nn = r.randint(1, 4); Lb = r.choice([1, 2, 3, Q(1, 2)]); Lb = sp.sympify(Lb)
        c = (nn + 1) / Lb ** (nn + 1); E_ = (nn + 1) * Lb / (nn + 2)
        st = [r'$\displaystyle\int_0^{%s} c x^{%d}dx = c\frac{%s^{%d}}{%d} = 1 \Rightarrow c = %s$.' % (L(Lb), nn, L(Lb), nn + 1, nn + 1, L(c)),
              r'$E(X) = \displaystyle\int_0^{%s} x\cdot c x^{%d}dx = c\frac{%s^{%d}}{%d} = %s$.' % (L(Lb), nn, L(Lb), nn + 2, nn + 2, L(E_))]
        B.add(r'$X$ has pdf $f(x) = c x^{%d}$ for $0 \le x \le %s$ (and $0$ otherwise). Determine $c$ and $E(X)$.' % (nn, L(Lb)), [P_num('$c =$', c), P_num('$E(X) =$', E_)], st, 5)

    def exam_poly():
        k = r.choice([2, 3, 4]); Lb = r.choice([Q(1, 2), 1, 2, Q(1, 3)]); Lb = sp.sympify(Lb)
        c = (k + 1) / (k * Lb); f = c * (1 - (x / Lb) ** k)
        assert sp.simplify(integrate(f, (x, 0, Lb)) - 1) == 0
        E_ = sp.simplify(integrate(x * f, (x, 0, Lb)))
        fl = L(sp.factor(sp.expand(f)))
        st = [r'$E(X) = \displaystyle\int_0^{%s} x f(x)\,dx = %s\int_0^{%s}\left(x - %s\right)dx$.' % (L(Lb), L(c), L(Lb), L(sp.expand(x * (x / Lb) ** k))),
              r'$= %s\left[\frac{x^2}{2} - %s\right]_0^{%s} = %s$.' % (L(c), L(sp.expand(x ** (k + 2) / ((k + 2) * Lb ** k))), L(Lb), L(E_))]
        P = P_num('$E(X) =$', E_)
        B.add(r'A continuous random variable $X$ has pdf $f(x) = %s$ for $0 \le x \le %s$ and $0$ otherwise. What is $E(X)$?' % (fl, L(Lb)), [P], st, 3,
              mcq(P['latex'], num_distractors(E_, [Lb / 2, Lb / 3, Lb / 4, Lb / 8])))

    def uniform():
        a = r.randint(-2, 4); b = a + r.randint(2, 8); t_ = r.randint(a + 1, b - 1); k = cyc('u', 3)
        if k == 0:
            v = Q(a + b, 2); q = 'E(X)'; st = [r'$E(X) = \displaystyle\int_{%d}^{%d}\frac{x}{%d}dx = \frac{%d + %d}{2} = %s$.' % (a, b, b - a, a, b, L(v))]
        elif k == 1:
            v = Q((b - a) ** 2, 12); q = 'Var(X)'; st = [r'$Var(X) = E(X^2) - E(X)^2 = \frac{(b-a)^2}{12} = \frac{%d^2}{12} = %s$.' % (b - a, L(v))]
        else:
            v = Q(t_ - a, b - a); q = r'P(X \le %d)' % t_; st = [r'$P(X\le %d) = \displaystyle\int_{%d}^{%d}\frac{1}{%d}dx = \frac{%d}{%d} = %s$.' % (t_, a, t_, b - a, t_ - a, b - a, L(v))]
        P = P_num('$%s =$' % q, v)
        B.add(r'$X$ is uniformly distributed on $[%d, %d]$. Compute $%s$.' % (a, b, q), [P], st, 3, mcq(L(v), num_distractors(v)))

    def expo():
        lam = r.choice([1, 2, 3, Q(1, 2), Q(1, 3), Q(1, 4)]); lam = sp.sympify(lam); tt = r.choice([1, 2, 3]); k = cyc('e', 3)
        if k == 0:
            v = exp(-lam * tt); q = r'P(X > %d)' % tt; st = [r'$P(X > %d) = \displaystyle\int_{%d}^\infty %s e^{-%s x}dx = \Big[-e^{-%s x}\Big]_{%d}^{\infty} = %s$.' % (tt, tt, L(lam), L(lam), L(lam), tt, L(v))]
        elif k == 1:
            v = 1 / lam; q = 'E(X)'; st = [r'By parts: $E(X) = \displaystyle\int_0^\infty x\,%s e^{-%s x}dx = \Big[-xe^{-%s x}\Big]_0^\infty + \int_0^\infty e^{-%s x}dx = %s$.' % (L(lam), L(lam), L(lam), L(lam), L(v))]
        else:
            v = log(2) / lam; q = r'\text{the median } m'; st = [r'Solve $F(m) = 1 - e^{-%s m} = \tfrac12$: $e^{-%s m} = \tfrac12 \Rightarrow m = \dfrac{\ln 2}{%s} = %s$.' % (L(lam), L(lam), L(lam), L(v))]
        P = P_num('$%s =$' % q.replace(r'\text{the median } ', ''), v)
        B.add(r'$X$ has pdf $f(x) = %s e^{-%s x}$ for $x \ge 0$ (and $0$ otherwise). Compute $%s$.' % (L(lam), L(lam), q), [P], st, 4, mcq(L(v), num_distractors(v)))

    def cdf():
        a = r.choice([2, 3, 4, 5]); k = r.choice([2, 3])
        lo, hi = sorted(r.sample(range(0, a + 1), 2))
        v = Q(hi ** k - lo ** k, a ** k); fx = k * x ** (k - 1) / a ** k
        st = [r'$P(%d < X < %d) = F(%d) - F(%d) = \frac{%d^{%d} - %d^{%d}}{%d} = %s$.' % (lo, hi, hi, lo, hi, k, lo, k, a ** k, L(v)),
              r'The pdf is $f(x) = F^{\prime}(x) = %s$ on $[0, %d]$.' % (L(fx), a)]
        B.add(r'The cdf of $X$ is $F(x) = \dfrac{x^{%d}}{%d}$ for $0 \le x \le %d$ ($0$ before, $1$ after). Compute $P(%d < X < %d)$ and the pdf $f(x)$ on $[0, %d]$.' % (k, a ** k, a, lo, hi, a),
              [P_num('$P =$', v), P_expr('$f(x) =$', fx, sample={'x': [0.2, a]})], st, 5)

    def normalize():
        k = cyc('n', 3)
        if k == 0:
            tt = r.choice([2, 3]); aval = 2 * tt / (2 * tt - 3)
            st = [r'Substitute $u = a + 2\sqrt x$, $du = \frac{1}{\sqrt x}dx$; bounds $a+2$ to $a + %d$.' % (2 * tt),
                  r'$\displaystyle\int_{a+2}^{a+%d}\frac{a(a+2)}{u^2}du = a(a+2)\left(\frac{1}{a+2} - \frac{1}{a+%d}\right) = \frac{%da}{a + %d}$.' % (2 * tt, 2 * tt, 2 * tt - 2, 2 * tt),
                  r'Setting this to $1$: $%da = a + %d$, so $a = %s$.' % (2 * tt - 2, 2 * tt, L(aval))]
            B.add(r'For what value of $a \in \mathbb{N}$ is $f(x) = \dfrac{a^2 + 2a}{(a + 2\sqrt x)^2\sqrt x}$ for $1 \le x \le %d$ (and $0$ elsewhere) a probability density?' % (tt * tt),
                  [P_num('$a =$', aval)], st, 5, mcq(L(aval), num_distractors(aval)))
        else:
            b = r.choice([1, 2, 3, 4, 6]); kk = Q(6, b ** 3)
            st = [r'$\displaystyle\int_0^{%d} k\,x(%d - x)\,dx = k\left[\frac{%d x^2}{2} - \frac{x^3}{3}\right]_0^{%d} = k\frac{%d}{6}$.' % (b, b, b, b, b ** 3),
                  r'Setting this to $1$: $k = %s$.' % L(kk)]
            B.add(r'For which $k$ is $f(x) = k\,x(%d - x)$ on $[0, %d]$ (and $0$ elsewhere) a probability density function?' % (b, b), [P_num('$k =$', kk)], st, 4, mcq(L(kk), num_distractors(kk)))

    B.fill(recip, 6); B.fill(power, 5); B.fill(exam_poly, 6); B.fill(uniform, 5); B.fill(expo, 5); B.fill(cdf, 3); B.fill(normalize, 5)


# =====================================================================
def conditional(B):
    r = B.rng
    cyc = Cycle()

    def bayes_test():
        prev = r.choice([Q(1, 100), Q(1, 50), Q(1, 20), Q(1, 10), Q(1, 1000)]); sens = r.choice([Q(9, 10), Q(95, 100), Q(99, 100), Q(4, 5)])
        fp = r.choice([Q(1, 20), Q(1, 10), Q(1, 100), Q(2, 100)])
        pe = sens * prev + fp * (1 - prev); v = sens * prev / pe
        st = [r'Let $D$ = has the disease, $+$ = positive test. Prior $P(D) = %s$.' % L(prev),
              r'Total probability: $P(+) = P(+|D)P(D) + P(+|\neg D)P(\neg D) = %s\cdot%s + %s\cdot%s = %s$.' % (L(sens), L(prev), L(fp), L(1 - prev), L(pe)),
              r'Bayes: $P(D|+) = \dfrac{P(+|D)P(D)}{P(+)} = \dfrac{%s}{%s} = %s$.' % (L(sens * prev), L(pe), L(v))]
        B.add(r'A disease affects $%s$ of the population. A test detects the disease in $%s$ of sick people, but also gives a positive result for $%s$ of healthy people. Given a positive test, what is the probability that the person is sick?' % (PCT(prev), PCT(sens), PCT(fp)),
              [P_prob('$P(D|+) =$', v)], st, 6, mcq(L(v), num_distractors(v, [sens, sens * prev, 1 - fp])))

    def factories():
        sh = r.choice([(Q(1, 2), Q(3, 10), Q(1, 5)), (Q(3, 5), Q(1, 4), Q(3, 20)), (Q(2, 5), Q(2, 5), Q(1, 5)), (Q(1, 4), Q(1, 4), Q(1, 2))])
        dr = [Q(r.randint(1, 6), 100) for _ in range(3)]
        pdx = sum(s * d for s, d in zip(sh, dr)); j = r.randrange(3); post = sh[j] * dr[j] / pdx
        names = ['A', 'B', 'C']
        st = [r'Total probability: $P(\text{def}) = ' + ' + '.join(r'%s\cdot%s' % (L(s), L(d)) for s, d in zip(sh, dr)) + r' = %s$.' % L(pdx),
              r'Bayes: $P(%s|\text{def}) = \dfrac{%s\cdot%s}{%s} = %s$.' % (names[j], L(sh[j]), L(dr[j]), L(pdx), L(post))]
        B.add(r'Factories A, B, C produce %s, %s and %s of all items, with defect rates %s, %s and %s respectively. Compute the probability that a random item is defective, and the probability that a defective item comes from %s.'
              % tuple(['$%s$' % PCT(s) for s in sh] + ['$%s$' % PCT(d) for d in dr] + [names[j]]),
              [P_prob(r'$P(\text{def}) =$', pdx), P_prob(r'$P(%s\,|\,\text{def}) =$' % names[j], post)], st, 6)

    def urns():
        r1, b1, r2, b2 = [r.randint(1, 6) for _ in range(4)]; p1 = r.choice([Q(1, 2), Q(1, 3), Q(2, 3)])
        pr = p1 * Q(r1, r1 + b1) + (1 - p1) * Q(r2, r2 + b2); v = p1 * Q(r1, r1 + b1) / pr
        st = [r'$P(R) = %s\cdot\frac{%d}{%d} + %s\cdot\frac{%d}{%d} = %s$.' % (L(p1), r1, r1 + b1, L(1 - p1), r2, r2 + b2, L(pr)),
              r'$P(U_1|R) = \dfrac{P(R|U_1)P(U_1)}{P(R)} = \dfrac{%s}{%s} = %s$.' % (L(p1 * Q(r1, r1 + b1)), L(pr), L(v))]
        B.add(r'Urn 1 has $%d$ red and $%d$ blue balls; urn 2 has $%d$ red and $%d$ blue balls. We choose urn 1 with probability $%s$ (otherwise urn 2) and draw one ball. It is red. What is the probability it came from urn 1?' % (r1, b1, r2, b2, L(p1)),
              [P_prob(r'$P(U_1|R) =$', v)], st, 5, mcq(L(v), num_distractors(v, [p1, Q(r1, r1 + b1)])))

    def die_cond():
        k = cyc('d', 4)
        conds = [('even', {2, 4, 6}), ('at least 3', {3, 4, 5, 6}), ('odd', {1, 3, 5}), ('not 6', {1, 2, 3, 4, 5})]
        evs = [('greater than 3', {4, 5, 6}), ('a prime', {2, 3, 5}), ('at most 2', {1, 2}), ('divisible by 3', {3, 6})]
        cn, cs = conds[k]; en, es = r.choice(evs)
        v = Q(len(cs & es), len(cs))
        st = [r'$B$ = "%s" $= %s$, $A$ = "%s" $= %s$.' % (cn, set_latex(sorted(cs)), en, set_latex(sorted(es))),
              r'$P(A|B) = \dfrac{P(A\cap B)}{P(B)} = \dfrac{%d/6}{%d/6} = %s$.' % (len(cs & es), len(cs), L(v))]
        B.add(r'A fair die is rolled. Given that the outcome is %s, what is the probability that it is %s?' % (cn, en), [P_prob('$P(A|B) =$', v)], st, 3,
              mcq(L(v), num_distractors(v, [Q(len(es), 6), Q(len(cs & es), 6)])))

    def indep():
        pa = Q(r.randint(1, 9), 10); pb = Q(r.randint(1, 9), 10); ind = r.random() < 0.5
        pab = pa * pb if ind else pa * pb + Q(r.choice([-1, 1]) * r.randint(1, 3), 100)
        if pab <= 0 or pab > min(pa, pb):
            raise ValueError
        st = [r'$A$ and $B$ are independent iff $P(A\cap B) = P(A)P(B)$.', r'$P(A)P(B) = %s$ %s $P(A\cap B) = %s$.' % (L(pa * pb), '=' if ind else r'\neq', L(pab))]
        B.add(r'Given $P(A) = %s$, $P(B) = %s$ and $P(A \cap B) = %s$. Are $A$ and $B$ independent?' % (L(pa), L(pb), L(pab)),
              [P_choice('Independent?', ['Yes', 'No'], 0 if ind else 1)], st, 3)

    def from_cond():
        pa = Q(r.randint(1, 9), 10); pba = Q(r.randint(1, 9), 10); pbn = Q(r.randint(1, 9), 10)
        pb = pba * pa + pbn * (1 - pa); v = pba * pa / pb
        st = [r'$P(B) = P(B|A)P(A) + P(B|\neg A)P(\neg A) = %s$.' % L(pb), r'$P(A|B) = \dfrac{P(B|A)P(A)}{P(B)} = %s$.' % L(v)]
        B.add(r'Given $P(A) = %s$, $P(B|A) = %s$ and $P(B|\neg A) = %s$. Compute $P(B)$ and $P(A|B)$.' % (L(pa), L(pba), L(pbn)),
              [P_prob('$P(B) =$', pb), P_prob('$P(A|B) =$', v)], st, 5)

    B.fill(bayes_test, 7); B.fill(factories, 5); B.fill(urns, 5); B.fill(die_cond, 6); B.fill(indep, 4); B.fill(from_cond, 4)
