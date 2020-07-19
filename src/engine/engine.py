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

    def most_commented_post(subreddit, after=None, before=None, limit=10):
        return self.__ps_api.search_submissions(
            after=datetime.strptime(after, "%d-%m-%Y"),
            before=datetime.strptime(before, "%d-%m-%Y"),
            subreddit=subreddit,
            sort_type='num_comments',
            limit=limit
        )

    def retrive_post_comments(post_id):
        return self.__ps_api.search_comments(

        )

    def retrive_author_posts(author):
        pass
