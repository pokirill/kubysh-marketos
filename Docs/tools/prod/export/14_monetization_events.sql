SELECT substr(md5(person_id), 1, 12) AS p, event_name, occurred_at AT TIME ZONE 'Europe/Moscow' AS occurred_msk,
       product, placement, price_minor, currency, is_trial, failure_reason,
       onboarding_variant, paywall_variant, offer_variant
FROM fct_monetization_event ORDER BY occurred_at
