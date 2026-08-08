# Project Charter: Internal Sales Fraud Detection & Analytics Platform

## 1. Project Title
Internal Sales Fraud Detection & Analytics Platform

## 2. Business Problem
Insurance companies process thousands of sales, customer interactions, refunds, and policy changes every day. Fraud investigators cannot manually review every transaction. This project uses data analytics and machine learning to identify suspicious employee behavior, prioritize high-risk fraud leads, and provide dashboards that support fraud investigations.

## 3. Goals & Objectives
- Reduce the volume of transactions investigators must manually review by surfacing only high-risk cases.
- Build a machine learning model that assigns a fraud risk score to each transaction.
- Provide an interactive dashboard that helps investigators prioritize and act on flagged cases quickly.
- Establish a repeatable data pipeline that can be re-run as new transaction data comes in.

### Key Questions This Project Answers
- Which employees have the highest fraud risk?
- Which customers appear suspicious?
- Are refunds increasing over time?
- Which regions have the most fraud activity?
- Which fraud rules trigger most often?
- What trends are emerging month over month?

## 4. Scope

**In scope:**
- Internal employee-driven transactions: sales, policy changes, refunds, commission activity.
- Behavioral pattern analysis (timing, frequency, magnitude of transactions per employee/agent).
- A working risk-scoring model and a dashboard to view results.

**Out of scope (for now):**
- Customer-facing or external fraud (e.g., claimant fraud, third-party fraud rings).
- Real-time streaming detection — this phase focuses on batch analysis of historical/uploaded data.
- Automated case resolution or disciplinary action — the platform flags and prioritizes only; humans investigate and decide.

## 5. Stakeholders
| Stakeholder | Interest |
|---|---|
| Fraud Investigation Team | Primary users; need accurate, prioritized leads |
| Compliance Department | Needs assurance the process is auditable and fair |
| IT / Data Team | Owns data access, security, and infrastructure |
| Executive Sponsor | Needs visibility into cost savings and risk reduction |

## 6. Data Sources

The platform is built around six core tables:

| Table | Purpose |
|---|---|
| Employees | Sales representatives and customer service agents |
| Customers | Customer information |
| Sales | Policies or product sales |
| Calls | Customer service interactions |
| Refunds | Refund transactions |
| Commissions | Employee commission payments |

*Note: Employee behavioral data is sensitive. Data access, storage, and anonymization approach should be confirmed with Compliance/IT before Phase 2 begins.*

### Table Relationships
           Employees
                 |
        EmployeeID
                 |
     ---------------------
     |         |        |
   Sales     Calls   Refunds
     |
 CustomerID
     |
Customers

`EmployeeID` links an employee to their sales, calls, and refund activity. `CustomerID` links each sale to the customer involved. `Commissions` ties back to `EmployeeID` as well, since commission payments are calculated per sale per employee.

## 7. Success Metrics
- Model precision/recall targets (to be defined once labeled/historical fraud data is available).
- Percentage reduction in transactions requiring full manual review.
- Investigator feedback on the usefulness/accuracy of flagged leads.
- Time-to-detection improvement compared to the current manual process.

## 8. Deliverables (Phase 1)
- This project charter
- System architecture diagram (`docs/architecture_diagram.png`)
- Data dictionary outlining available fields and sources
- Defined project scope and success criteria (above)

## 9. Timeline (High-Level)
| Phase | Description | Status |
|---|---|---|
| Phase 1 | Project Planning | In Progress |
| Phase 2 | Data Exploration & Cleaning | Not Started |
| Phase 3 | Feature Engineering & Model Prototyping | Not Started |
| Phase 4 | Dashboard Development | Not Started |
| Phase 5 | Testing & Deployment | Not Started |

## 10. Assumptions & Constraints
- Historical transaction data is available and accessible for analysis.
- Some transactions may not have confirmed fraud labels, which may require an unsupervised or semi-supervised approach initially.
- Data privacy and internal HR policies must be respected throughout.