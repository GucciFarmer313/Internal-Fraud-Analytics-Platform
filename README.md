# 🛡️ Internal Sales Fraud Detection & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An automated AI/ML data analytics platform engineered to help insurance internal audit teams flag suspicious employee transaction patterns, evaluate policy refunds, and prioritize high-risk fraud investigations.

---

## 📌 Project Overview

Insurance enterprises handle thousands of sales transactions, policy modifications, and customer refunds daily. Manual review processes cannot scale to cover every transaction, which means internal fraudulent activity — such as artificial sales commission padding, unauthorized policy refunds, or off-hours policy changes — often goes unnoticed until significant financial loss occurs.

This platform ingests internal transaction logs, cleans and engineers behavioral feature indicators, trains machine learning classifiers to generate risk probabilities, and surfaces the results through an interactive **Flask web dashboard** so fraud investigators can prioritize their review queue.

---

## ⚙️ Key Features

- **Automated Data Ingestion & Cleaning** — standardizes raw transaction logs using `pandas` and `numpy`.
- **Feature Engineering Engine** — flags anomalies such as out-of-hours transactions, unusual refund-to-sale ratios, and high-frequency policy changes per agent ID.
- **Predictive Fraud Scoring** — uses `scikit-learn` models (Random Forest / Logistic Regression) to assign an objective risk score (0–100%) to every transaction.
- **Visual Analytics Dashboard** — auto-generates distribution graphs using `matplotlib` and `seaborn` directly on the Flask dashboard.
- **Batch Analysis Interface** — simple web UI supporting file uploads for real-time risk evaluation.

---

## 🏗️ System Architecture & Workflow

```
┌───────────────────────────────┐
│ 1. INPUT                      │
│ - Raw Sales & Policy CSVs     │
│ - Employee IDs & Timestamps   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ 2. PROCESSING                 │
│ - pandas: Data Cleaning       │
│ - sklearn: Feature Scaling    │
│ - ML Model: Fraud Probability │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ 3. OUTPUT                     │
│ - Fraud Risk Probability Score│
│ - Seaborn / Matplotlib Charts │
│ - Flask Web Dashboard         │
└───────────────────────────────┘
```

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.9+
- **Data Processing & Analytics:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn`
- **Data Visualization:** `matplotlib`, `seaborn`
- **Web Framework:** `Flask`
- **Version Control & Management:** Git, GitHub, JIRA
- **IDE:** Visual Studio Code (VS Code)

---

## 📁 Project Structure

```
Internal-Fraud-Analytics-Platform/
├── .github/            # CI/CD workflows and issue templates
├── data/               # Raw and processed transaction data
├── docs/               # Project charter, architecture diagrams
├── notebooks/          # Exploratory analysis and model prototyping
├── src/                # Core source code (data processing, modeling, visualization)
├── static/             # CSS and static assets for the Flask dashboard
├── templates/          # HTML templates for the Flask dashboard
├── tests/              # Unit and integration tests
├── app.py              # Flask application entry point
├── requirements.txt    # Python dependencies
├── LICENSE
└── README.md
```

---

## 🚀 Quickstart & Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/GucciFarmer313/internal-sales-fraud-detection.git
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

### 4. Run the Application
```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`.

---

## 📊 Usage

1. Upload a transaction CSV file through the dashboard.
2. The platform cleans the data and engineers risk-relevant features automatically.
3. Each transaction is scored with a fraud risk probability.
4. Review flagged high-risk transactions and supporting charts directly in the dashboard.

---

## 🧭 Project Status

**Phase 1: Project Planning** — currently defining the business problem, project charter, and data requirements. See `docs/project_charter.md` for details. Model development and dashboard implementation follow in later phases.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.