"""Run the full pipeline: generate -> clean -> store -> analyse -> chart -> report."""
import pandas as pd
from src.config import RAW_CSV, CLEAN_CSV, DATA_DIR
from src.generate_data import generate
from src.cleaning import clean
from src.database import save_to_db
from src import visualize, report


def main():
    DATA_DIR.mkdir(exist_ok=True)
    if not RAW_CSV.exists():
        generate().to_csv(RAW_CSV, index=False)
        print("Step 1: synthetic data created ->", RAW_CSV.name)
    raw = pd.read_csv(RAW_CSV)
    print(f"Step 2: loaded {len(raw)} raw rows")
    df = clean(raw)
    print(f"Step 3: cleaned data -> {len(df)} rows (removed {len(raw) - len(df)} bad/duplicate rows)")
    df.to_csv(CLEAN_CSV, index=False)
    save_to_db(df)
    print("Step 4: saved to SQLite (data/expenses.db)")
    visualize.all_charts(df)
    print("Step 5: charts saved to images/")
    print("Step 6: report\n")
    print(report.generate_reports(df))


if __name__ == "__main__":
    main()
