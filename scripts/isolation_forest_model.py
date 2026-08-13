import os
import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load the per-employee feature dataset
FEATURES_PATH = os.path.join("data", "employee_risk_features.csv")
df = pd.read_csv(FEATURES_PATH)

# 2. Select features for model training
# Note: We prioritize rate-based features (RefundRate, RefundPercent, AfterHoursRate)
# over raw counts (TotalRefundCount, TotalSalesAmount) because raw counts are
# confounded by sales volume/tenure -- a high-volume honest employee naturally has
# higher raw counts than a low-volume one. Rates are normalized for that, and are
# a cleaner fraud signal. We keep total volume as light context, not the main driver.
feature_cols = [
    "RefundRate",
    "RefundPercent",
    "AfterHoursRate",
    "TotalSalesCount",       # kept as light context (very different scale, minor influence)
]
X = df[feature_cols].fillna(0)

# 3. Initialize and train Isolation Forest
# contamination=0.10 assumes ~10% of employees are potential anomalies/fraud
model = IsolationForest(
    n_estimators=100,
    contamination=0.10,
    random_state=42
)

# Fit model and predict (-1 = Anomaly/Fraud, 1 = Normal)
df["Anomaly_Prediction"] = model.fit_predict(X)

# Decision function returns anomaly score (lower/more negative = higher risk)
df["Anomaly_Score"] = model.decision_function(X)

# Map labels to human-readable format
df["Is_Flagged_Fraud"] = df["Anomaly_Prediction"].apply(lambda x: "Yes" if x == -1 else "No")

# Sort by lowest score (highest risk first)
df_sorted = df.sort_values(by="Anomaly_Score", ascending=True)

# 4. Save results back to CSV
OUTPUT_PATH = os.path.join("data", "isolation_forest_results.csv")
df_sorted.to_csv(OUTPUT_PATH, index=False)

# 5. Print summary
print("✓ Isolation Forest training complete!\n")
print("Top 10 High-Risk Flagged Employees:")
print(
    df_sorted[
        ["EmployeeID", "EmployeeName", "RefundRate", "AfterHoursRate", "Anomaly_Score", "Is_Flagged_Fraud"]
    ].head(10)
)

# 6. Verify against ground truth, with precision/recall
GROUND_TRUTH_PATH = os.path.join("data", "fraud_ground_truth.csv")
if os.path.exists(GROUND_TRUTH_PATH):
    ground_truth = pd.read_csv(GROUND_TRUTH_PATH)
    planted_ids = set(ground_truth["EmployeeID"].unique().tolist())
    flagged_ids = set(df[df["Is_Flagged_Fraud"] == "Yes"]["EmployeeID"].tolist())

    true_positives = planted_ids.intersection(flagged_ids)
    false_positives = flagged_ids - planted_ids
    false_negatives = planted_ids - flagged_ids

    precision = len(true_positives) / len(flagged_ids) if flagged_ids else 0
    recall = len(true_positives) / len(planted_ids) if planted_ids else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    print(f"\n--- Ground Truth Validation ---")
    print(f"Planted fraudulent employees: {sorted(planted_ids)}")
    print(f"Flagged by Isolation Forest:  {sorted(flagged_ids)}")
    print(f"\nTrue Positives  ({len(true_positives)}): {sorted(true_positives)}")
    print(f"False Positives ({len(false_positives)}): {sorted(false_positives)}")
    print(f"False Negatives ({len(false_negatives)}): {sorted(false_negatives)}")
    print(f"\nPrecision: {precision:.2%}  (of flagged employees, how many were truly fraudulent)")
    print(f"Recall:    {recall:.2%}  (of truly fraudulent employees, how many were caught)")
    print(f"F1 Score:  {f1:.2%}")