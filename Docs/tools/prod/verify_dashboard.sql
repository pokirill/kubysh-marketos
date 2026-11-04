-- Сверка дашборда PMF: каждая цифра двумя путями — по витрине (fct_*) и по сырым событиям (product_events,
-- payments). Расхождение больше пары процентов = разбирать, прежде чем нести цифру в стратегию.
-- Активность = app/analytics/activity.py. «Реальные» = installations.installation_class = 'real'.
\pset pager off
\pset footer off
SET statement_timeout = '300s';

-- Режим только чтения запрещает временные таблицы, поэтому общие части подставляются переменными psql.
\set raw_day 'raw_day AS (SELECT DISTINCT a.person_id, (e.timestamp AT TIME ZONE ''Europe/Moscow'')::date AS day FROM product_events e JOIN installations i ON i.id = e.installation_id AND i.installation_class = ''real'' JOIN person_aliases a ON a.alias_type = ''installation'' AND a.alias_value = e.installation_id WHERE e.name NOT LIKE ''analytics.%'' AND e.name NOT LIKE ''error.%'' AND e.name NOT LIKE ''net.%'' AND e.name NOT IN (''push.received'', ''push.sent''))'
\set raw_first 'raw_first AS (SELECT a.person_id, min(e.timestamp) AS first_event_at, min(e.timestamp) FILTER (WHERE e.name = ''first_launch'') AS first_launch_at FROM product_events e JOIN installations i ON i.id = e.installation_id AND i.installation_class = ''real'' JOIN person_aliases a ON a.alias_type = ''installation'' AND a.alias_value = e.installation_id GROUP BY 1)'
\set mart_people 'mart_people AS (SELECT * FROM fct_person WHERE install_class = ''real'')'

\echo '=== A. Свежесть: as_of_date должен быть сегодняшним (иначе это замороженная база) ==='
SELECT key, built_at AT TIME ZONE 'Europe/Moscow' AS built_msk, as_of_date,
       (now() AT TIME ZONE 'Europe/Moscow')::date AS today_msk,
       CASE WHEN as_of_date >= (now() AT TIME ZONE 'Europe/Moscow')::date - 1 THEN 'ok' ELSE 'УСТАРЕЛА' END AS verdict
FROM mart_build_state ORDER BY built_at DESC;

\echo '=== B. Сколько реальных людей: витрина против сырых событий ==='
WITH :raw_first, :mart_people
SELECT (SELECT count(*) FROM mart_people) AS mart_people,
       (SELECT count(*) FROM raw_first) AS raw_people_with_events,
       (SELECT count(*) FROM raw_first WHERE first_launch_at IS NOT NULL) AS raw_people_first_launch,
       (SELECT count(*) FROM mart_people m WHERE NOT EXISTS (SELECT 1 FROM raw_first r WHERE r.person_id = m.person_id))
         AS mart_without_raw_events,
       (SELECT count(*) FROM installations WHERE installation_class = 'real') AS real_installations,
       (SELECT count(*) FROM installations i WHERE installation_class = 'real'
          AND NOT EXISTS (SELECT 1 FROM product_events e WHERE e.installation_id = i.id)) AS installs_without_events,
       (SELECT count(*) FROM person_merge_log) AS person_merges;

\echo '=== C. DAU / WAU / MAU на вчера (последний полный день, МСК) ==='
WITH :raw_day, :mart_people, d AS (SELECT (now() AT TIME ZONE 'Europe/Moscow')::date - 1 AS d)
SELECT (SELECT d FROM d) AS day,
       (SELECT count(DISTINCT person_id) FROM raw_day, d WHERE day = d.d) AS dau_raw,
       (SELECT count(DISTINCT pd.person_id) FROM fct_person_day pd JOIN mart_people USING (person_id), d
          WHERE pd.is_active AND pd.day = d.d) AS dau_mart,
       (SELECT count(DISTINCT person_id) FROM raw_day, d WHERE day BETWEEN d.d - 6 AND d.d) AS wau_raw,
       (SELECT count(DISTINCT pd.person_id) FROM fct_person_day pd JOIN mart_people USING (person_id), d
          WHERE pd.is_active AND pd.day BETWEEN d.d - 6 AND d.d) AS wau_mart,
       (SELECT count(DISTINCT person_id) FROM raw_day, d WHERE day BETWEEN d.d - 29 AND d.d) AS mau_raw,
       (SELECT count(DISTINCT pd.person_id) FROM fct_person_day pd JOIN mart_people USING (person_id), d
          WHERE pd.is_active AND pd.day BETWEEN d.d - 29 AND d.d) AS mau_mart;

