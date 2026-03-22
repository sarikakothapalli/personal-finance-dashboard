import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Finance Dashboard", page_icon="💰")

# Load data
df = pd.read_csv("spending.csv")

# Data cleaning
df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"])
df["Month"] = df["Date"].dt.strftime("%Y-%m")

# Title
st.title("💰 Personal Finance Dashboard")
st.markdown("Track your spending, analyze patterns, and understand your habits 📊")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("📅 Filter Data")

start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Category"].isin(category))
]

# ---------------- METRICS ----------------
total_spending = filtered_df["Amount"].sum()
st.metric("💰 Total Spending", f"₹{total_spending}")

# ---------------- PIE CHART ----------------
category_spend = filtered_df.groupby("Category")["Amount"].sum().reset_index()

fig1 = px.pie(
    category_spend,
    names="Category",
    values="Amount",
    title="🧾 Spending by Category"
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- LINE CHART ----------------
monthly_spend = filtered_df.groupby("Month")["Amount"].sum().reset_index()

fig2 = px.line(
    monthly_spend,
    x="Month",
    y="Amount",
    title="📈 Monthly Spending Trend",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# ---------------- INSIGHTS ----------------
st.subheader("🧠 Insights")

if not category_spend.empty:
    max_category = category_spend.loc[category_spend["Amount"].idxmax()]
    st.write(f"👉 You spend the most on **{max_category['Category']}**")

    avg_spend = filtered_df["Amount"].mean()
    st.write(f"👉 Average transaction amount is **₹{round(avg_spend, 2)}**")

    total_transactions = filtered_df.shape[0]
    st.write(f"👉 Total number of transactions: **{total_transactions}**")
else:
    st.write("No data available for selected filters ❌")