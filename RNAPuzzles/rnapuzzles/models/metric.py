from django.db import models


class Metric(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
