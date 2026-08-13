# generate_employees.py
# Creates a synthetic Employees table

import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_EMPLOYEES = 80

roles = ["Sales Representative", "Customer Service Agent", "Senior Sales Rep", "Account Manager"]
regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]

employees = []
for i in range(1, NUM_EMPLOYEES + 1):
    employee_id = f"EMP{i:04d}"
    employees.append({
        "EmployeeID": employee_id,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": fake.company_email(),
        "Role": random.choice(roles),
        "Region": random.choice(regions),
        "HireDate": fake.date_between(start_date="-5y", end_date="-30d"),
    })

df_employees = pd.DataFrame(employees)
df_employees.to_csv("data/employees.csv", index=False)

print("Employees table saved successfully!")
print(df_employees.head())
print(f"\nTotal employees generated: {len(df_employees)}")