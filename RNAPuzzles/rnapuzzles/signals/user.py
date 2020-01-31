from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from ..models import CustomUser
from django.contrib.auth.models import Group


@receiver(post_save, sender=CustomUser)
def add_user_group(sender, instance: CustomUser, **kwargs):

    if kwargs.get("created", False):
        object, _ = Group.objects.get_or_create(name="Defaults")
        # object,_ = Group.objects.get(name="Default")
        object.user_set.add(instance)
        # assign_perm("rnapuzzles.view_newsmodel", instance)

        if instance.role == CustomUser.ORGANIZER:  # Organizer

            object, created = Group.objects.get_or_create(name="Organizers")
            object.user_set.add(instance)
            if created:
                assign_perm("rnapuzzles.view_newsmodel", object)
                assign_perm("rnapuzzles.view_puzzleinfo", object)
                assign_perm("rnapuzzles.add_puzzleinfo", object)
                assign_perm("rnapuzzles.view_faqmodel", object)
                assign_perm("rnapuzzles.view_resourcesmodel", object)
                assign_perm("rnapuzzles.view_group", object)
                assign_perm("rnapuzzles.view_submission", object)
                assign_perm("rnapuzzles.accept_group", object)

        if instance.role == 3:
            assign_perm("rnapuzzles.change_group", instance, instance.group_name)
            assign_perm("rnapuzzles.name_group", instance, instance.group_name)
            assign_perm("rnapuzzles.accept_group", instance, instance.group_name)

    if instance.role in [2, 3]:
        object, created = Group.objects.get_or_create(name="Participant")
        object.user_set.add(instance)
        assign_perm("rnapuzzles.change_group", instance, instance.group_name)
        if created:
            assign_perm("rnapuzzles.view_newsmodel", object)
            assign_perm("rnapuzzles.view_puzzleinfo", object)
            assign_perm("rnapuzzles.view_faqmodel", object)
            assign_perm("rnapuzzles.view_resourcesmodel", object)
            assign_perm("rnapuzzles.view_group", object)
            assign_perm("rnapuzzles.add_submission", object)


@receiver(pre_save, sender=CustomUser)
def user_is_active(sender, instance, **kwargs):
    if instance.is_disabled and instance.is_active:
        instance.is_active = False

    if not instance.is_active and instance.email_confirmed and instance.is_authorised and not instance.is_disabled:
        instance.is_active = True
