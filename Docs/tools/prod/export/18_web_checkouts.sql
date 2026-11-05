SELECT substr(md5(w.id), 1, 12) AS checkout, substr(md5(pa.person_id), 1, 12) AS p, w.placement,
       w.expires_at AT TIME ZONE 'Europe/Moscow' AS expires_msk,
       w.opened_at AT TIME ZONE 'Europe/Moscow' AS opened_msk
FROM web_checkouts w
LEFT JOIN person_aliases pa ON pa.alias_type = 'installation' AND pa.alias_value = w.installation_id
ORDER BY w.expires_at
