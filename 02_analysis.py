import sqlite3
from pathlib import Path
import pandas as pd, numpy as np

ROOT=Path("."); OUT=ROOT/"output"; OUT.mkdir(exist_ok=True)
con=sqlite3.connect(ROOT/"data/banking.db")
c=pd.read_csv(ROOT/"data/customers.csv"); l=pd.read_csv(ROOT/"data/loans.csv"); t=pd.read_csv(ROOT/"data/transactions.csv")
c.to_sql("customers",con,if_exists="replace",index=False); l.to_sql("loans",con,if_exists="replace",index=False); t.to_sql("transactions",con,if_exists="replace",index=False)

qs={
"kpi_summary":'''SELECT COUNT(DISTINCT c.customer_id) customers,COUNT(DISTINCT l.loan_id) loans,ROUND(SUM(l.loan_amount),2) loan_exposure,ROUND(SUM(CASE WHEN l.status='Default' THEN l.loan_amount ELSE 0 END)*100.0/NULLIF(SUM(l.loan_amount),0),2) default_exposure_pct,ROUND(SUM(t.fee),2) fee_revenue,ROUND(AVG(c.income),2) avg_income FROM customers c LEFT JOIN loans l ON c.customer_id=l.customer_id LEFT JOIN transactions t ON c.customer_id=t.customer_id;''',
"monthly_performance":'''SELECT strftime('%Y-%m',transaction_date) month,ROUND(SUM(CASE WHEN direction='Credit' THEN amount ELSE 0 END),2) credits,ROUND(SUM(CASE WHEN direction='Debit' THEN amount ELSE 0 END),2) debits,ROUND(SUM(fee),2) fee_revenue,COUNT(*) transactions FROM transactions GROUP BY 1 ORDER BY 1;''',
"regional_risk":'''SELECT c.region,COUNT(DISTINCT c.customer_id) customers,COUNT(l.loan_id) loans,ROUND(SUM(l.loan_amount),2) exposure,ROUND(SUM(CASE WHEN l.status='Default' THEN l.loan_amount ELSE 0 END),2) default_amount,ROUND(SUM(CASE WHEN l.status='Default' THEN l.loan_amount ELSE 0 END)*100.0/NULLIF(SUM(l.loan_amount),0),2) default_exposure_pct FROM customers c LEFT JOIN loans l ON c.customer_id=l.customer_id GROUP BY c.region ORDER BY default_exposure_pct DESC;''',
"loan_product_performance":'''SELECT loan_type,COUNT(*) loans,ROUND(SUM(loan_amount),2) exposure,ROUND(AVG(interest_rate)*100,2) avg_rate,ROUND(SUM(CASE WHEN status='Default' THEN loan_amount ELSE 0 END)*100.0/NULLIF(SUM(loan_amount),0),2) default_exposure_pct FROM loans GROUP BY loan_type ORDER BY exposure DESC;''',
"customer_risk_profile":'''WITH x AS (SELECT customer_id,SUM(loan_amount) exposure,SUM(CASE WHEN status='Default' THEN loan_amount ELSE 0 END) default_amount,COUNT(*) loan_count FROM loans GROUP BY customer_id), y AS (SELECT customer_id,COUNT(*) transactions,SUM(fee) fees FROM transactions GROUP BY customer_id) SELECT c.customer_id,c.region,c.income,COALESCE(x.exposure,0) exposure,COALESCE(x.default_amount,0) default_amount,COALESCE(x.loan_count,0) loan_count,COALESCE(y.transactions,0) transactions,COALESCE(y.fees,0) fees,RANK() OVER(ORDER BY COALESCE(x.exposure,0) DESC) exposure_rank FROM customers c LEFT JOIN x ON c.customer_id=x.customer_id LEFT JOIN y ON c.customer_id=y.customer_id;'''
}
for n,q in qs.items(): pd.read_sql_query(q,con).to_csv(OUT/f"{n}.csv",index=False)

cp=pd.read_csv(OUT/"customer_risk_profile.csv")
cp["exposure_income_ratio"]=cp.exposure/cp.income.replace(0,np.nan)
cp["default_flag"]=(cp.default_amount>0).astype(int)
cp["risk_segment"]=np.select([
 (cp.default_flag.eq(1))&(cp.exposure_income_ratio>.5),
 (cp.default_flag.eq(1))|(cp.exposure_income_ratio>.35),
 (cp.exposure_income_ratio<.15)&(cp.transactions>=8)
],["High Risk","Medium Risk","Low Risk"],default="Watchlist")
cp.to_csv(OUT/"customer_risk_segments.csv",index=False)

tx=t[["customer_id","transaction_date"]].copy()
tx["month"]=pd.to_datetime(tx.transaction_date).dt.to_period("M").dt.to_timestamp()
first=tx.groupby("customer_id").month.min().rename("cohort_month")
tx=tx.join(first,on="customer_id")
tx["cohort_index"]=(tx.month.dt.year-tx.cohort_month.dt.year)*12+tx.month.dt.month-tx.cohort_month.dt.month
co=tx.groupby(["cohort_month","cohort_index"]).customer_id.nunique().reset_index()
base=co[co.cohort_index==0][["cohort_month","customer_id"]].rename(columns={"customer_id":"cohort_size"})
co=co.merge(base,on="cohort_month"); co["retention_pct"]=np.round(co.customer_id*100/co.cohort_size,2)
co.to_csv(OUT/"cohort_activity.csv",index=False)
con.close(); print("Analysis complete. BI-ready files are in output/.")
