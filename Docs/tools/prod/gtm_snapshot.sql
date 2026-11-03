-- Срез прода для GTM-стратегии. Только чтение, без персональных данных (почты, телефоны, имена не выбираются).
-- Дополняет дашборд PMF: каналы, страны, оплата по шагам, рефералы, банки, сегменты Макс/Ксюша.
-- Запуск: Docs/tools/prod/gtm_snapshot.sh (см. шапку там). Схема сверена с finik-backend
-- app/infrastructure/persistence/models.py на 03.11.2026.

\pset pager off
\pset footer off
\set ON_ERROR_ROLLBACK on
SET statement_timeout = '60s';
BEGIN READ ONLY;

\echo '=== 0. Свежесть витрины: built_at должен быть сегодняшним ==='
SELECT key, built_at AT TIME ZONE 'Europe/Moscow' AS built_msk, as_of_date, build_kind,
       source_max_received_at AT TIME ZONE 'Europe/Moscow' AS last_event_msk
FROM mart_build_state ORDER BY built_at DESC;

\echo '=== 0b. Релизы с 1.7 (даты для когорт до/после пейвола) ==='
SELECT app_version, build, released_at::date, channel
FROM dim_release WHERE app_version >= '1.7' ORDER BY released_at;

\echo '=== 1. App Store: загрузки и конверсия страницы по неделям и странам (с 01.09) ==='
SELECT date_trunc('week', day)::date AS week, territory,
       sum(impressions) AS impressions, sum(page_views) AS page_views, sum(units) AS units,
       round(100.0 * sum(units) / nullif(sum(page_views), 0), 1) AS view_to_unit_pct
FROM ext_appstore_daily WHERE day >= '2026-09-01'
GROUP BY 1, 2 ORDER BY 1, units DESC;

\echo '=== 2. App Store: источники загрузок по неделям (поиск, просмотр, веб, приложения) ==='
SELECT date_trunc('week', day)::date AS week, source_type, metric, sum(value) AS value
FROM ext_appstore_source_daily WHERE day >= '2026-09-01'
GROUP BY 1, 2, 3 ORDER BY 1, 3, 4 DESC;

\echo '=== 3. Люди по метке атрибуции (source/campaign) с 01.09: дошли ли до активации и оплаты ==='
SELECT source, campaign, count(*) AS people,
       count(plan_fixed_at) AS plan_fixed,
       count(*) FILTER (WHERE activated_48h) AS activated_48h,
       count(*) FILTER (WHERE active_weeks >= 2) AS active_2w_plus,
       count(trial_started_at) AS trial,
       count(first_purchase_at) AS paid
FROM fct_person
WHERE install_class = 'real' AND first_seen_date >= '2026-09-01'
GROUP BY 1, 2 ORDER BY people DESC LIMIT 40;

\echo '=== 4. Страны (по гео установки) с 01.09 ==='
SELECT coalesce(country_code, '??') AS country, count(*) AS people,
       count(*) FILTER (WHERE activated_48h) AS activated_48h,
       count(first_purchase_at) AS paid
FROM fct_person
WHERE install_class = 'real' AND first_seen_date >= '2026-09-01'
GROUP BY 1 ORDER BY people DESC LIMIT 15;

\echo '=== 5. Оплаты: все попытки по провайдеру, тарифу и статусу ==='
SELECT provider, plan, status, error_code, is_recurrent_init,
       count(*) AS attempts, sum(amount_kopecks) / 100 AS rub
FROM payments GROUP BY 1, 2, 3, 4, 5 ORDER BY attempts DESC;

\echo '=== 5b. Подтвержденные оплаты по одной (без данных человека): когда, тариф, сумма, версия, канал, дни от установки ==='
SELECT p.confirmed_at AT TIME ZONE 'Europe/Moscow' AS confirmed_msk, p.provider, p.plan,
       p.amount_kopecks / 100 AS rub, p.is_recurrent_init,
       fp.first_version, fp.last_version, fp.source, fp.campaign, fp.country_code,
       (p.confirmed_at::date - fp.first_seen_date) AS days_from_install,
       fp.active_weeks, fp.goals_count, fp.emergency_enabled
FROM payments p
JOIN accounts a ON a.id = p.account_id
LEFT JOIN fct_person fp ON fp.person_id = a.person_id
WHERE p.status = 'CONFIRMED'
ORDER BY p.confirmed_at;

\echo '=== 5c. Подписки по статусу и тарифу (активные, отмененные, с неудачными списаниями) ==='
SELECT provider, plan, status, count(*) AS subs,
       count(cancel_requested_at) AS cancel_requested,
       count(*) FILTER (WHERE failed_charge_count > 0) AS failed_charges
FROM subscriptions GROUP BY 1, 2, 3 ORDER BY subs DESC;

