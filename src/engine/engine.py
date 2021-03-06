from datetime import datetime

from engine.models import RedditCredential

from submission.models import Submission, Comment, RedditUser

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
                    'author_id': comment.author,
                    'body': comment.body,
                    'created_at': datetime.utcfromtimestamp(comment.created_utc),
                    'submission_id': comment.link_id.split('_')[1],
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
                    'author_id': comment.author.name if comment.author else None,
                    'body': comment.body,
                    'score': comment.score,
                    'created_at': datetime.utcfromtimestamp(comment.created_utc),
                    'submission_id': comment._submission.id,
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
            'name': getattr(redditor, 'name'),
            'submissions_karma': getattr(redditor, 'link_karma'),
            'comments_karma': getattr(redditor, 'comment_karma'),
            'created_at': datetime.utcfromtimestamp(getattr(redditor, 'created_utc'))
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

    def update_comments_score(self, comments_id):

        num_comments = len(comments_id)
        for i, comment_id in enumerate(comments_id):
            try:
                comment = Comment.objects.get(id=comment_id)
                score = self.__rd_socket.comment(id=comment_id).score
                comment.score = int(score)
                comment.save()
            except Exception as ex:
                print(ex)
                pass

            if i % 500 == 0:
                print(f'{i+1}/{num_comments}')

        print(f'{i+1}/{num_comments}')

    def update_submissions_score(self, submissions_id):

        num_submissions = len(submissions_id)
        for i, submission_id in enumerate(submissions_id):
            submission = Submission.objects.get(id=submission_id)
            score = self.__rd_socket.submission(id=submission_id).score
            submission.score = score
            submission.save()

            if i % 500 == 0:
                print(f'{i+1}/{num_submissions}')

        print(f'{i+1}/{num_submissions}')

    def update_submissions_comments(self, submissions_ids=None):
        comments_ids = {comment.id for comment in Comment.objects.all()}
        authors_names = {author.name for author in RedditUser.objects.all()}
        submissions = Submission.objects.filter(id__in=submissions_ids) if submissions_ids else Submission.objects.all()

        for i, submission in enumerate(submissions):
            print(f'{i}/{len(submissions)} - {submission.id}')
            comments = [
                comment for comment in self.retrive_submission_comments(submission.id)
                if comment['id'] not in comments_ids]

            authors = [
                comment['author_id'] for comment in comments
                if comment['author_id'] not in authors_names]

            authors_bulk = []
            for author in authors:
                try:
                    authors_bulk.append(RedditUser(**self.redditor_info(author)))
                except Exception:
                    authors_bulk.append(RedditUser(name=author))

            RedditUser.objects.bulk_create(authors_bulk, ignore_conflicts=True)

            comments = [Comment(**comment) for comment in comments]
            Comment.objects.bulk_create(comments, ignore_conflicts=True)
