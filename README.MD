# FinGuard: End-to-End Automated Financial ETL Pipeline & Risk Intelligence Analytics

## Project Overview

This project delivers a production-ready, fully automated monthly ETL (Extract, Transform, Load) Pipeline designed to ingest, validate, filter, and store massive transaction data scales. Operating on an enterprise level relational database storage tier, the workflow seamlessly bridges backend automated data engineering with a frontline Business Intelligence dashboard that exposes critical, systemic fraud vectors across merchant categories, temporal windows, geographies, and demographics.

---

## Architecture & System Automation

### Technologies Used

* **API Extraction:** Dynamic stream caching utilizing `kagglehub` API wrappers.
* **Python** – Core ETL engineering logic, data quality firewalls, and email automation
* **PostgreSQL (pgAdmin)** – Persistent, optimized relational data storage
* **Pandas** – Advanced data cleaning and matrix operations
* **SQLAlchemy & psycopg2** – High-speed Python-to-Postgres database connectivity links
* **Power BI Desktop** – Front-end semantic modeling, DAX architecture, and interactive risk visuals
* **Windows Task Scheduler** – End-to-end cron orchestration engine for zero-manual operations
* **SMTP (Email Protocol)** – Automated downstream risk reporting and stakeholder notification pipelines

---

## Project Structure

```text
FinGuard_Automated-Financial-ETL-Data-Quality-Pipeline/
├── Financial_ETL_Pipeline/
│   ├──Financial_data_anomalies_Check.py
│   ├──send_email.py
│   └──sql_scripts/
│       ├──schema.sql
│       └──analytical_queries.sql
├──FinGuard_Dashboard.pbix
├──DQ_ISSUE.csv
├──dashboard.png
├──email_alert.png
└──README.md
```

---

## The ETL Lifecycle (Phases of Automation)

### Phase 1: Ingestion & Extraction

The system programmatically monitors target local directory paths for raw, monthly incoming transaction dumps containing over **1.29 million rows**. A structural schema validation gate is instantly executed to guarantee incoming file consistency and prevent systemic schema drift.

### Phase 2: The Data Quality Firewall & Feature Engineering

Before a single row hits production storage, Python transforms the raw dataframe:

* **Data Quality Checks:** The script scans for missing data, handles null mutations, standardizes raw types, and flags duplicate entry points to ensure zero data redundancy.
* **Feature Engineering:** A custom analytical logic gate computes and inserts a specialized row-level flag (`high_value_risk`) to instantly isolate high-exposure transaction records for target downstream monitoring.

### Phase 3: High-Speed Database Loading & Persistence

![Terminal_success](/Dashboard/Images/Terminal_success.png)
The fully processed, cleaned dataset is programmatically pushed into a local PostgreSQL database instance (`FinGuard_DB`) using a chunked, multi-threaded connection stream.

* **Performance:** The pipeline successfully writes all **1.29 million rows** into the permanent production table `final_transactions` in just under **126 seconds**.
* **Data Persistence:** Unlike client query windows, the data is physically locked onto the computer's hard disk. Closing pgAdmin, shutting down the terminal, or restarting the hardware has zero impact on storage integrity.

### Phase 4: Downstream Business Intelligence Handshake

![FinGuard Analytics Dashboard](/Dashboard/Images/Recording%202026-06-25%20153613.gif)

Power BI Desktop is mapped directly to the local database via an **Import** model connection.

* **Automated Refresh:** The data pipeline operates with decoupled architecture. When a new monthly data batch updates the underlying database table, clicking a single **Refresh** button inside the Power BI dashboard triggers an automated loop. The semantic model instantly recalculates all DAX measures, re-scales the time-series trends, and populates the charts without requiring manual dashboard design overhauls.

> **Deployment Note:** This dashboard is built using Power BI Desktop connected directly to the local PostgreSQL database engine. Due to cloud licensing constraints for local showcase environments, the raw Power BI workbook (`FinGuard_Dashboard.pbix`) is included directly in this repository for local inspection.

---

## Orchestration Using Windows Task Scheduler

