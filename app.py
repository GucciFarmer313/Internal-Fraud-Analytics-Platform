# app.py
# Flask dashboard for the Internal Sales Fraud Analytics Platform

import os
import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DATA_PATH = os.path.join("data", "isolation_forest_results.csv")
SALES_PATH = os.path.join("data", "sales.csv")
REFUNDS_PATH = os.path.join("data", "refunds.csv")

def load_data():
    """Load the scored employee data fresh on each request."""
    df = pd.read_csv(DATA_PATH)
    return df


@app.route("/")
def dashboard():
    df = load_data()

    # KPI calculations
    total_employees = len(df)
    flagged_count = len(df[df["Is_Flagged_Fraud"] == "Yes"])
    total_refund_amount = df["TotalRefundAmount"].sum()
    total_sales_amount = df["TotalSalesAmount"].sum()

    kpis = {
        "total_employees": total_employees,
        "flagged_count": flagged_count,
        "total_refund_amount": round(total_refund_amount, 2),
        "total_sales_amount": round(total_sales_amount, 2),
    }

    # Top 10 highest-risk employees for the chart (most negative anomaly score first)
    top_risk = df.sort_values("Anomaly_Score", ascending=True).head(10)
    chart_labels = top_risk["EmployeeID"].tolist()
    chart_scores = (-top_risk["Anomaly_Score"]).round(3).tolist()  # flip sign so higher bar = higher risk

    return render_template(
        "dashboard.html",
        kpis=kpis,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
    )


@app.route("/api/employees")
def api_employees():
    """Serve the full employee table as JSON for the frontend table/filter."""
    df = load_data()
    columns = [
        "EmployeeID", "EmployeeName", "Role", "Region",
        "TotalSalesCount", "TotalSalesAmount",
        "AfterHoursSalesCount", "AfterHoursRate",
        "TotalRefundCount", "RefundRate",
        "Anomaly_Score", "Is_Flagged_Fraud",
    ]
    
    records = df[columns].to_dict(orient="records")
    return jsonify(records)


@app.route("/api/investigation/<employee_id>")

def api_investigation(employee_id):

    sales = pd.read_csv(SALES_PATH)
    refunds = pd.read_csv(REFUNDS_PATH)

    employee_sales = sales[
        sales["EmployeeID"] == employee_id
    ].copy()

    evidence = employee_sales.merge(
        refunds,
        on="SaleID",
        how="left",
        suffixes=("_sale", "_refund")
    )

    return jsonify(
        evidence.fillna("").to_dict(orient="records")
    )

@app.route("/api/investigation/save", methods=["POST"])
def save_investigation():

    data = request.get_json()

    employee_id = data.get("employee_id")
    case_status = data.get("case_status")
    case_disposition = data.get("case_disposition")
    analyst_notes = data.get("analyst_notes")

    print("Investigation Decision Received:")
    print("Employee ID:", employee_id)
    print("Case Status:", case_status)
    print("Case Disposition:", case_disposition)
    print("Analyst Notes:", analyst_notes)

    return jsonify({
        "success": True,
        "message": "Investigation decision received"
    })
if __name__ == "__main__":
    app.run(debug=True)
    