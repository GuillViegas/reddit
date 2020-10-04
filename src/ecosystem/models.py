from django.db import models
from django.contrib.postgres.fields import ArrayField


class Seed(models.Model):
    seed = models.ForeignKey("submission.Submission", null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=40000, blank=True, null=True)
    subreddits = ArrayField(models.CharField(max_length=100), null=True)
    redditors = ArrayField(models.CharField(max_length=100), null=True)
    comments = ArrayField(models.CharField(max_length=7), null=True)
    submissions = ArrayField(models.CharField(max_length=7), null=True)
    r_idx = models.PositiveIntegerField(default=0)
    domain = ArrayField(models.CharField(max_length=100), null=True)
