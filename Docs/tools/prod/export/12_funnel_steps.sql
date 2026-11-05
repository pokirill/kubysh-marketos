SELECT substr(md5(person_id), 1, 12) AS p, step_key, step_order, first_at AT TIME ZONE 'Europe/Moscow' AS first_msk
FROM fct_funnel_step ORDER BY p, step_order
