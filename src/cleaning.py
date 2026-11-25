"""Load, clean and auto-categorize expense data."""
import pandas as pd
from .config import CATEGORY_KEYWORDS


def guess_category(note):
    note = str(note).lower()
    for cat, words in CATEGORY_KEYWORDS.items():
        if any(w in note for w in words):
            return cat
    return "Other"


def clean(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])          # unusable rows
    df = df[df["amount"] > 0]
    df["payment_method"] = df["payment_method"].astype(str).str.strip().str.title()
    df["payment_method"] = df["payment_method"].replace({"Upi": "UPI"})
    df["category"] = df["category"].astype("object").where(df["category"].notna(), None)
    df["category"] = df["category"].apply(lambda x: x.strip().title() if isinstance(x, str) else x)
    missing = df["category"].isna()
    df.loc[missing, "category"] = df.loc[missing, "note"].apply(guess_category)  # auto-categorize
    df = df.drop_duplicates().sort_values("date").reset_index(drop=True)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df
