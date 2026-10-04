# Banking Customer & Credit Risk Analytics

End-to-end banking analytics project using SQL, Python (Pandas/NumPy), and BI-ready reporting.

## Tools
SQL | Python | Pandas | NumPy | Power BI/Tableau-ready CSVs

## Analysis
- Customer profitability and activity
- Loan portfolio and credit exposure
- Default and delinquency risk
- Customer risk segmentation
- Regional and monthly performance
- Loan product performance
- Cohort activity analysis

## Run
```bash
pip3 install pandas numpy
python3 src/01_generate_data.py
python3 src/02_analysis.py
```

The project generates 520,000+ transactions, 60,000 customers and 15,000 loans.

## Project Structure
```text
banking-credit-risk-analytics/
├── data/
├── sql/
│   └── advanced_analysis.sql
├── src/
│   ├── 01_generate_data.py
│   └── 02_analysis.py
├── output/
└── README.md
```
