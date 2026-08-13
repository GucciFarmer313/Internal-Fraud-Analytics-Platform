import os
import sqlite3
import pandas as pd

# 1. Define paths
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "fraud_analytics.db")

# 2. Map CSV file names to target SQLite table names
files_to_tables = {
    "employees.csv": "employees",
    "Telco-Customer-Churn.csv": "customers",
    "sales.csv": "sales",
    "calls.csv": "calls",
    "refunds.csv": "refunds",
    "commissions.csv": "commissions",
    "fraud_ground_truth.csv": "fraud_ground_truth",
}

# 3. Connect to SQLite database (creates 'fraud_analytics.db' if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
print(f"Loading CSV files into SQLite database at: {DB_PATH}\n")

try:
    # 4. Loop through each CSV file and write to SQLite
    for csv_file, table_name in files_to_tables.items():
        csv_path = os.path.join(DATA_DIR, csv_file)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Write DataFrame to SQLite database table
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"✓ Loaded '{csv_file}' -> Table: '{table_name}' ({len(df)} rows)")
        else:
            print(f"⚠️ Warning: File '{csv_path}' not found. Skipping.")

    # 5. Add indexes on EmployeeID for faster joins in later fraud-scoring queries
    print("\nCreating indexes...")
    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_sales_emp ON sales(EmployeeID)",
        "CREATE INDEX IF NOT EXISTS idx_refunds_emp ON refunds(EmployeeID)",
        "CREATE INDEX IF NOT EXISTS idx_commissions_emp ON commissions(EmployeeID)",
        "CREATE INDEX IF NOT EXISTS idx_calls_emp ON calls(EmployeeID)",
        "CREATE INDEX IF NOT EXISTS idx_sales_cust ON sales(CustomerID)",
        "CREATE INDEX IF NOT EXISTS idx_refunds_sale ON refunds(SaleID)",
        "CREATE INDEX IF NOT EXISTS idx_commissions_sale ON commissions(SaleID)",
    ]
    for stmt in index_statements:
        conn.execute(stmt)
    conn.commit()
    print("✓ Indexes created.")

    print("\nSuccess! All CSV files loaded into fraud_analytics.db.")

finally:
    # 6. Always close the connection, even if something above failed
    conn.close()