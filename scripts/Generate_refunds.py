# generate_refunds.py
# Creates a synthetic Refunds table, linked to real sales

import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

# Load existing tables to link against
df_sales = pd.read_csv("data/sales.csv")

refund_reasons = [
    "Customer Dissatisfaction",
    "Billing Error",
    "Duplicate Charge",
    "Service Not Delivered",
    "Cancellation Within Grace Period",
    "Goodwill Adjustment",
]

# Only a subset of sales result in a refund (realistic: ~8-12%)
REFUND_RATE = 0.10
refund_candidates = df_sales.sample(frac=REFUND_RATE, random_state=42)

refunds = []
for i, row in enumerate(refund_candidates.itertuples(), start=1):
    refund_id = f"REF{i:05d}"

    # Refund amount is a portion of the original sale (partial or full refund)
    refund_amount = round(row.SaleAmount * random.uniform(0.3, 1.0), 2)

    refunds.append({
        "RefundID": refund_id,
        "SaleID": row.SaleID,
        "CustomerID": row.CustomerID,
        "EmployeeID": row.EmployeeID,
        "RefundDate": fake.date_between(start_date="-2y", end_date="today"),
        "RefundAmount": refund_amount,
        "Reason": random.choice(refund_reasons),
    })

df_refunds = pd.DataFrame(refunds)
df_refunds.to_csv("data/refunds.csv", index=False)

print("Refunds table saved successfully!")
print(df_refunds.head())
print(f"\nTotal refunds generated: {len(df_refunds)}")
print(f"Refund rate: {len(df_refunds) / len(df_sales):.1%}")