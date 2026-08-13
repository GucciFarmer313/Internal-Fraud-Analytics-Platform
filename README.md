# 🛡️ Internal Sales Fraud Detection & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An end-to-end data analytics platform that identifies suspicious employee behavior in an insurance sales context — built to demonstrate SQL, Python, pandas, machine learning, and dashboarding skills through a realistic, portfolio-ready fraud investigation workflow.

---

## 📌 Project Overview

Insurance enterprises handle thousands of sales transactions, policy modifications, and customer refunds daily. Manual review processes cannot scale to cover every transaction, which means internal fraudulent activity — such as artificial refund abuse, duplicate customer accounts, or off-hours policy changes — often goes unnoticed until significant financial loss occurs.

This platform combines a real-world dataset (IBM Telco Customer Churn) with synthetically generated Employee, Sales, Calls, Refunds, and Commissions data, deliberately injects realistic fraud scenarios, and applies unsupervised machine learning (Isolation Forest) to flag high-risk employees — with results validated against a known ground truth.

---

## ⚙️ Key Features

- **Data Warehouse Layer** — 7 relational tables (Employees, Customers, Sales, Calls, Refunds, Commissions, Fraud Ground Truth) loaded into a SQLite database with indexed joins.
- **Synthetic Fraud Injection** — deliberately planted, realistic fraud patterns: abnormal refund volume, after-hours sales activity, and duplicate customer accounts.
- **SQL-Based Feature Engineering** — per-employee risk metrics (refund rate, after-hours rate, sales volume) calculated via SQL aggregation.
- **Unsupervised Anomaly Detection** — scikit-learn's Isolation Forest flags high-risk employees without needing pre-labeled fraud data.
- **Validated Results** — model output checked against ground truth: **100% recall**, catching all planted fraudulent employees within the top-ranked results.
- **Interactive Dashboard** *(in progress)* — Flask web app with KPIs, charts, and filters to surface flagged employees.

---

## 🏗️ System Architecture & Workflow

```
┌─────────────────────────────────────────────┐
│ 1. DATA GENERATION                           │
│ - Real: IBM Telco Customer Churn (Customers) │
│ - Synthetic: Employees, Sales, Calls,        │
│   Refunds, Commissions (Faker + pandas)      │
│ - Deliberate fraud scenario injection        │
└───────────────────┬───────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 2. DATA WAREHOUSE                            │
│ - SQLite database (fraud_analytics.db)       │
│ - Indexed on EmployeeID / CustomerID / SaleID│
└───────────────────┬───────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 3. ANALYTICS LAYER                           │
│ - SQL aggregation: refund rate, after-hours  │
│   rate, sales volume per employee            │
└───────────────────┬───────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 4. MACHINE LEARNING LAYER                    │
│ - scikit-learn Isolation Forest              │
│ - Anomaly scoring + fraud flagging           │
│ - Validated against ground truth             │
└───────────────────┬───────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 5. DASHBOARD LAYER                           │
│ - Flask web app: KPIs, charts, fraud alerts  │
│ - Power BI: supplementary BI dashboard       │
└─────────────────────────────────────────────┘
```

---

## 📊 Model Results

The Isolation Forest model was validated against a known set of 5 deliberately planted fraudulent employees:

| Metric | Result |
|---|---|
| Recall | 100% (5/5 planted fraud cases caught) |
| Precision | 62.5% (5 true positives / 8 flagged) |
| F1 Score | 76.9% |

All 5 planted fraudulent employees ranked in the **top 5** highest anomaly scores out of 80 total employees. The 3 false positives are documented and analyzed as realistic borderline cases rather than tuned away — see `docs/project_charter.md` for discussion.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.9+
- **Data Generation:** `pandas`, `Faker`
- **Database:** SQLite
- **Machine Learning:** `scikit-learn` (Isolation Forest)
- **Data Visualization:** `matplotlib`, `seaborn`, Chart.js
- **Web Framework:** `Flask`
- **BI Tool:** Power BI
- **Version Control:** Git, GitHub
- **IDE:** Visual Studio Code (VS Code)

---

## 📁 Project Structure

```
Internal-Fraud-Analytics-Platform/
├── .github/             # CI/CD workflows and issue templates
├── data/                # Raw, processed, and generated datasets + SQLite DB
├── docs/                # Project charter, architecture diagrams
├── notebooks/           # Exploratory analysis and model prototyping
├── scripts/             # Data generation, fraud injection, SQL, ML pipeline
├── models/              # Saved trained model files
├── reports/             # Generated reports and exports
├── static/              # CSS and static assets for the Flask dashboard
├── templates/           # HTML templates for the Flask dashboard
├── tests/                # Unit and integration tests
├── app.py               # Flask application entry point
├── requirements.txt     # Python dependencies
├── LICENSE
└── README.md
```

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/internal-sales-fraud-detection.git
cd internal-sales-fraud-detection
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the Dataset and Run the Pipeline
```bash
python scripts/Generate_employees.py
python scripts/Generate_sales.py
python scripts/Generate_calls.py
python scripts/Generate_refunds.py
python scripts/Generate_commissions.py
python scripts/Inject_fraud_scenarios.py
python scripts/load_to_sqlite.py
python scripts/fraud_risk_score.py
python scripts/isolation_forest_model.py
```

### 5. Run the Dashboard
```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`.

---

## 🧭 Project Status

- ✅ Phase 1: Project Planning — complete
- ✅ Data Warehouse Layer — complete
- ✅ Analytics Layer (SQL feature engineering) — complete
- ✅ Machine Learning Layer (Isolation Forest, validated) — complete
- 🔄 Dashboard Layer (Flask) — in progress
- ⏳ Power BI supplementary dashboard — planned

See `docs/project_charter.md` for full project scope, objectives, and data source details.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.