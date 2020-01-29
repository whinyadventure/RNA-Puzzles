from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import FaqModel
from guardian.shortcuts import assign_perm


@receiver(post_save, sender=FaqModel)
def assign_news_perm(sender, instance: FaqModel, **kwargs):

    if kwargs.get("created", False):
        assign_perm("rnapuzzles.change_fagmodel", instance.author, instance)
        assign_perm("rnapuzzles.delete_fagmodel", instance.author, instance)
