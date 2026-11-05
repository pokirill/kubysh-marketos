SELECT key, built_at AT TIME ZONE 'Europe/Moscow' AS built_msk, as_of_date, build_kind,
       source_max_received_at AT TIME ZONE 'Europe/Moscow' AS last_event_msk
FROM mart_build_state ORDER BY built_at DESC
