from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class Submission(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    title = models.CharField(max_length=300, blank=True, null=True)
    body = models.CharField(max_length=40000, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    subreddit = models.ForeignKey('submission.SubReddit', on_delete=models.PROTECT)
    author = models.ForeignKey('submission.RedditUser', on_delete=models.SET_NULL, null=True)
    score = models.PositiveIntegerField(default=0)
    num_comments = models.PositiveIntegerField(default=0)
    num_writers = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    retrieved_on = models.DateTimeField()
    extra = JSONField(default=dict, null=True, blank=True)


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    author = models.ForeignKey('submission.RedditUser', on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=40000, blank=True, null=True)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    submission = models.ForeignKey("submission.Submission", null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey("submission.Comment", null=True, on_delete=models.CASCADE)
    retrive_on = models.DateTimeField()
    extra = JSONField(default=dict, null=True, blank=True)


class RedditUser(models.Model):
    name = models.CharField(max_length=100)
    submissions_karma = models.PositiveIntegerField(default=0)
    comments_karma = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()
    last_update = models.DateTimeField(auto_now=True)


class SubReddit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    short_description = models.CharField(max_length=500)
    num_subscribers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()
    last_update = models.DateTimeField(auto_now=True)
