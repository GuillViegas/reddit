SELECT count(*)
FROM submission_comment AS com
WHERE com.created_at > %(after)s and com.created_at < %(before)s
