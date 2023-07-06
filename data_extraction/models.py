from django.db import models

class DailyBestPost(models.Model):
    title = models.TextField()
    body = models.TextField()
    score = models.IntegerField()
    url = models.URLField()
    created_utc = models.DateTimeField(null=True, blank=True)

class DBPComment(models.Model):
    post = models.ForeignKey(DailyBestPost, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    score = models.IntegerField()
    created_utc = models.DateTimeField(null=True, blank=True)

class PostByTopic(models.Model):
    title = models.TextField()
    body = models.TextField()
    topic = models.CharField(max_length=255)
    score = models.IntegerField()
    url = models.URLField()
    created_utc = models.DateTimeField(null=True, blank=True)

    
class PBTComment(models.Model):
    post = models.ForeignKey(PostByTopic, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    topic = models.CharField(max_length=255)
    score = models.IntegerField()
    created_utc = models.DateTimeField(null=True, blank=True)
