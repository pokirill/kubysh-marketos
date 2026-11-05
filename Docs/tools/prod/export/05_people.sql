SELECT substr(md5(person_id), 1, 12) AS p, install_class, distribution_channel,
       source, campaign, creative_id, content_id, influencer_id, country_code, language,
       first_seen_at AT TIME ZONE 'Europe/Moscow' AS first_seen_msk, first_seen_date, cohort_week,
       first_version, last_version, last_seen_at AT TIME ZONE 'Europe/Moscow' AS last_seen_msk,
       last_active_at AT TIME ZONE 'Europe/Moscow' AS last_active_msk,
       onboarding_completed_at, first_paycheck_open_at, plan_fixed_at, first_tx_at, tx_count_48h,
       core_action_at, activated_48h, activation_event_at, activation_source, habit_14d, habit_tx_days_14d,
       first_ai_message_at, trial_started_at, trial_end_at, trial_length_days, subscription_status,
       first_purchase_at, first_period_end_at, periods_started, periods_closed,
       active_days, active_weeks, max_consecutive_tx_weeks,
       emergency_enabled, has_already_saved, goals_count, days_to_next_paycheck,
       onboarding_variant, paywall_variant, offer_variant, lifecycle_state,
       growth_events_json::text AS growth_events
FROM fct_person ORDER BY first_seen_at
