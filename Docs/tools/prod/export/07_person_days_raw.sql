-- Активные дни по СЫРЫМ событиям, мимо витрины. Активность = как в app/analytics/activity.py.
SELECT substr(md5(a.person_id), 1, 12) AS p, i.installation_class,
       (e.timestamp AT TIME ZONE 'Europe/Moscow')::date AS day_msk,
       count(*) AS events, count(DISTINCT e.name) AS distinct_events,
       string_agg(DISTINCT e.app_version, ',') AS versions
FROM product_events e
JOIN installations i ON i.id = e.installation_id
JOIN person_aliases a ON a.alias_type = 'installation' AND a.alias_value = e.installation_id
WHERE e.name NOT LIKE 'analytics.%' AND e.name NOT LIKE 'error.%' AND e.name NOT LIKE 'net.%'
  AND e.name NOT IN ('push.received', 'push.sent')
GROUP BY 1, 2, 3 ORDER BY 3, 1
