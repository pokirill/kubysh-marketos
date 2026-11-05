SELECT substr(md5(person_id), 1, 12) AS p, day, day_no, is_active, sessions, session_seconds, events,
       tx_count, paycheck_opens, metric_opens, insight_shown, ai_messages, errors
FROM fct_person_day ORDER BY day, p
