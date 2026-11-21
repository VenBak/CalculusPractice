"""The ten real past exams (IBC017 Calculus and Probability), transcribed question by question.

Answers follow the official solutions; every answer that can be computed is re-checked with SymPy below
(see verify()). Usage: python3 -I past_exams.py <site_dir>
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from past_common import *  # noqa: F401,F403
from sympy import sqrt, exp, log, sin, cos, tan, atan, pi, E, Rational as R, limit, integrate, diff, oo as OO, binomial

STD_120 = [
    'You get 10 points for writing your name and student number on each page (the grade is (points + 10)/10).',
    'For each item the maximum score is indicated; in total you can score 100 points.',
    'A regular calculator is allowed; graphical/programmable calculators, phones and other devices are not.',
    'You have 120 minutes (most students with extra time: 150 minutes).',
    'Always explain your calculations. Do not write numbers in digits (e.g. 0.25) but use fractions (e.g. 1/4) and simplify as much as possible.',
]
STD_180 = [s.replace('120 minutes (most students with extra time: 150 minutes)', '180 minutes (most students with extra time: 210 minutes)') for s in STD_120]
RESIT_2025 = [
    'You get 10 points for starting the exam, so your minimum grade is 1. Your grade is the sum of your scores divided by 10.',
    'For each item the maximum score is indicated; in total you can score 100 points.',
    'A regular (non-graphical) calculator is allowed; phones and other devices are not.',
    'You may bring one A4 “cheat sheet” (both sides).',
    'You have 180 minutes (most students with extra time: 210 minutes).',
    'If your answer involves expressions that can easily be computed with a calculator, do these calculations. Check whether your answer is sensible.',
]
SEL = 'Select the best fitting answer.'
TFI = 'Answer T(rue) or F(alse).'
yx = sp.Symbol('y', real=True)
POS2 = {'x': [0.5, 3], 'y': [0.5, 3]}


# =====================================================================================
def exam_2021_1():
    qs = []
    qs.append(question('1', 9, '', [item('', r'If $$\lim_{x\to1}\frac{A\pi\tan(\pi x)+B\pi^2\ln(x)+C\cos(\pi x)+3}{\pi^2(x-1)^2}=2$$ then what are the values of $A$, $B$, and $C$? [Hint: $A, B, C\in\mathbb{Z}$]',
        [N('$A =$', 1), N('$B =$', -1), N('$C =$', 3)], 9, 'lhopital',
        r'The denominator tends to $0$, so the numerator must tend to $0$ as well — that gives a first equation. Then apply L\'Hôpital and repeat the argument; the last step gives the value $2$.',
        [r'Denominator $\to 0$, so the numerator must $\to 0$: $C\cos\pi + 3 = 0 \Rightarrow C = 3$.',
         r"L'Hôpital: $\dfrac{\frac{A\pi^2}{\cos^2(\pi x)} + \frac{B\pi^2}{x} - C\pi\sin(\pi x)}{2\pi^2(x-1)}$. The numerator must vanish at $x=1$: $A\pi^2 + B\pi^2 = 0 \Rightarrow B = -A$.",
         r"L'Hôpital again: $\dfrac{\frac{2A\pi^3\sin(\pi x)}{\cos^3(\pi x)} - \frac{B\pi^2}{x^2} - C\pi^2\cos(\pi x)}{2\pi^2} \to \dfrac{-B\pi^2 + C\pi^2}{2\pi^2} = \dfrac{C - B}{2}$.",
         r'$\dfrac{3 - B}{2} = 2 \Rightarrow B = -1$, so $A = 1$, $B = -1$, $C = 3$.'])]))
    qs.append(question('2', 10, '', [item('', r'If $$\lim_{n\to\infty}\sum_{r=1}^{n}\frac{9r^2+4rn+5n^2}{(n+r)(n^2+r^2)} = A\ln(2)$$ then what is the value of $A$? [Hint: $A\in\mathbb{N}$]',
        [N('$A =$', 7)], 10, 'riemann',
        r'Divide numerator and denominator by $n^3$ to write the sum as $\frac1n\sum f(\frac rn)$; the limit is $\int_0^1 f(x)\,dx$. Then use partial fractions.',
        [r'$\displaystyle\lim\frac1n\sum_{r=1}^n\frac{9(\frac rn)^2 + 4\frac rn + 5}{(1+\frac rn)(1+(\frac rn)^2)} = \int_0^1\frac{9x^2+4x+5}{(1+x)(1+x^2)}dx$.',
         r'Partial fractions: $\dfrac{5}{1+x} + \dfrac{4x}{1+x^2}$.',
         r'$= 5\ln|1+x|\Big|_0^1 + 2\ln(1+x^2)\Big|_0^1 = 5\ln 2 + 2\ln 2 = 7\ln 2$ (the second term with $u = 1 + x^2$).',
         r'So $A = 7$.'])]))
    f3 = r'f(x)=\frac{\sqrt{1-x}}{x^2-x-6}'
    qs.append(question('3', 15, SEL, [
        item('(a)', r'Let $%s$. Then the domain of $f$ is' % f3,
             [CH('', [r'$(-\infty,1)$', r'$(-\infty,-2)\cup(-2,1)$', r'$(-\infty,1)\setminus\{-2,3\}$', 'None of the above'], 3)], 3, 'domain-range',
             r'Root: $1 - x \ge 0$. Denominator: $x^2 - x - 6 = (x-3)(x+2) \neq 0$. Is $x = 1$ allowed?',
             [r'$1 - x \ge 0 \iff x \le 1$, and $x \neq -2, 3$.', r'So $D_f = (-\infty,-2)\cup(-2,1]$. Since $1$ belongs to the domain, none of (A)–(C) is right: **(D)**.']),
        item('(b)', r'Let $%s$. How many asymptotes (both horizontal and vertical) does $f$ have?' % f3,
             [CH('', ['1', '2', '3', '4'], 1)], 3, 'asymptotes',
             r'Only the part $x \le 1$ is in the domain. Which zeros of the denominator lie there, and what happens as $x\to-\infty$?',
             [r'Vertical asymptote at $x = -2$ ($x = 3$ is outside the domain).', r'As $x\to-\infty$: $f(x)\to0$, so $y = 0$ is a horizontal asymptote. Total: **2 (B)**.']),
        item('(c)', r'Let $f(x)$ be an odd function, and $g(x)$ be an even function, then',
             [CH('', [r'$(f\circ g)(x)$ is even, and $(g\circ f)(x)$ is even.', r'$(f\circ g)(x)$ is odd, and $(g\circ f)(x)$ is even.',
                      r'$(f\circ g)(x)$ is even, and $(g\circ f)(x)$ is odd.', r'$(f\circ g)(x)$ is odd, and $(g\circ f)(x)$ is odd.'], 0)], 3, 'even-odd',
             r'Write out $f(g(-x))$ and $g(f(-x))$ and use the parity of the inner function first.',
             [r'$f(g(-x)) = f(g(x))$: even.', r'$g(f(-x)) = g(-f(x)) = g(f(x))$: even. **(A)**']),
        item('(d)', r'Given is the following graph of the functions $f$, $f^{\prime}$, and $f^{\prime\prime}$. %s Identify which curve belongs to $f$, $f^{\prime}$, and $f^{\prime\prime}$.' % img('2021-06-q3d-graph.png', 'Graph with a blue, a red and a green curve on [-3, 3]'),
             [CH('', [r"$f$ = blue, $f'$ = red, $f''$ = green", r"$f$ = blue, $f'$ = green, $f''$ = red", r"$f$ = red, $f'$ = blue, $f''$ = green",
                      r"$f$ = red, $f'$ = green, $f''$ = blue", r"$f$ = green, $f'$ = blue, $f''$ = red", r"$f$ = green, $f'$ = red, $f''$ = blue"], 1)], 3, 'function-analysis',
             r'Where a curve has a horizontal tangent (minimum/maximum), its derivative must cross or touch $0$.',
             [r'Blue has its minimum at $x=0$; green is $0$ at $x=0$, negative left and positive right: green $= $ blue$^{\prime}$.',
              r'Green increases on $(-2,2)$ and decreases outside; red is positive on $(-2,2)$ and negative outside: red $=$ green$^{\prime}$. **(B)**']),
        item('(e)', r'Use the same graph as in (d). Identify where the blue curve is concave.',
             [CH('', [r'$(0,\infty)$', r'$(-2,2)$', r'$(-2,0)\cup(0,2)$', r'$(-\infty,-2)\cup(2,\infty)$'], 3)], 3, 'concavity',
             r"Blue is $f$; concave means $f'' < 0$ — read off where the red curve is negative.",
             [r"$f'' = $ red $< 0$ on $(-\infty,-2)\cup(2,\infty)$. **(D)**"]),
    ]))
    qs.append(question('4', 5, '', [item('', r'For what value of $a\in\mathbb{N}$ is the following function a probability distribution: $$f(x)=\begin{cases}\dfrac{a^2+2a}{(a+2\sqrt{x})^2\sqrt{x}} & \text{if } 1\le x\le 4\\ 0 & \text{elsewhere}\end{cases}$$',
        [N('$a =$', 4)], 5, 'continuous',
        r'Set $\int_1^4 f(x)\,dx = 1$ and substitute $u = a + 2\sqrt x$, $du = \frac{1}{\sqrt x}dx$.',
        [r'$u = a + 2\sqrt x$, $du = \frac{dx}{\sqrt x}$, bounds $a+2$ to $a+4$.',
         r'$\displaystyle 1 = \int_{a+2}^{a+4}\frac{a(a+2)}{u^2}du = -a(a+2)\Big[\frac1u\Big]_{a+2}^{a+4} = \frac{2a}{a+4}$.',
         r'$2a = a + 4 \Rightarrow a = 4$.'])]))
    qs.append(question('5', 5, '', [item('', r'A wooden figure has the shape of a near-cone by rotating the function $f(x)=\sqrt{5}\sqrt[3]{x}$ around the $x$-axis. It is 8 cm high. We can compute the volume over $[a,b]$ for any function $g(x)$ as the integral $$\int_a^b\pi(g(x))^2\,dx,$$ i.e., for the wooden figure $a=0$, $b=8$, $g(x)=f(x)$. We want to create a similar figure, but the shape is too difficult to replicate. We decide to make it a regular cone, that is by rotating $f(x)=ax$ around the $x$-axis. Since we want the figure to have the same height, and the same volume, what is the $a>0$ we should choose? [Hint: $a$ should be a rational number, enter it in the form $p/q$.]',
        [N('$a =$', R(3, 4))], 5, 'area',
        r'Compute both volumes with $\pi\int_0^8 g(x)^2dx$ and set them equal.',
        [r'$\pi\int_0^8 5x^{2/3}dx = \pi\big[3x^{5/3}\big]_0^8 = 96\pi$.', r'$\pi\int_0^8 a^2x^2dx = a^2\pi\frac{512}{3}$.', r'$a^2 = 96\cdot\frac{3}{512} = \frac{9}{16}$, so $a = \frac34$.'])]))
    qs.append(question('6', 5, '', [item('', r'A $n$-sided dice has $n$ sides with pips $1, 2, \dots, n$. What is the expectation of a 41-sided dice?',
        [N('$E(X) =$', 21)], 5, 'discrete',
        r'Each side has probability $\frac1n$; use $\sum_{i=1}^n i = \frac{n(n+1)}{2}$.',
        [r'$E(X) = \sum_{i=1}^n \frac1n\, i = \frac1n\cdot\frac{n(n+1)}2 = \frac{n+1}{2}$.', r'For $n = 41$: $E(X) = 21$.'])]))
    qs.append(question('7', 10, TFI, [
        item('(a)', r'$f(x)=\dfrac{x^2-x-6}{x+2}$ has a slant asymptote as the degree in the numerator is one more than the degree of the denominator.', [TF(False)], 2, 'asymptotes',
             r'Factor the numerator first.', [r'$\frac{(x+2)(x-3)}{x+2} = x - 3$ with a hole at $x=-2$: the graph *is* a line, so there is no slant asymptote. **False**']),
        item('(b)', r"If $f$ has an inflection point in $x$ then $f''(x)=0$ (assuming $f''$ exists).", [TF(True)], 2, 'concavity',
             r"At an inflection point $f''$ changes sign.", [r"$f''$ changes sign there, so (when it exists) it equals $0$. **True**"]),
        item('(c)', r'$\dfrac{2x(x+1)}{(x^2+1)^2}$ can be split into $\dfrac{Ax+B}{(x^2+1)}+\dfrac{Cx+D}{(x^2+1)^2}$.', [TF(True)], 2, 'partial-fractions',
             r'What is the partial-fraction form for a repeated irreducible quadratic factor?', [r'A repeated irreducible quadratic needs linear numerators over $(x^2+1)$ and $(x^2+1)^2$. **True**']),
        item('(d)', r'The area between any two functions $f$ and $g$ on an interval $[a,b]$ is given by $\int_a^b f(x)-g(x)\,dx$ (assuming that both $f$ and $g$ are defined on $[a,b]$ and finite).', [TF(False)], 2, 'area',
             r'What if $g$ lies above $f$ somewhere?', [r'The area is $\int_a^b|f(x)-g(x)|\,dx$; without the absolute value parts can cancel. **False**']),
        item('(e)', r'$\lim_{x\to a}[f(x)+g(x)]=\lim_{x\to a}f(x)+\lim_{x\to a}g(x)$ always holds.', [TF(False)], 2, 'limits',
             r'The sum rule needs both limits to exist.', [r'Counterexample: $f(x) = \frac1x$, $g(x) = -\frac1x$ at $a = 0$: the left side is $0$, the right side does not exist. **False**']),
    ]))
    fxy = x ** yx / E
    qs.append(question('8', 5, '', [item('', r'Let $f(x,y)=\dfrac{x^y}{e}$. First, determine $\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(x,y)$ and then use this result to determine the value $\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(e,2)\in\mathbb{N}$.',
        [EX(r'$\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(x,y) =$', diff(fxy, yx, x), vars=('x', 'y'), sample=POS2), N('Value at $(e,2)$:', 3)], 5, 'partial-derivatives',
        r'Write $x^y = e^{y\ln x}$: then $\frac{\partial}{\partial y}x^y = x^y\ln x$. Differentiate that with respect to $x$ (product rule).',
        [r'$\frac{\partial}{\partial y}\frac{x^y}{e} = \frac1e\ln(x)\,x^y$.', r'$\frac{\partial}{\partial x}\Big(\frac1e\ln(x)x^y\Big) = \frac1e\Big(\frac1x x^y + \ln(x)\,y\,x^{y-1}\Big) = \frac1e(y\ln x + 1)x^{y-1}$.',
         r'At $(e,2)$: $\frac1e(2 + 1)e = 3$.'])]))
    qs.append(question('9', 5, '', [item('', r'Given the function $f(x)=x^2\sqrt{x^3-2}$. Let $F$ be the primitive of $f$ going through the point $P=(3,28)$. What is the $y$-intercept of the tangent line of $F$ going through $P$?',
        [N('$b =$', -107)], 5, 'substitution',
        r'You do not need $F$ itself: the slope of the tangent is $F^{\prime}(3) = f(3)$.',
        [r'Slope $F^{\prime}(3) = f(3) = 9\cdot\sqrt{25} = 45$.', r'$28 = 45\cdot3 + b \Rightarrow b = -107$.'])]))
    qs.append(question('10', 10, '', [item('', r'Let $p(u)$, $q(u)$, and $r(u)$ be polynomials in $u$. We have $$\int e^{3x}\sin(e^x)\,dx=\int p(u)\sin(u)\,du=q(u)\sin(u)+r(u)\cos(u)+C$$ then what are $p(u)$, $q(u)$, and $r(u)$? (Use substitution to obtain $p(u)$, integration by parts to obtain $q(u)$ and $r(u)$. Give the polynomials in terms of the variable $u$, not in the original variable $x$.) Finally, use this to compute the value of the following definite integral. $$\int_{-\infty}^{\ln(\pi)}e^{3x}\sin(e^x)\,dx.$$',
        [EX('$p(u) =$', u ** 2, vars=('u',)), EX('$q(u) =$', 2 * u, vars=('u',)), EX('$r(u) =$', 2 - u ** 2, vars=('u',)), N('Value of the definite integral:', pi ** 2 - 4)], 10, 'by-parts',
        r'Substitute $u = e^x$ ($du = e^x dx$, so $e^{3x}dx = u^2du$). Then integrate $u^2\sin u$ by parts twice; the bounds become $0$ and $\pi$.',
        [r'$u = e^x$: $\int e^{3x}\sin(e^x)dx = \int u^2\sin u\,du$, so $p(u) = u^2$.',
         r'$\int u^2\sin u\,du = -u^2\cos u + 2\int u\cos u\,du = -u^2\cos u + 2u\sin u - 2\int\sin u\,du = 2u\sin u + (2-u^2)\cos u + C$.',
         r'So $q(u) = 2u$, $r(u) = 2 - u^2$.', r'Bounds: $x\to-\infty \Rightarrow u\to0$; $x = \ln\pi \Rightarrow u = \pi$.',
         r'Value: $[2u\sin u + (2-u^2)\cos u]_0^\pi = (\pi^2 - 2) - 2 = \pi^2 - 4$.'])]))
    qs.append(question('11', 11, 'Compute the following limits.', [
        item('(a)', r'$\lim_{t\to0}t^2\ln(6t^2)$', [N('Limit:', 0)], 6, 'lhopital',
             r'Form $0\cdot(-\infty)$: rewrite as $\dfrac{\ln(6t^2)}{1/t^2}$ and apply L\'Hôpital.',
             [r'$\lim\frac{\ln(6t^2)}{t^{-2}} \overset{LH}{=} \lim\frac{12t/(6t^2)}{-2t^{-3}} = \lim\frac{2/t}{-2/t^3} = \lim(-t^2) = 0$.']),
        item('(b)', r'$\lim_{t\to4}\dfrac{8t-8\sqrt{3t+4}}{t-4}$', [N('Limit:', 5)], 5, 'limits',
             r'Form $\tfrac00$: multiply numerator and denominator by $t + \sqrt{3t+4}$ (or use L\'Hôpital).',
             [r'$8\cdot\dfrac{t-\sqrt{3t+4}}{t-4}\cdot\dfrac{t+\sqrt{3t+4}}{t+\sqrt{3t+4}} = 8\cdot\dfrac{t^2-3t-4}{(t-4)(t+\sqrt{3t+4})} = 8\cdot\dfrac{t+1}{t+\sqrt{3t+4}}$.',
              r'At $t = 4$: $8\cdot\frac58 = 5$.']),
    ]))
    return exam('2021-1', year='2021–2022', sitting=1, kind='Exam', date='June 23, 2022', iso='2022-06-23', minutes=120,
                file='calc-exam-2021-01', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2021_2():
    qs = []
    qs.append(question('1', 9, '', [item('', r'If $$\lim_{x\to1}\frac{A\cdot x^x+B\ln(x)+Cx^3-2}{(x-1)^2}=-6$$ then what are the values of $A$, $B$, and $C$? [Hint: $A,B,C\in\mathbb{Z}$]',
        [N('$A =$', 5), N('$B =$', 4), N('$C =$', -3)], 9, 'lhopital',
        r'The numerator must tend to $0$ (one equation); after one L\'Hôpital step it must tend to $0$ again (second equation); the third step gives the value. Recall $(x^x)^{\prime} = x^x(\ln x + 1)$.',
        [r'Numerator $\to 0$: $A + C - 2 = 0$.', r"L'Hôpital: $\dfrac{Ax^x(\ln x + 1) + \frac Bx + 3Cx^2}{2(x-1)}$; numerator at $1$: $A + B + 3C = 0$.",
         r"L'Hôpital again: $\dfrac{Ax^x((\ln x+1)^2 + \frac1x) - \frac{B}{x^2} + 6Cx}{2} \to \dfrac{2A - B + 6C}{2} = -6$.",
         r'Solving: $A = 5$, $B = 4$, $C = -3$.'])]))
    qs.append(question('2', 10, '', [item('', r'Given is the following integral $$I=\int\frac{2x^5+4x^4+10x^3+22x^2+4x+5}{(x+1)^2(x^2+4)}\,dx = \int p(x)\,dx+\int\frac{A}{x+1}\,dx+\int\frac{B}{(x+1)^2}\,dx+\int\frac{Cx+D}{x^2+4}\,dx$$ Give $p(x)$ and $A,B,C,D\in\mathbb{Z}$. You don’t need to compute the integrals of each term.',
        [EX('$p(x) =$', 2 * x), N('$A =$', -2), N('$B =$', 3), N('$C =$', 2), N('$D =$', 1)], 10, 'partial-fractions',
        r'Expand the denominator ($x^4 + 2x^3 + 5x^2 + 8x + 4$) and do polynomial long division first; then decompose the remainder fraction.',
        [r'$(x+1)^2(x^2+4) = x^4+2x^3+5x^2+8x+4$; long division gives quotient $2x$ and remainder $6x^2 - 4x + 5$.',
         r'$6x^2-4x+5 = A(x+1)(x^2+4) + B(x^2+4) + (Cx+D)(x+1)^2$.',
         r'Comparing coefficients: $A + C = 0$, $A + B + 2C + D = 6$, $4A + C + 2D = -4$, $4A + 4B + D = 5$.',
         r'Solution: $p(x) = 2x$, $A = -2$, $B = 3$, $C = 2$, $D = 1$.'])]))
    graphs = img('2021-07-q3a-graphs.png', 'Four graphs: function A top left, B top right, C bottom left, D bottom right')
    opts = ['Function A', 'Function B', 'Function C', 'Function D']
    qs.append(question('3', 15, SEL, [
        item('(a)', r'Match the graphs shown in Figure 1 to the following functions: i. $f(x)=xe^{-x}$; ii. $f(x)=e^x$; iii. $f(x)=e^{x^2}$; iv. $f(x)=e^{-x}$. %s *Figure 1: Top left: Function A, Top right: Function B, Bottom left: Function C, Bottom right: Function D.*' % graphs,
             [CH(r'i. $f(x) = xe^{-x}$', opts, 0, pts=1.5), CH(r'ii. $f(x) = e^x$', opts, 2, pts=1.5), CH(r'iii. $f(x) = e^{x^2}$', opts, 3, pts=1.5), CH(r'iv. $f(x) = e^{-x}$', opts, 1, pts=1.5)],
             6, 'domain-range', r'Look at the behaviour for $x\to\pm\infty$ and whether the graph is symmetric or has a maximum.',
             [r'$xe^{-x}$ goes to $-\infty$ for $x\to-\infty$ and has a maximum at $x = 1$: A.', r'$e^x$ increases from $0$: C. $e^{x^2}$ is a symmetric U-shape: D. $e^{-x}$ decreases to $0$: B.']),
        item('(b)', r'Which of the following functions is not even?',
             [CH('', [r'$f(x)=0$;', r'$f(x)=\cos(x)$;', r'$f(x)=x^4+x^2$;', 'None of the above.'], 3)], 3, 'even-odd',
             r'Check $f(-x) = f(x)$ for each one.', [r'All three satisfy $f(-x) = f(x)$ (the zero function is both even and odd). **(D)**']),
        item('(c)', r'Let $f(x)$ be an odd function, and $g(x)$ be an even function. If $f, g$ are differentiable everywhere, then',
             [CH('', [r"$f'(x)$ is even, and $g'(x)$ is even.", r"$f'(x)$ is odd, and $g'(x)$ is even.", r"$f'(x)$ is even, and $g'(x)$ is odd.", r"$f'(x)$ is odd, and $g'(x)$ is odd."], 2)], 3, 'even-odd',
             r'Differentiate $f(-x) = -f(x)$ and $g(-x) = g(x)$ with the chain rule.',
             [r"$-f'(-x) = -f'(x) \Rightarrow f'(-x) = f'(x)$: even.", r"$-g'(-x) = g'(x)$: odd. **(C)**"]),
        item('(d)', r'Which of the following functions is *not differentiable* in the most points on the interval $[-100,100]$? (A) $f(x)=\begin{cases}x+2 & \text{if } x<-1;\\ |x| & \text{if } -1\le x\le1;\\ -x+2 & \text{if } x>1.\end{cases}$ (B) $f(x)=\begin{cases}0 & \text{if } x\in\mathbb{Q};\\ 1 & \text{if } x\in\mathbb{R}.\end{cases}$ (C) $f(x)=|\sin(x)|$; (D) $f(x)=\ln|x|+x^4-17$.',
             [CH('', ['(A)', '(B)', '(C)', '(D)'], 1)], 3, 'continuity',
             r'Count the points where each function has a corner, a jump or is undefined. A function that jumps between $0$ and $1$ on every interval is nowhere continuous.',
             [r'(A) has corners at $x = -1, 0, 1$: 3 points. (C) has corners at the multiples of $\pi$: 63 points. (D) fails only at $x = 0$.',
              r'(B) is the indicator-type function that is discontinuous everywhere, hence differentiable nowhere. **(B)**']),
    ]))
    qs.append(question('4', 5, '', [item('', r'Let $f_c(x)=\frac14x^3$ for $0<x<c$ and $f_c(x)=0$ otherwise. For what value $c$ can $f_c(x)$ be a pdf?',
        [N('$c =$', 2)], 5, 'continuous', r'$f_c \ge 0$ for $c > 0$; set $\int_0^c\frac14x^3dx = 1$.',
        [r'$\int_0^c\frac14x^3dx = \frac1{16}c^4 = 1 \iff c^4 = 16$.', r'$c > 0$, so $c = 2$.'])]))
    qs.append(question('5', 5, '', [item('', r'Compute the following integral using a trigonometric substitution $$\int\frac{dx}{\sqrt{9-x^2}}=A\arcsin\left(\frac{x}{B}\right)+C.$$ with $A,B\in\mathbb{N}$ and $C$ an arbitrary constant.',
        [N('$A =$', 1), N('$B =$', 3)], 5, 'substitution', r'Substitute $x = 3\sin\varphi$, so $dx = 3\cos\varphi\,d\varphi$ and $\sqrt{9 - x^2} = 3\cos\varphi$.',
        [r'$x = 3\sin\varphi$: $\displaystyle\int\frac{3\cos\varphi\,d\varphi}{3\cos\varphi} = \int d\varphi = \varphi + C = \arcsin\left(\frac x3\right) + C$.', r'$A = 1$, $B = 3$.'])]))
    qs.append(question('6', 5, '', [item('', r'In the previous exam we saw that the expectation of a 41-sided dice with pips $1,2,\dots,41$ has an expectation of 21. Let us now consider a doubling cube with pips $2,4,8,16,\dots,2^n$. What is the minimal number of sides this doubling cube must have to also have an expectation of 21?',
        [N('$n =$', 6)], 5, 'discrete', r'$E(X) = \frac1n\sum_{i=1}^n 2^i$. Try $n = 1, 2, 3, \dots$',
        [r'$E = \frac1n(2 + 4 + \dots + 2^n)$: $n=1$: $2$; $n=2$: $3$; $n=3$: $\frac{14}3$; …', r'$n = 6$: $\frac16(2+4+8+16+32+64) = 21$. So $6$ sides.'])]))
    qs.append(question('7', 10, TFI, [
        item('(a)', r'Let $b$ be a positive root of $b^5-5b^2+1=0$, with $b\approx1.66798$. The function $f(x)=x^4-2x$ for $-1<x<b$, and $f(x)=0$ otherwise, is a pdf.', [TF(False)], 2, 'continuous',
             r'A pdf must be non-negative everywhere. Try a value such as $x = 1$.', [r'$f(1) = 1 - 2 = -1 < 0$, so it is not a pdf. **False**']),
        item('(b)', r'Let $f(x)=|\cos(x)|$. Its limit at $\frac{\pi}{2}$ exists and is equal to $0$.', [TF(True)], 2, 'limits',
             r'Limits are about values, not about derivatives.', [r'$|\cos x|$ is continuous, so the limit is $|\cos\frac\pi2| = 0$ (only the derivative fails to exist). **True**']),
        item('(c)', r'For an even function $f(x)$, we have $\int_0^af(x)dx=\int_{-a}^0f(x)dx$.', [TF(True)], 2, 'even-odd',
             r'An even function is symmetric in the $y$-axis.', [r'Substitute $x\mapsto -x$: the two areas are mirror images. **True**']),
        item('(d)', r'$\int\frac{3x^2}{x^3}dx=3\ln(x)+C$', [TF(False)], 2, 'substitution',
             r'What is the antiderivative of $\frac1x$ on the whole domain $x \neq 0$?', [r'$\int\frac3x dx = 3\ln|x| + C$ (absolute value needed). **False**']),
        item('(e)', r'There exist polynomial functions $f(x):\mathbb{R}\to\mathbb{R}$ that have zero roots. (A polynomial function is a function $f(x)=\sum_{i=0}^na_ix^i$ for some $n\in\mathbb{N}$ and some $a_i\in\mathbb{R}$.)', [TF(True)], 2, 'domain-range',
             r'Think of a parabola that stays above the $x$-axis.', [r'For example $f(x) = x^2 + 2$ has no real roots. **True**']),
    ]))
    fq8 = R(1, 2) * (exp(yx) - exp(-yx)) * sin(x)
    qs.append(question('8', 5, '', [item('', r'Let $f(x,y)=\frac12(e^y-e^{-y})\sin(x)$. First, determine $\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(x,y)$ and then use this result to determine the value $\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(\pi,\ln(2))\in\mathbb{Q}$.',
        [EX(r'$\dfrac{\partial}{\partial x}\dfrac{\partial}{\partial y}f(x,y) =$', diff(fq8, yx, x), vars=('x', 'y'), sample={'x': [-2, 2], 'y': [-1, 1]}), N(r'Value at $(\pi,\ln 2)$:', R(-5, 4))], 5, 'partial-derivatives',
        r'Differentiate with respect to $y$ first ($\frac{d}{dy}e^{-y} = -e^{-y}$), then with respect to $x$.',
        [r'$\frac{\partial}{\partial y}f = \frac12(e^y + e^{-y})\sin x$; $\frac{\partial}{\partial x}$: $\frac12(e^y+e^{-y})\cos x$.', r'At $(\pi,\ln2)$: $\frac12(2 + \frac12)(-1) = -\frac54$.'])]))
    qs.append(question('9', 5, '', [item('', r'Find a point $(x,y)$ on $f(x)=x^3-6x+7$ where the tangent line to $f$ in $(x,y)$ is parallel to the tangent line to $f$ at $(-3,2)$.',
        [N('$x =$', 3), N('$y =$', 16)], 5, 'implicit-tangent', r'Parallel lines have equal slopes: solve $f^{\prime}(x) = f^{\prime}(-3)$ for the other solution.',
        [r"$f'(x) = 3x^2 - 6$, $f'(-3) = 21$.", r'$3x^2 - 6 = 21 \iff x = \pm3$; the other point is $x = 3$, $y = f(3) = 16$.'])]))
    qs.append(question('10', 10, '', [item('', r'Compute the following integral using partial integration $$\int_0^\pi\frac1\pi x^2\cos(4x)\,dx=\frac1\pi\left(p(x)\sin(4x)\Big|_0^\pi-\int_0^\pi q(x)\sin(4x)\,dx\right)=\frac1\pi\Big(\big(r(x)\sin(4x)+s(x)\cos(4x)\big)\Big|_0^\pi\Big)=A$$ with $p(x),q(x),r(x)$, and $s(x)$ polynomials in $x$ and $A\in\mathbb{Q}$.',
        [EX('$p(x) =$', x ** 2 / 4), EX('$q(x) =$', x / 2), EX('$r(x) =$', x ** 2 / 4 - R(1, 32)), EX('$s(x) =$', x / 8), N('$A =$', R(1, 8))], 10, 'by-parts',
        r'By parts twice: first $f = x^2$, $g^{\prime} = \cos(4x)$ (so $g = \frac14\sin 4x$), then $f = x$, $g^{\prime} = \sin(4x)$.',
        [r'First step: $p(x) = \frac14x^2$ and $q(x) = \frac12x$.', r'$\int\frac12x\sin(4x)dx = -\frac18x\cos(4x) + \frac1{32}\sin(4x)$.',
         r'So the antiderivative is $\big(\frac14x^2 - \frac1{32}\big)\sin(4x) + \frac18x\cos(4x)$: $r(x) = \frac14x^2 - \frac1{32}$, $s(x) = \frac18x$.',
         r'$A = \frac1\pi\big(\frac18\pi\cos 4\pi - 0\big) = \frac18$.'])]))
    qs.append(question('11', 11, 'Compute the following limits:', [
        item('(a)', r'$\lim_{x\to1}\dfrac{x^3-7x+6}{x^2-1}$', [N('Limit:', -2)], 5, 'limits', r'Factor: $x = 1$ is a root of both numerator and denominator.',
             [r'$\frac{(x-1)(x-2)(x+3)}{(x-1)(x+1)} = \frac{(x-2)(x+3)}{x+1} \to \frac{-4}{2} = -2$.']),
        item('(b)', r'$\lim_{t\to\infty}(e^t+t)^{\frac1t}$', [N('Limit:', E)], 6, 'lhopital', r'Form $\infty^0$: take the logarithm, $\ln L = \lim\frac{\ln(e^t + t)}{t}$, and apply L\'Hôpital.',
             [r'$\ln L = \lim\frac{\ln(e^t+t)}{t} \overset{LH}{=} \lim\frac{e^t + 1}{e^t + t} \overset{LH}{=} \lim\frac{e^t}{e^t + 1} \overset{LH}{=} 1$.', r'So $L = e$.']),
    ]))
    return exam('2021-2', year='2021–2022', sitting=2, kind='Resit', date='July 5, 2022', iso='2022-07-05', minutes=120,
                file='calc-exam-2021-02', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2022_1():
    qs = []
    qs.append(question('1', 10, '', [item('', r'Given is the implicit equation $y(-x^2-y^2+1)-\frac{4}{25}=0$. Compute the slope $m$ and intercept $b$ of the tangent line $y=mx+b$ through the point $A=\left(\frac25,\frac15\right)$. [Hint: $m,b\in\mathbb{Q}$ and $\frac{m}{b}\in\mathbb{Z}$.]',
        [N('$m =$', R(2, 9)), N('$b =$', R(1, 9))], 10, 'implicit-tangent',
        r'Differentiate implicitly (product rule on $y\cdot(\dots)$), solve for $\frac{dy}{dx}$, substitute $A$, then use the point-slope form.',
        [r"$0 = y'(-x^2-y^2+1) + y(-2x - 2yy') = (-x^2-3y^2+1)y' - 2xy$.", r"$y' = \dfrac{2xy}{-x^2-3y^2+1}$; at $A$: $\dfrac{4/25}{18/25} = \frac29$.",
         r'$y - \frac15 = \frac29(x - \frac25) \Rightarrow y = \frac29x + \frac19$.'])]))
    qs.append(question('2', 7, '', [item('', r'Compute the following series $$\frac{1}{2n+1}+\frac{1}{2n+2}+\cdots+\frac{1}{6n}$$ when $n$ goes to infinity. [Hint: your answer lies in the set $\{\ln(\frac12), 0, \ln(\frac32), \ln(2), \ln(\frac52), \ln(3), \ln(\frac72), \ln(4)\}$.]',
        [N('Limit:', log(3))], 7, 'riemann', r'Write the sum as $\sum_{r=1}^{4n}\frac{1}{2n + r} = \sum\frac1n\cdot\frac{1}{2 + r/n}$; $x = r/n$ runs from $0$ to $4$.',
        [r'$\lim\sum_{r=1}^{4n}\frac1n\cdot\frac{1}{2 + \frac rn} = \int_0^4\frac{1}{2+x}dx$.', r'$= \ln|2+x|\Big|_0^4 = \ln6 - \ln2 = \ln3$.'])]))
    qs.append(question('3', 8, '', [item('', r'Rewrite, using partial fractions, the left hand side equation into the form on the right $$\frac{7x^2-2x+1}{x^3-x^2+x-1}=\frac{p_n(x)}{p_d(x)}+\frac{q_n(x)}{q_d(x)}$$ where $p_n,p_d,q_n,q_d$ are polynomials with $deg(p_d)<deg(q_d)$.',
        [EX(r'$\dfrac{p_n(x)}{p_d(x)} =$', 3 / (x - 1), sample={'x': [1.5, 4]}), EX(r'$\dfrac{q_n(x)}{q_d(x)} =$', (4 * x + 2) / (x ** 2 + 1), sample={'x': [1.5, 4]})], 8, 'partial-fractions',
        r'Factor the denominator: $x = 1$ is a root, so $x^3 - x^2 + x - 1 = (x-1)(x^2+1)$. Then $\frac{A}{x-1} + \frac{Bx+C}{x^2+1}$.',
        [r'$x^3-x^2+x-1 = (x-1)(x^2+1)$.', r'$7x^2-2x+1 = A(x^2+1) + (Bx+C)(x-1)$; $x=1$: $A = 3$; $x = 0$: $C = 2$; $x=-1$: $B = 4$.', r'So $\dfrac{3}{x-1} + \dfrac{4x+2}{x^2+1}$.'])]))
    qs.append(question('4', 7, '', [item('', r'Calculate the following limit $$\lim_{x\to0}(1+2x)^{\frac{1}{3x}}$$',
        [N('Limit:', exp(R(2, 3)))], 7, 'lhopital', r'Form $1^\infty$: compute $\ln A = \lim\frac{\ln(1+2x)}{3x}$ with L\'Hôpital.',
        [r'$\ln A = \lim\frac{\ln(1+2x)}{3x} \overset{LH}{=} \lim\frac{2/(1+2x)}{3} = \frac23$.', r'$A = e^{2/3}$.'])]))
    qs.append(question('5', 6, '', [item('', r'Use substitution to transform the following integral $$\int_0^2 8e^{-\sqrt{1+2x^2}}x^5\,dx=\int_a^b e^{-u}p(u)\,du$$ where $p(u)$ is a polynomial in $u$ with integer coefficients ($\mathbb{Z}$) and $a,b\in\mathbb{N}$.',
        [EX('$p(u) =$', u ** 5 - 2 * u ** 3 + u, vars=('u',)), N('$a =$', 1), N('$b =$', 3)], 6, 'substitution',
        r'With $u = \sqrt{1+2x^2}$: $u\,du = 2x\,dx$ and $x^2 = \frac12(u^2-1)$. Write $x^5 = x^2\cdot x^2\cdot x$.',
        [r'$u^2 = 1 + 2x^2 \Rightarrow 2u\,du = 4x\,dx \Rightarrow x\,dx = \frac12u\,du$; bounds $u(0) = 1$, $u(2) = 3$.',
         r'$8\int e^{-u}\cdot\frac12(u^2-1)\cdot\frac12(u^2-1)\cdot\frac12u\,du = \int_1^3 e^{-u}(u^5 - 2u^3 + u)\,du$.'])]))
    qs.append(question('6', 10, TFI, [
        item('(a)', r'If $\int_{-1}^1 4x^2+bx+3\,dx=\int_{-1}^1 4x^2+3\,dx$ then $b=0$.', [TF(False)], 2, 'even-odd', r'What is $\int_{-1}^1 bx\,dx$ for any $b$?', [r'$bx$ is odd, so its integral over $[-1,1]$ is $0$ for every $b$. **False**']),
        item('(b)', r"If $f:[0,1]\to\mathbb{R}$ is differentiable and $f(0)=f(1)$ then $f'(x)=0$ for some $x\in(0,1)$.", [TF(True)], 2, 'function-analysis', r"Rolle's theorem.", [r'Differentiable implies continuous, so Rolle applies. **True**']),
        item('(c)', r"If $\lim_{x\to\infty}f'(x)=0$, then $f$ has a horizontal asymptote", [TF(False)], 2, 'asymptotes', r'Think of $\ln x$.', [r"$f(x) = \ln x$: $f'(x) = \frac1x\to0$ but $f\to\infty$. **False**"]),
        item('(d)', r"$[f(\ln(x))]^{\prime}=\dfrac{f'(x)}{x}$", [TF(False)], 2, 'derivative-rules', r'Chain rule: where is $f^{\prime}$ evaluated?', [r"$[f(\ln x)]^{\prime} = \dfrac{f'(\ln x)}{x}$. **False**"]),
        item('(e)', r'If $f:\mathbb{R}\to\mathbb{R}$ is even and convex, then $f$ has a minimum at $0$.', [TF(True)], 2, 'concavity', r'Use the chord between $(-x, f(x))$ and $(x, f(x))$.',
             [r'For convex $f$ the chord between $(-x, f(-x)) = (-x, f(x))$ and $(x, f(x))$ lies above the graph, in particular above $(0, f(0))$; so $f(0)\le f(x)$. **True**']),
    ]))
    Aa, Bb = sp.symbols('A b', positive=True)
    opts7 = [r'$\sqrt{\frac{1}{abA}}$', r'$\sqrt{\frac{A}{ab}}$', r'$\sqrt{\frac{b}{aA}}$', r'$\sqrt{\frac{bA}{a}}$', r'$\sqrt{\frac{a}{bA}}$', r'$\sqrt{\frac{aA}{b}}$', r'$\sqrt{\frac{ab}{A}}$', r'$\sqrt{abA}$']
    qs.append(question('7', 7, '', [item('', r'You are designing a rectangular poster to contain a fixed amount $A$ for the printed area (measured in square centimeters) and have margins of $a$ centimeters at the top and bottom and $b$ centimeters at the sides. Find the horizontal dimension of the printed area on the poster (in terms of $a$, $b$, and $A$) if you want to minimize the amount of posterboard needed. [Hint: your answer lies in $\{\sqrt{\frac{1}{abA}}, \sqrt{\frac{A}{ab}}, \sqrt{\frac{b}{aA}}, \sqrt{\frac{bA}{a}}, \sqrt{\frac{a}{bA}}, \sqrt{\frac{aA}{b}}, \sqrt{\frac{ab}{A}}, \sqrt{abA}\}$]',
        [CH('Horizontal dimension $x =$', opts7, 3)], 7, 'function-analysis',
        r'Printed area $xy = A$; the board is $(x + 2b)(y + 2a)$. Eliminate $y = A/x$ and minimise over $x$.',
        [r'Board: $(x+2b)(\frac Ax + 2a) = A + 2ax + \frac{2bA}{x} + 4ab$.', r'Derivative: $2a - \frac{2bA}{x^2} = 0 \Rightarrow x^2 = \frac{bA}{a}$.', r'$x = \sqrt{\frac{bA}{a}}$.'])]))
    qs.append(question('8', 15, SEL, [
        item('(a)', r'Consider the following two statements $$1.\ \int\frac{1}{(x+2)^2(x-4)}dx=\int\frac{A}{x+2}+\frac{B}{(x+2)^2}+\frac{C}{x-4}dx$$ $$2.\ \int\frac{1}{(x-2)(x^2-4)}dx=\int\frac{A}{x-2}+\frac{Bx+C}{x^2-4}dx$$ for some yet undetermined values of $A$, $B$, and $C$. Then',
             [CH('', ['Both statements are correct', 'Statement 1 is correct, statement 2 is wrong', 'Statement 1 is wrong, statement 2 is correct', 'Both statements are wrong'], 1)], 3, 'partial-fractions',
             r'Factor $x^2 - 4$ completely in statement 2.', [r'Statement 1 is the standard form. In 2, $(x-2)(x^2-4) = (x-2)^2(x+2)$ — a repeated linear factor, not an irreducible quadratic. **(B)**']),
        item('(b)', r'The domain of the function $f(x)=\sqrt{\ln\frac{1}{|x|}}$ is',
             [CH('', [r'$(-\infty,-1]\cup[1,\infty)$', r'$[1,\infty)$', r'$[-1,1]$', 'None of the above'], 3)], 3, 'domain-range',
             r'Need $x\neq0$ and $\ln\frac1{|x|}\ge0$, i.e. $\frac1{|x|}\ge1$.', [r'$D_f = [-1,0)\cup(0,1]$, which is not listed. **(D)**']),
        item('(c)', r'The function $\dfrac{x^2+2x-5}{x-3}$ has a slant asymptote of',
             [CH('', [r'$y=x-3$', r'$y=x+3$', r'$y=x+4$', r'$y=x+5$'], 3)], 3, 'asymptotes', r'Long division by $x - 3$.', [r'$\frac{x^2+2x-5}{x-3} = x + 5 + \frac{10}{x-3}$. **(D)**']),
        item('(d)', r'The function $\lfloor x^3-2x^2+x\rfloor$ has a derivative at (Note that $\lfloor x\rfloor$ denotes the flooring function.)',
             [CH('', [r'$x=0$', r'$x=+1$', r'$x=-1$', 'This function has no derivative in any integer point.'], 1)], 3, 'continuity',
             r'$x^3 - 2x^2 + x = x(x-1)^2$. Near which point does the inside stay within one integer step?',
             [r'Near $x = 1$, $x(x-1)^2$ is a small non-negative number, so the floor is constantly $0$: derivative $0$. At $x = 0$ and $x=-1$ the floor jumps. **(B)**']),
        item('(e)', r'The derivative of the function $\ln(\sin x+\cos x)$ at $x=\frac{\pi}{2}$ is',
             [CH('', ['$0$', '$+1$', '$-1$', r'$+\infty$'], 2)], 3, 'derivative-rules', r'Chain rule: $\frac{\cos x - \sin x}{\sin x + \cos x}$.', [r"$f'(\frac\pi2) = \frac{0 - 1}{1 + 0} = -1$. **(C)**"]),
    ]))
    qs.append(question('9', 6, '', [item('', r'Given is the following distribution function $$f(x)=\begin{cases}0 & \text{if } x\le2,\\ \frac12x-1 & \text{if } 2<x\le3,\\ -\frac16x+1 & \text{if } 3<x\le6,\\ 0 & \text{if } x>6.\end{cases}$$ which has a cumulative distribution function of the form $$F(x)=\begin{cases}0 & \text{if } x\le2,\\ \frac14x^2-x+C_1 & \text{if } 2<x\le3,\\ -\frac1{12}x^2+x+C_2 & \text{if } 3<x\le6,\\ 1 & \text{if } x>6.\end{cases}$$ Determine $C_1$ and $C_2$.',
        [N('$C_1 =$', 1), N('$C_2 =$', -2)], 6, 'continuous', r'The cdf is continuous: $F(2) = 0$ and $F(6) = 1$.',
        [r'$F(2) = 1 - 2 + C_1 = 0 \Rightarrow C_1 = 1$.', r'$F(6) = -3 + 6 + C_2 = 1 \Rightarrow C_2 = -2$.', r'Check at $x = 3$: $\frac94 - 3 + 1 = \frac14 = -\frac34 + 3 - 2$.'])]))
    qs.append(question('10', 6, '', [item('', r'Suppose we throw 3 fair coins. Let the variable $X$ be the amount that you can win or lose in this experiment and be defined as follows. If you throw 3 heads, you win 200 Euro, however, if you throw 1 tail you loose 12 Euro, if you throw 2 tails you loose 24 Euro, and if you throw 3 tails you loose 36 Euro. What is the expected amount that you win or loose in this experiment? [Hint: $\mathbb{E}[X]\in\mathbb{N}$.]',
        [N(r'$\mathbb{E}[X] =$', 7)], 6, 'discrete', r'Number of tails is binomial($3,\frac12$): probabilities $\frac18,\frac38,\frac38,\frac18$.',
        [r'$E[X] = 200\cdot\frac18 - 12\cdot\frac38 - 24\cdot\frac38 - 36\cdot\frac18 = 25 - 4.5 - 9 - 4.5 = 7$.'])]))
    qs.append(question('11', 8, '', [item('', r'Let $f(x,y)=\dfrac{x^{2y}+(y-1)(y-2)(y-3)}{e}$. Evaluate $\dfrac{\partial}{\partial x}\left(\dfrac{\partial}{\partial y}f(x,y)\right)$ in the point $(e,1)$. [Hint: your answer is a natural number.]',
        [N('Value:', 6)], 8, 'partial-derivatives', r'The polynomial in $y$ disappears after differentiating with respect to $x$. Use $\frac{\partial}{\partial x}x^{2y} = 2y\,x^{2y-1}$.',
        [r'$\frac{\partial}{\partial x}f = \frac1e\,2y\,x^{2y-1}$.', r'$\frac{\partial}{\partial y}$: $\frac1e\big(2x^{2y-1} + 2y\,x^{2y-1}\cdot2\ln x\big)$.', r'At $(e,1)$: $\frac1e(2e + 4e) = 6$.'])]))
    return exam('2022-1', year='2022–2023', sitting=1, kind='Exam', date='June 16, 2023', iso='2023-06-16', minutes=120,
                file='calc-exam-2022-01', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2022_2():
    qs = []
    qs.append(question('1', 10, '', [item('', r'Given is the implicit equation $y^2(1-x-y)^2-2=0$. Compute the slope $m$ and intercept $b$ of the tangent line $y=mx+b$ through the point $A=\left(\frac35,\frac75\right)$. [Hint: $m,b\in\mathbb{Q}$ and $\frac{b}{m}\in\mathbb{Z}$.]',
        [N('$m =$', R(-7, 12)), N('$b =$', R(7, 4))], 10, 'implicit-tangent',
        r"Differentiate implicitly (product + chain rule), factor out $2y(1-x-y)$, solve for $y'$ and substitute $A$.",
        [r"$0 = 2yy'(1-x-y)^2 + y^2\cdot2(1-x-y)(-1-y')$; dividing by $2y(1-x-y)$: $0 = (1-x-2y)y' - y$.", r"$y' = \dfrac{y}{1-x-2y}$; at $A$: $\dfrac{7/5}{-12/5} = -\frac7{12}$.",
         r'$y - \frac75 = -\frac7{12}(x - \frac35) \Rightarrow y = -\frac7{12}x + \frac74$.',
         r'(Remark: $A$ does not satisfy the curve equation exactly — the official solution evaluates the slope formula at $A$, as done here.)'])]))
    qs.append(question('2', 6, '', [item('', r"Compute the derivative of the function $f(x)=x^{\ln x}$ and show that $$f'(x)=A\cdot x^B\cdot\ln(x)$$ with $A\in\{1,2,3,4\}$ and $B\in\{\ln(x),\ln(x)+1,\ln(x)-1,1-\ln(x)\}$.",
        [CH('$A =$', ['$1$', '$2$', '$3$', '$4$'], 1), CH('$B =$', [r'$\ln(x)$', r'$\ln(x)+1$', r'$\ln(x)-1$', r'$1-\ln(x)$'], 2)], 6, 'derivative-rules',
        r"Logarithmic differentiation: $\ln f = (\ln x)^2$, so $\frac{f'}{f} = \frac{2\ln x}{x}$.",
        [r'$\ln f(x) = \ln x\cdot\ln x = (\ln x)^2$, so $[\ln f]^{\prime} = \frac{2\ln x}{x}$.', r"$f'(x) = x^{\ln x}\cdot\frac{2\ln x}{x} = 2x^{\ln x - 1}\ln x$: $A = 2$, $B = \ln(x) - 1$."])]))
    tri = img('2023-07-q3-triangle.png', 'Equilateral triangle with an inscribed rectangle of width x and height y; t on both sides of the base')
    tt = sp.Symbol('t', real=True)
    qs.append(question('3', 10, r'Consider a paper in the form of an equilateral triangle where each side has a length of $a$. What is the maximum area of a rectangle that you can cut off from this paper? %s Let $x$ be the width of the rectangle tangent to the base of the triangle and $y$ the height as shown in the figure. Let $t$ be the lenght of the triangle base left and right of the rectangle base, i.e., $a=x+2t$.' % tri, [
        item('(a)', r'What is the angle of each triangle corner (in radians)?', [N('Angle:', pi / 3)], 2, 'function-analysis', r'All three angles of an equilateral triangle are equal and sum to $\pi$.', [r'$60^\circ = \frac13\pi$.']),
        item('(b)', r'Express the height $y$ in terms of $t$ using the right-angle triangle with sides $y$ and $t$.', [EX('$y =$', sqrt(3) * tt, vars=('t',), sample={'t': [0.5, 3]})], 2, 'function-analysis', r'$\tan(\frac\pi3) = \frac{y}{t}$.', [r'$\sqrt3 = \tan(\frac13\pi) = \frac yt \Rightarrow y = \sqrt3\,t$.']),
        item('(c)', r'Express $y$ in terms of $a$ and $x$.', [EX('$y =$', sqrt(3) * (a - x) / 2, vars=('a', 'x'), sample={'a': [2, 5], 'x': [0.2, 1.5]})], 2, 'function-analysis', r'Use $a = x + 2t$ to eliminate $t$.', [r'$t = \frac{a-x}2$, so $y = \frac{a-x}{2}\sqrt3$.']),
        item('(d)', r'Express the area of the rectangle in terms of $x$ and $a$. What value does $x$ take for the area to be maximal?',
             [EX('Area $=$', x * (a - x) * sqrt(3) / 2, vars=('x', 'a'), sample={'a': [2, 5], 'x': [0.2, 1.5]}, pts=1), EX('Maximising $x =$', a / 2, vars=('a',), sample={'a': [1, 5]}, pts=1)], 2, 'function-analysis',
             r'Area $= x\cdot y$; differentiate with respect to $x$ ($a$ is a constant).', [r'$A(x) = x\cdot\frac{a-x}2\sqrt3$; $A^{\prime}(x) = \frac12\sqrt3a - \sqrt3x = 0 \Rightarrow x = \frac12a$.']),
        item('(e)', r'What is the maximal area for the rectangle in terms of $a$?', [EX('Maximal area $=$', sqrt(3) * a ** 2 / 8, vars=('a',), sample={'a': [1, 5]})], 2, 'function-analysis', r'Substitute $x = \frac a2$ into the area.', [r'$\frac12a\cdot\frac12(a - \frac12a)\sqrt3 = \frac18\sqrt3a^2$.']),
    ]))
    qs.append(question('4', 7, '', [item('', r'Compute the following series $$\frac1n+\frac{1}{\sqrt{n^2+n}}+\frac{1}{\sqrt{n^2+2n}}+\cdots+\frac{1}{3n}$$ when $n$ goes to infinity.',
        [N('Limit:', 4)], 7, 'riemann', r'The general term is $\frac{1}{\sqrt{n^2 + rn}} = \frac1n\cdot\frac{1}{\sqrt{1 + r/n}}$; the last term $\frac1{3n} = \frac1{\sqrt{9n^2}}$ gives $r = 8n$.',
        [r'$\lim\sum_{r=0}^{8n}\frac1n\cdot\frac{1}{\sqrt{1+\frac rn}} = \int_0^8\frac{1}{\sqrt{1+x}}dx$.', r'$= 2\sqrt{1+x}\Big|_0^8 = 6 - 2 = 4$.'])]))
    qs.append(question('5', 6, '', [item('', r'If $$\lim_{x\to2}\frac{A\ln\left(\frac12x\right)+B(x-1)^2+Ce^{2-x}}{(2-x)^2}=\frac12$$ then what are the values of $A,B,C\in\mathbb{Q}$?',
        [N('$A =$', R(-12, 5)), N('$B =$', R(2, 5)), N('$C =$', R(-2, 5))], 6, 'lhopital',
        r'Numerator $\to0$ at $x = 2$ gives $B + C = 0$; after one L\'Hôpital step the numerator must vanish again; the second step gives the value $\frac12$.',
        [r'At $x=2$: $A\ln1 + B + C = 0 \Rightarrow C = -B$.', r"L'Hôpital: $\dfrac{\frac Ax + 2B(x-1) - Ce^{2-x}}{-2(2-x)}$; numerator at $2$: $\frac A2 + 2B - C = \frac A2 + 3B = 0$.",
         r"L'Hôpital again: $\dfrac{-\frac{A}{x^2} + 2B + Ce^{2-x}}{2} \to \dfrac{-\frac A4 + 2B + C}{2} = \dfrac{-\frac A4 + B}{2} = \frac12$.",
         r'Solving: $A = -\frac{12}5$, $B = \frac25$, $C = -\frac25$.'])]))
    SET8 = ['$a$', '$a+b$', '$a^2$', '$a^2+b$', '$b$', '$b^2$', '$a+b^2$', '$a^2+b^2$']
    qs.append(question('6', 8, '', [item('', r'Compute the following integral using partial integration $$\int\cos(ax)e^{bx}\,dx=\frac{A}{B}\cdot\sin(ax)e^{bx}+\frac{C}{D}\cdot\cos(ax)e^{bx}$$ where $a,b$ are some unspecified values and $$A,B,C,D\in\{a,a+b,a^2,a^2+b,b,b^2,a+b^2,a^2+b^2\}$$',
        [CH('$A =$', SET8, 0), CH('$B =$', SET8, 7), CH('$C =$', SET8, 4), CH('$D =$', SET8, 7)], 8, 'by-parts',
        r'Integrate by parts twice (integrating the trig factor each time); the original integral reappears — move it to the left-hand side and solve.',
        [r'$\int\cos(ax)e^{bx}dx = \frac1a\sin(ax)e^{bx} + \frac{b}{a^2}\cos(ax)e^{bx} - \frac{b^2}{a^2}\int\cos(ax)e^{bx}dx$.',
         r'$\left(\frac{b^2}{a^2} + 1\right)\int\cos(ax)e^{bx}dx = \frac1a\sin(ax)e^{bx} + \frac{b}{a^2}\cos(ax)e^{bx}$.',
         r'$\int\cos(ax)e^{bx}dx = \frac{a}{a^2+b^2}\sin(ax)e^{bx} + \frac{b}{a^2+b^2}\cos(ax)e^{bx}$.'])]))
    qs.append(question('7', 10, TFI, [
        item('(a)', r'The function $\lfloor x^2\rfloor$ on the domain $[1,2)$ has a derivative everywhere except for $x=\sqrt2$ and $x=\sqrt3$.', [TF(False)], 2, 'continuity', r'What happens at the left endpoint $x = 1$?', [r'It is also not differentiable at $x = 1$ (the official solution: "f is also discontinuous in 1"). **False**']),
        item('(b)', r'If $f(x)=\sqrt{x}$ and $g(x)=x^2-1$, then $D_{g\circ f}=R_{f\circ g}$, with $D$ the domain, and $R$ the range of the given function.', [TF(True)], 2, 'domain-range',
             r'Compute both sets.', [r'$g\circ f = x - 1$ on $D = [0,\infty)$; $f\circ g = \sqrt{x^2-1}$ has range $[0,\infty)$. Equal. **True**']),
        item('(c)', r'$\lim_{x\to2}\dfrac{\sqrt{x+2}-2}{\sqrt{x+7}-3}=\dfrac23$.', [TF(False)], 2, 'limits', r'L\'Hôpital or conjugates.', [r'$\lim\frac{1/(2\sqrt{x+2})}{1/(2\sqrt{x+7})} = \frac{\sqrt9}{\sqrt4} = \frac32$. **False**']),
        item('(d)', r'If $f$ is an odd function, then it is continuous at $x=0$.', [TF(False)], 2, 'even-odd', r'Find an odd function that is not even defined at $0$.', [r'$f(x) = \frac1{x^3}$ is odd but not continuous at $0$. **False**']),
        item('(e)', r'If $\int f(x)dx=x^4+1$, then $f(\sqrt[3]{x})=4x$.', [TF(True)], 2, 'substitution', r'$f$ is the derivative of $x^4 + 1$.', [r'$f(x) = 4x^3$, so $f(\sqrt[3]x) = 4x$. **True**']),
    ]))
    qs.append(question('8', 15, SEL, [
        item('(a)', r'The domain of the function $f(x)=\sqrt{\dfrac{1}{\ln\left(\frac{1}{2-x^2}\right)}}$ is',
             [CH('', [r'$(-\infty,-1]\cup[1,\infty)$', r'$[1,\infty)$', r'$[-1,1]$', 'None of the above'], 3)], 3, 'domain-range',
             r'Need $2 - x^2 > 0$ and $\ln\frac{1}{2-x^2} > 0$ (it is in a denominator under a root).', [r'$x$ cannot be $\pm\sqrt2$ or $\pm1$; the domain is $(-\sqrt2,-1)\cup(1,\sqrt2)$. **(D)**']),
        item('(b)', r'Let $f(x)=\dfrac{x^3-x^2}{x^2-4}$. We are interested in the total number horizontal, vertical, and slant asymptotes of $f$. The function $f$ has',
             [CH('', ['1 asymptote', '2 asymptotes', '3 asymptotes', '4 asymptotes'], 2)], 3, 'asymptotes', r'$\frac{x^2(x-1)}{(x-2)(x+2)}$: degree 3 over degree 2.', [r'Two vertical asymptotes ($x=\pm2$) and one slant asymptote. **(C)**']),
        item('(c)', r"Given that $\arctan(x)'=\frac{1}{1+x^2}$, what is the derivative of the function $\ln(\arctan(x))$ at $x=1$?",
             [CH('', [r'$\frac{2}{\pi}$', r'$\frac{\pi}{2}$', '$0$', r'$\infty$'], 0)], 3, 'derivative-rules', r'Chain rule.', [r"$y' = \frac{1}{(1+x^2)\arctan x}$; at $1$: $\frac{1}{2\cdot\pi/4} = \frac2\pi$. **(A)**"]),
        item('(d)', r'Let $\lfloor x\rfloor$ be the floor function. The function $\lfloor\sqrt{4-x^2}\rfloor$ has a derivative at',
             [CH('', [r'$x=0$', r'$x=1$', r'$x=2$', 'This function has no derivative in any integer point.'], 1)], 3, 'continuity', r'Near $x = 1$, $\sqrt{4 - x^2}\approx1.73$.', [r'Near $x = 1$ the floor is constantly $1$, so the derivative is $0$. At $0$ it jumps from $1$ to $2$; $2$ is an endpoint. **(B)**']),
        item('(e)', r"Let $f=\dfrac{1}{x(x-1)(x+1)}$ and consider the following two statements 1. $f$ is odd. 2. $f'$ is even. Then",
             [CH('', ['Both statements are correct', 'Statement 1 is correct, statement 2 is wrong', 'Statement 1 is wrong, statement 2 is correct', 'Both statements are wrong'], 0)], 3, 'even-odd',
             r'$x(x-1)(x+1) = x^3 - x$.', [r'$f(-x) = -f(x)$, and the derivative of an odd function is even. **(A)**']),
    ]))
    qs.append(question('9', 6, '', [item('', r'Let $f(x)=\sqrt{\dfrac{x^3-2x}{4x+2}}$. This function has two slant asymptotes, one when $x$ goes to $-\infty$, and one when $x$ goes to $\infty$. Compute only the **slopes** of these two slant asymptotes.',
        [N(r'Slope for $x\to-\infty$:', R(-1, 2)), N(r'Slope for $x\to\infty$:', R(1, 2))], 6, 'asymptotes',
        r'Slope $= \lim f(x)/x$. Careful: $\frac1x = \pm\sqrt{\frac1{x^2}}$ depending on the sign of $x$.',
        [r'$\frac{f(x)}{x} = \pm\sqrt{\frac{x^3-2x}{x^2(4x+2)}} = \pm\sqrt{\frac{1 - 2/x^2}{4 + 2/x}} \to \pm\frac12$.', r'Slope $-\frac12$ for $x\to-\infty$, $\frac12$ for $x\to\infty$.'])]))
    qs.append(question('10', 6, '', [item('', r'Given is the following function $$f(x)=\begin{cases}kx\sqrt{4-x^2} & \text{if } x\in[0,2],\\ 0 & \text{otherwise.}\end{cases}$$ For what value of $k\in\mathbb{Q}$ is $f$ a distribution function?',
        [N('$k =$', R(3, 8))], 6, 'continuous', r'Normalise with $u = 4 - x^2$, $-\frac12du = x\,dx$.',
        [r'$1 = k\int_0^2x\sqrt{4-x^2}dx = k\int_0^4\frac12\sqrt u\,du = k\cdot\frac13u^{3/2}\Big|_0^4 = \frac83k$.', r'$k = \frac38$.'])]))
    qs.append(question('11', 6, '', [item('', r'Let $f(t,x,y)=te^{-t}\sin(x-y)+e^{-2t}\cos(x+y)$. Evaluate $\dfrac{\partial^3}{\partial y\partial x\partial t}f(t,x,y)$ in the point $(0,\pi,\pi)$. [Hint: the answer is a natural number.]',
        [N('Value:', 2)], 6, 'partial-derivatives', r'Differentiate one variable at a time: first $t$, then $x$, then $y$.',
        [r'$\partial_t$: $(e^{-t} - te^{-t})\sin(x-y) - 2e^{-2t}\cos(x+y)$.', r'$\partial_x$: $(e^{-t}-te^{-t})\cos(x-y) + 2e^{-2t}\sin(x+y)$.', r'$\partial_y$: $(e^{-t}-te^{-t})\sin(x-y) + 2e^{-2t}\cos(x+y)$.', r'At $(0,\pi,\pi)$: $0 + 2\cos(2\pi) = 2$.'])]))
    return exam('2022-2', year='2022–2023', sitting=2, kind='Resit', date='July 7, 2023', iso='2023-07-07', minutes=120,
                file='calc-exam-2022-02', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2023_1():
    qs = []
    qs.append(question('1', 10, '', [item('', r'Given is the implicit equation $x(1-x^2-y^2)-1=0$. Compute the slope $m$ and intercept $b$ of the tangent line $y=mx+b$ through the point $(x,y)=(-1,1)$. [Hint: $m,b\in\mathbb{Q}$.]',
        [N('$m =$', R(3, 2)), N('$b =$', R(5, 2))], 10, 'implicit-tangent', r"Differentiate both sides (product rule on $x\cdot(\dots)$) and solve for $\frac{dy}{dx}$.",
        [r"$0 = (1 - x^2 - y^2) + x(-2x - 2yy') = (-2xy)y' + (1 - 3x^2 - y^2)$.", r"$y' = \dfrac{1-3x^2-y^2}{2xy}$; at $(-1,1)$: $\frac{-3}{-2} = \frac32$.", r'$y - 1 = \frac32(x+1) \Rightarrow y = \frac32x + \frac52$.'])]))
    figs = {k: img('2024-06-q2f-%s.png' % k, 'Option %s graph' % k) for k in 'ABCD'}
    qs.append(question('2', 32, SEL, [
        item('(a)', r'$\lim_{x\to\infty}\dfrac{\sqrt{16x^4+1}}{2x^2-3x+5}$ is', [CH('', ['$0$', '$1$', '$2$', '$4$', '$8$', 'non-existent'], 2)], 4, 'limits', r'Divide numerator and denominator by $x^2$.', [r'$\frac{\sqrt{16 + 1/x^4}}{2 - 3/x + 5/x^2}\to\frac42 = 2$. **(C)**']),
        item('(b)', r'Let $f$ be the piecewise-linear function defined as follows $$f=\begin{cases}2x-2 & \text{for } x<3\\ 2x-4 & \text{for } x\ge3\end{cases}$$ then which of the following three statements are true? I. $\lim_{h\to0^-}\frac{f(3+h)-f(3)}{h}=2$. II. $\lim_{h\to0^+}\frac{f(3+h)-f(3)}{h}=2$. III. $f^{\prime}(3)=2$.',
             [CH('', ['None', 'I only', 'II only', 'III only', 'I and II only', 'I, II, and III'], 2)], 4, 'continuity', r'$f(3) = 2$ comes from the second piece. Compute the left quotient with that value.',
             [r'I: $\frac{(2(3+h)-2) - 2}{h} = 2 + \frac2h\to\pm\infty$ — false.', r'II: $\frac{2h}{h} = 2$ — true. III: $f$ jumps at $3$, so no derivative — false. **(C)**']),
        item('(c)', r'The domain of the function $f=\ln(1-2\ln(e\cdot x))$ is', [CH('', [r'$(0,\frac12e)$', r'$(0,2e)$', r'$(0,e^{-2})$', r'$(0,e^2)$', r'$(0,e^{-\frac12})$', r'$(0,e^{\frac12})$'], 4)], 4, 'domain-range',
             r'Inner: $ex > 0$. Outer: $1 - 2\ln(ex) > 0$.', [r'$\ln(ex) < \frac12 \iff ex < e^{1/2} \iff x < e^{-1/2}$. **(E)**']),
        item('(d)', r'Consider the functions $f(x)=\sin(x)$, $g(x)=|x|$ and $h(x)=x^3$. Which of the following functions is odd (in terms of parity)?', [CH('', ['$g$', r'$g\circ h$', r'$f\circ g$', r'$f\circ h$', r'$f\circ g\circ h$'], 3)], 4, 'even-odd',
             r'Any composition with $g$ (even) on the inside is even.', [r'$f(h(-x)) = \sin(-x^3) = -\sin(x^3)$: odd. The others are even. **(D)**']),
        item('(e)', r'Using partial fractions, the integral $$\int\frac{x^2+1}{(x-1)(x^2-1)}dx$$ can be rewritten as',
             [CH('', [r'$\int\frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{C}{x+1}dx$', r'$\int\frac{A}{x-1}+\frac{B}{(x^2-1)}dx$', r'$\int\frac{A}{x-1}+\frac{Bx+C}{(x^2-1)}dx$', r'$\int\frac{A}{x-1}+\frac{B}{x+1}dx$', r'$\int\frac{Ax+B}{(x^2-1)}+\frac{C}{x+1}dx$', 'None of the above'], 0)], 4, 'partial-fractions',
             r'$x^2 - 1$ is not irreducible.', [r'$(x-1)(x^2-1) = (x-1)^2(x+1)$: repeated linear factor. **(A)**']),
        item('(f)', r'The graph $f^{\prime}$ of the derivative of a function $f$ is shown below %s which of the following could be the graph of $f$?' % img('2024-06-q2f-fprime.png', "Graph of f' on [0, 6]"),
             [CH('', ['(A) %s' % figs['A'], '(B) %s' % figs['B'], '(C) %s' % figs['C'], '(D) %s' % figs['D']], 0)], 4, 'function-analysis',
             r"$f' < 0$: $f$ decreases; $f' > 0$: $f$ increases; $f' = 0$ without sign change: horizontal tangent but no extremum. $f$ must be continuous.",
             [r"$f' < 0$ on $(0,1)$, $> 0$ on $(1,3)\cup(3,5)$ (touching $0$ at $3$), $< 0$ on $(5,6)$: minimum at $1$, flat point at $3$, maximum at $5$.",
              r'Only graph (A) has this shape and is continuous (graph (C) has jumps, so it cannot be a differentiable function). **(A)**',
              r'Note: the official answer key printed (C). Graph (C) is discontinuous, however, while $f$ must be differentiable, so this site marks (A) as correct.']),
        item('(g)', r'A continuous random variable $X$ has the probability density function: $$f(x)=\begin{cases}\frac83(1-8x^3) & \text{if } 0\le x\le\frac12,\\ 0 & \text{otherwise.}\end{cases}$$ Then the expected value of $X$ is',
             [CH('', [r'$\frac12$', r'$\frac13$', r'$\frac14$', r'$\frac15$', r'$\frac18$'], 3)], 4, 'continuous', r'$E(X) = \int_0^{1/2}x\cdot\frac83(1 - 8x^3)\,dx$.', [r'$\frac83\big[\frac{x^2}2 - \frac{8x^5}5\big]_0^{1/2} = \frac83\big(\frac18 - \frac1{20}\big) = \frac15$. **(D)**']),
        item('(h)', r'The slant asymptote of $f(x)=\dfrac{2(x-2)(x+2)}{x-3}$ is given by', [CH('', ['$2x$', '$2(x+1)$', '$2(x+2)$', '$2(x+3)$', '$2(x+4)$', '$2(x+5)$'], 3)], 4, 'asymptotes', r'Expand and divide by $x - 3$.', [r'$\frac{2x^2-8}{x-3} = 2x + 6 + \frac{10}{x-3}$. **(D)**']),
    ]))
    qs.append(question('3', 12, '', [item('', r'Compute the area $A$ of the region bounded by • the function $f(x)=-8x^3+16x^2-6x=-2x(4x^2-8x+3)$, • the tangent line $l(x)$ to $f$ at $x=p$, $p>0$ that goes through $(0,0)$ (see figure below) %s' % img('2024-06-q3-area.png', 'Cubic f with tangent line l through the origin touching at x = p; shaded region A'),
        [N('$A =$', R(2, 3))], 12, 'area', r'The tangent through the origin is $l(x) = f^{\prime}(p)x$; solve $l(p) = f(p)$ for $p > 0$, then integrate $l - f$ over $[0, p]$.',
        [r"$f'(x) = -24x^2 + 32x - 6$, $l(x) = f'(p)x$.", r'$(-24p^2+32p-6)p = -8p^3 + 16p^2 - 6p \Rightarrow p = 1$; $l(x) = 2x$.',
         r'$A = \int_0^1 2x - (-8x^3+16x^2-6x)\,dx = \int_0^1 8x^3-16x^2+8x\,dx = 2 - \frac{16}3 + 4 = \frac23$.'])]))
    qs.append(question('4', 6, '', [item('', r'Compute the following series $$\frac{e^{\frac1n}}{n^2}+\frac{2e^{\frac2n}}{n^2}+\frac{3e^{\frac3n}}{n^2}+\ldots+\frac{e}{n}$$ when $n$ goes to infinity.',
        [N('Limit:', 1)], 6, 'riemann', r'The $r$-th term is $\frac{r e^{r/n}}{n^2} = \frac1n\cdot\frac rn e^{r/n}$.', [r'$\lim\frac1n\sum\frac rn e^{r/n} = \int_0^1xe^xdx$.', r'By parts: $xe^x\big|_0^1 - \int_0^1e^xdx = e - (e - 1) = 1$.'])]))
    qs.append(question('5', 6, '', [item('', r'Give all **critical points** for the function $$f(x)=\frac{\sqrt x}{1+7x}$$ on the domain $D_f=[0,\infty)$, i.e., all points where $f^{\prime}(x)=0$ *and* where the derivative does not exist (which includes limit values going to $\infty$ or $-\infty$).',
        [ST('Critical points:', [0, R(1, 7)])], 6, 'function-analysis', r'Quotient rule; bring everything on one fraction. Check both $f^{\prime} = 0$ and where $f^{\prime}$ does not exist.',
        [r"$f'(x) = \dfrac{\frac{1}{2\sqrt x}(1+7x) - 7\sqrt x}{(1+7x)^2} = \dfrac{1 - 7x}{2\sqrt x(1+7x)^2}$.", r"$f' = 0$ at $x = \frac17$; $f'$ does not exist at $x = 0$. Critical points $\{0, \frac17\}$."])]))
    qs.append(question('6', 6, '', [item('', r'Use $u$-substition with $u=\sqrt{x^2+2}$ to show that $$\int_{\sqrt2}^2x^3\ln\left(1+\sqrt{x^2+2}\right)dx=\int_a^bp(u)\ln(q(u))\,du$$ with $p(u)$ and $q(u)$ polynomials in $u$ and some $a,b\in\mathbb{R}$. (You do not need to evaluate the integral further.)',
        [EX('$p(u) =$', u ** 3 - 2 * u, vars=('u',)), EX('$q(u) =$', 1 + u, vars=('u',)), N('$a =$', 2), N('$b =$', sqrt(6))], 6, 'substitution',
        r'$u^2 = x^2 + 2 \Rightarrow u\,du = x\,dx$ and $x^2 = u^2 - 2$. Write $x^3dx = x^2\cdot x\,dx$.',
        [r'$u\,du = x\,dx$, $x^2 = u^2 - 2$.', r'$\int x^2\ln(1+\sqrt{x^2+2})\,x\,dx = \int(u^2-2)\ln(1+u)\,u\,du = \int(u^3-2u)\ln(1+u)\,du$.', r'Bounds: $u(\sqrt2) = 2$, $u(2) = \sqrt6$.'])]))
    qs.append(question('7', 6, '', [item('', r'Compute the following limit $$L=\lim_{x\to\pi}\left(\frac{x}{\pi}\right)^{\frac{1}{\sin(x)}}.$$ What is the value of $L$?',
        [CH('', ['$1$', '$e$', '$e^{-1}$', r'$e^{\pi}$', r'$e^{-\pi}$', r'$e^{\frac1\pi}$', r'$e^{-\frac1\pi}$', r'does not exist (i.e, goes to $\infty$)'], 6)], 6, 'lhopital',
        r'Form $1^\infty$: $\ln L = \lim\frac{\ln(x/\pi)}{\sin x}$, form $\tfrac00$.', [r"$\ln L = \lim_{x\to\pi}\frac{\ln(x/\pi)}{\sin x}\overset{LH}{=}\lim\frac{1/x}{\cos x} = \frac{1/\pi}{-1} = -\frac1\pi$.", r'$L = e^{-1/\pi}$. **(G)**'])]))
    qs.append(question('8', 6, '', [item('', r'On a typical day, ten percent of the vehicles passing through the tunnel under the Nijmegen train station have a German license plate. Let’s assume we observe 20 vehicles coming out of the tunnel on such a day. What is the probability (without any additional information) that **at least two** out of these 20 vehicles will have German license plates? *Hint: Observing a vehicle having a German license plate is an independent “success” after 20 “trials”.*',
        [N(r'$P =$', 1 - R(9, 10) ** 20 - 20 * R(1, 10) * R(9, 10) ** 19, tol={'abs': 5e-4})], 6, 'discrete',
        r'Binomial with $n = 20$, $p = 0.1$; use the complement $1 - b(0) - b(1)$.',
        [r'$b(k) = \binom{20}{k}0.1^k0.9^{20-k}$.', r'$P = 1 - 0.9^{20} - 20\cdot0.1\cdot0.9^{19}\approx 0.608$ (about $60.8\%$).'])]))
    qs.append(question('9', 6, '', [item('', r'Consider the reciprocal distribution on the interval $[2,4]$ given by the probability density function (pdf): $$p(x)=\frac{1}{cx},\quad 2\le x\le4.$$ What is the value of constant $c$ such that the pdf is properly normalized? After finding $c$, derive the corresponding cumulative distribution function (cdf) for $x\in[2,4]$.',
        [N('$c =$', log(2)), EX('$F(x) =$', log(x) / log(2) - 1, sample={'x': [2, 4]})], 6, 'continuous', r'$\int_2^4\frac{1}{cx}dx = \frac{\ln4 - \ln2}{c}$. The cdf is $F(x) = \int_2^x p(t)\,dt$.',
        [r'$\frac{\ln4-\ln2}{c} = \frac{\ln2}{c} = 1 \Rightarrow c = \ln2$.', r'$F(x) = \int_2^x\frac{dt}{t\ln2} = \frac{\ln x - \ln 2}{\ln2} = \log_2x - 1$.'])]))
    return exam('2023-1', year='2023–2024', sitting=1, kind='Exam', date='June 17, 2024', iso='2024-06-17', minutes=120,
                file='calc-exam-2023-01', instructions=STD_120, questions=qs,
                note='Question 2(f): the official key says (C); this site marks (A) — see the worked solution.')


# =====================================================================================
def exam_2023_2():
    qs = []
    AB = {'a': [0.5, 3], 'b': [0.5, 3]}
    qs.append(question('1', 6, r'Let $a,b\in\mathbb{R}$. Compute the following limits', [
        item('(a)', r'$$\lim_{x\to\infty}\sqrt{x^2-ax}-\sqrt{x^2-bx}$$', [EX('Limit:', (b - a) / 2, vars=('a', 'b'), sample=AB)], 3, 'limits', r'Multiply by the conjugate $\frac{\sqrt{x^2-ax}+\sqrt{x^2-bx}}{\sqrt{x^2-ax}+\sqrt{x^2-bx}}$.',
             [r'$= \lim\dfrac{(b-a)x}{\sqrt{x^2-ax}+\sqrt{x^2-bx}} = \lim\dfrac{b-a}{\sqrt{1-\frac ax}+\sqrt{1-\frac bx}} = \frac12(b-a)$.']),
        item('(b)', r'$$\lim_{x\to\infty}\frac{x}{ax+b\sin(x)}$$', [EX('Limit:', 1 / a, vars=('a', 'b'), sample=AB)], 3, 'limits', r'Squeeze: $ax - b\le ax + b\sin x\le ax + b$ (for $b > 0$).',
             [r'The expression lies between $\frac{x}{ax-b}$ and $\frac{x}{ax+b}$, which both tend to $\frac1a$. The limit is $\frac1a$.']),
    ]))
    SET8 = ['$a$', '$a+b$', '$a^2$', '$a^2+b$', '$b$', '$b^2$', '$a+b^2$', '$a^2+b^2$']
    qs.append(question('2', 8, '', [item('', r'Compute the following integral using partial integration $$\int\sin(ax)e^{bx}\,dx=\frac{A}{B}\cdot\sin(ax)e^{bx}-\frac{C}{D}\cdot\cos(ax)e^{bx}\ (+constant)$$ where $a,b$ are some unspecified values and $$A,B,C,D\in\{a,a+b,a^2,a^2+b,b,b^2,a+b^2,a^2+b^2\}$$',
        [CH('$A =$', SET8, 4), CH('$B =$', SET8, 7), CH('$C =$', SET8, 0), CH('$D =$', SET8, 7)], 8, 'by-parts',
        r'Integrate by parts twice; the original integral reappears with factor $-\frac{b^2}{a^2}$. Move it to the left and solve.',
        [r'$\int\sin(ax)e^{bx}dx = -\frac1a\cos(ax)e^{bx} + \frac b{a^2}\sin(ax)e^{bx} - \frac{b^2}{a^2}\int\sin(ax)e^{bx}dx$.',
         r'$\left(\frac{b^2}{a^2}+1\right)\int\sin(ax)e^{bx}dx = \frac{b}{a^2}\sin(ax)e^{bx} - \frac1a\cos(ax)e^{bx}$.',
         r'$\int\sin(ax)e^{bx}dx = \frac{b}{a^2+b^2}\sin(ax)e^{bx} - \frac{a}{a^2+b^2}\cos(ax)e^{bx}$: $A = b$, $B = a^2+b^2$, $C = a$, $D = a^2+b^2$.'])]))
    qs.append(question('3', 28, SEL, [
        item('(a)', r'%s The graph of the even function $y=f(x)$ consists of 4 line segments $$f(x)=\begin{cases}x+6 & \text{if } x<-3\\ -x & \text{if } -3\le x<0\\ x & \text{if } 0\le x<3\\ -x+6 & \text{if } x>3\end{cases},$$ as shown above. Which of the statements about $f$ is false?' % img('2024-07-q3a-graph.png', 'Graph of f: zigzag with peaks at (-3,3) and (3,3)'),
             [CH('', [r'$\lim_{x\to0}(f(x)-f(0))=0$', r'$\lim_{x\to0}\frac{f(x)-f(0)}{x}=0$', r'$\lim_{x\to0}\frac{f(x)-f(-x)}{2x}=0$', r'$\lim_{x\to2}\frac{f(x)-f(2)}{x-2}=1$', r'$\lim_{x\to3}\frac{f(x)-f(3)}{x-3}$ does not exist.'], 1)], 4, 'continuity',
             r'Near $0$, $f(x) = |x|$. Which one-sided difference quotients differ?', [r'$\frac{f(x)-f(0)}{x} = \frac{|x|}{x}$ is $-1$ on the left and $1$ on the right: the limit does not exist, so (B) is false. The others hold. **(B)**']),
        item('(b)', r'An $n$-sided dice has $n$ sides with pips $\{1,2,\dots,n\}$. What is the expectation of a 20-sided dice?', [CH('', ['$9.5$', '$10$', '$10.5$', '$11$', '$20$'], 2)], 4, 'discrete', r'$E = \frac{n+1}{2}$.', [r'$\frac{21}{2} = 10.5$. **(C)**']),
        item('(c)', r'Let $f(x,y)$ be $e^{xy}\sin(x+y)$. What is the formula for $\frac{\partial}{\partial x}\frac{\partial}{\partial y}f(x,y)$?',
             [CH('', [r'$xye^{xy}\cos(x+y)$', r'$(x+y)e^{xy}\sin(x+y)$', r'$(x+y)e^{xy}\sin(x+y)+e^{xy}(\sin(x+y)+\cos(x+y))$', r'$xye^{xy}\sin(x+y)+(x+y)e^{xy}\cos(x+y)$', r'$xye^{xy}\sin(x+y)+ye^{xy}\cos(x+y)-e^{xy}\sin(x+y)$'], 3)], 4, 'partial-derivatives',
             r'$\frac{\partial}{\partial y}$ first (product rule), then $\frac{\partial}{\partial x}$ of each term.', [r'$f_y = xe^{xy}\sin(x+y) + e^{xy}\cos(x+y)$.', r'$f_{yx} = e^{xy}\sin + xye^{xy}\sin + xe^{xy}\cos + ye^{xy}\cos - e^{xy}\sin = xye^{xy}\sin(x+y) + (x+y)e^{xy}\cos(x+y)$. **(D)**']),
        item('(d)', r'Let $$f(x)=\begin{cases}x^2+2 & \text{if } x<-2\\ mx+b & \text{if } -2\le x\le2\\ x^2-2 & \text{if } x>2\end{cases}$$ For what values $m,b$ is $f(x)$ continuous?',
             [CH('', [r'$m=-2,b=2$', r'$m=1,b=8$', r'$m=-\frac12,b=5$', r'$m=2,b=10$', r'$m=-1,b=4$'], 4)], 4, 'continuity', r'Match the values at $x = -2$ and $x = 2$.', [r'$-2m + b = 6$ and $2m + b = 2$ give $m = -1$, $b = 4$. **(E)**']),
        item('(e)', r'Let $f(x)=\frac12x+\frac14$ on $[1,2]$ (and $0$ elsewhere) be a probability density function. Then the cumulative distribution function is $$F(x)=\begin{cases}0 & \text{if } x<1\\ \frac14x^2+\frac14x+c & \text{if } 1\le x\le2\\ 1 & \text{if } x>2\end{cases}$$ where $c$ is',
             [CH('', [r'$-\frac12$', r'$-\frac14$', '$0$', r'$\frac14$', r'$\frac12$'], 0)], 4, 'continuous', r'$F$ is continuous: $F(1) = 0$.', [r'$\frac14 + \frac14 + c = 0 \Rightarrow c = -\frac12$. **(A)**']),
        item('(f)', r'Let $f(x)=\dfrac{x^2-x}{x^2-4}$. We are interested in the total number of horizontal, vertical, and slant asymptotes of $f$. (Note that if the asymptote at $+\infty$ is the same as the asymptote at $-\infty$ this is counted as 1 asymptote.) The function $f$ has',
             [CH('', ['1 asymptote', '2 asymptotes', '3 asymptotes', '4 asymptotes', '5 asymptotes'], 2)], 4, 'asymptotes', r'Factor: does anything cancel? Equal degrees.', [r'Vertical $x = \pm2$ (no cancellation), horizontal $y = 1$: 3 asymptotes. **(C)**']),
        item('(g)', r'The derivative of $f(x)=(\sin(x))^x$ is',
             [CH('', [r'$(\sin(x))^x\left(\sin(x)+\frac{x\sin(x)}{\cos(x)}\right)$', r'$(\sin(x))^x\left(\sin(x)+\frac{x\cos(x)}{\sin(x)}\right)$', r'$(\sin(x))^x\left(\ln(\sin(x))+\frac{x\sin(x)}{\cos(x)}\right)$', r'$(\sin(x))^x\left(\ln(\sin(x))+\frac{x\cos(x)}{\sin(x)}\right)$', 'None of the above'], 3)], 4, 'derivative-rules',
             r'Logarithmic differentiation: $\ln f = x\ln(\sin x)$.', [r"$[\ln f]' = \ln(\sin x) + x\frac{\cos x}{\sin x}$, so $f' = (\sin x)^x\left(\ln(\sin x) + \frac{x\cos x}{\sin x}\right)$. **(D)**"]),
    ]))
    qs.append(question('4', 6, '', [item('', r'Let $f(x)=\dfrac{x+5}{2x-1}$. Determine the (maximum real) domain of $f$, the range of $f$, and the inverse of $f$.',
        [IV('Domain:', S.Reals - FiniteSet(R(1, 2))), IV('Range:', S.Reals - FiniteSet(R(1, 2))), EX('$f^{-1}(x) =$', (x + 5) / (2 * x - 1), sample={'x': [1, 4]})], 6, 'inverse',
        r'Domain: denominator $\neq 0$. Range: the horizontal asymptote value is never attained. Inverse: solve $y = f(x)$ for $x$.',
        [r'$D(f) = \mathbb{R}\setminus\{\frac12\}$.', r'$f\to\frac12$ for $x\to\pm\infty$ and $f\to\pm\infty$ near $\frac12$: $R(f) = \mathbb{R}\setminus\{\frac12\}$.',
         r'$(2x-1)y = x + 5 \Rightarrow x(2y-1) = y + 5 \Rightarrow x = \frac{y+5}{2y-1}$, so $f^{-1}(x) = \frac{x+5}{2x-1}$.'])]))
    qs.append(question('5', 12, '', [item('', r'The parabolas with equations $f(x)=4-x^2$ and $g(x)=\frac7{16}(4-x^2)$ are shown in the figure below. %s An isosceles trapezoid $ABCD$ is placed between $f=4-x^2$ and $g=\frac7{16}(4-x^2)$ as shown above such that • $A$ and $D$ have the same $y$-value and lie on the upper parabola $f$. • $C$ and $B$ have the same $y$-value and lie on the upper parabola $f$. • $T$, the turning point of the lower parabola, lies on $BC$. (An isosceles trapezoid is a trapezoid where the base angles have the same measure. As a consequence the two legs are also of equal length and it has reflection symmetry. Remember that the area of the trapezoid can be computed as $\frac{(AD+BC)y}{2}$, where $y$ is the height of the trapezoid.) Let $A=(x,f(x))$ for some $x>0$. Find $x>0$ that gives the maximum area for the trapezoid $ABCD$ and compute this value.' % img('2024-07-q5-trapezoid.png', 'Trapezoid ABCD between the two parabolas'),
        [N('$x =$', R(1, 2)), N('Maximum area:', 4)], 12, 'function-analysis', r'$T = (0, g(0)) = (0, \frac74)$ fixes $BC$. Write the height and the area as functions of $x$ only, then maximise.',
        [r'$T = (0,\frac74)$; $4 - x^2 = \frac74$ gives $B = (\frac32, \frac74)$, so $BC = 3$.', r'Height $y = (4 - x^2) - \frac74 = \frac94 - x^2$; $A(x) = \frac{(2x+3)(\frac94 - x^2)}{2} = -x^3 - \frac32x^2 + \frac94x + \frac{27}8$.',
         r"$A'(x) = -3x^2 - 3x + \frac94 = 0 \Rightarrow x = \frac12$ ($x > 0$).", r'$A(\frac12) = 4$.'])]))
    qs.append(question('6', 6, '', [item('', r'Find an equation of the tangent line to the curve $x^2+y^2=(2x^2+2y^2-x)^2$ at the point $(0,\frac12)$.',
        [EX('$y =$', x + R(1, 2))], 6, 'implicit-tangent', r"Differentiate both sides (chain rule on the right), substitute $(0,\frac12)$ before solving for $y'$.",
        [r"$2x + 2yy' = 2(2x^2+2y^2-x)(4x + 4yy' - 1)$.", r"At $(0,\frac12)$: $y' = 2\cdot\frac12(2y' - 1) \Rightarrow y' = 1$.", r'$y - \frac12 = 1\cdot(x - 0)$, i.e. $y = x + \frac12$.'])]))
    qs.append(question('7', 6, '', [item('', r'Compute the following limit $$\lim_{n\to\infty}\sum_{r=1}^n\frac{3r^2+2rn+n^2}{(r+n)(r^2+n^2)}=\ln(A)$$',
        [N('$A =$', 4)], 6, 'riemann', r'Divide by $n^3$: $\frac1n\cdot\frac{3x^2+2x+1}{(x+1)(x^2+1)}$ with $x = \frac rn$; then partial fractions.',
        [r'$= \int_0^1\frac{3x^2+2x+1}{(x+1)(x^2+1)}dx = \int_0^1\frac1{x+1} + \frac{2x}{x^2+1}dx$.', r'$= \big[\ln|x+1| + \ln(x^2+1)\big]_0^1 = 2\ln 2 = \ln4$, so $A = 4$.'])]))
    qs.append(question('8', 6, '', [item('', r'Let $f(x)=(x^2+2x-1)e^{-x}$. Determine the inflection points of $f$ and determine where $f$ is convex (concave up) and concave (concave down).',
        [ST('Inflection points ($x$-values):', [-1, 3], pts=2), IV('$f$ is convex on:', Union(Interval.open(-oo, -1), Interval.open(3, oo)), loose=True, pts=2), IV('$f$ is concave on:', Interval.open(-1, 3), loose=True, pts=2)], 6, 'concavity',
        r"Product rule twice; $e^{-x} > 0$, so the sign of $f''$ is the sign of the polynomial factor.",
        [r"$f'(x) = (-x^2+3)e^{-x}$; $f''(x) = (x^2-2x-3)e^{-x} = (x-3)(x+1)e^{-x}$.", r"$f'' = 0$ at $x\in\{-1, 3\}$ with sign changes.", r'Convex on $(-\infty,-1)\cup(3,\infty)$, concave on $(-1,3)$.'])]))
    qs.append(question('9', 6, '', [item('', r'Let $n,m>0$. Determine the slant asymptote when $x$ goes to $\infty$ of the function $$f(x)=\frac{\sqrt{x}+x^2}{nx+m}$$',
        [EX('$y =$', x / n - m / n ** 2, vars=('x', 'n', 'm'), sample={'x': [-2, 2], 'n': [0.5, 3], 'm': [0.5, 3]})], 6, 'asymptotes',
        r'Not a rational function: use $a = \lim\frac{f(x)}{x}$ and $b = \lim(f(x) - ax)$.',
        [r'$a = \lim\frac{\sqrt x + x^2}{nx^2 + mx} = \frac1n$.', r'$b = \lim\left(\frac{\sqrt x+x^2}{nx+m} - \frac xn\right) = \lim\frac{n\sqrt x - mx}{n^2x + nm} = -\frac{m}{n^2}$.', r'$y = \frac1nx - \frac{m}{n^2}$.'])]))
    qs.append(question('10', 6, '', [item('', r'Suppose that there are two different boxes of fruit. In Box 1 there are 10 apples and 90 oranges. In Box 2 there are 80 apples and 120 oranges. Take one of the two boxes at random (with equal probability), and pick a fruit at random from the chosen box. Suppose that you drew an apple, then what is the probability that you chose from Box 1?',
        [NP(r'$P(\text{Box 1}\mid\text{apple}) =$', R(1, 5))], 6, 'conditional', r'Total probability for $P(\text{apple})$, then Bayes.',
        [r'$P(\text{apple}\mid B_1) = \frac1{10}$, $P(\text{apple}\mid B_2) = \frac25$.', r'$P(\text{apple}) = \frac1{10}\cdot\frac12 + \frac25\cdot\frac12 = \frac14$.', r'$P(B_1\mid\text{apple}) = \frac{\frac1{10}\cdot\frac12}{\frac14} = \frac15$.'])]))
    return exam('2023-2', year='2023–2024', sitting=2, kind='Resit', date='July 8, 2024', iso='2024-07-08', minutes=120,
                file='calc-exam-2023-02', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2024_1():
    qs = []
    qs.append(question('1', 9, r'Let $2x^2-4x-xy+y^2+1=0$ be the implicit equation of an ellipse. Consider the lines tangent to the ellipse at $x=\frac12$.', [
        item('(a)', r'Find the points on the ellipse that the tangent lines go through.', [ST(r'$y$-coordinates of the points (both have $x = \frac12$):', [1, R(-1, 2)])], 3, 'implicit-tangent',
             r'Substitute $x = \frac12$ and solve the quadratic in $y$.', [r'$\frac12 - 2 - \frac12y + y^2 + 1 = 0 \iff y^2 - \frac12y - \frac12 = 0 \iff (y-1)(y+\frac12) = 0$.', r'Points $(\frac12, 1)$ and $(\frac12, -\frac12)$.']),
        item('(b)', r'Determine the equations of the tangent lines at $x=\frac12$.', [EX(r'Tangent at $(\frac12, 1)$: $y =$', 2 * x, pts=3), EX(r'Tangent at $(\frac12, -\frac12)$: $y =$', -x, pts=3)], 6, 'implicit-tangent',
             r"Differentiate implicitly: $4x - 4 - y - xy' + 2yy' = 0$, so $y' = \frac{y + 4 - 4x}{2y - x}$.",
             [r"$y' = \dfrac{y+4-4x}{2y-x}$: $2$ at $(\frac12,1)$ and $-1$ at $(\frac12,-\frac12)$.", r'Point-slope form: both lines pass through the origin: $y = 2x$ and $y = -x$.']),
    ]))
    qs.append(question('2', 6, '', [item('', r'Consider the region bounded by the parabolas $f(x)=-x^2+5$ and $g(x)=(x-1)^2$. Determine the area of this region using integration.',
        [N('Area:', 9)], 6, 'area', r'Intersections from $-x^2 + 5 = (x-1)^2$; on that interval $f$ lies above $g$.',
        [r'$2x^2 - 2x - 4 = 0 \iff x\in\{-1, 2\}$.', r'$\int_{-1}^2 (f - g)\,dx = 2\int_{-1}^2(2 + x - x^2)dx = 2\left[2x + \frac{x^2}2 - \frac{x^3}3\right]_{-1}^2 = 2\cdot\frac92 = 9$.'])]))
    qs.append(question('3', 6, '', [item('', r'Determine the following limit $$\lim_{n\to\infty}\sum_{r=10n}^{37n}\frac{r}{\sqrt{n^3(r-n)}}$$',
        [N('Limit:', 132)], 6, 'riemann', r'Write the term as $\frac1n\cdot\frac{r/n}{\sqrt{r/n - 1}}$; $x = r/n$ runs from $10$ to $37$. Then substitute $u = \sqrt{x-1}$.',
        [r'$= \int_{10}^{37}\frac{x}{\sqrt{x-1}}dx$.', r'$u = \sqrt{x-1}$, $x = u^2 + 1$, $dx = 2u\,du$: $\int_3^6\frac{u^2+1}{u}2u\,du = \int_3^6 2u^2 + 2\,du$.', r'$= \left[\frac23u^3 + 2u\right]_3^6 = 156 - 24 = 132$.'])]))
    qs.append(question('4', 6, '', [item('', r'Let $f(x)=(-x^2+3x-2)e^x$. Determine the inflection points of $f$ and determine where $f$ is convex (concave up) and concave (concave down).',
        [ST('Inflection points ($x$-values):', [-2, 1], pts=2), IV('$f$ is convex on:', Interval.open(-2, 1), loose=True, pts=2), IV('$f$ is concave on:', Union(Interval.open(-oo, -2), Interval.open(1, oo)), loose=True, pts=2)], 6, 'concavity',
        r"Product rule twice; the sign of $f''$ is the sign of its polynomial factor.",
        [r"$f'(x) = (-x^2+x+1)e^x$, $f''(x) = (-x^2-x+2)e^x = -(x+2)(x-1)e^x$.", r'Inflection points $x\in\{-2,1\}$; concave on $(-\infty,-2)\cup(1,\infty)$, convex on $(-2,1)$.'])]))
    qs.append(question('5', 6, '', [item('', r'If $$\lim_{x\to0}\frac{A}{\ln(Bx+C)}-\frac1x=5$$ then what are the values of $A$, $B$, and $C$?',
        [N('$A =$', 10), N('$B =$', 10), N('$C =$', 1)], 6, 'lhopital', r'Combine to one fraction $\frac{Ax - \ln(Bx+C)}{x\ln(Bx+C)}$. For a finite limit the forms must be $\tfrac00$ — this forces $C$ and then $A = B$.',
        [r'$\frac{Ax - \ln(Bx+C)}{x\ln(Bx+C)}$: at $0$ the numerator is $-\ln C$, so $C = 1$.', r"L'Hôpital: $\dfrac{A(Bx+1) - B}{(Bx+1)\ln(Bx+1) + Bx}$; numerator at $0$: $A - B = 0$.",
         r"L'Hôpital again (with $B = A$): $\dfrac{A^2}{A\ln(Ax+1) + 2A}\to\frac A2 = 5$, so $A = B = 10$, $C = 1$."])]))
    terms = [r'$\frac{A}{x+1}$', r'$\frac{B}{x-1}$', r'$\frac{C}{(x+1)^2}$', r'$\frac{D}{(x-1)^2}$', r'$\frac{Ex+F}{x^2+1}$', r'$\frac{Gx+H}{x^2-1}$', r'$\frac{Ix+J}{(x^2+1)^2}$', r'$\frac{Kx+L}{(x^2-1)^2}$']
    qs.append(question('6', 6, '', [item('', r'Divide the fraction $$\frac{1}{x^4+2x^3+2x^2+2x+1}$$ into partial fractions by selecting terms from $$\left\{\frac{A}{x+1},\frac{B}{x-1},\frac{C}{(x+1)^2},\frac{D}{(x-1)^2},\frac{Ex+F}{x^2+1},\frac{Gx+H}{x^2-1},\frac{Ix+J}{(x^2+1)^2},\frac{Kx+L}{(x^2-1)^2}\right\}$$ You don’t need to determine the values for $A,\dots,L$. Omit terms that are clearly $0$.',
        [MULTI('Select all terms that are needed:', terms, [0, 2, 4])], 6, 'partial-fractions', r'Factor the denominator: try $x = -1$ (twice).',
        [r'$x^4+2x^3+2x^2+2x+1 = (x+1)^2(x^2+1)$.', r'So $\frac{A}{x+1} + \frac{C}{(x+1)^2} + \frac{Ex+F}{x^2+1}$.'])]))
    qs.append(question('7', 6, '', [item('', r'Let $f(x)=\dfrac{x^2-3x+2}{x^2-4}$. Determine the domain, range, and number of asymptotes of $f$. (Note that if the asymptote at $+\infty$ is the same as the asymptote at $-\infty$ this is counted as 1 asymptote.)',
        [IV('Domain:', S.Reals - FiniteSet(-2, 2)), IV('Range:', S.Reals - FiniteSet(R(1, 4), 1)), N('Number of asymptotes:', 2)], 6, 'domain-range',
        r'Factor: $\frac{(x-2)(x-1)}{(x-2)(x+2)}$. A cancelled factor gives a hole — and a value missing from the range.',
        [r'$D_f = \mathbb{R}\setminus\{-2, 2\}$.', r'$f$ behaves like $g(x) = \frac{x-1}{x+2}$ with a hole at $x = 2$: vertical asymptote $x = -2$, horizontal $y = 1$ — 2 asymptotes.',
         r'$g$ never equals $1$, and the hole removes $g(2) = \frac14$: $R_f = \mathbb{R}\setminus\{\frac14, 1\}$.'])]))
    qs.append(question('8', 9, r'Let $p(x)=\frac{a}{\pi}x\sin(x)$ for $x\in[-\pi,\pi]$ and $0$ elsewhere be a probability density function.', [
        item('(a)', r'Determine the value for $a$.', [N('$a =$', R(1, 2))], 6, 'continuous', r'By parts: $\int x\sin x\,dx = \sin x - x\cos x$.', [r'$1 = \frac a\pi\big[\sin x - x\cos x\big]_{-\pi}^\pi = \frac a\pi(\pi + \pi) = 2a$, so $a = \frac12$.']),
        item('(b)', r'Find the constant $C$ of the cumulative distribution function $F(x)=\int_{-\infty}^xp(t)\,dt$ on the interval $[-\pi,\pi]$.', [N('$C =$', R(1, 2))], 3, 'continuous',
             r'On $[-\pi,\pi]$: $F(x) = \frac{1}{2\pi}(\sin x - x\cos x) + C$; use $F(-\pi) = 0$.', [r'$0 = \frac{1}{2\pi}(0 - \pi) + C = -\frac12 + C \Rightarrow C = \frac12$.']),
    ]))
    qs.append(question('9', 36, SEL, [
        item('(a)', r'Let $f(x)=\sqrt{4x^2-9}+x$ with domain $D_f$. What function can be used on $\mathbb{R}\setminus D_f$ to extend $f$ to a continuous function on $\mathbb{R}$?',
             [CH('', [r'$\frac12x$', r'$\frac23x$', '$x$', r'$\frac32x$', '$2x$'], 2)], 4, 'continuity', r'At the edges $x = \pm\frac32$ the root is $0$.', [r'$\mathbb{R}\setminus D_f = (-\frac32,\frac32)$; at $\pm\frac32$, $f(x) = x$, so extending with $x$ is continuous. **(C)**']),
        item('(b)', r'The slant asymptote of $f(x)=\dfrac{2(x-3)(x+3)}{x-2}$ is', [CH('', ['$2x$', '$2x+2$', '$2x+4$', '$2x+6$', '$2x+8$'], 2)], 4, 'asymptotes', r'Long division of $2x^2 - 18$ by $x - 2$.', [r'$f(x) = 2x + 4 - \frac{10}{x-2}$. **(C)**']),
        item('(c)', r'Let $f(x)=\dfrac{x-1}{x+1}$, then its inverse is', [CH('', [r'$\frac{1-x}{x-1}$', r'$\frac{1-x}{-x-1}$', r'$\frac{-1-x}{-x-1}$', r'$\frac{-(x-1)}{x-1}$', r'$\frac{-x-1}{x-1}$'], 4)], 4, 'inverse',
             r'Solve $y = \frac{x-1}{x+1}$ for $x$.', [r'$y(x+1) = x - 1 \Rightarrow x(y-1) = -y - 1 \Rightarrow x = \frac{-y-1}{y-1}$. **(E)**']),
        item('(d)', r'A continuous random variable $X$ has the probability distribution $$g(x)=\begin{cases}3(1-4x^2) & \text{if } 0\le x\le\frac12\\ 0 & \text{otherwise}\end{cases}$$ Then the expected value of $X$ is',
             [CH('', [r'$\frac{2}{16}$', r'$\frac{3}{16}$', r'$\frac{5}{16}$', r'$\frac{7}{16}$', r'$\frac{11}{16}$'], 1)], 4, 'continuous', r'$E(X) = \int_0^{1/2}3x(1 - 4x^2)dx$.', [r'$3\big[\frac{x^2}2 - x^4\big]_0^{1/2} = 3(\frac18 - \frac1{16}) = \frac3{16}$. **(B)**']),
        item('(e)', r'Let $f(x)=\dfrac{\sin(x)}{x}$ and $g(x)=\dfrac{\cos x}{1+x^2}$. Then', [CH('', [r'$f$ is odd, and $g$ is odd', r'$f$ is odd, and $g$ is even', r'$f$ is even, and $g$ is odd', r'$f$ is even, and $g$ is even', 'one of them is neither odd nor even'], 3)], 4, 'even-odd',
             r'odd/odd = even; even/even = even.', [r'$f$: odd over odd = even. $g$: even over even = even. **(D)**']),
        item('(f)', r'Let $f(x,y)=e^{3x+y}\ln(xy^2)$. The second partial derivative $\frac{\partial^2f}{\partial x\partial y}$ is',
             [CH('', [r'$e^{3x+y}\left(2\ln(xy^2)+\frac1x+\frac6y\right)$', r'$e^{3x+y}\left(2\ln(xy^2)+\frac2x+\frac3y\right)$', r'$e^{3x+y}\left(2\ln(xy^2)+\frac3x+\frac2y\right)$', r'$e^{3x+y}\left(3\ln(xy^2)+\frac1x+\frac6y\right)$', r'$e^{3x+y}\left(3\ln(xy^2)+\frac2x+\frac3y\right)$', r'$e^{3x+y}\left(3\ln(xy^2)+\frac3x+\frac2y\right)$'], 3)], 4, 'partial-derivatives',
             r'$\frac{\partial}{\partial y}\ln(xy^2) = \frac2y$ and $\frac{\partial}{\partial x}\ln(xy^2) = \frac1x$.', [r'$f_y = e^{3x+y}(\ln(xy^2) + \frac2y)$.', r'$f_{yx} = 3e^{3x+y}(\ln(xy^2) + \frac2y) + e^{3x+y}\frac1x = e^{3x+y}(3\ln(xy^2) + \frac1x + \frac6y)$. **(D)**']),
        item('(g)', r'A company that sells red-colored breakfast cereal organizes a promotional event during which a quarter of all of the boxes sold contain green-colored cereal instead (the other three quarters contain the regular red-colored cereal). A hungry client randomly picks up three boxes of cereal during the promotional period. What is the probability that the cereal in all three boxes has the same color?',
             [CH('', [r'$\frac{1}{64}$', r'$\frac{9}{64}$', r'$\frac{27}{64}$', r'$\frac{28}{64}$', r'$\frac{36}{64}$'], 3)], 4, 'discrete', r'All red or all green.', [r'$(\frac34)^3 + (\frac14)^3 = \frac{27}{64} + \frac1{64} = \frac{28}{64}$. **(D)**']),
        item('(h)', r'By computing the improper integral $\int_0^\infty\frac{3x^2}{(x^3+1)^2}dx$, we get the value', [CH('', ['$0$', r'$\frac13$', '$1$', '$3$', r'$\infty$'], 2)], 4, 'substitution', r'$u = x^3 + 1$.', [r'$\int_1^\infty\frac{du}{u^2} = \big[-\frac1u\big]_1^\infty = 1$. **(C)**']),
        item('(i)', r'The derivative of $(1+x^2)^{e^{-x}}$ is',
             [CH('', [r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{2x}{1+x^2}-\ln(1+x^2)\right)$', r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{2x}{1+x^2}+\ln(1+x^2)\right)$', r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{1}{1+x^2}-\ln(1+x^2)\right)$', r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{1}{1+x^2}+\ln(1+x^2)\right)$', r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{1}{1+x^2}-2x\ln(1+x^2)\right)$', r'$e^{-x}(1+x^2)^{e^{-x}}\cdot\left(\frac{1}{1+x^2}+2x\ln(1+x^2)\right)$'], 0)], 4, 'derivative-rules',
             r'Logarithmic differentiation: $\ln f = e^{-x}\ln(1+x^2)$.', [r'$[\ln f]^{\prime} = -e^{-x}\ln(1+x^2) + e^{-x}\frac{2x}{1+x^2}$. **(A)**']),
    ]))
    return exam('2024-1', year='2024–2025', sitting=1, kind='Exam', date='March 25, 2025', iso='2025-03-25', minutes=120,
                file='calc-exam-2024-01', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2024_2():
    qs = []
    qs.append(question('1', 36, SEL, [
        item('(a)', r'A continuous random variable $X$ has the probability distribution $$g(x)=\begin{cases}\frac13\lfloor x\rfloor & \text{if } 0\le x\le3\\ 0 & \text{otherwise}\end{cases}$$ with $\lfloor x\rfloor$ the floor function, i.e., returning the greatest integer less than or equal to $x$. Then the expected value of $X$ is',
             [CH('', [r'$\frac13\cdot\frac92$', r'$\frac13\cdot5$', r'$\frac13\cdot\frac{11}2$', r'$\frac13\cdot6$', r'$\frac13\cdot\frac{13}2$'], 4)], 4, 'continuous', r'Split $[0,3]$ into the pieces where $\lfloor x\rfloor$ is $0$, $1$ and $2$.', [r'$E = \frac13\left(\int_1^2x\,dx + \int_2^3 2x\,dx\right) = \frac13\left(\frac32 + 5\right) = \frac13\cdot\frac{13}2$. **(E)**']),
        item('(b)', r'Let $f(x)=\ln\left(\dfrac{e^x-1}{e^x+1}\right)$, then its domain is', [CH('', [r'$\mathbb{R}$', r'$(-\infty,0]$', r'$[0,\infty)$', 'none of the above'], 3)], 4, 'domain-range', r'The argument of $\ln$ must be $> 0$; $e^x + 1 > 0$ always.', [r'Need $e^x > 1$, i.e. $x > 0$: the domain is $(0,\infty)$, not listed. **(D)**']),
        item('(c)', r'Let $f(x)=\ln\left(\dfrac{e^x-1}{e^x+1}\right)$, then its inverse is', [CH('', [r'$\ln\left(\frac{1-e^x}{e^x-1}\right)$', r'$\ln\left(\frac{1-e^x}{-e^x-1}\right)$', r'$\ln\left(\frac{-1-e^x}{-e^x-1}\right)$', r'$\ln\left(\frac{-e^x-1}{e^x-1}\right)$'], 3)], 4, 'inverse',
             r'$e^y = \frac{e^x-1}{e^x+1}$: solve for $e^x$.', [r'$e^y(e^x+1) = e^x - 1 \Rightarrow e^x = \frac{1+e^y}{1-e^y} = \frac{-e^y-1}{e^y-1}$. **(D)**']),
        item('(d)', r'If $f$ is a function that is neither odd nor even, doesn’t have a minimum or a maximum, and never takes negative values, then $f$ could be', [CH('', [r'$\ln(x)$', r'$\frac1{|x|}$', r'$e^{-x}$', r'$|\ln(x)|$', 'none of the above'], 2)], 4, 'even-odd',
             r'Check each property for each candidate.', [r'$\ln x$ takes negative values; $\frac1{|x|}$ is even; $|\ln x|$ has a minimum at $1$. $e^{-x}$ satisfies everything. **(C)**']),
        item('(e)', r'Let $f(x,y)=\dfrac{x+y}{x-y}$. The second partial derivative $\frac{\partial^2f}{\partial x\partial y}$ is', [CH('', [r'$\frac{-2x-2y}{(x-y)^3}$', r'$\frac{2x+2y}{(x-y)^3}$', r'$\frac{-2x+2y}{(x-y)^3}$', r'$\frac{2x-2y}{(x-y)^3}$'], 0)], 4, 'partial-derivatives',
             r'Quotient rule for $f_y$, then again for $\partial_x$.', [r'$f_y = \frac{2x}{(x-y)^2}$; $\partial_x$: $\frac{2(x-y) - 4x}{(x-y)^3} = \frac{-2x-2y}{(x-y)^3}$. **(A)**']),
        item('(f)', r'Let $f(x)=x\sqrt{x^2-1}$ and $g(x)=\dfrac{\tan x}{x}$. Then', [CH('', [r'$f$ is odd, and $g$ is odd', r'$f$ is odd, and $g$ is even', r'$f$ is even, and $g$ is odd', r'$f$ is even, and $g$ is even', 'one of them is neither odd nor even'], 1)], 4, 'even-odd',
             r'odd·even = odd; odd/odd = even.', [r'$f$: $x$ odd times $\sqrt{x^2-1}$ even: odd. $g$: odd/odd: even. **(B)**']),
        item('(g)', r'One of the slant asymptotes of $f(x)=\sqrt{a+bx^2}$ for some $a,b\in\mathbb{N}$ is best described by:', [CH('', [r'$(a+b)x$', r'$-bx$', r'$\sqrt{a-b}\,x$', r'$\sqrt{b}\,x$', '$f$ has no slant asymptotes'], 3)], 4, 'asymptotes',
             r'For large $|x|$, $\sqrt{a + bx^2}\approx\sqrt b\,|x|$.', [r'$\lim\frac{f(x)}{x} = \sqrt b$ for $x\to\infty$ (and $b = \lim(f - \sqrt bx) = 0$): $y = \sqrt b\,x$. **(D)**']),
        item('(h)', r'Suppose that three standard dice, with faces numbered from ‘1’ to ‘6’, are rolled together. What is the probability of getting at least one ‘4’ after the roll?', [CH('', [r'$\frac{1}{216}$', r'$\frac{15}{216}$', r'$\frac{75}{216}$', r'$\frac{91}{216}$', r'$\frac{125}{216}$'], 3)], 4, 'discrete',
             r'Complement: no ‘4’ at all.', [r'$1 - (\frac56)^3 = 1 - \frac{125}{216} = \frac{91}{216}$. **(D)**']),
        item('(i)', r'What is the value of the improper integral $\int_0^\infty(\cos(x)-\sin(x))\,dx$?', [CH('', ['$0$', '$1$', r'$\sqrt2$', r'$\infty$', 'none of the above'], 4)], 4, 'substitution',
             r'Find the antiderivative and look at its behaviour as $x\to\infty$.', [r'$\int_0^R = \sin R + \cos R - 1$, which keeps oscillating: the improper integral does not exist. **(E)**']),
    ]))
    qs.append(question('2', 6, '', [item('', r'Let $G$ be the graph of the implicit function $ax^2-ax^2y+y^2+b=0$ for some $a,b\in\mathbb{Z}$. Let $A=(1,3)$ be a point of $G$ with a tangent line having a $y$-intercept of $-1$. Determine the slope $m\in\mathbb{Z}$ of this tangent line.',
        [N('$m =$', 4)], 6, 'implicit-tangent', r"Find $y'$ in terms of $a$ at $A$; the tangent $y - 3 = m(x - 1)$ must have intercept $-1$.",
        [r"$2ax - 2axy - ax^2y' + 2yy' = 0 \Rightarrow y' = \dfrac{2ax(y-1)}{2y - ax^2}$; at $A$: $\dfrac{4a}{6-a}$.", r'Intercept: $3 - \frac{4a}{6-a} = -1 \Rightarrow a = 3$ (and $b = -3$).', r'$m = \frac{12}{3} = 4$.'])]))
    qs.append(question('3', 6, '', [item('', r'Determine the following limit (in $\mathbb{N}$) $$\lim_{n\to\infty}e\cdot\prod_{r=1}^n\left(\left(1+\left(\frac rn\right)^2\right)^{\frac{2r}{n^2}}\right)$$',
        [N('Limit:', 4)], 6, 'riemann', r'Take the logarithm of the product: it becomes $\sum\frac1n\cdot2\frac rn\ln(1 + (\frac rn)^2)$.',
        [r'$\ln L = \lim\sum\frac1n\cdot2\frac rn\ln\left(1 + \left(\frac rn\right)^2\right) = \int_0^1 2x\ln(1+x^2)dx$.', r'$u = 1 + x^2$: $\int_1^2\ln u\,du = [u\ln u - u]_1^2 = 2\ln2 - 1 = \ln\frac4e$.', r'$L = \frac4e$, so the limit is $e\cdot\frac4e = 4$.'])]))
    qs.append(question('4', 6, '', [item('', r'Let $A$ be the area enclosed by the three half circles • $y=\sqrt{1-x^2}$, defined on the domain $x\in[-1,1]$; • $y=\sqrt{1-(x-1)^2}-1$, defined on the domain $x\in[0,2]$; • $y=\sqrt{1-(x+1)^2}-1$, defined on the domain $x\in[-2,0]$. Determine the size of the area $A\in\mathbb{N}$. *NB: You can use integral calculations to determine the area between the curves, but these are not needed as there is also a more intuitive solution than only requires a careful examination of the curves.*',
        [N('$A =$', 2)], 6, 'area', r'Sketch the three half circles. The parts below the $x$-axis exactly fill what is missing from a rectangle.',
        [r'The region below the $x$-axis is exactly the part missing from the rectangle with corners $(-1,0)$ and $(1,1)$ above the axis.', r'So $A$ equals the area of that rectangle: $2$.'])]))
    fq5 = sqrt((x ** 2 - 2) / (x - 2) * exp(x))
    qs.append(question('5', 6, '', [item('', r'Let $f(x)=\sqrt{\left(\dfrac{x^2-2}{x-2}\right)e^x}$. Compute the derivative using **logarithmic derivation**.',
        [EX("$f'(x) =$", fq5 * (x / (x ** 2 - 2) - 1 / (2 * (x - 2)) + R(1, 2)), sample={'x': [2.3, 4]})], 6, 'derivative-rules',
        r'$\ln f = \frac12\left(\ln(x^2-2) - \ln(x-2) + x\right)$; differentiate and multiply by $f$.',
        [r'$\ln f = \frac12\big(\ln(x^2-2) - \ln(x-2) + x\big)$ (the factor $e^x$ is inside the root).', r'$[\ln f]^{\prime} = \frac{x}{x^2-2} - \frac{1}{2(x-2)} + \frac12$.', r"$f'(x) = \sqrt{\frac{x^2-2}{x-2}e^x}\left(\frac{x}{x^2-2} - \frac{1}{2(x-2)} + \frac12\right)$."])]))
    qs.append(question('6', 6, '', [item('', r'Let $A,B,C\in\mathbb{Q}$ and $A,B,C>0$. Suppose that $$\lim_{x\to0}\frac{(A\cdot x+B)^3-8-C\cdot\sin(x)}{1-\cos(x)}=3$$ Determine the values for $A$, $B$, $C$.',
        [N('$A =$', R(1, 2)), N('$B =$', 2), N('$C =$', 6)], 6, 'lhopital', r'Denominator $\to0$: numerator $\to0$ gives $B$. After one L\'Hôpital step the denominator $\sin x\to0$ again.',
        [r'$B^3 - 8 = 0 \Rightarrow B = 2$.', r"L'Hôpital: $\dfrac{3(Ax+B)^2A - C\cos x}{\sin x}$; numerator at $0$: $12A - C = 0$.", r"L'Hôpital: $\dfrac{6(Ax+B)A^2 + C\sin x}{\cos x}\to12A^2 = 3 \Rightarrow A = \frac12$, $C = 6$."])]))
    qs.append(question('7', 6, '', [item('', r'Determine $\int\sin(2x)e^{4x}dx$.',
        [EX(r'$\displaystyle\int\sin(2x)e^{4x}dx =$', sin(2 * x) * exp(4 * x) / 5 - cos(2 * x) * exp(4 * x) / 10, sample={'x': [-1, 0.5]}, upc=True)], 6, 'by-parts',
        r'By parts twice (integrate $e^{4x}$ each time); the original integral comes back — solve for it.',
        [r'$\int\sin(2x)e^{4x}dx = \frac14\sin(2x)e^{4x} - \frac2{16}\cos(2x)e^{4x} - \frac14\int\sin(2x)e^{4x}dx$.', r'$\frac54\int\sin(2x)e^{4x}dx = \frac14\sin(2x)e^{4x} - \frac18\cos(2x)e^{4x}$.', r'$\int\sin(2x)e^{4x}dx = \frac15\sin(2x)e^{4x} - \frac1{10}\cos(2x)e^{4x} + C$.'])]))
    qs.append(question('8', 12, r'Determine the following limits (in $\mathbb{Z}$ when it exists) where $f$ and $g$ are defined by the following graphs %s %s' % (img('2025-06-q8-f.png', 'Graph of y = f(x) on [-4, 4]'), img('2025-06-q8-g.png', 'Graph of y = g(x) on [-4, 4]')), [
        item('(i)', r'$\lim_{x\to1}f(x)+g(x)$', [N('Limit:', 2)], 4, 'limits', r'Compute both one-sided limits of $f$ and $g$ at $1$ separately and add them.', [r'From the left: $1 + 1 = 2$; from the right: $4 + (-2) = 2$. The limit is $2$.']),
        item('(ii)', r'$\lim_{x\to-1}\dfrac{f(x)}{g(x)}$', [N('Limit:', 6)], 4, 'lhopital', r'$f(-1) = g(-1) = 0$: form $\tfrac00$. Both are straight lines near $-1$ — compare their slopes.', [r'Near $-1$: $f(x) = 3x + 3$ and $g(x) = \frac12x + \frac12$.', r"$\lim\frac{f}{g} = \frac{f'}{g'} = \frac{3}{1/2} = 6$."]),
        item('(iii)', r'$\lim_{x\to2}(f\circ g)(x)$', [N('Limit:', -3)], 4, 'limits', r'First find how $g(x)$ approaches its limit at $x = 2$ (from which side), then look at $f$ there.', [r'As $x\to2$, $g(x)\to-2$ from above.', r'$\lim_{y\downarrow-2}f(y) = -3$.']),
    ]))
    qs.append(question('9', 6, r'Consider a continuos random variable $X$ that takes values in the interval $[a,b]$ and has the following probability density function (pdf): $$p(x)=\frac{Z}{(b-a)^3}\left(x-\frac{a+b}{2}\right)^2$$ for $x\in[a,b]$, $Z>0$. This is sometimes called the $U$-quadratic distribution.', [
        item('(a)', r'What is the value of $Z\in\mathbb{N}$, such that $p(x)$ is properly normalized?', [N('$Z =$', 12)], 2, 'continuous', r'$\int\left(x - \frac{a+b}2\right)^2dx = \frac13\left(x - \frac{a+b}2\right)^3$.',
             [r'$1 = \frac{Z}{(b-a)^3}\cdot\frac13\left[\left(\frac{b-a}2\right)^3 - \left(-\frac{b-a}2\right)^3\right] = \frac{Z}{(b-a)^3}\cdot\frac13\cdot\frac{(b-a)^3}{4} = \frac{Z}{12}$.', r'$Z = 12$.']),
        item('(b)', r'Derive the **mean** and the **mode** of the above distribution, knowing that: • The mean is the expected value of the random variable, that is, $E(X)=\int xp(x)dx$; • The mode conists of all the values of $X$ for which the pdf $p(x)$ obtains its maximum, in other words $\arg\max_{x\in[a,b]}p(x)$.',
             [EX('Mean $=$', (a + b) / 2, vars=('a', 'b'), sample={'a': [0, 1], 'b': [2, 4]}, pts=2), STV('Mode (all values):', [a, b], ('a', 'b'), {'a': [0, 1], 'b': [2, 4]}, pts=2)], 4, 'continuous',
             r'The pdf is symmetric around $\frac{a+b}2$; where is a upward parabola largest on a closed interval?', [r'Symmetry around $\frac{a+b}2$ gives mean $\frac{a+b}2$.', r'The parabola is maximal at both endpoints: mode $\{a, b\}$.']),
    ]))
    return exam('2024-2', year='2024–2025', sitting=2, kind='Resit', date='June 23, 2025', iso='2025-06-23', minutes=120,
                file='calc-exam-2024-02', instructions=STD_120, questions=qs)


# =====================================================================================
def exam_2025_1():
    qs = []
    qs.append(question('1', 36, SEL, [
        item('(a)', r'Consider the function $f(x)=4x^2-\ln|x|$ for $x\neq0$. On which interval is $f$ increasing? (It may be increasing elsewhere too.)',
             [CH('', [r'$\left(-1,\frac{-1}{\sqrt2}\right)$', r'$\left(\frac{-1}{\sqrt2},\frac{-1}{2\sqrt2}\right)$', r'$\left(\frac{-1}{2\sqrt2},0\right)$', r'$\left(0,\frac{1}{2\sqrt2}\right)$', 'None of these'], 2)], 4, 'function-analysis',
             r"$f'(x) = 8x - \frac1x$; use a sign chart.", [r"$f'(x) = \frac{8x^2-1}{x} > 0$ on $(-\frac1{2\sqrt2}, 0)\cup(\frac1{2\sqrt2},\infty)$. **(C)**"]),
        item('(b)', r'The slant asymptote of $\dfrac{x^2-x-1}{x+1}$ is', [CH('', [r'$y=x+1$', r'$y=x$', r'$y=x-1$', r'$y=x-2$', 'None of these'], 3)], 4, 'asymptotes', r'Long division by $x + 1$.', [r'$\frac{x^2-x-1}{x+1} = x - 2 + \frac{1}{x+1}$. **(D)**']),
        item('(c)', r'Let $f(x)=x^4-4x^3-18x^2+15$. On which interval is $f$ convex? (It may be convex elsewhere too.)', [CH('', [r'$(-\infty,3)$', r'$(-1,3)$', r'$(-1,\infty)$', r'$(3,\infty)$', 'None of these'], 3)], 4, 'concavity',
             r"$f'' = 12x^2 - 24x - 36$; factor it.", [r"$f'' = 12(x-3)(x+1) > 0$ on $(-\infty,-1)\cup(3,\infty)$. **(D)**"]),
        item('(d)', r'Let $f(x)=x^4-4x^3-18x^2+15$. Where does $f$ have an inflection point? (It may have more than one inflection point.)', [CH('', [r'$x=-3$', r'$x=-2$', r'$x=-1$', r'$x=1$', 'None of these'], 2)], 4, 'concavity',
             r"Zeros of $f''$ with a sign change.", [r"$f'' = 12(x-3)(x+1)$ changes sign at $-1$ and $3$. **(C)**"]),
        item('(e)', r'The second partial derivative $\frac{\partial^2}{\partial x\partial y}(x-y)^3\ln(x-y)$ is equal to', [CH('', [r'$(x-y)(-6\ln(x-y)-5)$', r'$(x-y)(-6\ln(x-y)-3)$', r'$(x-y)(-6\ln(x-y)-2)$', r'$(x-y)(-6\ln(x-y)+1)$', 'None of these'], 0)], 4, 'partial-derivatives',
             r'Mind the inner derivative $-1$ when differentiating with respect to $y$.', [r'$\partial_y = -3(x-y)^2\ln(x-y) - (x-y)^2$.', r'$\partial_x$: $-6(x-y)\ln(x-y) - 3(x-y) - 2(x-y) = (x-y)(-6\ln(x-y) - 5)$. **(A)**']),
        item('(f)', r'Let $y^2-x^2y+x=1$ be an implicit function. Then the slope of the tangent at $(-1,-1)$ is equal to', [CH('', ['$-1$', r'$-\frac12$', r'$-\frac13$', r'$-\frac14$', r'$-\frac15$'], 2)], 4, 'implicit-tangent',
             r"Differentiate: $2yy' - 2xy - x^2y' + 1 = 0$.", [r"$y' = \frac{2xy - 1}{2y - x^2}$; at $(-1,-1)$: $\frac{1}{-3}$. **(C)**"]),
        item('(g)', r'The limit $$\lim_{n\to\infty}\sum_{r=1}^n\frac{re^{\frac rn}}{n^2}$$ is equal to', [CH('', ['$1$', '$2$', '$e$', '$e^2$', 'None of these'], 0)], 4, 'riemann', r'$\frac1n\sum\frac rne^{r/n}\to\int_0^1xe^xdx$.', [r'$\int_0^1xe^xdx = [(x-1)e^x]_0^1 = 1$. **(A)**']),
        item('(h)', r'Let $f=\sqrt{x^2-1}$ and $g=x\tan(x)$. Then', [CH('', [r'$(f\circ g)(x)$ is odd and $(g\circ f)(x)$ is odd', r'$(f\circ g)(x)$ is even and $(g\circ f)(x)$ is odd', r'$(f\circ g)(x)$ is odd and $(g\circ f)(x)$ is even', r'$(f\circ g)(x)$ is even and $(g\circ f)(x)$ is even', 'None of these'], 3)], 4, 'even-odd',
             r'Determine the parity of $f$ and $g$ first.', [r'$f$ is even; $g$ = odd·odd = even. A composition with an even inner function is even, so both are even. **(D)**']),
        item('(i)', r'The probability distribution of a random variable $X$ taking values in $S=\{1,2,3,4,5\}$ is given below (where $p_1$, $p_2$, and $k$ are unknown probabilities): $$\begin{array}{|c|c|c|c|c|c|}\hline X & 1 & 2 & 3 & 4 & 5\\ \hline P(X) & k & p_1 & 4k & p_2 & 2k\\ \hline\end{array}$$ It is further given that $P(X\le2)=0.25$ and $P(X\ge4)=0.35$. Which of the following two statements are true? (1) $p_1=p_2$ (2) $p_1+p_2=P(X=3)$',
             [CH('', ['Only (1) is true', 'Only (2) is true', 'Both (1) and (2) are true', 'Neither (1) nor (2) are true'], 0)], 4, 'discrete', r'$P(X = 3) = 1 - 0.25 - 0.35$ gives $k$.', [r'$4k = 0.4 \Rightarrow k = 0.1$; $p_1 = 0.25 - 0.1 = 0.15$, $p_2 = 0.35 - 0.2 = 0.15$.', r'$p_1 = p_2$ but $p_1 + p_2 = 0.3\neq0.4$. **(A)**']),
    ]))
    qs.append(question('2', 9, r'Let $$f(x)=\sqrt{\frac{x-1}{x+3}}$$', [
        item('(a)', r'Determine the domain of $f$', [IV('$D(f) =$', Union(Interval.open(-oo, -3), Interval(1, oo)))], 2, 'domain-range', r'Need $\frac{x-1}{x+3}\ge0$ and $x\neq-3$; sign chart.', [r'$\frac{x-1}{x+3}\ge0$ for $x < -3$ or $x\ge1$: $D(f) = (-\infty,-3)\cup[1,\infty)$.']),
        item('(b)', r'Is $f$ continuous?', [CH('', ['Yes', 'No'], 0)], 1, 'continuity', r'Compositions of continuous functions are continuous on their domain.', [r'Yes, on its domain $f$ is continuous.']),
        item('(c)', r'Compute the inverse $f^{-1}(x)$.', [EX('$f^{-1}(x) =$', (-3 * x ** 2 - 1) / (x ** 2 - 1), sample={'x': [0.1, 0.9]})], 3, 'inverse', r'Square both sides of $y = \sqrt{\frac{x-1}{x+3}}$ and solve for $x$.',
             [r'$y^2(x+3) = x - 1 \Rightarrow x(y^2-1) = -3y^2 - 1 \Rightarrow x = \frac{-3y^2-1}{y^2-1}$.', r'$f^{-1}(x) = \frac{-3x^2-1}{x^2-1}$.']),
        item('(d)', r'Determine $\lim_{x\to\infty}f(x)$, $\lim_{x\to-\infty}f(x)$, $\lim_{x\to-3^-}f(x)$', [N(r'$\lim_{x\to\infty}$:', 1, pts=R(2, 3)), N(r'$\lim_{x\to-\infty}$:', 1, pts=R(2, 3)), N(r'$\lim_{x\to-3^-}$:', OO, pts=R(2, 3))], 2, 'limits',
             r'For $x\to\pm\infty$ the fraction tends to $1$. For $x\to-3^-$ the denominator is a small negative number.', [r'Both limits at $\pm\infty$ equal $1$; $\lim_{x\to-3^-}f(x) = \infty$.']),
        item('(e)', r'Determine the range of $f$', [IV('$R(f) =$', Union(Interval.Ropen(0, 1), Interval.open(1, oo)))], 1, 'domain-range', r'Use (d): $f(1) = 0$, $f$ never reaches $1$, and grows without bound near $-3$.', [r'$R(f) = [0,1)\cup(1,\infty)$.']),
    ]))
    qs.append(question('3', 9, '', [
        item('(a)', r'Determine values $A,B\in\mathbb{N}$ such that the following limit exists $$\lim_{x\to0}f(x)=\lim_{x\to0}\frac{e^{3x}-Ax-B}{x}=1$$', [N('$A =$', 2), N('$B =$', 1)], 3, 'lhopital',
             r'The numerator must vanish at $0$ (gives $B$); then L\'Hôpital gives $3 - A$.', [r'$1 - B = 0 \Rightarrow B = 1$.', r"L'Hôpital: $\lim(3e^{3x} - A) = 3 - A = 1 \Rightarrow A = 2$."]),
        item('(b)', r'Let $g(x)$ be the continuous extension on $\mathbb{R}$ of the function $f$ above, such that $g(0)=\lim_{x\to0}f(x)=1$ for the values of $A$ and $B$ previously found. Determine now the tangent line of $g(x)$ in the point $(0,1)$. [Hint: $g^{\prime}$ is continuous, and for a continous function $h$ and $a\in D(h)$ we have $\lim_{x\to a}h(a)=h(a)$]',
             [EX('$y =$', R(9, 2) * x + 1)], 6, 'implicit-tangent', r"$g'(0) = \lim_{x\to0}g'(x)$; compute $g'$ with the quotient rule and apply L\'Hôpital twice.",
             [r"$g'(x) = \dfrac{(3e^{3x}-2)x - (e^{3x}-2x-1)}{x^2} = \dfrac{(3x-1)e^{3x} + 1}{x^2}$.", r"L'Hôpital twice: $\lim\frac{9xe^{3x}}{2x} = \frac92$.", r'Tangent: $y = \frac92x + 1$.']),
    ]))
    qs.append(question('4', 12, '', [
        item('(a)', r'If $$\int\frac{x^2+x+\frac14}{\sqrt{2x+1}}\,dx=A(\sqrt{2x+1})^B\ (+C)$$ Then what are the values for $A$ and $B$? [Hint: use $u$-substitution]', [N('$A =$', R(1, 20)), N('$B =$', 5)], 6, 'substitution',
             r'$u = \sqrt{2x+1}$: $u\,du = dx$ and $x^2 + x + \frac14 = \frac14(2x+1)^2 = \frac14u^4$.', [r'$\int\frac{\frac14u^4}{u}u\,du = \int\frac14u^4du = \frac1{20}u^5$.', r'$= \frac1{20}(\sqrt{2x+1})^5 + C$: $A = \frac1{20}$, $B = 5$.']),
        item('(b)', r'Determine $$\int\frac{5x^2+7x+3}{(x+1)(x^2+x+1)}\,dx=\int\frac{A}{x+1}+\frac{Bx+D}{x^2+x+1}\,dx=E\ln|x+1|+F\ln(x^2+x+1)+C$$ with $C$ the unspecified constant of integration.',
             [N('$A =$', 1), N('$B =$', 4), N('$D =$', 2), N('$E =$', 1), N('$F =$', 2)], 4, 'partial-fractions',
             r'$5x^2 + 7x + 3 = A(x^2+x+1) + (Bx + D)(x+1)$; substitute $x = -1, 0, 1$. Note $4x + 2 = 2(2x+1)$.',
             [r'$x=-1$: $A = 1$; $x = 0$: $D = 2$; $x = 1$: $B = 4$.', r'$\int\frac{1}{x+1} + 2\frac{2x+1}{x^2+x+1}dx = \ln|x+1| + 2\ln(x^2+x+1) + C$: $E = 1$, $F = 2$.']),
        item('(c)', r'Determine $$\int\frac{32}{16x^2-24x+25}\,dx=A\arctan(x+B)+C$$ with $C$ the unspecified constant of integration. [Hint: $\arctan(x)^{\prime}=\frac{1}{1+x^2}$.]', [N('$A =$', 2), N('$B =$', R(-3, 4))], 2, 'substitution',
             r'Divide by $16$ and complete the square: $x^2 - \frac32x + \frac{25}{16} = (x - \frac34)^2 + 1$.', [r'$\int\frac{2}{(x-\frac34)^2+1}dx = 2\arctan(x - \frac34) + C$.']),
    ]))
    qs.append(question('5', 3, '', [item('', r'Determine the limit $$\lim_{x\to\infty}\frac{\sqrt{9x^2+11x-7}}{\sqrt{|2x+5|+4x^2-2x-13}}$$', [N('Limit:', R(3, 2))], 3, 'limits', r'Divide numerator and denominator by $\sqrt{x^2} = x$.', [r'Only the quadratic terms survive: $\frac{\sqrt9}{\sqrt4} = \frac32$.'])]))
    qs.append(question('6', 6, '', [item('', r'If $$f(x)=\begin{cases}(1+\sin(x))^{\frac{A}{\sin(x)}} & -\frac\pi6<x<0\\ B & x=0\\ e^{\frac{\tan(2x)}{\tan(3x)}} & 0<x<\frac\pi6\end{cases}$$ is continuous in $0$, then what are $A$ and $B$?',
        [N('$A =$', R(2, 3)), N('$B =$', exp(R(2, 3)))], 6, 'lhopital', r'Compute both one-sided limits: the left one is of the form $1^\infty$ (take logs), the right one needs $\lim\frac{\tan 2x}{\tan 3x}$.',
        [r'$\ln L_1 = \lim A\frac{\ln(1+\sin x)}{\sin x} = A$ (L\'Hôpital), so $L_1 = e^A$.', r'$\lim\frac{\tan 2x}{\tan3x} = \frac23$, so $L_2 = e^{2/3}$.', r'Continuity: $e^A = e^{2/3} = B$: $A = \frac23$, $B = e^{2/3}$.'])]))
    qs.append(question('7', 6, '', [item('', r'Compute the area bounded by the curves $y=\sqrt x$ and $2y-x+3=0$, the $x$-axis, and which lies in the first quadrant (i.e., $x\ge0$ and $y\ge0$).',
        [N('Area:', 9)], 6, 'area', r'The line is $y = \frac12x - \frac32$; it meets $\sqrt x$ at $x = 9$ and the $x$-axis at $x = 3$.',
        [r'$\frac12x - \frac32 = \sqrt x \Rightarrow (x-3)^2 = 4x \Rightarrow x\in\{1, 9\}$; only $x = 9$ works: $(9,3)$.', r'Area $= \int_0^9\sqrt x\,dx - \int_3^9(\frac12x - \frac32)dx = 18 - 9 = 9$.'])]))
    qs.append(question('8', 3, '', [item('', r'Consider a pair of Sicherman dice, which are six-sided dice with non-standard numbers. One die has the sides $1,2,2,3,3,4$, while the other has the sides $1,3,4,5,6,8$, as can be seen in the figure below. %s *Figure 1: Pair of Sicherman dice* If you roll the pair of Sicherman dice, what is the probability that the sum of the two dice is even?' % img('2025-10-q8-dice.png', 'Nets of the two Sicherman dice'),
        [NP('$P =$', R(1, 2))], 3, 'discrete', r'Only parity matters: how many odd and even sides does each die have?',
        [r'Each die has three odd and three even sides: $P(\text{odd}) = P(\text{even}) = \frac12$.', r'Sum even iff both odd or both even: $\frac14 + \frac14 = \frac12$.'])]))
    tq = sp.Symbol('t', positive=True)
    pc = 1 - (exp(R(-1, 4)) + exp(R(-1, 2))) / 2
    pd = (1 - exp(R(-1, 4))) / (2 - exp(R(-1, 4)) - exp(R(-1, 2)))
    qs.append(question('9', 6, r'The time in minutes that it takes bank clerk A to serve a customer follows an exponential distribution with density: $$p_A(t)=\begin{cases}\frac14\cdot e^{-\frac14t} & t\ge0\\ 0 & t<0\end{cases}.$$', [
        item('(a)', r'What is the expected value of the service time (i.e., the mean service time in minutes) needed by bank clerk A to serve a customer?', [N('$E(T_A) =$', 4)], 2, 'continuous', r'Integrate $t\cdot p_A(t)$ by parts (or recall $E = \frac1\lambda$).', [r'$E(T_A) = \int_0^\infty\frac t4e^{-t/4}dt = \big[-te^{-t/4}\big]_0^\infty + \int_0^\infty e^{-t/4}dt = 4$.']),
        item('(b)', r'The bank has recently hired clerk B, whose mean service time (in minutes) is half that of bank clerk A. If the time (in minutes) that it takes bank clerk B to serve a customer still follows an exponential distribution $p_B(t)=\lambda\cdot e^{-\lambda t}$ for $t\ge0$, then what is the value of $\lambda$?', [N(r'$\lambda =$', R(1, 2))], 1, 'continuous', r'$E(T_B) = \frac1\lambda$.', [r'$\frac1\lambda = 2 \Rightarrow \lambda = \frac12$.']),
        item('(c)', r'A customer enters the bank when no one else is there, so they can be served by either bank clerk A or B. If the customer has an equal chance of being assigned to bank clerk A or B, what is the probability that they will be served in less than (or equal to) one minute? *Nota bene: Use the value of $\lambda$ determined in subexercise (b).*', [N(r'$P(T\le1) =$', pc, tol={'abs': 5e-4})], 2, 'conditional',
             r'Law of total probability over the clerk; $P(T\le1) = 1 - e^{-\lambda}$ for an exponential distribution.', [r'$P(T\le1) = \frac12(1 - e^{-1/4}) + \frac12(1 - e^{-1/2}) = 1 - \frac{e^{-1/4} + e^{-1/2}}{2}\approx0.307$.']),
        item('(d)', r'The customer was quite lucky, as their service time was in fact less than (or equal to) one minute. What is the probability that this customer was served by bank clerk A? *Hint: Use the results obtained in subexercise (c).*', [N(r'$P(C = A\mid T\le1) =$', pd, tol={'abs': 5e-4})], 1, 'conditional',
             r'Bayes: $\dfrac{P(T\le1\mid A)P(A)}{P(T\le1)}$.', [r'$\dfrac{(1 - e^{-1/4})\cdot\frac12}{1 - \frac{e^{-1/4}+e^{-1/2}}2} = \dfrac{1 - e^{-1/4}}{2 - e^{-1/4} - e^{-1/2}}\approx0.360$.']),
    ]))
    return exam('2025-1', year='2025–2026', sitting=1, kind='Exam', date='October 31, 2025', iso='2025-10-31', minutes=180,
                file='calc-exam-2025-01', instructions=STD_180, questions=qs)


# =====================================================================================
def exam_2025_2():
    qs = []
    qs.append(question('1', 36, 'Select the best fitting answer:', [
        item('(a)', r'If $f(x)=(ax^5+b)^3$, then the function $g$ such that $f(g(x))=g(f(x))$ could be given by',
             [CH('', [r'$g(x)=\left(\frac{b-x^{1/3}}{a}\right)^5$', r'$g(x)=\frac{1}{(ax^5+b)^3}$', r'$g(x)=(ax^5+b)^{1/3}$', r'$g(x)=\left(\frac{x^{1/3}-b}{a}\right)^{1/5}$', 'None of these'], 3)], 4, 'inverse',
             r'A function commutes with its own inverse: $f(f^{-1}(x)) = f^{-1}(f(x)) = x$.', [r'Solve $y = (ax^5+b)^3$: $x = \left(\frac{y^{1/3}-b}{a}\right)^{1/5}$ — the inverse works. **(D)**']),
        item('(b)', r'The *slant asymptote* of $\dfrac{2x^3-3x^2-1}{(x-1)(x+1)}$ is', [CH('', [r'$y=2x+1$', r'$y=2x-1$', r'$y=2x-2$', r'$y=2x-3$', 'None of these'], 3)], 4, 'asymptotes', r'Divide by $x^2 - 1$.', [r'$\frac{2x^3-3x^2-1}{x^2-1} = 2x - 3 + \frac{2x-4}{x^2-1}$. **(D)**']),
        item('(c)', r'The *indefinite integral* $\int x\sqrt{x+1}\,dx$ is', [CH('', [r'$\frac25\sqrt{(x+1)^5}-\frac23\sqrt{(x+1)^3}+C$', r'$\frac25\sqrt{(x+1)^5}-\frac23x\sqrt{(x+1)^3}+C$', r'$\frac25x\sqrt{(x+1)^5}-\frac23\sqrt{(x+1)^3}+C$', r'$\frac25x\sqrt{(x+1)^5}-\frac23x\sqrt{(x+1)^3}+C$', 'None of these'], 0)], 4, 'substitution',
             r'$u = x + 1$, so $x = u - 1$.', [r'$\int(u-1)\sqrt u\,du = \frac25u^{5/2} - \frac23u^{3/2} + C$. **(A)**']),
        item('(d)', r'The value of the *improper integral* $\int_0^8\frac{1}{\sqrt[3]{x}}\,dx$ is', [CH('', [r'$\frac32$', '$6$', '$12$', 'Undefined (the improper integral diverges)', 'None of these'], 1)], 4, 'substitution', r'$\int x^{-1/3}dx = \frac32x^{2/3}$.', [r'$\frac32\cdot8^{2/3} = \frac32\cdot4 = 6$. **(B)**']),
        item('(e)', r'The *second partial derivative* $\dfrac{\partial^2}{\partial x\partial y}\dfrac{xy}{x+y}$ is equal to', [CH('', [r'$\frac{xy}{(x+y)^4}$', r'$\frac{2xy}{(x+y)^3}$', r'$\frac{xy}{(x+y)^3}$', r'$\frac{2xy}{(x+y)^4}$', 'None of these'], 1)], 4, 'partial-derivatives',
             r'$\frac{\partial}{\partial y}\frac{xy}{x+y} = \frac{x^2}{(x+y)^2}$.', [r'$\partial_x\frac{x^2}{(x+y)^2} = \frac{2x(x+y) - 2x^2}{(x+y)^3} = \frac{2xy}{(x+y)^3}$. **(B)**']),
        item('(f)', r'Consider the continuous uniform distribution on the real interval $[0,4]$. The *standard deviation* of this distribution is equal to:', [CH('', [r'$\sqrt2$', '$2$', r'$\frac{\sqrt3}{2}$', r'$\frac34$', 'None of these'], 4)], 4, 'continuous',
             r'$Var = \frac{(b-a)^2}{12}$.', [r'$Var = \frac{16}{12} = \frac43$, so $\sigma = \frac{2}{\sqrt3}\approx1.15$ — not listed. **(E)**']),
        item('(g)', r'The function $f(x)=e^{-x}\left(x^2+2x-2\right)$ has a *local minimum* at', [CH('', [r'$x=-2$', r'$x=0$', r'$x=2$', r'$x=\infty$', 'None of these'], 0)], 4, 'function-analysis',
             r"$f'(x) = e^{-x}(4 - x^2)$; check where $f'$ changes from $-$ to $+$.", [r"$f' < 0$ for $x < -2$ and $> 0$ on $(-2,2)$: local minimum at $x = -2$. **(A)**"]),
        item('(h)', r'Let $f(x)=\lfloor x\rfloor$ and $g(x)=\lceil x\rceil$, where $\lfloor x\rfloor$ ($\lceil x\rceil$) is the floor (ceiling) function that rounds $x$ down (up) to the nearest integer, then',
             [CH('', [r'$f(x)-g(x)$ is odd and $f(x)+g(x)$ is odd', r'$f(x)-g(x)$ is even and $f(x)+g(x)$ is odd', r'$f(x)-g(x)$ is odd and $f(x)+g(x)$ is even', r'$f(x)-g(x)$ is even and $f(x)+g(x)$ is even', 'None of these'], 1)], 4, 'even-odd',
             r'Use $\lfloor -x\rfloor = -\lceil x\rceil$.', [r'$f(-x) - g(-x) = -\lceil x\rceil + \lfloor x\rfloor = f(x) - g(x)$: even.', r'$f(-x) + g(-x) = -\lceil x\rceil - \lfloor x\rfloor$: odd. **(B)**']),
        item('(i)', r'The *derivative* of the function $f(x)=\dfrac{x\sqrt[3]{3x+1}}{e^{2x}\cos x}$ is equal to',
             [CH('', [r'$\frac{x\sqrt[3]{3x+1}}{e^{2x}\cos x}\left(\frac1x+\frac{1}{3(3x+1)}-2-\sin x\right)$', r'$\frac{x\sqrt[3]{3x+1}}{e^{2x}\cos x}\left(\frac1x+\frac{1}{3x+1}+2-\sin x\right)$', r'$\frac{x\sqrt[3]{3x+1}}{e^{2x}\cos x}\left(\frac1x+\frac{1}{3x+1}-2+\tan x\right)$', r'$\frac{x\sqrt[3]{3x+1}}{e^{2x}\cos x}\left(\frac1x+\frac{1}{3(3x+1)}+2+\tan x\right)$', 'None of these'], 2)], 4, 'derivative-rules',
             r'Logarithmic differentiation: $\ln f = \ln x + \frac13\ln(3x+1) - 2x - \ln\cos x$.', [r'$[\ln f]^{\prime} = \frac1x + \frac13\cdot\frac{3}{3x+1} - 2 + \tan x$. **(C)**']),
    ]))
    qs.append(question('2', 6, r'Let $$f(x)=\frac{1}{|x-2|+|x+2|}$$ Answer the following subquestions:', [
        item('(a)', r'What is the domain of $f$?', [IV('$D(f) =$', S.Reals)], 1, 'domain-range', r'Can the denominator ever be $0$?', [r'$|x-2| + |x+2|\ge4 > 0$, so $D(f) = \mathbb{R}$.']),
        item('(b)', r'Is $f$ continuous?', [CH('', ['Yes', 'No'], 0)], 1, 'continuity', r'Write $f$ piecewise and check the break points $\pm2$.', [r'$f = \frac{1}{-2x}$ for $x\le-2$, $\frac14$ on $(-2,2)$, $\frac1{2x}$ for $x\ge2$; the pieces agree at $\pm2$: continuous.']),
        item('(c)', r'On which interval(s) is $f$ strictly increasing / strictly decreasing?', [IV('Strictly increasing on:', Interval(-oo, -2), loose=True, pts=R(1, 2)), IV('Strictly decreasing on:', Interval(2, oo), loose=True, pts=R(1, 2))], 1, 'function-analysis',
             r'Use the piecewise form from (b).', [r'Strictly increasing on $(-\infty,-2]$, strictly decreasing on $[2,\infty)$; constant on $[-2,2]$.']),
        item('(d)', r'On which interval(s) is $f$ increasing / decreasing?', [IV('Increasing on:', Interval(-oo, 2), loose=True, pts=R(1, 2)), IV('Decreasing on:', Interval(-2, oo), loose=True, pts=R(1, 2))], 1, 'function-analysis',
             r'A constant piece counts as both (non-strictly) increasing and decreasing.', [r'Increasing on $(-\infty,2]$, decreasing on $[-2,\infty)$.']),
        item('(e)', r'Determine $\lim_{x\to-\infty}f(x)$ and $\lim_{x\to\infty}f(x)$', [N(r'$\lim_{x\to-\infty}f(x) =$', 0, pts=R(1, 2)), N(r'$\lim_{x\to\infty}f(x) =$', 0, pts=R(1, 2))], 1, 'limits', r'For large $|x|$, $f(x) = \frac{1}{2|x|}$.', [r'Both limits are $0$.']),
        item('(f)', r'What is the range of $f$?', [IV('$R(f) =$', Interval.Lopen(0, R(1, 4)))], 1, 'domain-range', r'Maximum value on $[-2,2]$, tends to $0$ (never reached) at $\pm\infty$.', [r'$R(f) = (0, \frac14]$.']),
    ]))
    AB = {'a': [1.5, 4], 'b': [1.5, 4]}
    qs.append(question('3', 6, '', [item('', r'Determine $$\lim_{x\to0}\frac{(ab)^x-a^x-b^x+1}{x\tan(x)}$$', [EX('Limit:', log(a) * log(b), vars=('a', 'b'), sample=AB)], 6, 'lhopital',
        r'Form $\tfrac00$: apply L\'Hôpital twice; $(c^x)^{\prime} = c^x\ln c$.',
        [r"L'Hôpital: $\dfrac{\ln(ab)(ab)^x - \ln(a)a^x - \ln(b)b^x}{\tan x + x/\cos^2x}$ (still $\tfrac00$).", r"L'Hôpital again: numerator $\to\ln^2(ab) - \ln^2a - \ln^2b$, denominator $\to 1 + 1 = 2$.",
         r'$\frac{(\ln a + \ln b)^2 - \ln^2a - \ln^2b}{2} = \ln(a)\ln(b)$.'])]))
    qs.append(question('4', 6, '', [item('', r'Let $y+x^2y-5=0$ be an *implicit function*. Determine the tangent at $x=-2$.', [EX('$y =$', R(4, 5) * x + R(13, 5))], 6, 'implicit-tangent',
        r"At $x = -2$: $5y = 5$, so the point is $(-2, 1)$. Differentiate implicitly for $y'$.",
        [r"$y' + 2xy + x^2y' = 0 \Rightarrow y' = \frac{-2xy}{1+x^2}$; at $(-2,1)$: $\frac45$.", r'$y - 1 = \frac45(x+2) \Rightarrow y = \frac45x + \frac{13}5$.'])]))
    qs.append(question('5', 18, '', [
        item('(a)', r'Use *substitution* to transform the following integral $$\int_0^4e^{-\sqrt{1+\frac12x^2}}x^3\,dx=\int_a^be^{-u}p(u)\,du$$ with $p(u)$ a polynomial in $u$ with integer coefficients ($\mathbb{Z}$) and $a,b\in\mathbb{N}$.',
             [EX('$p(u) =$', 4 * u ** 3 - 4 * u, vars=('u',)), N('$a =$', 1), N('$b =$', 3)], 6, 'substitution', r'$u = \sqrt{1 + \frac12x^2}$: $2u\,du = x\,dx$ and $x^2 = 2(u^2 - 1)$.',
             [r'$2u\,du = x\,dx$, $x^2 = 2(u^2-1)$; bounds $u(0) = 1$, $u(4) = 3$.', r'$\int_1^3e^{-u}\cdot2(u^2-1)\cdot2u\,du = \int_1^3e^{-u}(4u^3 - 4u)\,du$.']),
        item('(b)', r'Determine $$\int\frac{2x^2-x+7}{(x+1)(x^2-2x+2)}\,dx=\int\frac{A}{x+1}+\frac{Bx+D}{x^2-2x+2}\,dx=A\ln|x+1|+D\arctan(x+E)+C$$ with $C$ the unspecified constant of integration and $A,B,D,E\in\mathbb{Z}$. [Hint: $\arctan(x)^{\prime}=\frac{1}{1+x^2}$.]',
             [N('$A =$', 2), N('$B =$', 0), N('$D =$', 3), N('$E =$', -1)], 6, 'partial-fractions',
             r'Substitute $x = -1, 0, 1$ in $2x^2 - x + 7 = A(x^2-2x+2) + (Bx+D)(x+1)$; then $x^2 - 2x + 2 = (x-1)^2 + 1$.',
             [r'$x = -1$: $A = 2$; $x = 0$: $D = 3$; $x = 1$: $B = 0$.', r'$\int\frac{2}{x+1} + \frac{3}{(x-1)^2+1}dx = 2\ln|x+1| + 3\arctan(x-1) + C$: $E = -1$.']),
        item('(c)', r'Compute the *limit for the sum* of the following series $$\frac{1}{n^2}e^{\frac1n}+\frac{2}{n^2}e^{\frac2n}+\frac{3}{n^2}e^{\frac3n}+\cdots+\frac1ne^1$$ when $n$ goes to infinity.', [N('Limit:', 1)], 6, 'riemann',
             r'$\frac{r}{n^2}e^{r/n} = \frac1n\cdot\frac rne^{r/n}$.', [r'$\int_0^1xe^xdx = (x-1)e^x\big|_0^1 = 1$.']),
    ]))
    qs.append(question('6', 6, r'Consider the *area between the curves* $y^2=bx$ and $x^2=by$.', [
        item('(a)', r'At which values of $x$ do the curves intersect?', [STV('Intersection $x$-values:', [0, b], ('b',), {'b': [1, 5]})], 2, 'area', r'Use the upper branch $y = \sqrt{bx}$ and $y = \frac1bx^2$.',
             [r'$\frac1bx^2 = \sqrt b\sqrt x \iff \sqrt x(x\sqrt x - b\sqrt b) = 0$.', r'$x = 0$ and $x = b$.']),
        item('(b)', r'If the area between $y^2=bx$ and $x^2=by$ is $27$, then what is the value of $b\in\mathbb{N}$?', [N('$b =$', 9)], 4, 'area', r'Area $= \int_0^b\left(\sqrt{bx} - \frac1bx^2\right)dx$.',
             [r'$\int_0^b\sqrt b\sqrt x - \frac1bx^2\,dx = \frac23b^2 - \frac13b^2 = \frac13b^2$.', r'$\frac13b^2 = 27 \Rightarrow b = 9$.']),
    ]))
    qs.append(question('7', 6, r'A *continuous probability distribution* has the following probability density function (pdf) on the real line: $$p(x)=A\cdot\frac{e^x}{(1+e^x)^2}.$$', [
        item('(a)', r'Find the constant $A\in\mathbb{N}$ such that the probability distribution function is properly normalized.', [N('$A =$', 1)], 2, 'continuous', r'$u = 1 + e^x$, $du = e^x dx$; the bounds become $1$ and $\infty$.', [r'$\int_1^\infty\frac{A}{u^2}du = A\left[-\frac1u\right]_1^\infty = A = 1$.']),
        item('(b)', r'Let $F(x)=\int_{-\infty}^xp(t)\,dt$ be the cumulative distribution function (cdf) of this distribution. Find the constant $B\in\mathbb{N}$ such that $F(\ln B)-F(-\ln B)=\frac13$.', [N('$B =$', 2)], 2, 'continuous',
             r'$F(\ln B) - F(-\ln B) = \int_{-\ln B}^{\ln B}p(x)\,dx$; substitute $u = 1 + e^x$.', [r'$\left[-\frac1u\right]_{1 + 1/B}^{1 + B} = -\frac{1}{1+B} + \frac{B}{1+B} = \frac{B-1}{B+1} = \frac13 \Rightarrow B = 2$.']),
        item('(c)', r'Consider a random variable $X$ that follows the distribution specified above. Compute the expected value $E(X)$ of this random variable. **Hint:** Use the fact that $p(x)=p(-x)\ \forall x\in\mathbb{R}$.', [N('$E(X) =$', 0)], 2, 'continuous',
             r'$x\cdot p(x)$ is an odd function.', [r'$p$ is even, so $x\,p(x)$ is odd and its integral over $\mathbb{R}$ is $0$ (the official solution also verifies this with the substitution $u = 1 + e^x$).']),
    ]))
    qs.append(question('8', 6, r'Suppose that you have a jar with 4 fair coins and 1 unfair coin (which has heads on both sides). You choose one of the 5 coins at random and then *flip the chosen coin* four times. The flips are independent trials.', [
        item('(a)', r'What is the probability of getting heads for all four flips (that is, the event HHHH)?', [NP('$P(HHHH) =$', R(1, 4))], 3, 'conditional', r'Total probability over fair/unfair coin.', [r'$P = \frac1{2^4}\cdot\frac45 + 1\cdot\frac15 = \frac1{20} + \frac15 = \frac14$.']),
        item('(b)', r'Given that all four flips resulted in heads (the event HHHH), what is the probability that you chose the unfair coin?', [NP(r'$P(\text{unfair}\mid HHHH) =$', R(4, 5))], 3, 'conditional', r'Bayes with the result of (a).', [r'$\frac{1\cdot\frac15}{\frac14} = \frac45$.']),
    ]))
    return exam('2025-2', year='2025–2026', sitting=2, kind='Resit', date='January 12, 2025', iso='2026-01-12', minutes=180,
                file='calc-exam-2025-02', instructions=RESIT_2025, questions=qs,
                note='The paper is dated “January 12, 2025”; as the resit of the October 2025 exam it is listed after it.')


EXAMS = [exam_2021_1, exam_2021_2, exam_2022_1, exam_2022_2, exam_2023_1, exam_2023_2, exam_2024_1, exam_2024_2, exam_2025_1, exam_2025_2]


# =====================================================================================
def verify():
    """Independent SymPy checks of the answers that can be computed."""
    X = x
    ck = []
    A_, B_, C_ = 1, -1, 3
    ck.append(sp.limit((A_ * pi * tan(pi * X) + B_ * pi ** 2 * log(X) + C_ * cos(pi * X) + 3) / (pi ** 2 * (X - 1) ** 2), X, 1) == 2)
    ck.append(sp.simplify(integrate((9 * X ** 2 + 4 * X + 5) / ((1 + X) * (1 + X ** 2)), (X, 0, 1)) - 7 * log(2)) == 0)
    ck.append(sp.simplify(integrate((4 ** 2 + 2 * 4) / ((4 + 2 * sqrt(X)) ** 2 * sqrt(X)), (X, 1, 4)) - 1) == 0)
    ck.append(sp.simplify(pi * integrate(5 * X ** R(2, 3), (X, 0, 8)) - pi * R(9, 16) * integrate(X ** 2, (X, 0, 8))) == 0)
    ck.append(sp.limit(X ** 2 * log(6 * X ** 2), X, 0) == 0)
    ck.append(sp.limit((8 * X - 8 * sqrt(3 * X + 4)) / (X - 4), X, 4) == 5)
    ck.append(sp.simplify(integrate(u ** 2 * sin(u), u) - (2 * u * sin(u) + (2 - u ** 2) * cos(u))) == 0)
    ck.append(sp.simplify(integrate(u ** 2 * sin(u), (u, 0, pi)) - (pi ** 2 - 4)) == 0)
    # 2021-2
    ck.append(sp.limit((5 * X ** X + 4 * log(X) - 3 * X ** 3 - 2) / (X - 1) ** 2, X, 1) == -6)
    num = 2 * X ** 5 + 4 * X ** 4 + 10 * X ** 3 + 22 * X ** 2 + 4 * X + 5
    ck.append(sp.simplify(num / ((X + 1) ** 2 * (X ** 2 + 4)) - (2 * X - 2 / (X + 1) + 3 / (X + 1) ** 2 + (2 * X + 1) / (X ** 2 + 4))) == 0)
    ck.append(sp.simplify(integrate(X ** 3 / 4, (X, 0, 2)) - 1) == 0)
    ck.append(sum(2 ** i for i in range(1, 7)) / 6 == 21 and all(sum(2 ** i for i in range(1, k + 1)) / k < 21 for k in range(1, 6)))
    ck.append(sp.simplify(diff(R(1, 2) * (exp(yx) - exp(-yx)) * sin(X), yx, X).subs({X: pi, yx: log(2)}) + R(5, 4)) == 0)
    ck.append(sp.simplify(integrate(X ** 2 * cos(4 * X), (X, 0, pi)) / pi - R(1, 8)) == 0)
    ck.append(sp.simplify(diff((X ** 2 / 4 - R(1, 32)) * sin(4 * X) + X / 8 * cos(4 * X), X) - X ** 2 * cos(4 * X)) == 0)
    ck.append(sp.limit((X ** 3 - 7 * X + 6) / (X ** 2 - 1), X, 1) == -2)
    ck.append(sp.limit((exp(X) + X) ** (1 / X), X, oo) == E)
    # 2022-1
    F1 = yx * (-X ** 2 - yx ** 2 + 1) - R(4, 25)
    m1 = (-diff(F1, X) / diff(F1, yx)).subs({X: R(2, 5), yx: R(1, 5)})
    ck.append(F1.subs({X: R(2, 5), yx: R(1, 5)}) == 0 and m1 == R(2, 9) and R(1, 5) - m1 * R(2, 5) == R(1, 9))
    ck.append(sp.simplify(integrate(1 / (2 + X), (X, 0, 4)) - log(3)) == 0)
    ck.append(sp.simplify((7 * X ** 2 - 2 * X + 1) / (X ** 3 - X ** 2 + X - 1) - 3 / (X - 1) - (4 * X + 2) / (X ** 2 + 1)) == 0)
    ck.append(sp.limit((1 + 2 * X) ** (1 / (3 * X)), X, 0) == exp(R(2, 3)))
    ck.append(abs(val(integrate(8 * exp(-sqrt(1 + 2 * X ** 2)) * X ** 5, (X, 0, 2))) - val(integrate(exp(-u) * (u ** 5 - 2 * u ** 3 + u), (u, 1, 3)))) < 1e-9)
    Ap, ap, bp = sp.symbols('A a b', positive=True)
    xx = sp.Symbol('xx', positive=True)
    board = (xx + 2 * bp) * (Ap / xx + 2 * ap)
    ck.append(sp.simplify(sp.solve(diff(board, xx), xx)[0] - sqrt(bp * Ap / ap)) == 0)
    ck.append(sp.Rational(200, 8) - 12 * R(3, 8) - 24 * R(3, 8) - 36 * R(1, 8) == 7)
    f11 = (X ** (2 * yx) + (yx - 1) * (yx - 2) * (yx - 3)) / E
    ck.append(sp.simplify(diff(f11, yx, X).subs({X: E, yx: 1})) == 6)
    # 2022-2
    ck.append(sp.limit((R(-12, 5) * log(X / 2) + R(2, 5) * (X - 1) ** 2 - R(2, 5) * exp(2 - X)) / (2 - X) ** 2, X, 2) == R(1, 2))
    ck.append(sp.simplify(integrate(1 / sqrt(1 + X), (X, 0, 8)) - 4) == 0)
    ck.append(sp.simplify(integrate(R(3, 8) * X * sqrt(4 - X ** 2), (X, 0, 2)) - 1) == 0)
    T, Xv, Yv = sp.symbols('T X Y', real=True)
    f3 = T * exp(-T) * sin(Xv - Yv) + exp(-2 * T) * cos(Xv + Yv)
    ck.append(sp.simplify(diff(f3, T, Xv, Yv).subs({T: 0, Xv: pi, Yv: pi})) == 2)
    ck.append(sp.limit((sqrt(X + 2) - 2) / (sqrt(X + 7) - 3), X, 2) == R(3, 2))
    ck.append(sp.limit(sqrt((X ** 3 - 2 * X) / (4 * X + 2)) / X, X, oo) == R(1, 2) and sp.limit(sqrt((X ** 3 - 2 * X) / (4 * X + 2)) / X, X, -oo) == R(-1, 2))
    # 2023-1
    F23 = X * (1 - X ** 2 - yx ** 2) - 1
    m23 = (-diff(F23, X) / diff(F23, yx)).subs({X: -1, yx: 1})
    ck.append(F23.subs({X: -1, yx: 1}) == 0 and m23 == R(3, 2))
    ck.append(sp.simplify(integrate(2 * X - (-8 * X ** 3 + 16 * X ** 2 - 6 * X), (X, 0, 1)) - R(2, 3)) == 0)
    ck.append(sp.simplify(integrate(X * exp(X), (X, 0, 1)) - 1) == 0)
    ck.append(sp.simplify(integrate(X * R(8, 3) * (1 - 8 * X ** 3), (X, 0, R(1, 2))) - R(1, 5)) == 0)
    ck.append(sp.limit((X / pi) ** (1 / sin(X)), X, pi) == exp(-1 / pi))
    ck.append(sp.solve(diff(sqrt(X) / (1 + 7 * X), X), X) == [R(1, 7)])
    # 2023-2
    ck.append(sp.limit(sqrt(X ** 2 - 2 * X) - sqrt(X ** 2 - 5 * X), X, oo) == R(3, 2))
    ck.append(sp.simplify(diff(b / (a ** 2 + b ** 2) * sin(a * X) * exp(b * X) - a / (a ** 2 + b ** 2) * cos(a * X) * exp(b * X), X) - sin(a * X) * exp(b * X)) == 0)
    ck.append(sp.simplify(diff(a / (a ** 2 + b ** 2) * sin(a * X) * exp(b * X) + b / (a ** 2 + b ** 2) * cos(a * X) * exp(b * X), X) - cos(a * X) * exp(b * X)) == 0)
    Aar = (2 * X + 3) * (R(9, 4) - X ** 2) / 2
    ck.append(R(1, 2) in sp.solve(diff(Aar, X), X) and Aar.subs(X, R(1, 2)) == 4)
    G6 = X ** 2 + yx ** 2 - (2 * X ** 2 + 2 * yx ** 2 - X) ** 2
    ck.append(G6.subs({X: 0, yx: R(1, 2)}) == 0 and (-diff(G6, X) / diff(G6, yx)).subs({X: 0, yx: R(1, 2)}) == 1)
    ck.append(sp.simplify(integrate((3 * X ** 2 + 2 * X + 1) / ((X + 1) * (X ** 2 + 1)), (X, 0, 1)) - log(4)) == 0)
    ck.append(sp.factor(diff((X ** 2 + 2 * X - 1) * exp(-X), X, 2)) == sp.factor((X - 3) * (X + 1) * exp(-X)))
    nn, mm = sp.symbols('nn mm', positive=True)
    fq9 = (sqrt(X) + X ** 2) / (nn * X + mm)
    ck.append(sp.simplify(sp.limit(fq9 / X, X, oo) - 1 / nn) == 0 and sp.simplify(sp.limit(fq9 - X / nn, X, oo) + mm / nn ** 2) == 0)
    # 2024-1
    G1 = 2 * X ** 2 - 4 * X - X * yx + yx ** 2 + 1
    sl = -diff(G1, X) / diff(G1, yx)
    ck.append(G1.subs({X: R(1, 2), yx: 1}) == 0 and G1.subs({X: R(1, 2), yx: R(-1, 2)}) == 0 and sl.subs({X: R(1, 2), yx: 1}) == 2 and sl.subs({X: R(1, 2), yx: R(-1, 2)}) == -1)
    ck.append(integrate(-X ** 2 + 5 - (X - 1) ** 2, (X, -1, 2)) == 9)
    ck.append(sp.simplify(integrate(X / sqrt(X - 1), (X, 10, 37)) - 132) == 0)
    ck.append(sp.factor(diff((-X ** 2 + 3 * X - 2) * exp(X), X, 2)) == sp.factor(-(X + 2) * (X - 1) * exp(X)))
    ck.append(sp.limit(10 / log(10 * X + 1) - 1 / X, X, 0) == 5)
    ck.append(sp.factor(X ** 4 + 2 * X ** 3 + 2 * X ** 2 + 2 * X + 1) == (X + 1) ** 2 * (X ** 2 + 1))
    ck.append(sp.simplify(integrate(R(1, 2) / pi * X * sin(X), (X, -pi, pi)) - 1) == 0)
    ck.append(sp.simplify(integrate(X * 3 * (1 - 4 * X ** 2), (X, 0, R(1, 2))) - R(3, 16)) == 0)
    ck.append(integrate(3 * X ** 2 / (X ** 3 + 1) ** 2, (X, 0, oo)) == 1)
    # 2024-2
    ck.append(sp.simplify(R(1, 3) * (integrate(X, (X, 1, 2)) + integrate(2 * X, (X, 2, 3))) - R(13, 6)) == 0)
    ck.append(sp.simplify(sp.limit((R(1, 2) * X + 2) ** 3 - 8 - 6 * sin(X), X, 0)) == 0 and sp.limit(((R(1, 2) * X + 2) ** 3 - 8 - 6 * sin(X)) / (1 - cos(X)), X, 0) == 3)
    ck.append(sp.simplify(diff(sin(2 * X) * exp(4 * X) / 5 - cos(2 * X) * exp(4 * X) / 10, X) - sin(2 * X) * exp(4 * X)) == 0)
    ck.append(sp.simplify(integrate(2 * X * log(1 + X ** 2), (X, 0, 1)) - (2 * log(2) - 1)) == 0)
    dq5 = diff(fq5_(), X) - fq5_() * (X / (X ** 2 - 2) - 1 / (2 * (X - 2)) + R(1, 2))
    ck.append(all(abs(val(dq5.subs(X, v))) < 1e-9 for v in (R(5, 2), 3, R(7, 2), 5)))
    aa, bb = sp.symbols('aa bb', positive=True)
    ck.append(sp.simplify(integrate(12 / (bb - aa) ** 3 * (X - (aa + bb) / 2) ** 2, (X, aa, bb)) - 1) == 0)
    ck.append(sp.simplify(integrate(X * 12 / (bb - aa) ** 3 * (X - (aa + bb) / 2) ** 2, (X, aa, bb)) - (aa + bb) / 2) == 0)
    G2 = 3 * X ** 2 - 3 * X ** 2 * yx + yx ** 2 - 3
    ck.append(G2.subs({X: 1, yx: 3}) == 0 and (-diff(G2, X) / diff(G2, yx)).subs({X: 1, yx: 3}) == 4 and 3 - 4 * 1 == -1)
    # 2025-1
    ck.append(sp.solve(sp.factor(diff(X ** 4 - 4 * X ** 3 - 18 * X ** 2 + 15, X, 2)), X) == [-1, 3])
    ck.append(sp.simplify(diff((X - yx) ** 3 * log(X - yx), yx, X) - (X - yx) * (-6 * log(X - yx) - 5)) == 0)
    G3 = yx ** 2 - X ** 2 * yx + X - 1
    ck.append(G3.subs({X: -1, yx: -1}) == 0 and (-diff(G3, X) / diff(G3, yx)).subs({X: -1, yx: -1}) == R(-1, 3))
    ck.append(sp.limit((exp(3 * X) - 2 * X - 1) / X, X, 0) == 1)
    gq = (exp(3 * X) - 2 * X - 1) / X
    ck.append(sp.limit(diff(gq, X), X, 0) == R(9, 2))
    ck.append(sp.simplify(diff(R(1, 20) * sqrt(2 * X + 1) ** 5, X) - (X ** 2 + X + R(1, 4)) / sqrt(2 * X + 1)) == 0)
    ck.append(sp.simplify((5 * X ** 2 + 7 * X + 3) / ((X + 1) * (X ** 2 + X + 1)) - 1 / (X + 1) - (4 * X + 2) / (X ** 2 + X + 1)) == 0)
    ck.append(sp.simplify(diff(2 * atan(X - R(3, 4)), X) - 32 / (16 * X ** 2 - 24 * X + 25)) == 0)
    ck.append(sp.limit(sqrt(9 * X ** 2 + 11 * X - 7) / sqrt(abs(2 * X + 5) + 4 * X ** 2 - 2 * X - 13), X, oo) == R(3, 2))
    ck.append(sp.limit((1 + sin(X)) ** (R(2, 3) / sin(X)), X, 0, '-') == exp(R(2, 3)) and sp.limit(tan(2 * X) / tan(3 * X), X, 0) == R(2, 3))
    ck.append(sp.simplify(integrate(sqrt(X), (X, 0, 9)) - integrate(X / 2 - R(3, 2), (X, 3, 9)) - 9) == 0)
    tq = sp.Symbol('t', positive=True)
    ck.append(integrate(tq / 4 * exp(-tq / 4), (tq, 0, oo)) == 4)
    # 2025-2
    lim3 = ((6) ** X - 2 ** X - 3 ** X + 1) / (X * tan(X))
    ck.append(abs(val(lim3.subs(X, R(1, 10 ** 5))) - val(log(2) * log(3))) < 1e-4)
    G4 = yx + X ** 2 * yx - 5
    ck.append(G4.subs({X: -2, yx: 1}) == 0 and (-diff(G4, X) / diff(G4, yx)).subs({X: -2, yx: 1}) == R(4, 5))
    ck.append(abs(val(integrate(exp(-sqrt(1 + X ** 2 / 2)) * X ** 3, (X, 0, 4))) - val(integrate(exp(-u) * (4 * u ** 3 - 4 * u), (u, 1, 3)))) < 1e-9)
    ck.append(sp.simplify((2 * X ** 2 - X + 7) / ((X + 1) * (X ** 2 - 2 * X + 2)) - 2 / (X + 1) - 3 / ((X - 1) ** 2 + 1)) == 0)
    bpos = sp.Symbol('bpos', positive=True)
    ck.append(sp.simplify(integrate(sqrt(bpos * X) - X ** 2 / bpos, (X, 0, bpos)) - bpos ** 2 / 3) == 0)
    ck.append(integrate(exp(X) / (1 + exp(X)) ** 2, (X, -oo, oo)) == 1)
    ck.append(sp.simplify(integrate(exp(X) / (1 + exp(X)) ** 2, (X, -log(2), log(2))) - R(1, 3)) == 0)
    ck.append(R(1, 16) * R(4, 5) + R(1, 5) == R(1, 4))
    ck.append(sp.simplify(diff(R(2, 5) * (X + 1) ** R(5, 2) - R(2, 3) * (X + 1) ** R(3, 2), X) - X * sqrt(X + 1)) == 0)
    ck.append(integrate(X ** R(-1, 3), (X, 0, 8)) == 6)
    ck.append(sp.simplify(diff(a * X * yx / (X + yx), yx, X) - 2 * a * X * yx / (X + yx) ** 3) == 0)
    bad = [i for i, c in enumerate(ck) if not bool(c)]
    assert not bad, 'SymPy verification failed for checks %s' % bad
    return len(ck)


def fq5_():
    return sqrt((x ** 2 - 2) / (x - 2) * exp(x))


def main(site):
    n_checks = verify()
    exams = [f() for f in EXAMS]
    idx = write(exams, os.path.join(site, 'data', 'past-exams'))
    for e in idx:
        print('%-7s %-22s %3d min %2d questions %2d items' % (e['id'], e['date'], e['minutes'], e['questions'], e['items']))
    print('SymPy checks passed:', n_checks)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
