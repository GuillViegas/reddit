  SELECT ruser.name, ruser.submissions_karma, ruser.comments_karma, ruser.created_at, ruser.last_update, count(comment.id) num_comments
  FROM public.submission_reddituser AS ruser
	LEFT JOIN public.submission_comment AS comment
		ON comment.author_id = ruser.name
  WHERE comment.created_at > %(after)s and comment.created_at < %(before)s
  GROUP BY ruser.name
  ORDER BY num_comments DESC
