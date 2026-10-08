# Internal Fraud Analytics Platform
## Portfolio Case Study

**Project Type:** End-to-End Fraud Detection and Investigation Analytics

**Technologies:** Python, SQL, SQLite, pandas, scikit-learn, Isolation Forest, Flask, Power BI, Git, GitHub

**Project Focus:** Fraud Detection, Risk Analytics, Machine Learning, Business Intelligence, and Investigation Case Management

---

## 1. Executive Summary

The Internal Fraud Analytics Platform is an end-to-end analytics solution designed to identify suspicious employee transaction patterns, prioritize potential fraud cases, and support data-driven investigations.

The project simulates an insurance-related sales environment where organizations must monitor refund activity, unusual transaction behavior, and potential employee misconduct while minimizing unnecessary investigations.

The platform combines SQL-based data processing, Python analytics, unsupervised machine learning, a Flask investigation dashboard, and Power BI reporting to support the complete fraud monitoring lifecycle.

Rather than automatically labeling employees as fraudulent, the solution generates risk indicators and anomaly scores that help investigators identify transactions and employees requiring additional review.

The completed solution demonstrates how data engineering, predictive analytics, machine learning, and business intelligence can work together to improve fraud monitoring and investigation decision-making.

## 2. Business Problem & Objectives

### Business Problem

Organizations that manage high volumes of sales and refund transactions face challenges identifying suspicious employee behavior before it leads to financial losses, operational disruptions, or compliance concerns.

Traditional fraud monitoring often relies on manual transaction reviews or predefined rules. These approaches can be time-consuming, generate unnecessary alerts, and fail to identify unusual combinations of employee behavior.

In the simulated insurance-related sales environment, the project focuses on three key risk patterns:

- **Abnormal Refund Activity:** Employees processing unusually high numbers or amounts of refunds relative to their sales activity.
- **After-Hours Transactions:** Sales recorded outside expected business hours that may require additional investigation.
- **Unusual Transaction Patterns:** Behavioral anomalies that differ significantly from normal employee activity.

### Project Objectives

The project was designed to:

1. Integrate employee, customer, sales, refund, call, and commission data into a structured SQLite database.
2. Engineer employee-level risk indicators using SQL and Python.
3. Apply Isolation Forest anomaly detection to prioritize potentially suspicious employees.
4. Validate model results against deliberately injected fraud scenarios.
5. Provide investigators with transaction-level evidence, case statuses, dispositions, and analyst notes.
6. Develop Power BI dashboards for executive fraud monitoring and detailed employee investigations.
7. Demonstrate a reproducible end-to-end fraud analytics workflow.

### Business Value

The platform demonstrates how organizations can prioritize higher-risk activity, reduce dependence on purely manual screening, and provide investigators with a consistent evidence-review workflow.

Because this project uses synthetic transactions and controlled fraud scenarios, these benefits represent **potential operational value**, not measured financial savings or proven improvements in a production environment.

## 3. Data Sources & Data Pipeline

### Data Sources

The platform combines a publicly available customer dataset with synthetically generated operational data to simulate an insurance-related sales and fraud monitoring environment.

| Dataset | Description |
|---|---|
| Customers | IBM Telco Customer Churn dataset containing 7,043 customer records |
| Employees | 80 synthetic employees with roles, regions, and employee identifiers |
| Sales | 7,054 simulated sales transactions |
| Calls | 5,000 simulated customer interaction records |
| Refunds | 903 simulated refund transactions |
| Commissions | 7,054 simulated commission records |
| Fraud Ground Truth | 13 labeled reference records used for fraud scenario validation |

### Data Pipeline

The solution follows a structured processing workflow:

1. **Data Generation:** Python scripts generate employee, sales, call, refund, and commission datasets.
2. **Fraud Scenario Injection:** Controlled suspicious activity is introduced into the synthetic transactions to provide known validation cases.
3. **Data Storage:** The datasets are loaded into a relational SQLite database (`fraud_analytics.db`).
4. **Data Preparation:** SQL and Python aggregate transactional activity into employee-level analytical features.
5. **Machine Learning:** Isolation Forest evaluates behavioral patterns and generates anomaly scores.
6. **Investigation Processing:** Flask retrieves employee risk indicators, transaction evidence, and investigation records.
7. **Business Intelligence:** Power BI combines operational, model, and investigation data into executive and employee-level dashboards.

### Data Quality & Integrity

The data preparation process includes validation of employee and transaction identifiers, relational joins, transaction dates, refund amounts, and analytical features.

SQLite indexes support efficient lookups across employee and sales identifiers.

Because the operational datasets are synthetic, the platform provides a controlled environment for testing fraud scenarios without exposing real customer transaction records.

## 4. Fraud Detection & Machine Learning

### Machine Learning Approach

The platform uses **Isolation Forest**, an unsupervised anomaly detection algorithm implemented with Python and scikit-learn.

Isolation Forest identifies observations that differ from typical patterns by isolating them through randomly constructed decision trees. Employees exhibiting unusual combinations of transaction behaviors receive anomaly scores that help prioritize investigation.

