import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Budget Boss", layout="wide")
st.title("Budget Boss")

# --- TIMEFRAME TOGGLE ---
st.sidebar.header("Timeframe View")
timeframe = st.sidebar.radio(
    "Select Timeframe:",
    ["Daily", "Weekly", "Biweekly", "Monthly"],
    index=2  # Default to Biweekly
)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Income", "Expenses", "Budget Bouncer"])

# --- DUMMY DATA ---
income_sources = {
    "Nicole": 10400,
    "Jon": 12450,
    "Rental Income": 3900,
    "Bonus": 972
}
expense_data = [
    {"Category": "Rent", "Amount": 2250, "Trip?": False},
    {"Category": "Electricity", "Amount": 500, "Trip?": False},
    {"Category": "Groceries", "Amount": 1750, "Trip?": False},
    {"Category": "Airbnb", "Amount": 3600, "Trip?": True},
    {"Category": "Rental Car", "Amount": 900, "Trip?": True},
    {"Category": "Flights", "Amount": 700, "Trip?": True},
    {"Category": "Trip Spending", "Amount": 6800, "Trip?": True}
]

income_df = pd.DataFrame(list(income_sources.items()), columns=["Source", "Amount"])
expenses_df = pd.DataFrame(expense_data)

# --- DASHBOARD TAB ---
with tab1:
    st.header("High-Level Overview")
    col1, col2, col3 = st.columns(3)
    total_income = income_df["Amount"].sum()
    total_expenses = expenses_df["Amount"].sum()
    remaining = total_income - total_expenses

    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Remaining", f"${remaining:,.2f}", delta=None if remaining >= 0 else f"-${abs(remaining):,.2f}")

    st.subheader(f"Spending by Category ({timeframe})")
    chart_data = expenses_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.bar_chart(chart_data)

# --- INCOME TAB ---
with tab2:
    st.header("Income Breakdown")
    st.dataframe(income_df, use_container_width=True)
    st.subheader("Income by Source")
    st.bar_chart(income_df.set_index("Source"))

# --- EXPENSES TAB ---
with tab3:
    st.header("Expenses Breakdown")
    st.data_editor(expenses_df, num_rows="dynamic", use_container_width=True)
    trip_total = expenses_df[expenses_df["Trip?"]]["Amount"].sum()
    non_trip_total = expenses_df[~expenses_df["Trip?"]]["Amount"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Trip Expenses", f"${trip_total:,.2f}")
    col2.metric("Non-Trip Expenses", f"${non_trip_total:,.2f}")

# --- SWIPE TO CATEGORIZE TAB ---
with tab4:
    st.header("Budget Bouncer Mode (Coming Soon)")
    st.markdown("You'll swipe left/right to categorize weird or unparsed expenses.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzI1NWRhZjE3NzFkZDExNjU5ODBlN2VmMmRlNTk2ZjkwYjVkNDc4NSZjdD1n/xT9IgzoKnwFNmISR8I/giphy.gif", caption="No entry for ambiguous transactions.")
