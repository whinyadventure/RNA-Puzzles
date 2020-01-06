from django.db import models
from . import *

class NewsModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()