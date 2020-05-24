from django.db import models


# Create your models here.
class Task(models.Model):
    body = models.TextField()
    ans = models.TextField()
    source = models.CharField(max_length=100)

