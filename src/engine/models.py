from django.db import models


class RedditCredential(models.Model):
    client_id = models.CharField(max_length=15)
    client_secret = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=50)