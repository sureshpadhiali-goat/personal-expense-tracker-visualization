# Project Guide

## 1. Explanation
**Simple:** an expense tracker records what you spend, groups it (food, rent, travel...), and shows where your money goes so you can budget and save.
**Technical:** a pipeline - ingest CSV/manual rows -> clean with pandas (dates, duplicates, nulls, text) -> rule-based categorization -> SQLite -> groupby aggregations -> Matplotlib/Seaborn/Streamlit -> report export.
**Who benefits:** students (allowance control), employees (savings goals), families (shared budgets), freelancers (irregular income, business vs personal), small businesses (petty cash).
**Workflow:** data entry -> storage -> cleaning -> category analysis -> monthly analysis -> visualization -> report.

## 2. Tech stack options
| Option | Stack | Difficulty | Output |
|---|---|---|---|
| A Easy | Python, CSV, pandas, Matplotlib | Low | Charts + text report |
| B Intermediate | + Seaborn, SQLite, modular `src/` | Medium | Charts, DB, CSV reports |
| C Advanced | + Streamlit, ML categorization, PDF reports | High | Interactive dashboard |
**Chosen:** B with the Streamlit dashboard from C (this repo).

## 3. Architecture
```
[Manual form / CSV / synthetic] -> cleaning.py -> SQLite (database.py)
                                      |                |
                              auto-categorize     analysis.py
                                                       |
                                  visualize.py <-------+-------> report.py
                                   (images/)                   (reports/, outputs/)
                                                       |
                                                   app.py (Streamlit)
```

## 4. Phases
1. Setup: install Python, venv. Mistake: skipping venv.
2. Folders: create structure. Mistake: everything in one file.
3. CSV: run generate_data.py. Mistake: committing real personal data.
4. Loading: pd.read_csv. Mistake: wrong relative paths (use pathlib).
5. Cleaning: dates, duplicates, nulls. Mistake: not converting date to datetime.
6. Category analysis: groupby sum. Mistake: forgetting sort_values.
7. Monthly trend: period strings. Mistake: sorting months as text in mixed formats.
8. Visualization: save PNGs. Mistake: plt.show() on a server (use Agg backend).
9. Reports: text + CSV. Mistake: no insights, only numbers.
10. GitHub: commit, push. Mistake: not adding .gitignore.

## 6. Installation
Windows: `py -m venv venv`, `venv\Scripts\activate`, `pip install -r requirements.txt`
Mac: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`

## 8. Simulation
- Records: generate_data.py makes ~3 random expenses/day plus rent on the 1st.
- Categories: assigned by generator; missing ones are inferred from note keywords.
- Grouping: `groupby('category')`, `groupby('month')`.
- Monthly trend: sum per `YYYY-MM`.
- Overspending: spent > budget in `config.BUDGETS` -> "OVER BUDGET".
- Insights: top category share, over-budget list, savings rate.
Upload to GitHub: images/*.png, reports/expense_report.txt, outputs/*.csv, a dataset sample.

## 9. Expected terminal output
See README "Sample Output" or run `python main.py`.

## 10. GitHub steps
```bash
git init
git add .
git commit -m "Initial commit: project structure"
git branch -M main
git remote add origin https://github.com/<username>/Personal-Expense-Tracker-Visualization.git
git push -u origin main
```
Repo name: `Personal-Expense-Tracker-Visualization`
Description: Python expense tracker with pandas analysis, SQLite storage, charts, reports and a Streamlit dashboard.
Topics: python, pandas, data-analysis, data-visualization, streamlit, sqlite, matplotlib, seaborn, personal-finance, expense-tracker

## 12. Six-day proof plan
| Day | Work | Commit message | Screenshot |
|---|---|---|---|
| 1 | Setup, folders, requirements | `chore: project structure and requirements` | folder tree |
| 2 | generate_data.py, raw CSV | `feat: synthetic expense dataset generator` | dataset preview |
| 3 | cleaning.py, analysis.py | `feat: data cleaning and analysis` | terminal output |
| 4 | category + payment charts | `feat: category and payment charts` | bar + pie |
| 5 | monthly + daily charts | `feat: monthly and daily trend charts` | line charts |
| 6 | report, README, dashboard | `docs: README, report and dashboard` | report, GitHub preview |

## 13. Screenshots checklist
Folder tree, dataset preview (raw vs clean), terminal output, category bar, monthly line, payment pie, daily trend, expense_report.txt, Streamlit dashboard, GitHub repo page.

## 14. Interview preparation
1. **Explain your project.** I built a Python expense tracker that loads transaction data, cleans it with pandas, auto-categorizes missing categories using keyword rules, stores it in SQLite, analyses spending by category, month and payment method, checks budgets, draws charts and exports reports, with a Streamlit dashboard on top. I used synthetic data since I had no bank access.
2. **Why synthetic data?** Real bank data is private; synthetic data with deliberate errors let me practise realistic cleaning, and the pipeline accepts any CSV in the same format.
3. **How did you clean the data?** Converted dates, coerced amounts to numeric, dropped invalid rows, removed duplicates, normalised text and payment labels.
4. **How does auto-categorization work?** Keyword matching on the note field against a dictionary in config.py; unmatched notes become "Other". Next step: ML text classification.
5. **Why SQLite?** Zero setup, file-based, SQL queries, easy to move to PostgreSQL later.
6. **How do you detect overspending?** Monthly category totals vs budgets in config; spent > budget flags OVER BUDGET.
7. **Why modular code?** Each file has one job, so it is testable and reusable (dashboard and CLI share analysis.py).
8. **What challenges did you face?** Dirty dates and duplicates, matplotlib without a display (Agg backend), partial-month budget comparisons.
9. **How would you scale it?** Bank/UPI statement import, PostgreSQL, scheduled jobs, user login, ML categorization.
10. **What did you learn?** End-to-end data workflow: ingest, clean, store, analyse, visualize, communicate insights, plus Git/GitHub.
**HR version:** "I built a tool that shows people where their money goes and helps them stay within budget, and I published it with documentation on GitHub."