\echo '=== D. Недельные когорты: люди, план, G1, G2 — витрина против сырых событий ==='
\echo '    G2 = хотя бы один активный день с 7-го по 13-й день жизни среди зафиксировавших план (как в дашборде)'
WITH :raw_day, :raw_first, :mart_people, c AS (
  SELECT m.person_id, m.cohort_week, m.first_seen_date, m.plan_fixed_at, m.core_action_at,
         ((now() AT TIME ZONE 'Europe/Moscow')::date - m.first_seen_date) AS age,
         (r.first_event_at AT TIME ZONE 'Europe/Moscow')::date AS raw_first_day
  FROM mart_people m LEFT JOIN raw_first r USING (person_id)
  WHERE m.first_seen_date >= '2026-08-31'
)
SELECT cohort_week,
       count(*) AS people_mart,
       count(*) FILTER (WHERE raw_first_day <> first_seen_date) AS first_day_differs,
       count(plan_fixed_at) AS with_plan,
       count(*) FILTER (WHERE plan_fixed_at IS NOT NULL AND age >= 2) AS g1_base,
       count(*) FILTER (WHERE plan_fixed_at IS NOT NULL AND age >= 2 AND core_action_at IS NOT NULL) AS g1_hit,
       count(*) FILTER (WHERE plan_fixed_at IS NOT NULL AND age >= 14) AS g2_base,
       count(*) FILTER (WHERE plan_fixed_at IS NOT NULL AND age >= 14 AND EXISTS (
          SELECT 1 FROM fct_person_day pd WHERE pd.person_id = c.person_id AND pd.is_active
            AND pd.day_no BETWEEN 7 AND 13)) AS g2_hit_mart,
       count(*) FILTER (WHERE plan_fixed_at IS NOT NULL AND age >= 14 AND EXISTS (
          SELECT 1 FROM raw_day rd WHERE rd.person_id = c.person_id
            AND rd.day - c.first_seen_date BETWEEN 7 AND 13)) AS g2_hit_raw
FROM c GROUP BY 1 ORDER BY 1;

\echo '=== E. Платящие: банк (payments) против витрины и событий приложения ==='
SELECT (SELECT count(*) FROM payments WHERE status = 'CONFIRMED') AS confirmed_payments,
       (SELECT count(DISTINCT a.person_id) FROM payments p JOIN accounts a ON a.id = p.account_id
          WHERE p.status = 'CONFIRMED') AS paying_people_bank,
       (SELECT sum(amount_kopecks) / 100 FROM payments WHERE status = 'CONFIRMED') AS rub_confirmed,
       (SELECT count(*) FROM fct_person WHERE first_purchase_at IS NOT NULL) AS paying_people_mart,
       (SELECT count(DISTINCT person_id) FROM fct_monetization_event WHERE event_name = 'purchase.succeeded')
         AS purchase_succeeded_people,
       (SELECT count(*) FROM subscriptions WHERE status = 'active') AS active_subscriptions;

\echo '=== F. Пейвол и переход к оплате: сырые события против витрины монетизации ==='
SELECT e.name,
       count(DISTINCT a.person_id) AS people_raw,
       (SELECT count(DISTINCT person_id) FROM fct_monetization_event m WHERE m.event_name = e.name) AS people_mart
FROM product_events e
JOIN person_aliases a ON a.alias_type = 'installation' AND a.alias_value = e.installation_id
WHERE e.name LIKE 'paywall%' OR e.name LIKE 'purchase%' OR e.name LIKE 'checkout%' OR e.name LIKE 'trial%'
   OR e.name LIKE 'pay_%' OR e.name LIKE 'subscription%'
GROUP BY 1 ORDER BY 2 DESC;

\echo '=== G. Загрузки App Store против первых запусков по неделям ==='
WITH :raw_first, :mart_people
SELECT w.week, w.asc_units,
       (SELECT count(*) FROM raw_first r WHERE date_trunc('week', r.first_event_at AT TIME ZONE 'Europe/Moscow')::date = w.week)
         AS raw_new_people,
       (SELECT count(*) FROM mart_people m WHERE m.cohort_week = w.week) AS mart_new_people
FROM (SELECT date_trunc('week', day)::date AS week, sum(units) AS asc_units
      FROM ext_appstore_daily WHERE day >= '2026-08-31' GROUP BY 1) w
ORDER BY 1;
