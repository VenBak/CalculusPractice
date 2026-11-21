# Calculus & Probability — Exam Practice

A static website for practising the IBC017 *Calculus and Probability* exam.

- **Topic practice:** 20 topics, 29–38 questions each (645 in total).
  - Type your answer and get instant right/wrong feedback, the correct answer and a worked solution.
  - Every question has a 💡 **hint** button that reveals hints one at a time: first the approach or rule to use, then the shape of the answer (e.g. "a negative integer", or "a union of 2 intervals").
- **Random problem:** a random question from any topic. You can filter by area and limit it to questions you have not solved yet. Each topic page also has a "random question in this topic" button.
- **Refreshers:** each topic has a short guide covering the idea, the key rules, a worked example and common mistakes. You can open it inside the practice page or as its own page (`guide.html`).
- **Time per question:**
  - A clock runs while you work on a question and resets for the next one.
  - Every answered attempt logs its time, so you can see your average time per topic.
  - **Flagging** a question pauses its clock until you unflag it.
  - Time on a question you leave unanswered is kept for when you come back.
- **Practice exams:** 90 points in 3 hours, laid out like the real exam.
  - Question 1 is 12 multiple-choice items × 3 pt (36 pt), followed by open questions worth 3–6 pt (54 pt).
  - Countdown timer, auto-save, flags, hints, and time logged per question.
- **Past exams:** all 10 real exams (two per academic year, 2021–2022 to 2025–2026), with the questions exactly as on the paper and the official answers.
  - Sit an exam under its original time limit, or browse it with per-item checking, hints and solutions.
- **Results & progress:**
  - Score out of 90 and grade (`(points + 10) / 10`).
  - Breakdown by area and topic.
  - Time and hints used per question.
  - Review of every question.
  - A score chart across all exams.
- **Backup & transfer** (`data.html`): copy all your data as one string and paste it into the same page on another device, browser or copy of the site. You can **merge** it or **replace** what is there, or use a `.json` file instead.
- **Dark mode:** use the moon/sun button in the header. Until you pick one, the site follows your system setting.
- **Reference page:** the exam formula sheet (sections 1–6), plus an extended reference (sections 7–13):
  - all derivatives and primitives;
  - standard limits and L'Hôpital forms;
  - log and trig identities;
  - function analysis, integration techniques;
  - probability rules and distributions.

There is no build step, no server code and no external requests: KaTeX and math.js are vendored in `vendor/`.

## Deploy to GitHub Pages

1. Create a new repository on GitHub (e.g. `calc-exam-practice`).
2. Put **the contents of this folder** in the repository, so that `index.html` is at the repository root. You can upload them on GitHub, or run:
   ```bash
   cd calc-exam-practice
   git init && git add . && git commit -m "Exam practice site"
   git branch -M main
   git remote add origin https://github.com/<your-user>/calc-exam-practice.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings → Pages → Build and deployment**, set **Source** to *Deploy from a branch*, choose branch `main` and folder `/ (root)`, then click **Save**.
4. After a minute the site is live at `https://<your-user>.github.io/calc-exam-practice/`.

The `.nojekyll` file tells GitHub Pages to serve the files as they are. To try the site locally, open `index.html`, or run `python3 -m http.server` in this folder and visit <http://localhost:8000>.

**Updating an existing deployment:** replace all files. Your progress is stored in the browser, not in the repository, so it is kept. Progress from the previous version keeps working, because question IDs are unchanged.

## Typing answers

| Kind | Examples |
|---|---|
| Numbers | `3/4`, `-2`, `sqrt(2)/2`, `e^(1/2)`, `ln(3)`, `pi/4`, `2ln2` |
| Expressions | `2x*e^(3x)`, `ln(x^2+1)`, `(x+1)/(x-2)`, `cbrt(x-1)`, `arctan(e^x)` (`+ C` optional for antiderivatives) |
| Intervals | `(-inf, 2) U [3, inf)`, `[0, 1/sqrt(e))`, `R \ {-2, 3}` |
| Sets of values | `{0, 1/7}` (any order; past-exam sets may contain parameters such as `{a/2, -b}`) |
| Probabilities | exact fraction, or a decimal with ≥ 3 decimals |
| Choices | click the option; "select all that apply" items use checkboxes |

Answers are checked mathematically, not as text:
- numbers are evaluated exactly (relative tolerance 10⁻⁶);
- expressions are compared at many random points (antiderivatives up to a constant);
- intervals are normalised, and open/closed brackets must match, except for monotonicity and convexity intervals, where both are accepted.

If the checker ever rejects an equivalent answer in topic practice, use **"My answer was right — count it"**.

## File structure

```
index.html              topic overview, progress, shortcuts
practice.html           practise a topic (?topic=<id>&q=<n>) or random problems (?mode=random)
guide.html              topic refreshers (?topic=<id>; without it: index of all refreshers)
exam.html               timed practice exam generated from the bank
past-exams.html         list of real past exams by academic year
past-exam.html          sit (?id=<exam id>) or browse (&mode=browse) a past exam
results.html            results of one exam (?id=<result id>)
history.html            all exams, score chart, weak topics, time per topic
reference.html          exam formula sheet + extended reference
data.html               backup & transfer (export / import / delete)
css/style.css           all styles, light and dark theme
js/core/
  theme.js              dark/light mode (loaded in <head> to avoid a flash)
  math-check.js         answer parsing & checking (uses math.js)
  storage.js            localStorage: progress, times, flags, exams, export/import
  bank.js               loads question & past-exam files, builds and grades exams
  timer.js              per-question stopwatch (pauses when flagged or the tab is hidden)
  exam-runner.js        shared exam screen for practice and past exams
  guide-view.js         renders a refresher
  ui.js                 rendering helpers (KaTeX, answer fields, hints, dialogs, theme toggle)
js/pages/               one script per page
data/topics.js          areas and topics
data/bank/<topic>.js    generated questions with answers, hints and worked solutions
data/past-exams/        index.js + one file per real exam
data/guides.js          refresher texts
assets/past-exams/      graphs and figures cropped from the exam papers
vendor/                 KaTeX 0.16 and math.js 13 (MIT licensed)
tools/question-generator/  Python generators for data/bank and data/past-exams
```

## Regenerating the data

All answers are computed or verified with SymPy, not typed by hand.

```bash
pip install sympy
python3 tools/question-generator/build.py        # rewrites data/topics.js and data/bank/
python3 tools/question-generator/past_exams.py   # rewrites data/past-exams/ (runs 85 SymPy checks first)
```

**Practice bank:**
- Each topic is a function in `foundations.py`, `derivatives.py`, `integrals.py` or `probability.py`.
- To add a question template, give it a prompt, answer parts, solution steps and points, and give it a method hint in `hints.py`.
- The answer-shape hints are generated automatically.

**Past exams:**
- Transcribed in `past_exams.py` with the helpers from `past_common.py`.
- Each exam must total 90 points.

## Your data

Everything is stored only in the browser you use, under these `localStorage` keys:

| Key | Contents |
|---|---|
| `cpt.progress` | last result, attempts, times and hints per question |
| `cpt.exams` | submitted exams |
| `cpt.activeExam` | an exam in progress |
| `cpt.pending` | unanswered time per question |
| `cpt.flags` | flags per question |
| `cpt.theme` | light or dark mode |

The **Data** page turns all of this into one transfer string (`CPT2:` followed by base64-encoded JSON) that you can paste into another copy of the site.
