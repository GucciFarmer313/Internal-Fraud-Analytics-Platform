# generate_commissions.py
# Creates a synthetic Commissions table, linked to sales and employees

import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

# Load existing tables to link against
df_sales = pd.read_csv("data/sales.csv")

# Standard commission rate range (varies slightly per sale to feel realistic)
COMMISSION_RATE_MIN = 0.05
COMMISSION_RATE_MAX = 0.12

commissions = []
for i, row in enumerate(df_sales.itertuples(), start=1):
    commission_id = f"COMM{i:05d}"
    rate = round(random.uniform(COMMISSION_RATE_MIN, COMMISSION_RATE_MAX), 3)
    commission_amount = round(row.SaleAmount * rate, 2)

    commissions.append({
        "CommissionID": commission_id,
        "SaleID": row.SaleID,
        "EmployeeID": row.EmployeeID,
        "CommissionDate": row.SaleDate,
        "CommissionRate": rate,
        "CommissionAmount": commission_amount,
    })

df_commissions = pd.DataFrame(commissions)
df_commissions.to_csv("data/commissions.csv", index=False)

print("Commissions table saved successfully!")
print(df_commissions.head())
print(f"\nTotal commissions generated: {len(df_commissions)}")
print(f"Total commission paid out: ${df_commissions['CommissionAmount'].sum():,.2f}")