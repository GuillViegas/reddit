from praw import Reddit
from engine.models import RedditCredential

class SearchEngine:

    __rd_socket = None

    def __init__(self, user_agent):
        rd_credential = RedditCredential.objects.get(user_agent=user_agent)
        self.__rd_socket = Reddit(
            client_id=rd_credential.client_id, 
            client_secret=rd_credential.client_secret, 
            user_agent=rd_credential.user_agent)

    def new_credential(client_id, client_secret, user_agent, domain):
        rd_credential = RedditCredential(
            client_id=client_id, 
            client_secret=client_secret,
            user_agent=user_agent,
            domain=domain,
        )
        rd_credential.save()

    

