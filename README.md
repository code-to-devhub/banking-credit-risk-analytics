# Banking Customer & Credit Risk Analytics

End-to-end banking analytics project focused on customer behavior, loan portfolio performance, credit risk, and profitability using SQL and Python.

## 🛠️ Tools & Technologies

* SQL
* Python
* Pandas
* NumPy
* SQLite
* Power BI / Tableau-ready CSV outputs

## 📊 Key Analysis

* Customer profitability and transaction activity
* Loan portfolio and credit exposure analysis
* Default rate and delinquency analysis
* Customer risk segmentation
* Regional risk and performance analysis
* Loan product performance
* Monthly revenue and performance trends
* Customer cohort activity analysis

## 🔍 Advanced SQL Analysis

Implemented:

* CTEs
* Window Functions
* `RANK()` and `LAG()`
* Customer-level aggregations
* Risk and exposure calculations
* Regional and product-level analysis

## 🐍 Python Analysis

Python was used for:

* Data generation and preparation
* Data cleaning
* Feature engineering
* Customer risk profiling
* Risk segmentation
* KPI and performance analysis
* BI-ready output generation

## 📁 Project Structure

```text
banking-credit-risk-analytics/
│
├── README.md
├── sql/
│   └── advanced_analysis.sql
│
├── src/
│   ├── 01_generate_data.py
│   └── 02_analysis.py
│
└── output/
    ├── kpi_summary.csv
    ├── monthly_performance.csv
    ├── regional_risk.csv
    ├── loan_product_performance.csv
    ├── customer_risk_profile.csv
    ├── customer_risk_segments.csv
    └── cohort_activity.csv
```

## ▶️ How to Run

```bash
pip3 install pandas numpy
```

Generate the dataset:

```bash
python3 src/01_generate_data.py
```

Run the analysis:

```bash
python3 src/02_analysis.py
```

The analysis outputs are automatically generated inside the `output/` folder.

## 💡 Key Business Insights

* Identified high-risk customer segments based on credit exposure and repayment behavior.
* Analyzed default and delinquency patterns across regions and loan products.
* Identified high-value customers based on transaction activity and profitability.
* Evaluated loan exposure and default risk to support credit-monitoring decisions.
* Generated BI-ready datasets for executive reporting.

## 🎯 Business Recommendations

* Strengthen monitoring of high-risk customer segments.
* Apply targeted retention strategies for valuable customers.
* Review high-default loan products and regional risk patterns.
* Use customer risk profiles for proactive credit-risk management.
* Optimize lending and customer engagement strategies using behavioral insights.

## ⚠️ Data Note

This project uses **synthetic banking data** created for portfolio and analytical demonstration purposes. No real customer or sensitive banking information is used.
