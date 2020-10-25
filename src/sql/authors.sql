SELECT DISTINCT author_id as author
FROM submission_comment
WHERE created_at > %(after)s and created_at < %(before)s
