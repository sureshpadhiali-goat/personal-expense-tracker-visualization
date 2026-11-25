"""Spending analysis functions."""
import pandas as pd
from .config import BUDGETS, MONTHLY_INCOME


def by_category(df):
    return df.groupby("category")["amount"].sum().sort_values(ascending=False).round(2)


def by_month(df):
    return df.groupby("month")["amount"].sum().round(2)


def by_payment(df):
    return df.groupby("payment_method")["amount"].sum().sort_values(ascending=False).round(2)


def daily(df):
    return df.groupby("date")["amount"].sum()


def avg_daily_spend(df):
    days = (df["date"].max() - df["date"].min()).days + 1
    return round(df["amount"].sum() / days, 2)


def budget_check(df, month):
    """Compare one month's category spend against budgets."""
    m = df[df["month"] == month].groupby("category")["amount"].sum()
    t = pd.DataFrame({"spent": m, "budget": pd.Series(BUDGETS)}).fillna(0)
    t["difference"] = t["budget"] - t["spent"]
    t["status"] = ["OVER BUDGET" if b and s > b else "OK" for s, b in zip(t["spent"], t["budget"])]
    return t.round(2)


def savings_summary(df):
    s = pd.DataFrame({"spent": by_month(df)})
    s["income"] = MONTHLY_INCOME
    s["savings"] = s["income"] - s["spent"]
    s["savings_rate_%"] = (s["savings"] / s["income"] * 100).round(1)
    return s
