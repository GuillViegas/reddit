from praw import Reddit
from psaw import PushshiftAPI
from engine.models import RedditCredential

class SearchEngine:

    __rd_socket = None
    __ps_api = None

    def __init__(self, user_agent, use_praw=False):
        rd_credential = RedditCredential.objects.get(user_agent=user_agent)
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

    def search_by_num_comments():
        pass
