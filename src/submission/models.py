from django.db import models

# Create your models here.
class Submission(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    title = models.CharField(max_length=300, blank=True, null=True)
    body = models.CharField(max_length=40000, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    subreddit = models.ForeignKey('submission.SubReddit', on_delete=models.PROTECT)
    author = models.ForeignKey('submission.RedditUser', on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField()
    num_comments = models.PositiveIntegerField()
    num_writers = models.PositiveIntegerField()
    created_at = models.DateTimeField()


class Comment(models.Model):
    author = models.ForeignKey('submission.RedditUser', on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=40000, blank=True, null=True)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    submission = models.ForeignKey("submission.Submission", null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey("submission.Comment", null=True, on_delete=models.CASCADE)


class RedditUser(models.Model):
    pass


class SubReddit(models.Model):
    # id =
    # name = models.CharField(max_length=100, blank=True, null=True)
    # description =
    # num_subscribers =
    # created_at =
    pass
