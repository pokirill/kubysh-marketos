SELECT substr(md5(i.id), 1, 12) AS inst, substr(md5(a.person_id), 1, 12) AS p,
       i.installation_class, i.distribution_channel, i.distribution_source, i.source, i.campaign,
       i.creative_id, i.content_id, i.influencer_id, i.country, i.locale, i.timezone,
       g.country_code AS geo_country, i.app_version, i.device_model, i.os_version,
       i.created_at AT TIME ZONE 'Europe/Moscow' AS created_msk,
       i.attribution_recorded_at AT TIME ZONE 'Europe/Moscow' AS attribution_msk,
       i.last_seen_at AT TIME ZONE 'Europe/Moscow' AS last_seen_msk,
       (i.apns_device_token IS NOT NULL) AS has_push_token
FROM installations i
LEFT JOIN person_aliases a ON a.alias_type = 'installation' AND a.alias_value = i.id
LEFT JOIN installation_geo g ON g.installation_id = i.id
ORDER BY i.created_at
