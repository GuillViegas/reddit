SELECT ruser.name, ruser.submissions_karma, ruser.comments_karma, ruser.created_at, ruser.last_update, count(submission.id) num_submissions
  FROM public.submission_reddituser AS ruser
	LEFT JOIN public.submission_submission AS submission
		ON submission.author_id = ruser.name
  WHERE submission.created_at > %(after)s and submission.created_at < %(before)s
  GROUP BY ruser.name
  ORDER BY num_submissions DESC
