from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    title = models.CharField(max_length=300, blank=True, null=True)
    body = models.CharField(max_length=40000, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    subreddit = models.ForeignKey('post.SubReddit', on_delete=models.PROTECT)
    author = models.ForeignKey('post.RedditUser', on_delete=models.SET_NULL)
    score = models.PositiveIntegerField()
    num_comments = models.PositiveIntegerField()
    created_at = models.DateTimeField()


class Comment(models.Model):
    author = models.ForeignKey('post.RedditUser', on_delete=models.PROTECT)
    body = models.CharField(max_length=40000, blank=True, null=True)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    post = models.ForeignKey("post.Post", null=True, on_delete=models.PROTECT)
    parent = models.ForeignKey("post.Comment", null=True, on_delete=models.PROTECT)


class RedditUser(models.Model):
    pass


class SubReddit(models.Model):
    pass