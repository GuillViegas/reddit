from datetime import datetime

from engine.models import RedditCredential

from submission.models import Submission, Comment

from praw import Reddit
from psaw import PushshiftAPI


class SearchEngine:

    __rd_socket = None
    __ps_api = None

    def __init__(self, user_agent=False, use_praw=False):
        rd_credential = (
            RedditCredential.objects.get(user_agent=user_agent) if user_agent else RedditCredential.objects.first()
        )

        self.__rd_socket = Reddit(
            client_id=rd_credential.client_id,
            client_secret=rd_credential.client_secret,
            user_agent=rd_credential.user_agent)

        self.__ps_api = PushshiftAPI(self.__rd_socket if use_praw else None)

    def new_credential(client_id, client_secret, user_agent, domain):
        rd_credential = RedditCredential(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            domain=domain,
        )
        rd_credential.save()

    def most_commented_submissions(self, subreddit=None, before=None, after=None, limit=10):
        return [
        {
            'id': submission.id,
            'title': submission.title,
            'body': submission.selftext,
            'url': submission.url,
            'subreddit': submission.subreddit,
            'author': submission.author,
            'num_comments': submission.num_comments,
            'created_at': datetime.utcfromtimestamp(submission.created_utc),
            'retrieved_on': datetime.utcfromtimestamp(submission.retrieved_on)
        }
        for submission in self.__ps_api.search_submissions(
                before=datetime.strptime(before, "%d-%m-%Y") if before else None,
                after=datetime.strptime(after, "%d-%m-%Y") if after else None,
                subreddit=subreddit,
                sort_type='num_comments',
                limit=limit
        )] or [None]

    def retrive_submission_by_id(self, submission_id):
        submission = self.__rd_socket.submission(id=submission_id)

        submission = {
            'id': submission.id,
            'title': submission.title,
            'body': submission.selftext,
            'url': submission.url,
            'subreddit': submission.subreddit.display_name,
            'author': submission.author.name,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'created_at': datetime.utcfromtimestamp(submission.created_utc),
            'retrieved_on': datetime.now()
        }

        return submission

    def retrive_submission_comments(self, submission_id, before=None, after=None, method='psaw'):
        comments = None

        if method == 'psaw':
            comments = [
                {
                    'id': comment.id,
                    'author': comment.author,
                    'body': comment.body,
                    'created_at': datetime.utcfromtimestamp(comment.created_utc),
                    'submission': comment.link_id.split('_')[1],
                    'parent': comment.parent_id.split('_')[1],
                    'retrieved_on': datetime.utcfromtimestamp(comment.retrieved_on)
                }
                for comment in self.__ps_api.search_comments(
                link_id=submission_id,
                after=datetime.strptime(after, "%d-%m-%Y") if after else None,
                before=datetime.strptime(before, "%d-%m-%Y") if before else None,
            )]

        if method == 'praw' or not comments:
            comments = [
                {
                    'id': comment.id,
                    'author': comment.author.name if comment.author else None,
                    'body': comment.body,
                    'score': comment.score,
                    'created_at': datetime.utcfromtimestamp(comment.created_utc),
                    'submission': comment._submission.id,
                    'parent': comment.parent_id.split('_')[1],
                    'retrieved_on': datetime.now()
                }

            for comment in self.__rd_socket.submission(id=submission_id).comments.replace_more(limit=0)]

        return  comments

    def retrive_redditor_submissions(self, redditor, domain=None, before=None, after=None, method='psaw'):
        submission = None

        if method == 'psaw':
            submissions = [
            {
                'id': submission.id,
                'title': submission.title,
                'body': submission.selftext,
                'url': submission.url,
                'subreddit': submission.subreddit,
                'author': submission.author,
                'num_comments': submission.num_comments,
                'created_at': datetime.utcfromtimestamp(submission.created_utc),
                'retrieved_on': datetime.utcfromtimestamp(submission.retrieved_on)
            } for submission in self.__ps_api.search_submissions(
                    author=redditor,
                    domain=domain,
                    before=datetime.strptime(before, "%d-%m-%Y") if before else None,
                    after=datetime.strptime(after, "%d-%m-%Y") if after else None
                )
            ]

        if method == 'praw' or not submissions:
            submissions = [{
                    'id': submission.id,
                    'title': submission.title,
                    'body': submission.selftext,
                    'url': submission.url,
                    'subreddit': submission.subreddit.display_name,
                    'author': submission.author.name,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_at': datetime.utcfromtimestamp(submission.created_utc),
                    'retrieved_on': datetime.now()
                }
            for submission in self.__rd_socket.redditor(redditor).submissions.new()
            if not domain or submission.subreddit.display_name in domain]

        return submissions

    def redditor_info(self, redditor):
        redditor = self.__rd_socket.redditor(redditor)

        return {
            'name': redditor.name,
            'submissions_karma': redditor.link_karma,
            'comments_karma': redditor.comment_karma,
            'created_at': datetime.utcfromtimestamp(redditor.created_utc)
        }

    def subreddit_info(self, subreddit):
        subreddit = self.__rd_socket.subreddit(subreddit)

        return {
            'name': subreddit.display_name,
            'description': subreddit.description[:5000],
            'short_description': subreddit.public_description,
            'num_subscribers': subreddit.subscribers,
            'created_at': datetime.utcfromtimestamp(subreddit.created_utc),
            'last_update': datetime.now()
        }
