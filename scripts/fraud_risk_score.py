import os
import sqlite3
import pandas as pd

# 1. Connect to SQLite database
DB_PATH = os.path.join("data", "fraud_analytics.db")
conn = sqlite3.connect(DB_PATH)

print("Calculating per-employee fraud risk features using SQL...\n")

# 2. SQL query to aggregate features per employee
#    Refunds and commissions are pre-aggregated in subqueries (refund_agg, commission_agg)
#    BEFORE joining to sales, to avoid join fan-out inflating totals.
query = """
WITH refund_agg AS (
    SELECT
        SaleID,
        COUNT(*) AS RefundCount,
        SUM(RefundAmount) AS RefundTotal
    FROM refunds
    GROUP BY SaleID
),
commission_agg AS (
    SELECT
        SaleID,
        SUM(CommissionAmount) AS CommissionTotal
    FROM commissions
    GROUP BY SaleID
)
SELECT
    e.EmployeeID,
    e.FirstName || ' ' || e.LastName AS EmployeeName,
    e.Role,
    e.Region,

    -- Total Sales Metrics
    COUNT(DISTINCT s.SaleID) AS TotalSalesCount,
    COALESCE(SUM(s.SaleAmount), 0) AS TotalSalesAmount,

    -- After-Hours Sales (11 PM - 4 AM)
    SUM(CASE WHEN CAST(strftime('%H', s.SaleDate) AS INTEGER) >= 23
               OR CAST(strftime('%H', s.SaleDate) AS INTEGER) < 4
             THEN 1 ELSE 0 END) AS AfterHoursSalesCount,

    -- Refund Metrics (pre-aggregated, one row per SaleID)
    COALESCE(SUM(ra.RefundCount), 0) AS TotalRefundCount,
    COALESCE(SUM(ra.RefundTotal), 0) AS TotalRefundAmount,

    -- Commission Metrics (pre-aggregated, one row per SaleID)
    COALESCE(SUM(ca.CommissionTotal), 0) AS TotalCommissionAmount

FROM employees e
LEFT JOIN sales s ON e.EmployeeID = s.EmployeeID
LEFT JOIN refund_agg ra ON s.SaleID = ra.SaleID
LEFT JOIN commission_agg ca ON s.SaleID = ca.SaleID
GROUP BY e.EmployeeID, EmployeeName, e.Role, e.Region;
"""

# 3. Read SQL results directly into a Pandas DataFrame
df_features = pd.read_sql(query, conn)

# 4. Calculate derived risk ratios
df_features["RefundRate"] = (
    df_features["TotalRefundCount"] / df_features["TotalSalesCount"]
).fillna(0)

df_features["RefundPercent"] = (
    df_features["TotalRefundAmount"] / df_features["TotalSalesAmount"]
).fillna(0)

df_features["AfterHoursRate"] = (
    df_features["AfterHoursSalesCount"] / df_features["TotalSalesCount"]
).fillna(0)

# 5. Display sample results
print("✓ Per-employee features generated successfully!")
print(f"Total Employees Analyzed: {len(df_features)}\n")
print(df_features.head())

# 6. Sanity check: flag employees with notably high metrics (quick visual gut-check)
print("\nTop 10 by RefundRate:")
print(df_features.sort_values("RefundRate", ascending=False).head(10)[
    ["EmployeeID", "EmployeeName", "TotalSalesCount", "TotalRefundCount", "RefundRate"]
])

print("\nTop 10 by AfterHoursRate:")
print(df_features.sort_values("AfterHoursRate", ascending=False).head(10)[
    ["EmployeeID", "EmployeeName", "TotalSalesCount", "AfterHoursSalesCount", "AfterHoursRate"]
])

# 7. Save extracted features to CSV inside data folder
output_path = os.path.join("data", "employee_risk_features.csv")
df_features.to_csv(output_path, index=False)
print(f"\nFeatures saved to: {output_path}")

# Close connection
conn.close()