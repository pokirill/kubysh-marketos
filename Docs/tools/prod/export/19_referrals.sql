SELECT substr(md5(person_id), 1, 12) AS p, substr(md5(invited_by_person_id), 1, 12) AS invited_by, invited_at
FROM person_referrals ORDER BY invited_at
