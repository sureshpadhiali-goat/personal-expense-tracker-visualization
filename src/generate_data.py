"""Create a synthetic expense dataset (deliberately a bit messy for cleaning practice)."""
import numpy as np
import pandas as pd
from .config import RAW_CSV, DATA_DIR

NOTES = {
    "Food": ["Swiggy order", "Grocery store", "Lunch at cafe", "Zomato dinner", "Tea and snacks"],
    "Rent": ["Monthly rent"],
    "Transport": ["Uber ride", "Metro recharge", "Petrol", "Ola cab"],
    "Shopping": ["Amazon purchase", "Flipkart order", "New shoes"],
    "Bills": ["Electricity bill", "WiFi bill", "Mobile recharge"],
    "Entertainment": ["Movie tickets", "Netflix", "Spotify"],
    "Health": ["Pharmacy", "Doctor visit", "Gym fee"],
    "Education": ["Udemy course", "Textbook", "Exam fee"],
}
RANGES = {"Food": (80, 700), "Transport": (40, 600), "Shopping": (400, 2500),
          "Bills": (200, 1500), "Entertainment": (150, 900),
          "Health": (100, 1200), "Education": (300, 1800)}
# Food is the most frequent everyday spend
WEIGHTS = {"Food": .38, "Transport": .20, "Shopping": .10, "Bills": .08,
           "Entertainment": .10, "Health": .07, "Education": .07}
METHODS = ["UPI", "Cash", "Credit Card", "Debit Card"]


def generate(start="2026-06-01", end="2026-11-23", seed=42):
    rng = np.random.default_rng(seed)
    cats, probs = list(WEIGHTS), list(WEIGHTS.values())
    rows = []
    for day in pd.date_range(start, end):
        if day.day == 1:  # rent on the 1st
            rows.append([day, "Rent", 12000, "UPI", "Monthly rent"])
        for _ in range(rng.integers(0, 4)):
            cat = rng.choice(cats, p=probs)
            lo, hi = RANGES[cat]
            rows.append([day, cat, round(float(rng.uniform(lo, hi)), 2),
                         rng.choice(METHODS, p=[.5, .2, .2, .1]), rng.choice(NOTES[cat])])
    df = pd.DataFrame(rows, columns=["date", "category", "amount", "payment_method", "note"])
    # inject mess: missing categories, odd text, duplicates, missing amounts
    df.loc[df.sample(8, random_state=1).index, "category"] = np.nan
    df.loc[df.sample(5, random_state=2).index, "payment_method"] = " upi "
    df = pd.concat([df, df.sample(4, random_state=3)], ignore_index=True)
    df.loc[df.sample(2, random_state=4).index, "amount"] = np.nan
    return df.sample(frac=1, random_state=5).reset_index(drop=True)


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    generate().to_csv(RAW_CSV, index=False)
    print(f"Saved {RAW_CSV}")
