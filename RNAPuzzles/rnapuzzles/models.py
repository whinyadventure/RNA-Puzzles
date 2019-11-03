from django.db import models
from django.contrib.auth import models as AuthModels


# Create your models here.


class UserRoles(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)


class User(AuthModels.User):
    email = models.EmailField()
    role = models.ForeignKey(UserRoles, on_delete=models.SET_NULL)

