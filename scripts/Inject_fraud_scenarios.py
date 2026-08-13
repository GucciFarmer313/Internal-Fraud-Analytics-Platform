# inject_fraud_scenarios.py
# Deliberately injects realistic fraud patterns into the existing tables:
#   1. A handful of employees with abnormally high refund activity
#   2. After-hours sales activity for those same employees
#   3. Duplicate customer accounts used to push extra sales/commissions
#
# Also writes data/fraud_ground_truth.csv listing exactly what was injected,
# so you can later measure whether your model actually catches it.

import os
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, time, timedelta

fake = Faker()
Faker.seed(99)
random.seed(99)
np.random.seed(99)

# ---------- Safety check: don't double-inject ----------
if os.path.exists("data/fraud_ground_truth.csv"):
    print("⚠️  data/fraud_ground_truth.csv already exists.")
    print("This means fraud has already been injected once.")
    print("Running this script again will corrupt your data.")
    print("\nTo start over, first regenerate the base tables by running:")
    print("  python scripts/Generate_employees.py")
    print("  python scripts/Generate_sales.py")
    print("  python scripts/Generate_calls.py")
    print("  python scripts/Generate_refunds.py")
    print("  python scripts/Generate_commissions.py")
    print("Then run this script once.")
    exit()

# ---------- Load existing tables ----------
df_employees = pd.read_csv("data/employees.csv")
df_sales = pd.read_csv("data/sales.csv")
df_refunds = pd.read_csv("data/refunds.csv")
df_commissions = pd.read_csv("data/commissions.csv")

# Force SaleDate/RefundDate to proper datetime, no matter how they were stored
df_sales["SaleDate"] = pd.to_datetime(df_sales["SaleDate"])
df_refunds["RefundDate"] = pd.to_datetime(df_refunds["RefundDate"])

ground_truth = []  # collects a record of every fraud injection we make

# ---------- Pick our "suspicious" employees ----------
NUM_SUSPICIOUS = 5
suspicious_employees = df_employees.sample(n=NUM_SUSPICIOUS, random_state=99)["EmployeeID"].tolist()
print(f"Suspicious employees selected: {suspicious_employees}")

# ================================================================
# SCENARIO 1: Abnormal refund activity for suspicious employees
# ================================================================
extra_refund_rows = []
refund_counter = len(df_refunds) + 1

for emp_id in suspicious_employees:
    emp_sales = df_sales[df_sales["EmployeeID"] == emp_id]
    n_extra = int(len(emp_sales) * random.uniform(0.4, 0.6))
    flagged_sales = emp_sales.sample(n=min(n_extra, len(emp_sales)), random_state=99)

    for row in flagged_sales.itertuples():
        refund_id = f"REF{refund_counter:05d}"
        refund_counter += 1
        refund_amount = round(row.SaleAmount * random.uniform(0.85, 1.0), 2)

        extra_refund_rows.append({
            "RefundID": refund_id,
            "SaleID": row.SaleID,
            "CustomerID": row.CustomerID,
            "EmployeeID": row.EmployeeID,
            "RefundDate": row.SaleDate + timedelta(days=random.randint(1, 10)),
            "RefundAmount": refund_amount,
            "Reason": "Customer Dissatisfaction",
        })

    ground_truth.append({
        "ScenarioType": "Abnormal Refund Volume",
        "EmployeeID": emp_id,
        "Detail": f"{len(flagged_sales)} additional near-full refunds injected"
    })

df_extra_refunds = pd.DataFrame(extra_refund_rows)
df_refunds = pd.concat([df_refunds, df_extra_refunds], ignore_index=True)

# ================================================================
# SCENARIO 2: After-hours sales activity
# ================================================================
def random_after_hours_time():
    hour = random.choice(list(range(23, 24)) + list(range(0, 4)))
    minute = random.randint(0, 59)
    return time(hour, minute)

sales_indices_to_flag = []
for emp_id in suspicious_employees:
    emp_sale_idx = df_sales[df_sales["EmployeeID"] == emp_id].sample(
        frac=0.3, random_state=99
    ).index
    sales_indices_to_flag.extend(emp_sale_idx)

for idx in sales_indices_to_flag:
    original_date = df_sales.loc[idx, "SaleDate"]
    new_time = random_after_hours_time()
    df_sales.loc[idx, "SaleDate"] = datetime.combine(original_date.date(), new_time)

for emp_id in suspicious_employees:
    count = len([i for i in sales_indices_to_flag if df_sales.loc[i, "EmployeeID"] == emp_id])
    ground_truth.append({
        "ScenarioType": "After-Hours Sales",
        "EmployeeID": emp_id,
        "Detail": f"{count} sales shifted to 11PM-4AM window"
    })

# ================================================================
# SCENARIO 3: Duplicate customer accounts
# ================================================================
duplicate_rows = []
sale_counter = len(df_sales) + 1

for emp_id in suspicious_employees[:3]:
    real_customer = df_sales[df_sales["EmployeeID"] == emp_id].sample(1, random_state=99).iloc[0]
    fake_customer_id = real_customer["CustomerID"] + "-DUP"

    n_fake_sales = random.randint(2, 5)
    for _ in range(n_fake_sales):
        sale_id = f"SALE{sale_counter:05d}"
        sale_counter += 1
        fake_sale_amount = round(random.uniform(20, 100), 2)
        duplicate_rows.append({
            "SaleID": sale_id,
            "CustomerID": fake_customer_id,
            "EmployeeID": emp_id,
            "SaleDate": fake.date_between(start_date="-1y", end_date="today"),
            "SaleAmount": fake_sale_amount,
            "PaymentMethod": "Electronic check",
            "Contract": "Month-to-month",
        })

    ground_truth.append({
        "ScenarioType": "Duplicate Customer Account",
        "EmployeeID": emp_id,
        "Detail": f"Fake CustomerID {fake_customer_id} with {n_fake_sales} sales"
    })

df_duplicate_sales = pd.DataFrame(duplicate_rows)
df_duplicate_sales["SaleDate"] = pd.to_datetime(df_duplicate_sales["SaleDate"])
df_sales = pd.concat([df_sales, df_duplicate_sales], ignore_index=True)

# New commissions for the duplicate sales
extra_commissions = []
comm_counter = len(df_commissions) + 1
for row in df_duplicate_sales.itertuples():
    rate = round(random.uniform(0.05, 0.12), 3)
    extra_commissions.append({
        "CommissionID": f"COMM{comm_counter:05d}",
        "SaleID": row.SaleID,
        "EmployeeID": row.EmployeeID,
        "CommissionDate": row.SaleDate,
        "CommissionRate": rate,
        "CommissionAmount": round(row.SaleAmount * rate, 2),
    })
    comm_counter += 1

df_commissions = pd.concat([df_commissions, pd.DataFrame(extra_commissions)], ignore_index=True)

# ---------- Save everything back out ----------
df_sales.to_csv("data/sales.csv", index=False)
df_refunds.to_csv("data/refunds.csv", index=False)
df_commissions.to_csv("data/commissions.csv", index=False)

df_ground_truth = pd.DataFrame(ground_truth)
df_ground_truth.to_csv("data/fraud_ground_truth.csv", index=False)

print("\nFraud scenarios injected successfully!")
print(f"Refunds table: {len(df_refunds)} total rows")
print(f"Sales table: {len(df_sales)} total rows")
print(f"Commissions table: {len(df_commissions)} total rows")
print(f"\nGround truth log saved to data/fraud_ground_truth.csv")
print(df_ground_truth)