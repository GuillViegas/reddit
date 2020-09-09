from submission.models import Submission
from datetime import datetime

class Ecosystem:

    __search_engine = None
    __seed = None
    __comments = None
    __submissions = None
    __redditors = None

    def __init__(self, search_engine):
        self.__search_engine = search_engine

    def __filter_comments(self, comments, score=0):
        self.__comments.extend([
            comment for comment in comments
            if self.__search_engine.submission_score(comment.id) > score])

    def __filter_redditors(self, comments, popularity=0):
        self.__redditors.extend(filter(
            lambda author: (author['submissions_karma'] + author['submissions_karma']) > score,
            [expression[self.__search_engine.redditor_info(comment.author) for comment in comments]))

    def createEcosystem(
        self,
        submission_id=None,
        seed_params={
            'subreddit': None,
            'before': None,
            'after': None
        },
        filters={
            'submssions': {
                'score': 0
            },
            'comments': {
                'score': 0
            },
            'reddituser': {
                'popularity': 0
            }
        },
        max_interactions=None,
        save=True):

        if submission_id:
            try:
                submission = Submission.objects.get(submission_id)
            except Submission.DoesNotExist:
                submission = self.__search_engine.retrive_submission_by_id(submission_id)

        if not submission:
            submission = (self.__search_engine.most_commented_submissions(
                                    subreddit=seed_params.get('subrredit'),
                                    before=seed_params.get('before'),
                                    after=seed_params.get('after'),
                                    limit=1) or [None])[0]

        # move this logic to another place, maybe submission app
        # Submission.objects.create(
        #     id=submission.id,
        #     title=submission.title,
        #     body=submission.selftext,
        #     url=submission.url,
        #     subreddit=submission.subreddit,
        #     author=submission.author,
        #     score=__search_engine.submission_score(submission.id),
        #     num_comments=submission.num_comments,
        #     num_writers=__search_engine.submission_writters(submission_id),
        #     created_at=datetime.fromtimestamp(submission.created_utc),
        #     retrived_on=datetime.fromtimestamp(submission.retrieved_on)
        # )

        self.__seed = submission
        self.__comments = []
        self.__submissions = [seed]
        self.__redditor = [self.__seed.author]
        interactions = 0

        # to save multiple instances bulk_create
        while(interactions < max_interactions if max_interactions else True):
            comments = self.__search_engine.retrive_submission_comments(seed.id)
            self.__filter_comments(comments, filters['comments']['score'])
            self.__filter_redditors(comments, filters['reddituser']['popularity']

            interactions += 1
