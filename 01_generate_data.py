import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
OUT=Path("data"); OUT.mkdir(exist_ok=True)
N=520_000; NC=60_000; NL=15_000
dates=pd.date_range("2024-01-01","2025-12-31",freq="D")

customers=pd.DataFrame({
 "customer_id":np.arange(1,NC+1),
 "age":np.random.randint(21,66,NC),
 "region":np.random.choice(["North","South","East","West","Central"],NC),
 "income":np.round(np.random.lognormal(np.log(55000),.55,NC).clip(18000,300000),2),
 "tenure_months":np.random.randint(1,121,NC)
})
loans=pd.DataFrame({
 "loan_id":np.arange(1,NL+1),
 "customer_id":np.random.randint(1,NC+1,NL),
 "loan_type":np.random.choice(["Personal","Home","Auto","Education","Business"],NL,p=[.30,.22,.20,.12,.16]),
 "loan_amount":np.round(np.random.lognormal(np.log(18000),.9,NL).clip(1000,250000),2),
 "interest_rate":np.round(np.random.uniform(.06,.20,NL),4),
 "loan_start":np.random.choice(dates,NL),
 "status":np.random.choice(["Active","Closed","Default"],NL,p=[.68,.25,.07])
})
tx=pd.DataFrame({
 "transaction_id":np.arange(1,N+1),
 "customer_id":np.random.randint(1,NC+1,N),
 "transaction_date":np.random.choice(dates,N),
 "transaction_type":np.random.choice(["Deposit","Withdrawal","Transfer","Card Payment","Fee"],N,p=[.25,.18,.22,.25,.10]),
 "amount":np.round(np.random.lognormal(np.log(220),1.0,N).clip(5,20000),2)
})
tx["direction"]=np.where(tx.transaction_type.eq("Deposit"),"Credit","Debit")
tx["fee"]=np.where(tx.transaction_type.eq("Fee"),tx.amount,np.round(tx.amount*np.random.choice([0,.001,.002,.005],N,p=[.75,.10,.10,.05]),2))
customers.to_csv(OUT/"customers.csv",index=False); loans.to_csv(OUT/"loans.csv",index=False); tx.to_csv(OUT/"transactions.csv",index=False)
print(f"Generated {N:,} transactions, {NC:,} customers and {NL:,} loans.")
