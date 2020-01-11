from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from ..models import ResourcesModel, FaqModel
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group


@receiver(post_save, sender=FaqModel)
def assign_news_perm(sender, instance: FaqModel, **kwargs):
    if kwargs.get("created", False):
        assign_perm("rnapuzzles.change_fagmodel", instance.author, instance)
        assign_perm("rnapuzzles.delete_fagmodel", instance.author, instance)
