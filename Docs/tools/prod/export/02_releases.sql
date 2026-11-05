SELECT app_version, build, released_at AT TIME ZONE 'Europe/Moscow' AS released_msk, channel, source, summary
FROM dim_release ORDER BY released_at