To eliminate repetitive manual script execution, the pipeline is scheduled using **Windows Task Scheduler**.

* **Trigger:** Set to execute on a strict monthly cron loop.
* **Action:** Task Scheduler wakes the system environment, calls the root Python executable, and runs the entire ETL pipeline from raw extraction to database loading in the background. This ensures regular database updates with absolute zero manual human intervention.

---

## Automated Stakeholder Email Alert (Monthly)

![Email_alert](/Dashboard/Images/Email_alert_1.png)
![Email_alert](/Dashboard/Images/Email_alert_2.png)
Immediately after the database load confirms success, an isolated Python utility (`send_email.py`) utilizes the SMTP protocol to push an executive alert directly to stakeholders and data owners. This proactive email ensures transparency across the firm by containing:

* A precise audit summary of newly processed monthly records.
* Aggregated logs detailing rows caught by the Data Quality Firewall.
* A direct CSV attachment (`DQ_ISSUE.csv`) highlighting specific anomalous records for immediate remediation.

---

## Business Intelligence & Financial Risk Findings

With the pipeline infrastructure verified, advanced analytical modeling and PostgreSQL aggregations were applied to the dataset to reveal key operational vulnerabilities.

### Insight 1: High-Fraud Merchant Categories

* **Online Shopping (`shopping_net`):** Primary exploit vector with **$1.71M** lost across **1,713 cases**.
* **In-Person Shopping (`shopping_pos`):** **$739K** lost across **843 cases**.
* **Miscellaneous Online (`misc_net`):** **$729K** lost across **915 cases**.

#### Analyst Takeaway: The Digital Vulnerability

Physical retail registers handle more traffic (116K transactions) than online portals (97K), yet online shopping suffers from **more than double** the fraud incidents and financial losses. This highlights a clear vulnerability in card-not-present digital checkout environments.

> **Action Item:** Implement mandatory multi-factor authentication (MFA) or 3D-Secure protocols explicitly for the `shopping_net` and `misc_net` digital checkout pipelines.

---

### Insight 2: The Late-Night Attack Window

* **The Spike:** Baseline transaction risk spikes to **2.88%** between 10:00 PM and Midnight (nearly triple the daytime average).
* **The Damage:** Hours 22 and 23 alone account for over **$2.48 Million** in cumulative financial losses.

#### Analyst Takeaway: The Midnight Blind Spot

Fraudsters intentionally strike during late-night windows to exploit consumer inactivity. A transaction cleared at 11:30 PM gives criminals an **8-hour detection headstart** before the average cardholder wakes up to review mobile notifications.

> **Action Item:** Automatically tighten risk engine velocity-trigger thresholds for online transactions initialized after 10:00 PM, forcing biometric or SMS step-up authentication.

---

### Insight 3: Geographic Risk Assessment

* **Volume Leaders:** New York (**$295K / 555 cases**) and Texas (**$265K / 479 cases**) represent the highest absolute losses.
* **The Efficiency Outlier:** Ohio (**$169K / 321 cases**) vs. California (**$171K / 326 cases**).

#### Analyst Takeaway: Volatility vs. Volume

California processes nearly 10,000 more transactions than Ohio, yet Ohio suffers nearly identical losses and exhibits a much higher standalone fraud rate (**0.69% vs 0.58%**). Transactions originating from Ohio carry significantly higher statistical risk.

> **Action Item:** Adjust the fraud engine's location-based scoring to apply a specialized risk-multiplier to transactions originating from high-exposure sectors in NY, TX, and OH.

---

### Insight 4: Demographic Profiling

* **System Footprint:** Female cardholders generate the highest baseline transaction volume (709K vs. 586K).
* **The Fraud Inversion:** Fraudsters successfully breach male accounts more times in absolute numbers (**3,771 vs. 3,735**), yielding a higher base fraud rate (**0.64% vs 0.53%**).

#### Analyst Takeaway: Target Optimization

When a male account is compromised, bad actors optimize for larger ticket sizes. Fraudulent swipes on male cards run **$74 more expensive** on average, resulting in **$300,000 more** in total capital damage.

