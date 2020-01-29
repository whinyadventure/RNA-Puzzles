from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Group as CustomGroup
from guardian.shortcuts import assign_perm


@receiver(post_save, sender=CustomGroup)
def assign_news_perm(sender, instance: CustomGroup, **kwargs):
    if kwargs.get("created", False) and instance.leader is not None:
        assign_perm("rnapuzzles.change_newsmodel", instance.leader, instance)
