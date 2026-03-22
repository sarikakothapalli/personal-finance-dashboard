import pandas as pd

# Load data
df = pd.read_csv("spending.csv")

# Clean data
df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"])

# Create Month column
df["Month"] = df["Date"].dt.to_period("M")

# Total spending by category
category_spend = df.groupby("Category")["Amount"].sum()
print("\nSpending by Category:\n", category_spend)

# Monthly spending
monthly_spend = df.groupby("Month")["Amount"].sum()
print("\nMonthly Spending:\n", monthly_spend)