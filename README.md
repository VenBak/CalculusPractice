# Calculus & Probability — Exam Practice

A static website for practising the IBC017 *Calculus and Probability* exam:

- **Topic practice** — 20 topics (from the course summary and the practice-exam topic table), 29–38 questions each (645 in total). Type your answer, get instant right/wrong feedback, see the correct answer and a worked solution.
- **Progress tracking** — every attempt is saved in your browser's `localStorage`; each topic shows a progress bar (green = correct, red = wrong on the last attempt).
- **Practice exams** — 90 points in 3 hours, laid out like the real exam: question 1 is 12 multiple-choice items × 3 pt (36 pt), followed by open questions worth 3–6 pt (54 pt). There is a countdown timer, auto-save, question flags, and automatic submission at 0:00:00.
- **Results & history** — score out of 90, grade (`(points + 10) / 10`, as on the real exam where the name gives 10 free points), breakdown by area and topic, review of every question with its solution, and a chart of all past exam scores.
- **Reference page** — the formula sheet from the exam.

No build step, no server code and no external requests: KaTeX and math.js are vendored in `vendor/`.

## Deploy to GitHub Pages

1. Create a new repository on GitHub (e.g. `calc-exam-practice`).
2. Upload **the contents of this folder** (so `index.html` is at the repository root), or:
   ```bash
   cd calc-exam-practice
   git init && git add . && git commit -m "Exam practice site"
   git branch -M main
   git remote add origin https://github.com/<your-user>/calc-exam-practice.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`, **Save**.
4. After a minute the site is live at `https://<your-user>.github.io/calc-exam-practice/`.

The `.nojekyll` file tells GitHub Pages to serve the files as-is.

To try it locally you can simply open `index.html`, or run `python3 -m http.server` in this folder and visit <http://localhost:8000>.

## Typing answers

| Kind | Examples |
|---|---|
| Numbers | `3/4`, `-2`, `sqrt(2)/2`, `e^(1/2)`, `ln(3)`, `pi/4`, `2ln2` |
| Expressions | `2x*e^(3x)`, `ln(x^2+1)`, `(x+1)/(x-2)`, `cbrt(x-1)`, `arctan(e^x)` (`+ C` optional for antiderivatives) |
| Intervals | `(-inf, 2) U [3, inf)`, `[0, 1/sqrt(e))`, `R \ {-2, 3}` |
| Sets of values | `{0, 1/7}` (any order) |
| Probabilities | exact fraction, or a decimal with ≥ 3 decimals |

Answers are checked mathematically, not as text: numbers are evaluated exactly (relative tolerance 10⁻⁶), expressions are compared at many random points (antiderivatives up to a constant), intervals are normalised (endpoints and open/closed brackets must match). If the checker ever rejects an equivalent answer, use **“My answer was right — count it”**.

## File structure

```
index.html            topic overview and progress
practice.html         practise one topic (?topic=<id>&q=<n>)
exam.html             timed practice exam
results.html          results of one exam (?id=<exam id>)
history.html          all exams, score chart, weak topics, export/import
reference.html        formula sheet
css/style.css
js/core/
  math-check.js       answer parsing & checking (uses math.js)
  storage.js          localStorage persistence
  bank.js             loads question files, builds and grades exams
  ui.js               rendering helpers (KaTeX, answer fields, dialogs)
js/pages/             one script per page
data/topics.js        areas and topics
data/bank/<topic>.js  generated questions with answers and worked solutions
vendor/               KaTeX 0.16 and math.js 13 (MIT licensed)
tools/question-generator/   the Python generator for data/bank
assets/favicon.svg
```

## Regenerating or extending the question bank

The questions are generated (and their answers computed) with SymPy, so every stored answer is verified by a computer algebra system rather than typed by hand.

```bash
pip install sympy
python3 tools/question-generator/build.py      # rewrites data/ in this folder
```

Each topic is a function in `foundations.py`, `derivatives.py`, `integrals.py` or `probability.py`; add a template there (prompt, answer parts, solution steps, points) and rebuild. The exam blueprint (12 MC items + 54 open points, weighted Foundations 20 / Derivatives 35 / Integrals 22 / Probability 13) is set at the top of `js/core/bank.js`.

## Your data

Everything is stored only in the browser you use. The **Progress** page can export your progress to a JSON file and import it on another device, or delete it all.
