SELECT substr(md5(person_id), 1, 12) AS p, period_key, started_at, closed_at, source,
       plan_total_minor, actual_total_minor, deviation_minor, tx_count, transaction_days, is_complete
FROM fct_paycheck_period ORDER BY p, started_at
