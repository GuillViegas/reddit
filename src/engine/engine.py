from datetime import datetime

from praw import Reddit
from psaw import PushshiftAPI

from engine.models import RedditCredential

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
        return list(self.__ps_api.search_submissions(
            before=datetime.strptime(before, "%d-%m-%Y") if before else None,
            after=datetime.strptime(after, "%d-%m-%Y") if after else None,
            subreddit=subreddit,
            sort_type='num_comments',
            limit=limit
        ))

    def retrive_submission_by_id(self, submission_id):
        return (list(self.__ps_api.search_submissions(
            ids=[submission_id]
        )) or [None])[0]

    def retrive_submission_comments(self, submission_id, before=None, after=None):
        return list(self.__ps_api.search_comments(
            link_id=submission_id
        ))

    def retrive_redditor_submissions(self, redditor, before=None, after=None):
        return list(self.__ps_api.search_comments(
            author=redditor,
            before=datetime.strptime(before, "%d-%m-%Y") if before else None,
            after=datetime.strptime(after, "%d-%m-%Y") if after else None
        ))

    def redditor_info(self, redditor):
        redditor = self.__rd_socket.redditor(redditor)

        return {
            'name': redditor.name,
            'submissions_karma': redditor.link_karma,
            'comments_karma': redditor.comment_karma,
            'created_at': datetime.utcfromtimestamp(redditor.created_utc)
        }

    def submission_score(self, submission_id):
        return self.__rd_socket.submission(submission_id).score()

    def submission_writters(self, submission_id):
        return len(set(comment.author for comment in self.__ps_api.search_comments(link_id=[submission_id])))
