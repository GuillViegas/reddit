SELECT count(*)
FROM submission_submission AS sub
WHERE sub.id IN (
    SELECT submission_id
    FROM submission_comment
)
AND sub.created_at > %(after)s and sub.created_at < %(before)s
