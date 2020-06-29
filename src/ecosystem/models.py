from django.db import models


class seed(models.Model):
    seed = models.ForeignKey("post.Post", null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=40000, blank=True, null=True)
