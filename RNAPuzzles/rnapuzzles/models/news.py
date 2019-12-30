from django.db import models
from . import *

class NewsModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(default=True, null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    publish_at = models.DateTimeField(null=True)


    class Meta:
       ordering = ['public', '-publish_at']