\echo '=== 6. Страница оплаты: создано и открыто ссылок по месту показа и неделе ==='
SELECT date_trunc('week', expires_at)::date AS week_by_expiry, placement,
       count(*) AS checkouts, count(opened_at) AS opened,
       count(DISTINCT p.checkout_id) AS with_payment_attempt,
       count(DISTINCT p.checkout_id) FILTER (WHERE p.status = 'CONFIRMED') AS paid
FROM web_checkouts w
LEFT JOIN payments p ON p.checkout_id = w.id
GROUP BY 1, 2 ORDER BY 1, 2;

\echo '=== 6b. Попытки оплаты по неделям: создано, подтверждено, отклонено ==='
SELECT date_trunc('week', created_at)::date AS week, provider,
       count(*) AS attempts,
       count(*) FILTER (WHERE status = 'CONFIRMED') AS confirmed,
       count(*) FILTER (WHERE status IN ('REJECTED', 'CANCELED', 'DEADLINE_EXPIRED', 'AUTH_FAIL')) AS failed,
       count(*) FILTER (WHERE status IN ('NEW', 'FORM_SHOWED')) AS abandoned
FROM payments GROUP BY 1, 2 ORDER BY 1, 2;

\echo '=== 7. Воронка монетизации: события по неделям (люди, не события) ==='
SELECT date_trunc('week', occurred_at)::date AS week, event_name,
       count(DISTINCT person_id) AS people, count(*) AS events
FROM fct_monetization_event WHERE occurred_at >= '2026-09-01'
GROUP BY 1, 2 ORDER BY 1, 2;

\echo '=== 7b. Где ломается оплата: причины неудач ==='
SELECT event_name, failure_reason, placement, count(*) AS events, count(DISTINCT person_id) AS people
FROM fct_monetization_event
WHERE failure_reason IS NOT NULL AND occurred_at >= '2026-09-01'
GROUP BY 1, 2, 3 ORDER BY events DESC;

\echo '=== 7c. Шаги оплаты на стороне бэкенда (payment_analytics_events) ==='
SELECT event_name, count(*) AS events, count(DISTINCT payment_id) AS payments,
       min(occurred_at)::date AS first_day, max(occurred_at)::date AS last_day
FROM payment_analytics_events GROUP BY 1 ORDER BY events DESC;

\echo '=== 8. Сарафан: приглашения по неделям и награды ==='
SELECT date_trunc('week', invited_at)::date AS week, count(*) AS invited_people,
       count(DISTINCT invited_by_person_id) AS inviters
FROM person_referrals GROUP BY 1 ORDER BY 1;
SELECT role, count(*) AS rewards, count(consumed_at) AS consumed FROM referral_rewards GROUP BY 1;

\echo '=== 9. Банки (1.7.6): подключения по банку и состоянию ==='
SELECT provider, state, count(*) AS connections, count(last_success_at) AS synced_ok
FROM bank_connections GROUP BY 1, 2 ORDER BY 1, 3 DESC;

\echo '=== 10. Сегменты онбординга (Макс = подушка, Ксюша = цели) с 01.09: активация, удержание, оплата ==='
SELECT CASE
         WHEN emergency_enabled AND coalesce(goals_count, 0) = 0 THEN 'только подушка'
         WHEN emergency_enabled AND goals_count > 0             THEN 'подушка + цели'
         WHEN NOT emergency_enabled AND goals_count > 0         THEN 'только цели'
         WHEN emergency_enabled IS NULL                         THEN 'не прошел шаг'
         ELSE 'ни подушки, ни целей' END AS segment,
       count(*) AS people,
       count(*) FILTER (WHERE activated_48h) AS activated_48h,
       count(*) FILTER (WHERE active_weeks >= 2) AS active_2w_plus,
       count(*) FILTER (WHERE active_weeks >= 4) AS active_4w_plus,
       count(first_purchase_at) AS paid
FROM fct_person
WHERE install_class = 'real' AND first_seen_date >= '2026-09-01'
GROUP BY 1 ORDER BY people DESC;

\echo '=== 11. Ядро: сколько людей живут с Кубышем 4+ недели (кандидаты в отзывы и сарафан) ==='
SELECT count(*) FILTER (WHERE active_weeks >= 4) AS w4_plus,
       count(*) FILTER (WHERE active_weeks >= 8) AS w8_plus,
       count(*) FILTER (WHERE last_active_at >= now() - interval '7 days' AND active_weeks >= 4) AS w4_plus_active_now,
       count(*) FILTER (WHERE habit_14d) AS habit_14d
FROM fct_person WHERE install_class = 'real';

\echo '=== 12. Сколько дней от установки до пейвола (первый период) ==='
SELECT percentile_cont(ARRAY[0.25, 0.5, 0.75]) WITHIN GROUP (
         ORDER BY extract(epoch FROM (first_period_end_at - first_seen_at)) / 86400) AS days_p25_p50_p75,
       count(first_period_end_at) AS people_with_period_end
FROM fct_person WHERE install_class = 'real' AND first_seen_date >= '2026-09-01';

ROLLBACK;
