from django.db import models

from rnapuzzles.models import CustomUser


class FaqModel(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)