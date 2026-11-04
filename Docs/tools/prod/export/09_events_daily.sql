SELECT (timestamp AT TIME ZONE 'Europe/Moscow')::date AS day_msk, name, count(*) AS events,
       count(DISTINCT installation_id) AS installations
FROM product_events GROUP BY 1, 2 ORDER BY 1, 2
