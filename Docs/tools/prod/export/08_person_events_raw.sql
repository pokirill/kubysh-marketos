-- Каждое событие у каждого человека: сколько раз, когда впервые и в последний раз, в скольких днях.
SELECT substr(md5(a.person_id), 1, 12) AS p, e.name, count(*) AS events,
       min(e.timestamp) AT TIME ZONE 'Europe/Moscow' AS first_msk,
       max(e.timestamp) AT TIME ZONE 'Europe/Moscow' AS last_msk,
       count(DISTINCT (e.timestamp AT TIME ZONE 'Europe/Moscow')::date) AS days,
       min(e.app_version) AS min_version, max(e.app_version) AS max_version
FROM product_events e
JOIN person_aliases a ON a.alias_type = 'installation' AND a.alias_value = e.installation_id
GROUP BY 1, 2 ORDER BY 1, 4