The model does not independently determine whether fraud has occurred. Its purpose is to identify potentially suspicious activity requiring analyst review.

### Fraud Risk Features

Employee-level behavioral features include:

- **Refund Rate:** Proportion of an employee's sales associated with refunds.
- **After-Hours Rate:** Proportion of sales recorded outside expected business hours.
- **Transaction Volume:** Number of sales processed by an employee.
- **Refund Exposure:** Total value of refunds associated with an employee.
- **Commission Activity:** Total commissions associated with employee sales.

These features provide behavioral context for identifying potentially unusual employee activity.

### Model Validation

The Isolation Forest results were evaluated against five deliberately planted fraudulent employees within a population of 80 employees.

| Evaluation Metric | Result |
|---|---|
| Employees analyzed | 80 |
| Known fraudulent employees | 5 |
| Employees flagged by model | 8 |
| True positives | 5 |
| False positives | 3 |
| False negatives | 0 |
| Precision | 62.5% |
| Recall | 100% |
| F1 Score | 76.9% |

### Interpretation of Results

The model successfully identified all five deliberately planted fraud cases, achieving **100% recall** in the controlled dataset.

However, three additional employees were flagged despite not being part of the planted fraud scenarios, resulting in **62.5% precision**.

This illustrates an important operational tradeoff: prioritizing fraud detection may increase the number of cases requiring manual review.

The **76.9% F1 score** summarizes the balance between precision and recall.

These results are specific to the simulated dataset and should not be interpreted as evidence of equivalent performance in a real-world production environment.

### Model Limitations

- Synthetic fraud patterns may not represent the complexity of real-world fraud.
- Isolation Forest detects anomalies, which are not necessarily fraudulent.
- Model performance depends on the quality and relevance of behavioral features.
- Additional testing on representative, appropriately labeled operational data would be required before production deployment.
- Investigation decisions should remain subject to human review.

## 5. Fraud Investigation Workflow

### Flask Investigation Dashboard

The platform includes an interactive Flask web application that allows analysts to identify high-risk employees, review behavioral indicators, and investigate suspicious transactions.

The dashboard provides:

- Employee and fraud-lead KPI summaries.
- Employee search and regional filtering.
- Anomaly scores and behavioral risk indicators.
- Employee-level investigation details.
- Transaction-level sales and refund evidence.

### Transaction-Level Evidence Review

Investigators can select an employee to examine supporting transaction records, including:

- Sales and refund identifiers.
- Transaction dates and amounts.
- Refund reasons and payment methods.
- After-hours transaction indicators.
- Multiple-refund indicators.
- Transaction risk classifications.

This workflow helps analysts move from an employee-level anomaly alert to the underlying transaction evidence.

### Investigation Case Management

The Flask application integrates with SQLite to maintain investigation decisions and historical case records.

Analysts can record:

- **Case Status:** Open, Under Review, Escalated, or Closed.
- **Case Disposition:** No Fraud, Further Review Required, Suspected Fraud, or Confirmed Fraud.
- **Analyst Notes:** Observations, findings, and recommended follow-up actions.
- **Investigation History:** Previous decisions and their recorded timestamps.

Each saved investigation decision creates a record in the SQLite `investigations` table, supporting a history of case activity.

### Human-in-the-Loop Decision-Making

The machine learning model identifies unusual activity, but analysts remain responsible for reviewing the evidence and determining the appropriate case disposition.

This separation between automated risk detection and human investigation helps avoid treating an anomaly score as proof of fraud.

## 6. Power BI Reporting & Business Insights

### Executive Fraud Monitoring Dashboard

The Power BI executive dashboard provides a consolidated view of fraud indicators, transaction activity, refund exposure, and investigation outcomes.

**Key Performance Indicators**

| KPI | Result |
|---|---:|
| Employees Analyzed | 80 |
| Flagged Fraud Leads | 8 |
| Total Sales | 7,054 |
| Total Refunds | 903 |
| Total Refund Amount | $41,852.13 |
| Confirmed Fraud Cases | 1 |
| Employees with Investigation Cases | 2 |

**Executive Visualizations**

The dashboard includes:

- Employee anomaly-score rankings.
- Flagged fraud leads by geographic region.
- Investigation status and outcomes.
- Refund exposure by flagged employees.
- Refund rate versus after-hours activity analysis.

These visualizations help decision-makers identify employees requiring investigation and understand how risk indicators vary across the organization.

### Employee Fraud Investigation Dashboard

The second Power BI page provides a detailed view of individual employees and their associated transaction evidence.

Analysts can select an employee and examine:

- Anomaly score and fraud flag.
- Refund rate and after-hours transaction rate.
- Total refund exposure.
- Current investigation status and disposition.
- Latest analyst notes.
- Refund transaction details and risk classifications.

This enables a transition from executive-level monitoring to employee-specific investigation analysis.

### Business Insights

The simulated dataset and dashboards demonstrate several findings:

