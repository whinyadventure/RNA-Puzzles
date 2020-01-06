from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..models import CustomUser
from django.contrib.auth.models import Group


@receiver(post_save, sender=CustomUser)
def add_user_group(sender, instance, **kwargs):
    if (kwargs.get("created", False)):
        object, _ = Group.objects.get_or_create(name="Defaults")
        # object,_ = Group.objects.get(name="Default")
        object.user_set.add(instance)


@receiver(pre_save, sender=CustomUser)
def user_is_active(sender, instance, **kwargs):
    if instance.is_disabled and instance.is_active:
        instance.is_active = False
    if not instance.is_active and instance.email_confirmed and instance.is_authorised and not instance.is_disabled:
        instance.is_active = True
