SELECT substr(md5(s.id), 1, 12) AS sub, substr(md5(a.person_id), 1, 12) AS p, s.provider, s.plan, s.status,
       s.started_at, s.current_period_end, s.cancel_requested_at, s.failed_charge_count
FROM subscriptions s LEFT JOIN accounts a ON a.id = s.account_id
ORDER BY s.started_at
