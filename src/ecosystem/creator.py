from submission.models import Submission
from datetime import datetime

class Ecosystem:

    __search_engine = None

    def __init__(self, search_engine):
        self.__search_engine = search_engine

    def createEcosystem(
        self,
        submission_id=None,
        seed_params={
            'subreddit': None,
            'before': None,
            'after': None
        },
        max_interactions=None,
        save=True):

        if submission_id:
            try:
                submission = Submission.objects.get(submission_id)
            except Submission.DoesNotExist:
                submission = self.__search_engine.retrive_submission_by_id(submission_id)

                # move this logic to another place, maybe submission app
                Submission.objects.create(
                    id=submission.id,
                    title=submission.title,
                    body=submission.selftext,
                    url=submission.url,
                    subreddit=submission.subreddit,
                    author=submission.author,
                    score=__search_engine.submission_score(submission.id),
                    num_comments=submission.num_comments,
                    num_writers=__search_engine.submission_writters(submission_id),
                    created_at=datetime.fromtimestamp(submission.created_utc),
                    retrived_on=datetime.fromtimestamp(submission.retrieved_on)
                )

        if not submission:
            submission = (self.__search_engine.most_commented_submissions(
                                    subreddit=seed_params.get('subrredit'),
                                    before=seed_params.get('before'),
                                    after=seed_params.get('after'),
                                    limit=1) or [None])[0]

        seed = submission
        comments = []
        submissions = [seed]
        users = [seed.author]
        interactions = 0

        # to save multiple instances bulk_create
        while(interactions < max_interactions if max_interactions else True):
            comments = self.__search_engine.retrive_submission_comments(seed.id)

            interactions += 1
