# Задание агенту бэкенда: выгрузка прода для GTM

Нужно для GTM-стратегии и для сверки цифр дашборда PMF. Только чтение, без персональных данных.

## Самый простой путь

Из репозитория `pokirill/kubysh-marketos`, ветка `claude/jolly-noether-pgpg7d`, с машины, где есть SSH к проду:

```bash
HOST=root@201.24.56.21 bash Docs/tools/prod/export.sh
```

Скрипт сам выполнит все запросы из `Docs/tools/prod/export/*.sql`, `verify_dashboard.sql` и `gtm_snapshot.sql`
в контейнере Postgres в режиме только чтения и соберет архив в `~/kubysh_prod_export/`. Запросы проверены на
схеме из `app/infrastructure/persistence/models.py` (04.11.2026).

## Если запускать по-своему — что достать

Все id людей заменить на `substr(md5(person_id),1,12)`. Почты, телефоны, имена, номера заказов, сырые уведомления
банка не выгружать. Сначала `SELECT * FROM mart_build_state` — витрина должна быть сегодняшней.

1. **Люди:** `fct_person` целиком (реальные и нет, с `install_class`), включая `source/campaign`, страну, версии,
   даты онбординга, плана, первой траты, активации, триала, покупки, `active_weeks`, `emergency_enabled`,
   `goals_count`, `growth_events_json`.
2. **Активность двумя путями:** `fct_person_day` и активные дни по сырым `product_events` (человек × день МСК,
   активность как в `app/analytics/activity.py`) — чтобы сверить DAU/WAU/MAU и G2.
3. **События:** по каждому человеку и событию — сколько раз, первый и последний раз, в скольких днях; плюс
   события по дням; отбракованные события по дням и причинам.
4. **Установки:** `installations` + `installation_geo` (канал, метки, страна, локаль, версия, есть ли push-токен).
5. **Онбординг и периоды:** `fct_funnel_step`, `fct_paycheck_period`.
6. **Деньги:** `fct_monetization_event`, `payments` (статус, ошибка, тариф, сумма, даты), `payment_analytics_events`,
   `subscriptions`, `web_checkouts` (место показа, открыта ли).
7. **Рост:** `person_referrals`, `bank_connections` (банк, состояние, последняя синхронизация), количество
   `person_merge_log`.
8. **App Store:** `ext_appstore_daily`, `ext_appstore_source_daily`, `dim_release`.

Формат: CSV на каждую таблицу, архивом. Плюс ответ: совпадают ли витрина и сырые события по людям, DAU/WAU/MAU,
G1/G2 по недельным когортам и числу платящих (`payments.status = 'CONFIRMED'` против `fct_person.first_purchase_at`).
