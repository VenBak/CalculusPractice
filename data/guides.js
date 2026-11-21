/*
 * Refresher guides — one per topic: the idea, the key rules, a worked example and common mistakes.
 * Written in HTML with LaTeX between $…$ (rendered by KaTeX). String.raw keeps the backslashes intact.
 */
window.CalcGuides = {

'domain-range': {
  title: 'Domain & range',
  idea: String.raw`<p>The <strong>domain</strong> $D_f$ is the largest set of real $x$ for which the formula makes sense; the <strong>range</strong> $R(f)$ is the set of all values $f(x)$ that actually occur. For the domain you collect every restriction and intersect them; for the range you follow the building blocks.</p>`,
  rules: [
    String.raw`Fraction: denominator $\neq 0$.`,
    String.raw`Even root $\sqrt{g(x)}$: $g(x) \ge 0$ — but $> 0$ if the root is in a denominator.`,
    String.raw`Logarithm $\ln(g(x))$: $g(x) > 0$ (strictly).`,
    String.raw`Solve inequalities with a <em>sign chart</em>: mark the zeros of numerator and denominator, test the sign on each piece.`,
    String.raw`Basic ranges: $x^2 \in [0,\infty)$, $e^x \in (0,\infty)$, $\ln x \in \mathbb{R}$, $\sin x, \cos x \in [-1,1]$, $\arctan x \in (-\tfrac\pi2, \tfrac\pi2)$.`,
    String.raw`A shift $+c$ moves the range by $c$; multiplying by a negative number flips it. Check whether endpoints are <em>reached</em> (closed bracket) or only approached (open bracket).`,
    String.raw`For $\frac{ax+b}{cx+d}$ the range is $\mathbb{R}\setminus\{\frac ac\}$ (the horizontal asymptote value is never attained).`
  ],
  example: {
    question: String.raw`Find the domain of $f(x) = \dfrac{\sqrt{1-x}}{x^2-x-6}$.`,
    steps: [
      String.raw`Root: $1 - x \ge 0 \iff x \le 1$.`,
      String.raw`Denominator: $x^2 - x - 6 = (x-3)(x+2) \neq 0$, so $x \neq 3$ and $x \neq -2$.`,
      String.raw`Only $-2$ lies in $(-\infty, 1]$; $3$ is already excluded by the root.`,
      String.raw`$D_f = (-\infty,-2)\cup(-2,1]$ — note that $x = 1$ is included ($\sqrt0 = 0$ is fine).`
    ]
  },
  pitfalls: [
    String.raw`Forgetting to check whether an endpoint is included ($\ge$ versus $>$).`,
    String.raw`Removing a point that the other condition already excludes, or forgetting the denominator altogether.`,
    String.raw`For ranges: claiming a horizontal asymptote value is reached.`
  ]
},

'inverse': {
  title: 'Inverse functions',
  idea: String.raw`<p>An injective (one-to-one) function $f$ has an inverse $f^{-1}$ with $f^{-1}(f(x)) = x$. To find it, write $y = f(x)$, solve for $x$, and then rename the variables. The domain of $f^{-1}$ is the range of $f$.</p>`,
  rules: [
    String.raw`Recipe: $y = f(x)$ $\;\to\;$ isolate $x$ $\;\to\;$ swap $x \leftrightarrow y$.`,
    String.raw`Undo operations in reverse order: subtract/add, divide/multiply, then apply the inverse function ($e^{(\cdot)} \leftrightarrow \ln$, $(\cdot)^3 \leftrightarrow \sqrt[3]{\cdot}$).`,
    String.raw`For $y = \frac{ax+b}{cx+d}$: cross-multiply, collect the $x$-terms on one side and factor out $x$.`,
    String.raw`$D(f^{-1}) = R(f)$ and $R(f^{-1}) = D(f)$.`,
    String.raw`Derivative of the inverse: $(f^{-1})^{\prime}(y_0) = \dfrac{1}{f^{\prime}(x_0)}$ where $f(x_0) = y_0$.`,
    String.raw`A function commutes with its inverse: $f(f^{-1}(x)) = f^{-1}(f(x)) = x$.`
  ],
  example: {
    question: String.raw`Find the inverse of $f(x) = \dfrac{x+5}{2x-1}$.`,
    steps: [
      String.raw`$y = \frac{x+5}{2x-1} \Rightarrow y(2x-1) = x + 5 \Rightarrow 2xy - y = x + 5$.`,
      String.raw`Collect $x$: $2xy - x = y + 5 \Rightarrow x(2y - 1) = y + 5 \Rightarrow x = \frac{y+5}{2y-1}$.`,
      String.raw`Swap names: $f^{-1}(x) = \dfrac{x+5}{2x-1}$ (this $f$ is its own inverse), defined for $x \neq \frac12$.`
    ]
  },
  pitfalls: [
    String.raw`Confusing $f^{-1}(x)$ with $\frac{1}{f(x)}$.`,
    String.raw`Sign errors when moving the $x$-terms to one side.`,
    String.raw`Forgetting that the domain of the inverse is the range of $f$.`
  ]
},

'even-odd': {
  title: 'Even & odd functions',
  idea: String.raw`<p>$f$ is <strong>even</strong> if $f(-x) = f(x)$ (mirror symmetric in the $y$-axis) and <strong>odd</strong> if $f(-x) = -f(x)$ (point symmetric in the origin), for all $x$ in a symmetric domain. Most functions are neither. Always test by computing $f(-x)$.</p>`,
  rules: [
    String.raw`Even: $x^2, x^4, |x|, \cos x, e^{-x^2}$. Odd: $x, x^3, \sin x, \tan x, \arctan x$. Neither: $e^x$, $x + 1$, $\ln x$.`,
    String.raw`Products/quotients: even·even = even, odd·odd = even, even·odd = odd.`,
    String.raw`Sums: even + even = even, odd + odd = odd, even + odd = neither (unless one is $0$).`,
    String.raw`Composition $f\circ g$: if the inner $g$ is even, $f\circ g$ is even. If $g$ is odd, $f\circ g$ has the parity of $f$.`,
    String.raw`Derivatives swap parity: $f$ odd $\Rightarrow f^{\prime}$ even; $f$ even $\Rightarrow f^{\prime}$ odd.`,
    String.raw`Integrals: $f$ odd $\Rightarrow \int_{-a}^a f = 0$; $f$ even $\Rightarrow \int_{-a}^a f = 2\int_0^a f$.`
  ],
  example: {
    question: String.raw`Let $f$ be odd and $g$ even. What is the parity of $f\circ g$ and $g\circ f$?`,
    steps: [
      String.raw`$(f\circ g)(-x) = f(g(-x)) = f(g(x)) = (f\circ g)(x)$: even.`,
      String.raw`$(g\circ f)(-x) = g(f(-x)) = g(-f(x)) = g(f(x)) = (g\circ f)(x)$: even.`
    ]
  },
  pitfalls: [
    String.raw`Concluding "odd" because $f(-1) = -f(1)$ at a single point — the identity must hold for all $x$.`,
    String.raw`Forgetting the zero function is both even and odd.`,
    String.raw`Applying the rules for products to sums.`
  ]
},

'limits': {
  title: 'Limits',
  idea: String.raw`<p>$\lim_{x\to a} f(x)$ is the value $f(x)$ approaches as $x$ gets close to $a$ (not necessarily $f(a)$). First substitute; if you get a determinate number you are done. If you get an indeterminate form like $\tfrac00$ or $\tfrac\infty\infty$, simplify first.</p>`,
  rules: [
    String.raw`$\tfrac00$ with polynomials: factor and cancel the common factor.`,
    String.raw`Square roots: multiply numerator and denominator by the <em>conjugate</em> $(\sqrt A + B)$, using $(\sqrt A - B)(\sqrt A + B) = A - B^2$.`,
    String.raw`$x\to\pm\infty$ with fractions: divide numerator and denominator by the highest power in the denominator.`,
    String.raw`Standard limit: $\lim_{u\to0}\frac{\sin u}{u} = 1$ (also for $\tan$).`,
    String.raw`Squeeze theorem: if $g \le f \le h$ and $g, h \to L$, then $f \to L$. Typical with $-1 \le \sin(\cdot) \le 1$.`,
    String.raw`One-sided limits: the limit exists exactly when $\lim_{x\to a^-} = \lim_{x\to a^+}$.`,
    String.raw`The sum rule $\lim(f+g) = \lim f + \lim g$ only holds when both limits exist.`
  ],
  example: {
    question: String.raw`Compute $\displaystyle\lim_{t\to4}\frac{8t - 8\sqrt{3t+4}}{t-4}$.`,
    steps: [
      String.raw`Substituting gives $\tfrac{32 - 32}{0} = \tfrac00$.`,
      String.raw`Multiply by the conjugate: $8\cdot\dfrac{(t - \sqrt{3t+4})(t + \sqrt{3t+4})}{(t-4)(t+\sqrt{3t+4})} = 8\cdot\dfrac{t^2 - 3t - 4}{(t-4)(t+\sqrt{3t+4})}$.`,
      String.raw`Factor $t^2 - 3t - 4 = (t-4)(t+1)$ and cancel: $8\cdot\dfrac{t+1}{t+\sqrt{3t+4}}$.`,
      String.raw`Substitute $t = 4$: $8\cdot\frac58 = 5$.`
    ]
  },
  pitfalls: [
    String.raw`Writing "$= \tfrac00$" as an answer — it is a signal to simplify.`,
    String.raw`For $x\to-\infty$ with roots: $\sqrt{x^2} = |x| = -x$.`,
    String.raw`Splitting a limit into pieces that do not exist separately.`
  ]
},

'asymptotes': {
  title: 'Asymptotes',
  idea: String.raw`<p>An asymptote is a line the graph approaches. <strong>Vertical</strong> $x = a$: $f(x)\to\pm\infty$ as $x\to a$. <strong>Horizontal</strong> $y = L$: $f(x)\to L$ as $x\to\pm\infty$. <strong>Slant</strong> $y = ax + b$: $f(x) - (ax+b)\to0$ as $x\to\pm\infty$.</p>`,
  rules: [
    String.raw`Vertical: zeros of the denominator that do <em>not</em> cancel against the numerator (a cancelled factor gives a hole).`,
    String.raw`Rational function, degree numerator $<$ degree denominator: $y = 0$. Equal degrees: $y = $ ratio of leading coefficients. One degree higher: slant asymptote = quotient of the long division.`,
    String.raw`General slant asymptote: $a = \lim\frac{f(x)}{x}$, $b = \lim\big(f(x) - ax\big)$ — compute separately for $+\infty$ and $-\infty$.`,
    String.raw`$e^x\to0$ as $x\to-\infty$; divide by $e^x$ when $x\to+\infty$.`,
    String.raw`Only count vertical asymptotes inside the domain; and only check the infinite ends that belong to the domain.`,
    String.raw`If the asymptote at $+\infty$ equals the one at $-\infty$ it counts once.`
  ],
  example: {
    question: String.raw`Find the slant asymptote of $f(x) = \dfrac{2(x-2)(x+2)}{x-3}$.`,
    steps: [
      String.raw`Expand: $2(x^2 - 4) = 2x^2 - 8$.`,
      String.raw`Long division: $\dfrac{2x^2 - 8}{x - 3} = 2x + 6 + \dfrac{10}{x-3}$.`,
      String.raw`The remainder tends to $0$, so the slant asymptote is $y = 2x + 6 = 2(x+3)$.`
    ]
  },
  pitfalls: [
    String.raw`Counting a hole as a vertical asymptote.`,
    String.raw`Thinking "degree one higher" always gives a slant asymptote — check for cancellation first ($\frac{x^2-x-6}{x+2} = x - 3$ is a line with a hole).`,
    String.raw`Forgetting the sign of $\sqrt{x^2}$ for $x\to-\infty$.`
  ]
},

'continuity': {
  title: 'Continuity',
  idea: String.raw`<p>$f$ is continuous at $a$ when $\lim_{x\to a} f(x) = f(a)$: the limit exists (left = right) and equals the value. Polynomials, roots, $e^x$, $\ln$, trig functions and their combinations are continuous on their domain; problems only occur at break points of piecewise definitions or where a formula is undefined.</p>`,
  rules: [
    String.raw`Piecewise function: match the left limit, the right limit and the value at the break point.`,
    String.raw`Removable discontinuity: define $f(a) = \lim_{x\to a}f(x)$ (compute the limit by factoring or a standard limit).`,
    String.raw`Differentiable at $a$ $\Rightarrow$ continuous at $a$ (not the other way round: $|x|$ at $0$).`,
    String.raw`Differentiability of a piecewise function: continuity <em>and</em> equal one-sided derivatives.`,
    String.raw`One-sided derivative: $\lim_{h\to0^\pm}\frac{f(a+h) - f(a)}{h}$ — use the value $f(a)$ from the piece that contains $a$.`,
    String.raw`Floor $\lfloor\cdot\rfloor$: jumps where the inside crosses an integer; locally constant (derivative $0$) elsewhere.`
  ],
  example: {
    question: String.raw`Find $a, b$ such that $f(x) = x^2$ for $x\le 1$ and $f(x) = ax + b$ for $x > 1$ is differentiable.`,
    steps: [
      String.raw`Continuity at $1$: $1^2 = a + b$.`,
      String.raw`Equal derivatives at $1$: $2\cdot1 = a$, so $a = 2$.`,
      String.raw`Then $b = 1 - 2 = -1$: $f(x) = 2x - 1$ for $x > 1$ (the tangent line at $x=1$).`
    ]
  },
  pitfalls: [
    String.raw`Using the wrong piece for $f(a)$ when computing a one-sided difference quotient.`,
    String.raw`Assuming continuity implies differentiability.`,
    String.raw`Forgetting that a function is only judged on its domain.`
  ]
},

'derivative-rules': {
  title: 'Differentiation rules',
  idea: String.raw`<p>Break the function into simple pieces and combine their derivatives with the sum, product, quotient and chain rules. For functions of the form $u(x)^{v(x)}$ use logarithmic differentiation.</p>`,
  rules: [
    String.raw`Product: $(uv)^{\prime} = u^{\prime}v + uv^{\prime}$. Quotient: $\left(\frac uv\right)^{\prime} = \frac{u^{\prime}v - uv^{\prime}}{v^2}$.`,
    String.raw`Chain: $\big(f(g(x))\big)^{\prime} = f^{\prime}(g(x))\cdot g^{\prime}(x)$.`,
    String.raw`Basics: $(x^n)^{\prime} = nx^{n-1}$, $(e^x)^{\prime} = e^x$, $(a^x)^{\prime} = a^x\ln a$, $(\ln|x|)^{\prime} = \frac1x$, $(\sin x)^{\prime} = \cos x$, $(\cos x)^{\prime} = -\sin x$, $(\tan x)^{\prime} = \frac{1}{\cos^2x}$, $(\arctan x)^{\prime} = \frac{1}{1+x^2}$.`,
    String.raw`Logarithmic differentiation: $f^{\prime} = f\cdot\big(\ln f\big)^{\prime}$. For $f = u^v$: $\ln f = v\ln u$.`,
    String.raw`Products/quotients of many factors are also easier with $\ln$: $\ln\frac{ab}{c} = \ln a + \ln b - \ln c$.`
  ],
  example: {
    question: String.raw`Differentiate $f(x) = (\sin x)^x$.`,
    steps: [
      String.raw`$\ln f = x\ln(\sin x)$.`,
      String.raw`$(\ln f)^{\prime} = \ln(\sin x) + x\cdot\frac{\cos x}{\sin x}$ (product + chain rule).`,
      String.raw`$f^{\prime}(x) = (\sin x)^x\left(\ln(\sin x) + \frac{x\cos x}{\sin x}\right)$.`
    ]
  },
  pitfalls: [
    String.raw`$(x^x)^{\prime} \neq x\cdot x^{x-1}$ — the power rule needs a constant exponent.`,
    String.raw`Forgetting the inner derivative in the chain rule.`,
    String.raw`Sign error in the quotient rule ($u^{\prime}v - uv^{\prime}$, in that order).`
  ]
},

'lhopital': {
  title: "L'Hôpital's rule & indeterminate forms",
  idea: String.raw`<p>If $\lim\frac{f}{g}$ has the form $\tfrac00$ or $\tfrac{\pm\infty}{\pm\infty}$, then $\lim\frac fg = \lim\frac{f^{\prime}}{g^{\prime}}$ (if the latter exists). Differentiate numerator and denominator <em>separately</em>. Other indeterminate forms are first rewritten as a quotient.</p>`,
  rules: [
    String.raw`Check the form before every application; stop as soon as it is no longer indeterminate.`,
    String.raw`$0\cdot\infty$: write $f\cdot g = \dfrac{f}{1/g}$.`,
    String.raw`$\infty - \infty$: combine into one fraction.`,
    String.raw`$1^\infty$, $0^0$, $\infty^0$: compute $\ln L = \lim g\ln f$, then $L = e^{\ln L}$.`,
    String.raw`Standard results: $\lim_{x\to\infty}(1+\frac ax)^{bx} = e^{ab}$, $\lim_{x\to0}\frac{e^x-1}{x} = 1$, $\lim_{x\to0}\frac{\ln(1+x)}{x} = 1$.`,
    String.raw`Unknown constants: if the denominator tends to $0$ and the limit is finite, the numerator must tend to $0$ too — this gives an equation; repeat after each L'Hôpital step.`
  ],
  example: {
    question: String.raw`Compute $L = \displaystyle\lim_{x\to\pi}\left(\frac x\pi\right)^{1/\sin x}$.`,
    steps: [
      String.raw`Form $1^\infty$. Take logs: $\ln L = \lim\dfrac{\ln(x/\pi)}{\sin x}$, form $\tfrac00$.`,
      String.raw`L'Hôpital: $\lim\dfrac{1/x}{\cos x} = \dfrac{1/\pi}{-1} = -\dfrac1\pi$.`,
      String.raw`$L = e^{-1/\pi}$.`
    ]
  },
  pitfalls: [
    String.raw`Using the quotient rule instead of differentiating numerator and denominator separately.`,
    String.raw`Applying the rule to a limit that is not indeterminate (e.g. $\frac{1}{0^+}$).`,
    String.raw`Forgetting to exponentiate back at the end of a $1^\infty$ problem.`
  ]
},

'implicit-tangent': {
  title: 'Implicit differentiation & tangent lines',
  idea: String.raw`<p>When a curve is given by an equation $F(x, y) = 0$, treat $y$ as a function $y(x)$ and differentiate both sides with respect to $x$. Every time you differentiate an expression in $y$, multiply by $y^{\prime}$ (chain rule). Then solve for $y^{\prime}$.</p>`,
  rules: [
    String.raw`$\frac{d}{dx}y^2 = 2yy^{\prime}$, $\frac{d}{dx}(xy) = y + xy^{\prime}$, $\frac{d}{dx}e^{y} = e^{y}y^{\prime}$.`,
    String.raw`Shortcut: $y^{\prime} = -\dfrac{F_x}{F_y}$ (partial derivatives of $F$).`,
    String.raw`Tangent line at $(x_0, y_0)$: $y - y_0 = m(x - x_0)$ with $m = y^{\prime}(x_0, y_0)$; intercept $b = y_0 - m x_0$.`,
    String.raw`For an explicit function: $m = f^{\prime}(a)$, point $(a, f(a))$.`,
    String.raw`Parallel lines have equal slopes; perpendicular slopes multiply to $-1$.`,
    String.raw`Substitute the point <em>before</em> solving for $y^{\prime}$ if the algebra gets messy.`
  ],
  example: {
    question: String.raw`Tangent line to $x(1 - x^2 - y^2) - 1 = 0$ at $(-1, 1)$.`,
    steps: [
      String.raw`Differentiate: $(1 - x^2 - y^2) + x(-2x - 2yy^{\prime}) = 0$, i.e. $(1 - 3x^2 - y^2) - 2xy\,y^{\prime} = 0$.`,
      String.raw`$y^{\prime} = \dfrac{1 - 3x^2 - y^2}{2xy}$; at $(-1,1)$: $\dfrac{-3}{-2} = \dfrac32$.`,
      String.raw`$y - 1 = \frac32(x + 1)$, so $y = \frac32x + \frac52$: $m = \frac32$, $b = \frac52$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting the factor $y^{\prime}$ when differentiating terms in $y$.`,
    String.raw`Forgetting the product rule for mixed terms such as $x^2y$.`,
    String.raw`Using $x_0$ instead of $y_0$ in the intercept formula.`
  ]
},

'partial-derivatives': {
  title: 'Partial derivatives',
  idea: String.raw`<p>For $f(x, y)$, $\frac{\partial f}{\partial x}$ is the derivative with respect to $x$ while $y$ is treated as a <em>constant</em> (and vice versa). Mixed second derivatives are obtained by differentiating twice; for nice functions the order does not matter (Schwarz).</p>`,
  rules: [
    String.raw`$\frac{\partial^2 f}{\partial x\partial y} = \frac{\partial}{\partial x}\left(\frac{\partial f}{\partial y}\right) = \frac{\partial^2 f}{\partial y\partial x}$.`,
    String.raw`All one-variable rules still apply (product, quotient, chain).`,
    String.raw`$x^y = e^{y\ln x}$: $\frac{\partial}{\partial y}x^y = x^y\ln x$ and $\frac{\partial}{\partial x}x^y = yx^{y-1}$.`,
    String.raw`Constant factors like $\frac1e$ simply stay in front.`,
    String.raw`Choose the order that is easiest: a term without $x$ disappears after $\frac{\partial}{\partial x}$.`
  ],
  example: {
    question: String.raw`Compute $\frac{\partial^2}{\partial x\partial y}\frac{x^y}{e}$ at $(e, 2)$.`,
    steps: [
      String.raw`$\frac{\partial}{\partial y}\frac{x^y}{e} = \frac1e\,x^y\ln x$.`,
      String.raw`$\frac{\partial}{\partial x}$: $\frac1e\left(yx^{y-1}\ln x + x^y\cdot\frac1x\right) = \frac1e\,x^{y-1}(y\ln x + 1)$.`,
      String.raw`At $(e,2)$: $\frac1e\cdot e\cdot(2 + 1) = 3$.`
    ]
  },
  pitfalls: [
    String.raw`Treating the other variable as a function instead of a constant.`,
    String.raw`Forgetting the inner derivative, e.g. $\frac{\partial}{\partial y}\ln(x-y) = -\frac{1}{x-y}$.`,
    String.raw`Evaluating at the point before finishing the differentiation.`
  ]
},

'concavity': {
  title: 'Concavity & inflection points',
  idea: String.raw`<p>The sign of $f^{\prime\prime}$ describes the bending of the graph: $f^{\prime\prime} > 0$ convex (concave up, "cup"), $f^{\prime\prime} < 0$ concave (concave down, "cap"). An <strong>inflection point</strong> is a point of the domain where the concavity changes.</p>`,
  rules: [
    String.raw`Compute $f^{\prime\prime}$, factor it, make a sign chart.`,
    String.raw`Inflection point: $f^{\prime\prime}$ changes sign there. $f^{\prime\prime}(a) = 0$ alone is not enough ($x^4$ at $0$).`,
    String.raw`Factors like $e^{\pm x}$ and $(x^2+c)^k$ with $c > 0$ are always positive and do not affect the sign.`,
    String.raw`Second derivative test: $f^{\prime}(a) = 0$ and $f^{\prime\prime}(a) < 0$ $\Rightarrow$ local maximum; $f^{\prime\prime}(a) > 0$ $\Rightarrow$ local minimum.`,
    String.raw`Convex functions have their chords above the graph.`
  ],
  example: {
    question: String.raw`Where is $f(x) = (x^2 + 2x - 1)e^{-x}$ convex or concave?`,
    steps: [
      String.raw`$f^{\prime}(x) = (2x+2)e^{-x} - (x^2+2x-1)e^{-x} = (-x^2 + 3)e^{-x}$.`,
      String.raw`$f^{\prime\prime}(x) = -2xe^{-x} - (-x^2+3)e^{-x} = (x^2 - 2x - 3)e^{-x} = (x-3)(x+1)e^{-x}$.`,
      String.raw`Sign: positive for $x < -1$ and $x > 3$, negative in between.`,
      String.raw`Convex on $(-\infty,-1)\cup(3,\infty)$, concave on $(-1,3)$, inflection points at $x = -1$ and $x = 3$.`
    ]
  },
  pitfalls: [
    String.raw`Calling every zero of $f^{\prime\prime}$ an inflection point.`,
    String.raw`Mixing up convex/concave (convex = holds water = $f^{\prime\prime} > 0$).`,
    String.raw`Counting a point outside the domain (e.g. $x = 0$ for $\frac1x$).`
  ]
},

'function-analysis': {
  title: 'Critical points, monotonicity & extrema',
  idea: String.raw`<p>The derivative tells you where a function increases ($f^{\prime} > 0$) or decreases ($f^{\prime} < 0$). <strong>Critical points</strong> are points of the domain where $f^{\prime} = 0$ or where $f^{\prime}$ does not exist; extrema can only occur there or at endpoints.</p>`,
  rules: [
    String.raw`Write $f^{\prime}$ as one fraction and factor it; read off the zeros and the points where it is undefined.`,
    String.raw`First derivative test: $f^{\prime}$ changes from $+$ to $-$: local max; from $-$ to $+$: local min; no sign change: no extremum.`,
    String.raw`Absolute extrema on $[a,b]$: compare $f$ at the critical points <em>and</em> at the endpoints.`,
    String.raw`Optimisation: express the target quantity in one variable using the constraint, then set the derivative to $0$ and check it is a max/min.`,
    String.raw`Rolle: if $f$ is differentiable and $f(a) = f(b)$, then $f^{\prime}(c) = 0$ for some $c\in(a,b)$.`,
    String.raw`Reading graphs: zeros of $f^{\prime}$ are horizontal tangents of $f$; $f$ must be continuous wherever $f^{\prime}$ exists.`
  ],
  example: {
    question: String.raw`Critical points of $f(x) = \dfrac{\sqrt x}{1+7x}$ on $[0,\infty)$.`,
    steps: [
      String.raw`$f^{\prime}(x) = \dfrac{\frac{1}{2\sqrt x}(1+7x) - 7\sqrt x}{(1+7x)^2}$; multiply numerator and denominator by $2\sqrt x$: $\dfrac{1 - 7x}{2\sqrt x(1+7x)^2}$.`,
      String.raw`$f^{\prime} = 0 \iff x = \frac17$.`,
      String.raw`$f^{\prime}$ does not exist at $x = 0$ (it tends to $\infty$).`,
      String.raw`Critical points: $\{0, \frac17\}$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting points where $f^{\prime}$ does not exist.`,
    String.raw`Forgetting the endpoints when looking for absolute extrema.`,
    String.raw`Not checking that the critical point is actually a maximum in optimisation problems.`
  ]
},

'substitution': {
  title: 'Integration by substitution',
  idea: String.raw`<p>Substitution reverses the chain rule: if the integrand contains an inner function $g(x)$ together with (a multiple of) its derivative $g^{\prime}(x)$, set $u = g(x)$, $du = g^{\prime}(x)\,dx$ and integrate in $u$.</p>`,
  rules: [
    String.raw`$\displaystyle\int f(g(x))g^{\prime}(x)\,dx = \int f(u)\,du$.`,
    String.raw`Definite integrals: change the bounds too, $\displaystyle\int_a^b f(g(x))g^{\prime}(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$.`,
    String.raw`Roots: $u = \sqrt{x^2 + c}$ gives $u^2 = x^2 + c$, so $u\,du = x\,dx$ and $x^2 = u^2 - c$.`,
    String.raw`$u = e^x$: $du = e^x dx$, so $e^{kx}dx = u^{k-1}du$; $x\to-\infty$ becomes $u\to0$.`,
    String.raw`Trig substitution: $\sqrt{a^2 - x^2}$ with $x = a\sin\varphi$ gives $\int\frac{dx}{\sqrt{a^2-x^2}} = \arcsin\frac xa + C$.`,
    String.raw`Improper integrals: integrate up to a bound $R$ and take $\lim_{R\to\infty}$.`
  ],
  example: {
    question: String.raw`Transform $\displaystyle\int_{\sqrt2}^2 x^3\ln\left(1 + \sqrt{x^2+2}\right)dx$ with $u = \sqrt{x^2+2}$.`,
    steps: [
      String.raw`$u^2 = x^2 + 2 \Rightarrow 2u\,du = 2x\,dx \Rightarrow x\,dx = u\,du$, and $x^2 = u^2 - 2$.`,
      String.raw`$x^3\,dx = x^2\cdot x\,dx = (u^2 - 2)\,u\,du$.`,
      String.raw`Bounds: $x = \sqrt2 \mapsto u = 2$, $x = 2 \mapsto u = \sqrt6$.`,
      String.raw`Result: $\displaystyle\int_2^{\sqrt6}(u^3 - 2u)\ln(1+u)\,du$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting to replace $dx$ (or to change the bounds).`,
    String.raw`Leaving a mix of $x$ and $u$ in the integral.`,
    String.raw`$\int\frac1x dx = \ln|x|$ — the absolute value matters.`
  ]
},

'partial-fractions': {
  title: 'Partial fractions',
  idea: String.raw`<p>A rational function $\frac{P(x)}{Q(x)}$ with $\deg P < \deg Q$ can be split into simple fractions that you can integrate directly. If $\deg P \ge \deg Q$, first do polynomial long division.</p>`,
  rules: [
    String.raw`Factor $Q$ completely (try roots like $\pm1, \pm2$; $x^2 - a^2 = (x-a)(x+a)$).`,
    String.raw`Distinct linear factor $(x-a)$: term $\frac{A}{x-a}$.`,
    String.raw`Repeated $(x-a)^k$: terms $\frac{A_1}{x-a} + \dots + \frac{A_k}{(x-a)^k}$.`,
    String.raw`Irreducible quadratic ($b^2 - 4ac < 0$): term $\frac{Bx + C}{ax^2+bx+c}$; repeated: also $\frac{Dx+E}{(ax^2+bx+c)^2}$.`,
    String.raw`Find constants: multiply out and substitute the roots (cover-up), then compare coefficients for the rest.`,
    String.raw`Integrate: $\int\frac{A}{x-a} = A\ln|x-a|$, $\int\frac{2x}{x^2+1} = \ln(x^2+1)$, $\int\frac{1}{(x-p)^2+1} = \arctan(x-p)$.`
  ],
  example: {
    question: String.raw`Decompose $\dfrac{7x^2 - 2x + 1}{x^3 - x^2 + x - 1}$.`,
    steps: [
      String.raw`$x = 1$ is a root: $x^3 - x^2 + x - 1 = (x-1)(x^2+1)$.`,
      String.raw`$7x^2 - 2x + 1 = A(x^2+1) + (Bx + C)(x - 1)$.`,
      String.raw`$x = 1$: $6 = 2A \Rightarrow A = 3$. $x = 0$: $1 = 3 - C \Rightarrow C = 2$. $x = -1$: $10 = 6 + (-B+2)(-2) \Rightarrow B = 4$.`,
      String.raw`So $\dfrac{3}{x-1} + \dfrac{4x+2}{x^2+1}$.`
    ]
  },
  pitfalls: [
    String.raw`Treating $x^2 - 1$ as irreducible.`,
    String.raw`Using a constant numerator over an irreducible quadratic.`,
    String.raw`Skipping the long division when the numerator degree is too high.`
  ]
},

'area': {
  title: 'Area between curves & volumes',
  idea: String.raw`<p>The area between two graphs on $[a,b]$ is $\int_a^b|f(x) - g(x)|\,dx$. In practice: find the intersection points, determine which function lies on top on each piece, and integrate "top minus bottom".</p>`,
  rules: [
    String.raw`Intersections: solve $f(x) = g(x)$; they are usually the bounds.`,
    String.raw`If the curves cross inside the interval, split the integral.`,
    String.raw`Check which is on top with one test value in each piece.`,
    String.raw`Tangent line at $x = p$ through the origin: $l(x) = f^{\prime}(p)x$ with $l(p) = f(p)$.`,
    String.raw`Volume of revolution around the $x$-axis: $V = \pi\int_a^b f(x)^2\,dx$.`,
    String.raw`Geometric shortcuts are allowed: triangles, rectangles and (half) circles.`
  ],
  example: {
    question: String.raw`Area between $f(x) = -x^2 + 5$ and $g(x) = (x-1)^2$.`,
    steps: [
      String.raw`$-x^2 + 5 = x^2 - 2x + 1 \iff 2x^2 - 2x - 4 = 0 \iff x\in\{-1, 2\}$.`,
      String.raw`At $x = 0$: $f = 5 > 1 = g$, so $f$ is on top.`,
      String.raw`$A = \int_{-1}^2(-2x^2 + 2x + 4)\,dx = \left[-\tfrac23x^3 + x^2 + 4x\right]_{-1}^2 = \tfrac{20}{3} - \left(-\tfrac73\right) = 9$.`
    ]
  },
  pitfalls: [
    String.raw`Integrating $f - g$ across a crossing, so parts cancel.`,
    String.raw`Getting a negative "area" and not taking the absolute value.`,
    String.raw`Forgetting to square $f$ (and the factor $\pi$) in volumes.`
  ]
},

'riemann': {
  title: 'Limit of a sum (Riemann sums)',
  idea: String.raw`<p>A sum of the form $\frac1n\sum_{r=1}^n f\left(\frac rn\right)$ is a Riemann sum of $f$ on $[0,1]$ with $n$ strips; as $n\to\infty$ it tends to $\int_0^1 f(x)\,dx$. The trick is to recognise $f$.</p>`,
  rules: [
    String.raw`$\displaystyle\lim_{n\to\infty}\frac1n\sum_{r=1}^n f\!\left(\frac rn\right) = \int_0^1 f(x)\,dx$.`,
    String.raw`Divide numerator and denominator by the right power of $n$ so that only $\frac rn$ appears, plus one factor $\frac1n$.`,
    String.raw`If $r$ runs up to $kn$, $x = \frac rn$ runs up to $k$: $\int_0^k$. If it starts at $mn$: lower bound $m$.`,
    String.raw`Written-out sums: find the general ($r$-th) term first; the last term ($r = n$) tells you the upper bound.`,
    String.raw`Products: take logarithms, $\ln\prod = \sum\ln$.`
  ],
  example: {
    question: String.raw`$\displaystyle\lim_{n\to\infty}\left(\frac{e^{1/n}}{n^2} + \frac{2e^{2/n}}{n^2} + \dots + \frac en\right)$.`,
    steps: [
      String.raw`General term: $\dfrac{re^{r/n}}{n^2} = \dfrac1n\cdot\dfrac rn e^{r/n}$, so $f(x) = xe^x$ (last term $r = n$: $\frac{e}{n}$ ✓).`,
      String.raw`Limit $= \int_0^1 xe^x\,dx$.`,
      String.raw`By parts: $\left[xe^x\right]_0^1 - \int_0^1e^xdx = e - (e - 1) = 1$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting the factor $\frac1n$ (then the limit is not an integral).`,
    String.raw`Wrong bounds when $r$ does not run from $1$ to $n$.`,
    String.raw`Not simplifying $\frac{r}{n^2}$ as $\frac1n\cdot\frac rn$.`
  ]
},

'by-parts': {
  title: 'Integration by parts',
  idea: String.raw`<p>Integration by parts reverses the product rule: $\int f\,g^{\prime} = fg - \int f^{\prime}g$. Choose $f$ as the factor that becomes simpler when differentiated (polynomials, $\ln x$) and $g^{\prime}$ as the factor you can integrate ($e^{kx}$, $\sin$, $\cos$).</p>`,
  rules: [
    String.raw`$\displaystyle\int f g^{\prime}\,dx = fg - \int f^{\prime}g\,dx$; definite: $\displaystyle\int_a^b fg^{\prime} = [fg]_a^b - \int_a^b f^{\prime}g$.`,
    String.raw`Polynomial of degree $n$ times $e^{kx}$/sin/cos: apply the rule $n$ times.`,
    String.raw`$\int\ln x\,dx$: take $f = \ln x$, $g^{\prime} = 1$: result $x\ln x - x$.`,
    String.raw`$e^{bx}\sin(ax)$ or $e^{bx}\cos(ax)$: apply twice; the original integral reappears — move it to the left side and solve.`,
    String.raw`Combine with substitution first when there is an inner function (e.g. $u = e^x$).`
  ],
  example: {
    question: String.raw`Compute $\int u^2\sin u\,du$.`,
    steps: [
      String.raw`$f = u^2$, $g^{\prime} = \sin u$: $-u^2\cos u + 2\int u\cos u\,du$.`,
      String.raw`Again with $f = u$, $g^{\prime} = \cos u$: $\int u\cos u = u\sin u - \int\sin u = u\sin u + \cos u$.`,
      String.raw`Total: $-u^2\cos u + 2u\sin u + 2\cos u + C = 2u\sin u + (2 - u^2)\cos u + C$.`
    ]
  },
  pitfalls: [
    String.raw`Choosing $f = e^x$: the polynomial then grows instead of shrinking.`,
    String.raw`Sign errors with $\int\sin = -\cos$.`,
    String.raw`In cyclic integrals: forgetting to divide by the collected coefficient.`
  ]
},

'discrete': {
  title: 'Discrete probability',
  idea: String.raw`<p>A discrete random variable $X$ takes countably many values $x_i$ with probabilities $P(X = x_i)$ that are $\ge0$ and sum to $1$. The expectation is the probability-weighted average; the variance measures the spread around it.</p>`,
  rules: [
    String.raw`$E(X) = \sum_i x_i\,P(X = x_i)$; $Var(X) = \sum_i P(X=x_i)(x_i - E(X))^2 = E(X^2) - E(X)^2$.`,
    String.raw`Equally likely outcomes: $P(A) = \frac{\#\text{favourable}}{\#\text{possible}}$.`,
    String.raw`Binomial ($n$ independent trials, success probability $p$): $P(X = k) = \binom nk p^k(1-p)^{n-k}$.`,
    String.raw`"At least $k$": use the complement $1 - P(X \le k - 1)$.`,
    String.raw`$P(A\cup B) = P(A) + P(B) - P(A\cap B)$; $P(\neg A) = 1 - P(A)$.`,
    String.raw`Fair $n$-sided die: $E = \frac{n+1}{2}$, $Var = \frac{n^2-1}{12}$.`
  ],
  example: {
    question: String.raw`10% of cars have a German plate. Of 20 cars, what is $P(\text{at least two German})$?`,
    steps: [
      String.raw`Binomial with $n = 20$, $p = 0.1$.`,
      String.raw`$P(X\ge2) = 1 - P(X = 0) - P(X = 1) = 1 - 0.9^{20} - 20\cdot0.1\cdot0.9^{19}$.`,
      String.raw`$\approx 1 - 0.1216 - 0.2702 = 0.608$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting the binomial coefficient $\binom nk$.`,
    String.raw`Computing "at least" directly with many terms instead of the complement.`,
    String.raw`Counting unordered outcomes where the ordered ones are equally likely (two dice: 36 outcomes).`
  ]
},

'continuous': {
  title: 'Continuous distributions',
  idea: String.raw`<p>A continuous random variable has a <strong>pdf</strong> $f\ge0$ with $\int_{-\infty}^\infty f = 1$. Probabilities are areas: $P(a\le X\le b) = \int_a^b f(x)\,dx$. The <strong>cdf</strong> $F(x) = \int_{-\infty}^x f(t)\,dt$ is continuous, increasing from $0$ to $1$, and $F^{\prime} = f$.</p>`,
  rules: [
    String.raw`Normalising: solve $\int f(x)\,dx = 1$ for the unknown constant.`,
    String.raw`$E(X) = \int x f(x)\,dx$, $Var(X) = \int (x - E(X))^2 f(x)\,dx$.`,
    String.raw`$P(a < X < b) = F(b) - F(a)$; constants in a piecewise cdf follow from continuity ($F = 0$ at the left end, $1$ at the right end).`,
    String.raw`Uniform on $[a,b]$: $f = \frac1{b-a}$, $E = \frac{a+b}2$, $Var = \frac{(b-a)^2}{12}$.`,
    String.raw`Exponential with rate $\lambda$: $f = \lambda e^{-\lambda t}$ ($t\ge0$), $P(T > t) = e^{-\lambda t}$, $E = \frac1\lambda$.`,
    String.raw`Symmetric pdf around $m$ ($p(m + x) = p(m - x)$) $\Rightarrow E(X) = m$.`
  ],
  example: {
    question: String.raw`Find $c$ for $p(x) = \frac{1}{cx}$ on $[2,4]$ and the cdf.`,
    steps: [
      String.raw`$\int_2^4\frac{1}{cx}dx = \frac{\ln4 - \ln2}{c} = \frac{\ln2}{c} = 1 \Rightarrow c = \ln2$.`,
      String.raw`$F(x) = \int_2^x\frac{dt}{t\ln2} = \frac{\ln x - \ln2}{\ln2} = \log_2x - 1$ for $x\in[2,4]$.`
    ]
  },
  pitfalls: [
    String.raw`Forgetting that $f$ must be non-negative everywhere (not only integrate to $1$).`,
    String.raw`Computing $E(X)$ as $\int f$ instead of $\int x f$.`,
    String.raw`Using $P(X = a) > 0$ — for continuous variables single points have probability $0$.`
  ]
},

'conditional': {
  title: "Conditional probability & Bayes' rule",
  idea: String.raw`<p>$P(A\mid B)$ is the probability of $A$ when you know that $B$ happened: $P(A\mid B) = \frac{P(A\cap B)}{P(B)}$. Bayes' rule turns $P(E\mid H)$ (easy to know) into $P(H\mid E)$ (what you want).</p>`,
  rules: [
    String.raw`$P(A\cap B) = P(A\mid B)P(B) = P(B\mid A)P(A)$.`,
    String.raw`Law of total probability: $P(E) = \sum_i P(E\mid H_i)P(H_i)$ over a partition $H_1, H_2, \dots$`,
    String.raw`Bayes: $P(H\mid E) = \dfrac{P(E\mid H)P(H)}{P(E)}$.`,
    String.raw`Independence: $P(A\cap B) = P(A)P(B)$ (equivalently $P(A\mid B) = P(A)$).`,
    String.raw`Draw a tree: first level = the cause (urn, factory, coin), second level = the observation.`
  ],
  example: {
    question: String.raw`Box 1: 10 apples, 90 oranges; Box 2: 80 apples, 120 oranges. A box is chosen at random and an apple is drawn. $P(\text{Box 1}\mid\text{apple})$?`,
    steps: [
      String.raw`$P(\text{apple}\mid B_1) = \frac1{10}$, $P(\text{apple}\mid B_2) = \frac25$, $P(B_1) = P(B_2) = \frac12$.`,
      String.raw`Total probability: $P(\text{apple}) = \frac1{10}\cdot\frac12 + \frac25\cdot\frac12 = \frac14$.`,
      String.raw`Bayes: $P(B_1\mid\text{apple}) = \dfrac{\frac1{10}\cdot\frac12}{\frac14} = \frac15$.`
    ]
  },
  pitfalls: [
    String.raw`Confusing $P(A\mid B)$ with $P(B\mid A)$.`,
    String.raw`Forgetting the prior $P(H)$ in the numerator.`,
    String.raw`Assuming independence without checking.`
  ]
}

};
