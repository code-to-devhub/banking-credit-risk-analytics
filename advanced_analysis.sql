-- Advanced Banking & Credit Risk SQL
WITH customer_exposure AS (
 SELECT customer_id,SUM(loan_amount) exposure FROM loans GROUP BY customer_id
)
SELECT customer_id,exposure,RANK() OVER(ORDER BY exposure DESC) exposure_rank
FROM customer_exposure;

SELECT c.region,SUM(l.loan_amount) exposure,
SUM(CASE WHEN l.status='Default' THEN l.loan_amount ELSE 0 END) default_amount
FROM customers c JOIN loans l ON c.customer_id=l.customer_id GROUP BY c.region;

SELECT loan_type,SUM(loan_amount) exposure,
SUM(CASE WHEN status='Default' THEN loan_amount ELSE 0 END) default_amount
FROM loans GROUP BY loan_type ORDER BY exposure DESC;

WITH m AS (
 SELECT strftime('%Y-%m',transaction_date) month,SUM(fee) fee_revenue
 FROM transactions GROUP BY 1
)
SELECT month,fee_revenue,LAG(fee_revenue) OVER(ORDER BY month) previous_month
FROM m;
