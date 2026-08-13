# generate_calls.py
# Creates a synthetic Calls table (customer service interactions)

import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

# Load existing tables to link against
df_customers = pd.read_csv("data/Telco-Customer-Churn.csv")
df_employees = pd.read_csv("data/employees.csv")

customer_ids = df_customers["customerID"].tolist()
employee_ids = df_employees["EmployeeID"].tolist()

call_reasons = [
    "Billing Inquiry",
    "Technical Support",
    "Plan Change Request",
    "Complaint",
    "Refund Request",
    "Account Update",
    "Service Cancellation",
]

NUM_CALLS = 5000

calls = []
for i in range(1, NUM_CALLS + 1):
    call_id = f"CALL{i:05d}"
    calls.append({
        "CallID": call_id,
        "CustomerID": random.choice(customer_ids),
        "EmployeeID": random.choice(employee_ids),
        "CallDate": fake.date_time_between(start_date="-2y", end_date="now"),
        "Reason": random.choice(call_reasons),
        "DurationMinutes": round(random.uniform(1, 45), 1),
    })

df_calls = pd.DataFrame(calls)
df_calls.to_csv("data/calls.csv", index=False)

print("Calls table saved successfully!")
print(df_calls.head())
print(f"\nTotal calls generated: {len(df_calls)}")