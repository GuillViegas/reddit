from submission.models import Submission

class Ecosystem:

    __search_engine = None

    def __init__(self, search_engine):
        self.__search_engine = search_engine

    def createEcosystem(self, submission_id=None, seed_params=None, max_interactions=None):

        try:
            submission = Submission.objects.get(submission_id)
        except Submission.DoesNotExist:
            if submission_id:
                submission = self.__search_engine.retrive_submission_by_id(submission_id)

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

        while(interactions < max_interactions if max_interactions else True):
            comments = self.__search_engine.retrive_submission_comments(seed.id)
            interactions += 1
