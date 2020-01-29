from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import ResourcesModel
from guardian.shortcuts import assign_perm

@receiver(post_save, sender=ResourcesModel)
def assign_news_perm(sender, instance: ResourcesModel, **kwargs):

    if kwargs.get("created", False):
        assign_perm("rnapuzzles.change_resourcesmodel", instance.author, instance)
        assign_perm("rnapuzzles.delete_resourcesmodel", instance.author, instance)