1. **Concentrated Risk:** Eight of the 80 employees were flagged by the anomaly detection model for further review.
2. **Behavioral Indicators:** Several flagged employees exhibited unusually high refund rates and after-hours transaction activity.
3. **Refund Exposure:** The dashboard tracks $41,852.13 in total refund activity across the simulated dataset. This represents refund volume, not confirmed fraud losses.
4. **Investigation Outcomes:** The recorded case data includes one confirmed-fraud disposition and one pending decision across two employees with investigation records.
5. **Risk Prioritization:** Combining anomaly scores with supporting transaction evidence provides a structured basis for deciding which cases to review first.

### Reporting Limitations

The Power BI dashboards use imported datasets and exported investigation records. Updates to case decisions in the Flask application require refreshing the investigation export and Power BI dataset.

The dashboards demonstrate analytical and reporting capabilities using simulated data; they do not establish actual fraud losses or production-level operational improvements.

## 7. Challenges, Lessons Learned & Future Improvements

### Technical Challenges

**1. Integrating Multiple Data Sources**

The project required combining employee, customer, sales, refund, call, and commission data while maintaining consistent identifiers and relationships.

The solution used a structured SQLite database, relational joins, and employee-level feature engineering to create reusable analytical datasets.

**2. Distinguishing Anomalies from Confirmed Fraud**

Isolation Forest identified eight suspicious employees, including all five deliberately planted fraud cases. However, three additional employees were flagged.

This highlighted the difference between detecting unusual behavior and establishing fraudulent activity. The investigation workflow was designed to support human review rather than automatically classify flagged employees as fraudulent.

**3. Managing Investigation History**

The investigation application needed to preserve previous case decisions while displaying the latest status and disposition.

The solution stores investigation decisions as separate SQLite records and retrieves the most recent decision for each employee.

**4. Integrating Power BI with Investigation Data**

The investigation records were stored in SQLite, while Power BI used imported reporting datasets.

A Python export script was developed to convert investigation records into a CSV file for Power BI reporting. This introduced a refresh dependency that would need to be automated in a production environment.

### Lessons Learned

The project reinforced several important principles:

- Fraud detection models should support investigations rather than replace analyst judgment.
- Data quality and consistent relationships are essential for reliable analytics.
- Precision and recall must be interpreted in the context of business risk.
- Executive dashboards and investigation dashboards serve different audiences.
- Maintaining investigation history is important for traceability and case management.
- Clear documentation makes technical solutions easier to maintain, demonstrate, and evaluate.

### Future Improvements

The following enhancements could be explored in future development:

1. **Automated Data Refresh:** Replace manual CSV exports with scheduled or direct data integration.
2. **Cloud Deployment:** Evaluate AWS services for secure data storage, processing, monitoring, and application hosting.
3. **Model Monitoring:** Track changes in anomaly scores, alert volumes, and model performance over time.
4. **Enhanced Fraud Features:** Incorporate additional behavioral indicators, customer relationships, and transaction patterns.
5. **Role-Based Access Control:** Restrict investigation data and case decisions based on authorized user roles.
6. **Audit Logging:** Strengthen traceability of investigation updates and user actions.
7. **Production Validation:** Evaluate the model using representative operational data and appropriate governance controls.

These are proposed improvements and are not presented as features already implemented in the current platform.

## 8. Project Outcomes & Portfolio Links

### Project Deliverables

The completed project includes:

- A reproducible Python data-generation and processing workflow.
- A relational SQLite database integrating operational datasets.
- Employee-level fraud-risk features and Isolation Forest anomaly detection.
- Model validation using controlled fraud scenarios.
- An interactive Flask fraud investigation dashboard.
- Transaction-level evidence review and SQLite investigation history.
- A two-page Power BI reporting solution.
- GitHub documentation, architecture, and dashboard screenshots.

### Key Outcomes

| Outcome | Result |
|---|---|
| Employees analyzed | 80 |
| Planted fraud cases detected | 5 of 5 |
| Model recall | 100% |
| Model precision | 62.5% |
| Model F1 score | 76.9% |
| Flagged employees requiring review | 8 |
| Power BI dashboard pages | 2 |

The project demonstrates the ability to connect data engineering, SQL analytics, machine learning, web application development, investigation workflows, and business intelligence into a working analytics solution.

The evaluation results were obtained using simulated operational data and controlled fraud scenarios. They do not represent verified production performance or measured financial savings.

### Portfolio Resources

**GitHub Repository:** [Internal Fraud Analytics Platform](https://github.com/GucciFarmer313/Internal-Fraud-Analytics-Platform)

**Executive Dashboard:** [View Screenshot](screenshots/executive_fraud_monitoring.png)

**Employee Investigation Dashboard:** [View Screenshot](screenshots/employee_investigation_details.png)

**Project Charter:** [View Project Charter](project_charter.md)

### Project Conclusion

The Internal Fraud Analytics Platform demonstrates an end-to-end approach to identifying unusual employee activity and supporting structured fraud investigations.

By combining Python, SQL, Isolation Forest, Flask, SQLite, and Power BI, the project illustrates how technical analytics capabilities can support business risk monitoring and evidence-based decision-making.

The solution is intended as a portfolio demonstration and foundation for further development, rather than a production-ready fraud detection system.