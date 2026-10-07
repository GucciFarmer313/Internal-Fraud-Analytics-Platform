import os
import sqlite3
import pandas as pd

# Paths
DB_PATH = os.path.join("data", "fraud_analytics.db")
OUTPUT_PATH = os.path.join("data", "investigations.csv")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Read investigation history
query = """
SELECT
    InvestigationID,
    EmployeeID,
    CaseStatus,
    CaseDisposition,
    AnalystNotes,
    CreatedAt,
    UpdatedAt
FROM investigations
ORDER BY InvestigationID DESC
"""

df = pd.read_sql_query(query, conn)

# Export for Power BI
df.to_csv(OUTPUT_PATH, index=False)

conn.close()

print("Investigations exported successfully!")
print(f"Rows exported: {len(df)}")
print(f"File saved to: {OUTPUT_PATH}")
print(df.head())