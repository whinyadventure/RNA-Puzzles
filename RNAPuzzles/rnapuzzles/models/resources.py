from django.db import models


class ResourcesModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
