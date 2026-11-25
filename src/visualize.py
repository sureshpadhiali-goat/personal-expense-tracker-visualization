"""Matplotlib / Seaborn charts, saved to images/."""
import matplotlib
matplotlib.use("Agg")  # works without a display
import matplotlib.pyplot as plt
import seaborn as sns
from .config import IMAGES_DIR
from . import analysis

sns.set_theme(style="whitegrid")


def _save(fig, name):
    IMAGES_DIR.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / name, dpi=150)
    plt.close(fig)


def category_bar(df):
    s = analysis.by_category(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=s.values, y=s.index, ax=ax, palette="viridis", hue=s.index, legend=False)
    ax.set(title="Category-wise Spending", xlabel="Amount (INR)", ylabel="")
    _save(fig, "category_bar.png")


def monthly_line(df):
    s = analysis.by_month(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(s.index, s.values, marker="o", linewidth=2)
    ax.set(title="Monthly Spending Trend", xlabel="Month", ylabel="Amount (INR)")
    _save(fig, "monthly_line.png")


def payment_pie(df):
    s = analysis.by_payment(df)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(s.values, labels=s.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Payment Method Share")
    _save(fig, "payment_pie.png")


def daily_trend(df):
    s = analysis.daily(df)
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(s.index, s.values, alpha=.4, label="Daily")
    ax.plot(s.index, s.rolling(7, min_periods=1).mean(), linewidth=2, label="7-day average")
    ax.set(title="Daily Spending Trend", xlabel="Date", ylabel="Amount (INR)")
    ax.legend()
    _save(fig, "daily_trend.png")


def all_charts(df):
    category_bar(df); monthly_line(df); payment_pie(df); daily_trend(df)
