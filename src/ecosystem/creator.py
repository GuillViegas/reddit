from submission.models import (
    Comment,
    RedditUser,
    Submission,
    SubReddit)

from ecosystem.models import Seed
from datetime import datetime
from engine.engine import SearchEngine
from django.core.exceptions import ObjectDoesNotExist

class Ecosystem:

    __search_engine = None
    __seed = None
    __subreddit = set()
    __comments = []
    __submissions = []
    __redditors = []
    __r_idx = 0

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
            'seed_id': None,
            'subreddit': None,
            'before': None,
            'after': None
        },
        domain=None,
        max_attempts=3,
        max_interactions=None,
        save=True):

        import time
        t = time.process_time()

        if seed_params.get('seed_id'):
            self.__seed = Seed.objects.get(id='seed_id')
            self.__redditors = self.__seed.redditors
            self.__r_idx = self.__seed.r_idx
            self.__comments = self.__seed.comments
            self.__submissions = self.__seed.submissions
            self.__subreddit = set(self.__seed.subreddits)

        else:
            submission = None
            if submission_id:
                try:
                    submission = Submission.objects.get(id=submission_id)
                except ObjectDoesNotExist:
                    submission = self.__search_engine.retrive_submission_by_id(submission_id)

            if not submission:
                submission = self.__search_engine.most_commented_submissions(
                                        subreddit=seed_params.get('subreddit'),
                                        before=seed_params.get('before'),
                                        after=seed_params.get('after'),
                                        limit=1)[0]
                try:
                    submission = Submission.objects.get(id=submission['id'])
                except ObjectDoesNotExist:
                    try:
                        submission['subreddit'] = SubReddit.objects.get(name=submission['subreddit'])
                    except ObjectDoesNotExist:
                        subreddit = SubReddit(**self.__search_engine.subreddit_info(submission['subreddit']))
                        subreddit.save()

                        submission['subreddit'] = subreddit

                    try:
                        submission['author'] = RedditUser.objects.get(name=submission['author'])
                    except ObjectDoesNotExist:
                        author = RedditUser(**self.__search_engine.redditor_info(submission['author']))
                        author.save()

                        submission['author'] = author

                    submission = Submission(**submission)
                    submission.save()

            submission_seed = submission.to_dict()
            seed = Seed(seed=submission)
            seed.save()
            self.__seed = seed

            # if submission belongs to any subreddit
            self.__subreddit.add(submission_seed['subreddit'] if submission_seed['subreddit'][:2] != 'u_' else None)


            redditor = submission_seed['author']
            self.__redditors = [redditor.name]
            print(redditor.name)

            attempts = 0
            errors = []

        while self.__r_idx < len(self.__redditors):
            print(len(self.__redditors))

            try:
                redditor = RedditUser.objects.get(name=self.__redditors[self.__r_idx])
            except ObjectDoesNotExist:
                redditor = RedditUser(**self.__search_engine.redditor_info(self.__redditors[self.__r_idx]))
                redditor.save()

            try:
                submissions = self.__search_engine.retrive_redditor_submissions(self.__redditors[self.__r_idx], domain)

                for submission in submissions:
                    submission['author'] = redditor

                    try:
                        submission['subreddit'] = SubReddit.objects.get(name=submission['subreddit'])
                    except ObjectDoesNotExist:
                        subreddit = SubReddit(**self.__search_engine.subreddit_info(submission['subreddit']))
                        subreddit.save()

                        submission['subreddit'] = subreddit
                        self.__subreddit = self.__subreddit | {subreddit.name}

                submission_bulk = [Submission(**submission) for submission in submissions]

                comments = []

                print(time.process_time() - t)
                for i, submission in enumerate(submissions):
                    print("%d/%d" % (i+1, len(submissions)))
                    submission_comments = self.__search_engine.retrive_submission_comments(submission['id'])

                    for comment in submission_comments:
                        try:
                            comment['author'] = RedditUser.objects.get(name=comment['author'])
                        except ObjectDoesNotExist:
                            try:
                                author = RedditUser(**self.__search_engine.redditor_info(comment['author']))
                                author.save()

                                comment['author'] = author

                            except Exception:
                                pass

                        comment['submission'] = Submission(id=comment['submission'])

                    comments += submission_comments
                comments = [comment for comment in comments if not isinstance(comment['author'], str)]
                comment_bulk = [Comment(**comment) for comment in comments]

            except Exception as ex:
                if attempts < max_attempts:
                    attempts += 1

                else:
                    errors.append(self.__redditors[self.__r_idx])
                    attempts = 0
                    self.__r_idx += 1

                continue

            Submission.objects.bulk_create(submission_bulk, ignore_conflicts=True)
            self.__submissions += [submission['id'] for submissions in submissions]
            Comment.objects.bulk_create(comment_bulk, ignore_conflicts=True)
            self.__comments += [comment['id'] for comment in comments]

            self.__redditors += list({comment['author'].name for comment in comments} - set(self.__redditors))

            self.__r_idx += 1

            self.__seed.r_idx = self.__r_idx
            self.__seed.submissions = self.__submissions
            self.__seed.comments = self.__comments
            self.__seed.redditors = self.__redditors
            self.__seed.subreddits = list(self.__subreddit)
            self.__seed.save()

