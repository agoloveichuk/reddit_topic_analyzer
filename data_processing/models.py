from django.db import models

class NamedEntity(models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=50)
    frequency = models.IntegerField(default=0)
    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Phrase(models.Model):
    content = models.CharField(max_length=255)
    frequency = models.IntegerField(default=0)
    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.name