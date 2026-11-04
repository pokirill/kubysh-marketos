SELECT substr(md5(b.id), 1, 12) AS conn, substr(md5(a.person_id), 1, 12) AS p, b.provider, b.state,
       b.generation, b.last_success_at
FROM bank_connections b LEFT JOIN accounts a ON a.id = b.account_id
