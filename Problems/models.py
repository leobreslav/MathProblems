from django.db import models


# Create your models here.
class Task(models.Model):
    body = models.TextField()
    ans = models.TextField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return '№' + str(self.id) +'. '+self.body
