SELECT count(*) as num_comments
FROM submission_comment AS com
WHERE com.created_at > %(after)s and com.created_at < %(before)s
GROUP BY com.submission_id
ORDER BY num_comments
