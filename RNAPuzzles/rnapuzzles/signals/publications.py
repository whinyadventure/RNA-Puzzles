from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone


from publications.models import Publication
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group

