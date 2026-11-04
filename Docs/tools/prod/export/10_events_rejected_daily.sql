SELECT (first_seen_at AT TIME ZONE 'Europe/Moscow')::date AS day_msk, name, reason, count(*) AS events
FROM product_events_rejected GROUP BY 1, 2, 3 ORDER BY 1, 4 DESC
