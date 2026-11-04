SELECT substr(md5(payment_id), 1, 12) AS payment, event_name, occurred_at AT TIME ZONE 'Europe/Moscow' AS occurred_msk
FROM payment_analytics_events ORDER BY occurred_at
