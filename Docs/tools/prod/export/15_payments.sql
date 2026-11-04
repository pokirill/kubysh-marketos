-- Без почт, телефонов, номеров заказов и сырых уведомлений банка.
SELECT substr(md5(p.id), 1, 12) AS payment, substr(md5(a.person_id), 1, 12) AS p,
       substr(md5(p.subscription_id), 1, 12) AS sub, substr(md5(p.checkout_id), 1, 12) AS checkout,
       p.provider, p.plan, p.amount_kopecks, p.currency, p.status, p.error_code, p.is_recurrent_init,
       p.created_at AT TIME ZONE 'Europe/Moscow' AS created_msk,
       p.confirmed_at AT TIME ZONE 'Europe/Moscow' AS confirmed_msk
FROM payments p LEFT JOIN accounts a ON a.id = p.account_id
ORDER BY p.created_at
