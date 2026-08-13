# generate_sales.py
# Creates a synthetic Sales table, linking real Telco customers to synthetic employees

import random
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Load the real customer data and the employees you just generated
df_customers = pd.read_csv("data/Telco-Customer-Churn.csv")
df_employees = pd.read_csv("data/employees.csv")

employee_ids = df_employees["EmployeeID"].tolist()

sales = []
for i, row in df_customers.iterrows():
    sale_id = f"SALE{i+1:05d}"

    # Generate a date and give it a daytime business-hours timestamp (8 AM - 8 PM)
    sale_datetime = fake.date_time_between(
        start_date="-2y", end_date="now"
    ).replace(
        hour=random.randint(8, 20),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )

    sales.append(
        {
            "SaleID": sale_id,
            "CustomerID": row["customerID"],
            "EmployeeID": random.choice(employee_ids),
            "SaleDate": sale_datetime,
            "SaleAmount": round(row["MonthlyCharges"], 2),
            "PaymentMethod": row["PaymentMethod"],
            "Contract": row["Contract"],
        }
    )

df_sales = pd.DataFrame(sales)
df_sales.to_csv("data/sales.csv", index=False)

print("Sales table saved successfully with business-hours timestamps!")
print(df_sales.head())
print(f"\nTotal sales generated: {len(df_sales)}")