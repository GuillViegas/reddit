from submission.models import Submission
from datetime import datetime
from engine.engine import SearchEngine

class Ecosystem:

    __search_engine = None
    __seed = None
    __subreddit = None
    __comments = []
    __submissions = []
    __redditors = []

    def __init__(self, search_engine=None):
        self.__search_engine = search_engine or SearchEngine()

    # def __filter_comments(self, comments, score=0):
    #     self.__comments.extend([
    #         comment for comment in comments
    #         if self.__search_engine.submission_score(comment.id) > score])

    # def __filter_redditors(self, comments, popularity=0):
    #     redditors = filter(
    #         lambda author: (author['submissions_karma'] + author['submissions_karma']) > score,
    #         [self.__search_engine.redditor_info(comment.author) for comment in comments])

    #     self.__redditors.extend(redditors)

    #     return redditors

    def create(
        self,
        submission_id=None,
        seed_params={
            'subreddit': None,
            'before': None,
            'after': None
        },
        domain=None,
        max_interactions=None,
        save=True):
        import time
        t = time.process_time()

        submission = None
        if submission_id:
            try:
                submission = Submission.objects.get(id=submission_id).to_dict()
            except Submission.DoesNotExist:
                submission = self.__search_engine.retrive_submission_by_id(submission_id)

        if not submission:
            submission = self.__search_engine.most_commented_submissions(
                                    subreddit=seed_params.get('subreddit'),
                                    before=seed_params.get('before'),
                                    after=seed_params.get('after'),
                                    limit=1)[0]

        # move this logic to another place, maybe submission app
        # Submission.objects.create(
        #     id=submission.id,
        #     title=submission.title,
        #     body=submission.selftext,
        #     url=submission.url,
        #     subreddit=submission.subreddit,
        #     author=submission.author,
        #     score=self.__search_engine.submission_score(submission.id),
        #     num_comments=submission.num_comments,
        #     num_writers=len(self.__search_engine.submission_writters(submission_id)),
        #     created_at=datetime.fromtimestamp(submission.created_utc),
        #     retrived_on=datetime.fromtimestamp(submission.retrieved_on)
        # )

        self.__seed = submission
        # if submission belongs to any subreddit
        self.__subreddit = self.__seed['subreddit'] if self.__seed['subreddit'][:2] != 'u_' else None


        redditor = self.__seed['author']
        self.__redditors = [redditor]
        print(redditor)

        r_idx = 0
        while r_idx < len(self.__redditors):
            print(len(self.__redditors))
            submissions = self.__search_engine.retrive_redditor_submissions(self.__redditors[r_idx], domain)
            comments = []

            print(time.process_time() - t)
            for i, submission in enumerate(submissions):
                print("%d/%d" % (i+1, len(submissions)))
                comments += self.__search_engine.retrive_submission_comments(submission['id'])

            self.__submissions += submissions
            self.__comments += comments

            self.__redditors += list({comment['author'] for comment in comments} - set(self.__redditors))

            r_idx += 1

