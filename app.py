"""Streamlit dashboard: streamlit run app.py  (run `python main.py` first)"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.database import load_from_db, add_expense
from src import analysis
from src.config import CATEGORY_KEYWORDS

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("Personal Expense Tracker")

with st.sidebar:
    st.header("Add expense")
    d = st.date_input("Date")
    c = st.selectbox("Category", list(CATEGORY_KEYWORDS))
    a = st.number_input("Amount (INR)", min_value=0.0, step=10.0)
    m = st.selectbox("Payment", ["UPI", "Cash", "Credit Card", "Debit Card"])
    n = st.text_input("Note")
    if st.button("Save") and a > 0:
        add_expense(d, c, a, m, n)
        st.success("Saved")

df = load_from_db()
months = sorted(df["month"].unique())
sel = st.multiselect("Months", months, default=months)
df = df[df["month"].isin(sel)]

if df.empty:
    st.info("Select at least one month.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Total spend", f"INR {df['amount'].sum():,.0f}")
c2.metric("Avg daily", f"INR {analysis.avg_daily_spend(df):,.0f}")
c3.metric("Top category", analysis.by_category(df).index[0])

left, right = st.columns(2)
left.subheader("By category"); left.bar_chart(analysis.by_category(df))
right.subheader("Monthly trend"); right.line_chart(analysis.by_month(df))
fig, ax = plt.subplots()
p = analysis.by_payment(df)
ax.pie(p, labels=p.index, autopct="%1.0f%%")
left.subheader("Payment methods"); left.pyplot(fig)
right.subheader("Daily spending"); right.line_chart(analysis.daily(df))
st.subheader(f"Budget check - {sorted(sel)[-1]}")
st.dataframe(analysis.budget_check(df, sorted(sel)[-1]))
