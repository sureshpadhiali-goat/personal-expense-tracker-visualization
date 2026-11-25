"""SQLite storage."""
import sqlite3
import pandas as pd
from .config import DB_PATH


def save_to_db(df):
    with sqlite3.connect(DB_PATH) as con:
        out = df.copy()
        out["date"] = out["date"].dt.strftime("%Y-%m-%d")
        out.to_sql("expenses", con, if_exists="replace", index=False)


def load_from_db():
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql("SELECT * FROM expenses", con, parse_dates=["date"])


def add_expense(date, category, amount, method, note):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO expenses (date, category, amount, payment_method, note, month) "
                    "VALUES (?,?,?,?,?,?)",
                    (str(date), category, float(amount), method, note, str(date)[:7]))