> **Action Item:** Update machine learning risk coefficients to flag single ticket purchases on male accounts that exceed $500 for secondary customer confirmation.

---

### Insight 5: High-Value Risk Feature Optimization (`amt >= $1,000`)

![High_risk_rate](/Dashboard/Images/fraud_rate_of_%20over_$1000.png)

* **Minimal Friction:** The custom `$1,000` rule flags just **3,936 transactions** out of 1.29M—leaving **99.7%** of safe consumer traffic completely untouched.

* **High Efficiency:** Isolating this tiny 0.3% segment successfully captured over **$1.02 Million** in active fraud losses.

#### Analyst Takeaway: Hyper-Concentrated Density

While a baseline transaction has a fraction of a percent chance of being fraud (0.51%), a transaction crossing this $1,000 line hits a **24.11% fraud probability**. Nearly 1 in 4 transactions in this custom bucket is a confirmed attack.

> **Action Item:** Deploy an automatic, real-time push-notification freeze on any transaction exceeding $1,000, immediately neutralizing over 25% of the platform's financial fraud exposure footprint.

---

### Insight 6: Transaction Amount Profiling & Radar Subversion

* **Legitimate Transactions:** Average around **$67.67**, containing extreme individual consumer outliers that max out at **$28,948.90**.
* **Fraudulent Transactions:** Average a staggering **$531.32**—nearly **8 times higher** than normal consumer spending. Yet, their maximum cap is strictly controlled, topping out at just **$1,376.04**.

#### Analyst Takeaway: Strategic Financial Subversion

This reveals a highly calculated criminal pattern. Fraudsters on this network are not making massive, multi-thousand-dollar luxury purchases that immediately sound alarms at corporate security centers. Instead, they run a high-volume, mid-tier strategy. By capping their maximum swipes around $500 to $1,300, they systematically drain accounts while staying intentionally beneath the automated high-value alert parameters deployed by traditional banking networks.

---

### Insight 7: Vulnerability by Generational Age Groups

* The **Over 50** demographic is the primary target vector for successful fraud exploits.
* Accounts held by individuals over the age of 50 accounted for **3,267** independent fraud incidents.
* This generation suffered a staggering **$1.84 Million** in direct financial losses—**surpassing the financial damages of the Under 30 and 30-50 demographics combined.**

#### Analyst Takeaway: Vulnerable Demographics

This statistical evidence proves that older account holders face a severe exposure risk, underscoring the urgent business need for targeted account safety tools, protective transaction limits, and specialized monitoring algorithms for older age brackets.

---

## Key Features

-**End-to-End Monthly Automation:** Zero-touch processing handled completely by OS level task scheduling triggers.
-**Data Quality Firewall:** Integrated programmatic validation schema targeting data bias, mutations, and null metrics.
-**Decoupled BI Data Architecture:** Automated downstream database-to-canvas handshake allowing structural report updates upon refresh.
-**Enterprise Storage Performance:** Heavy dataset ingest optimization loading **1.29M records** in under **80 seconds**.
-**Proactive Notification Architecture:** Instant automated reporting routing technical data quality audits directly to stakeholders via email.

---

## Future Enhancements

-**Multi-Source Ingestion API:** Expand the Python pipeline to pull live transaction data directly from third-party financial web APIs rather than static local CSV file directories.
-**Enterprise Cloud Migration:** Transition the local PostgreSQL database tier to a managed cloud instance (such as AWS RDS or Azure SQL Database) to allow centralized, remote team access.
-**Advanced Fraud Alert Slack/Teams Integration:** Upgrade the automated notification utility to instantly send critical late-night $1,000+ fraud alerts directly to an active corporate Slack or Microsoft Teams security channel for real-time triage.

---

## 👤 Author

* **Priyanshu Verma** – Data Analyst | Data Science Enthusiast

---

## Dashboard Visualization

![FinGuard Analytics Dashboard](/Dashboard/Images/fraud_risk_Dashboard.png)
