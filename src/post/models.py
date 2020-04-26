from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    title = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=40000, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    subreddit = models.ForeignKey('post.SubReddit', on_delete=models.PROTECT)
    author = models.ForeignKey('post.RedditUser', on_delete=models.PROTECT)
    score = models.PositiveIntegerField()




class Comment(models.Model):
    pass


class RedditUser(models.Model):
    pass


class SubReddit(models.Model):
    author = models.ForeignKey('post.RedditUser', on_delete=models.PROTECT)
    created_at = models.DateTimeField()