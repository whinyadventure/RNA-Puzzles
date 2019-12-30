from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import CustomUser
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm

@receiver(post_save, sender=CustomUser)
def add_user_group(sender, instance, **kwargs):
    if(kwargs.get("created", False)):
        object,_ = Group.objects.get_or_create(name="Defaults")
       # object,_ = Group.objects.get(name="Default")
        object.user_set.add(instance)