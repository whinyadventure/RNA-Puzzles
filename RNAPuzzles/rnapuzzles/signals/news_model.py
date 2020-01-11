from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from ..models import NewsModel
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group


@receiver(post_save, sender=NewsModel)
def assign_news_perm(sender, instance: NewsModel, **kwargs):

    if kwargs.get("created", False):
        assign_perm("rnapuzzles.change_newsmodel", instance.author, instance)
        assign_perm("rnapuzzles.delete_newsmodel", instance.author, instance)

        object,_ = Group.objects.get_or_create(name="Defaults")
        assign_perm("rnapuzzles.view_newsmodel", object, instance)


@receiver(pre_save, sender=NewsModel)
def assign_publish_perm(sender, instance: NewsModel, **kwargs):

    if instance.publish_at is None and instance.public:
        instance.publish_at = timezone.now()
