"""CSV + text report generation."""
from datetime import date
from .config import REPORTS_DIR, OUTPUT_DIR
from . import analysis


def generate_reports(df):
    REPORTS_DIR.mkdir(exist_ok=True); OUTPUT_DIR.mkdir(exist_ok=True)
    analysis.by_category(df).to_csv(OUTPUT_DIR / "category_summary.csv")
    analysis.by_month(df).to_csv(OUTPUT_DIR / "monthly_summary.csv")
    analysis.by_payment(df).to_csv(OUTPUT_DIR / "payment_summary.csv")
    sav = analysis.savings_summary(df)
    sav.to_csv(OUTPUT_DIR / "savings_summary.csv")

    cat = analysis.by_category(df)
    last = df["month"].max()
    bud = analysis.budget_check(df, last)
    over = bud[bud["status"] == "OVER BUDGET"]
    lines = [
        "PERSONAL EXPENSE REPORT", f"Generated: {date.today()}", "=" * 40,
        f"Period: {df['date'].min().date()} to {df['date'].max().date()}",
        f"Transactions: {len(df)}",
        f"Total spending: INR {df['amount'].sum():,.2f}",
        f"Average daily spending: INR {analysis.avg_daily_spend(df):,.2f}",
        f"Highest spending category: {cat.index[0]} (INR {cat.iloc[0]:,.2f})",
        "", "Monthly spending:", analysis.by_month(df).to_string(),
        "", f"Budget check for {last} (partial month if data ends mid-month):", bud.to_string(),
        "", "Savings summary:", sav.to_string(), "",
        "Insights:",
        f"- {cat.index[0]} is the largest expense, {cat.iloc[0] / cat.sum() * 100:.1f}% of all spending.",
        (f"- Over budget in {last}: {', '.join(over.index)}." if len(over) else f"- No category exceeded budget in {last}."),
        f"- Average savings rate: {sav['savings_rate_%'].mean():.1f}%.",
    ]
    (REPORTS_DIR / "expense_report.txt").write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)
