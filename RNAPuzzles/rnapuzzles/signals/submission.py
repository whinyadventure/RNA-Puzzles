from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from rnapuzzles.models import Submission
from rnapuzzles.celery import spawn_tasks



@receiver(post_save, sender=Submission)
def post_save_challenge_change(sender, instance: Submission, *args, **kwargs):

    if kwargs.get("created", False):
        assign_perm("rnapuzzles.view_submission", instance.user, instance)
        print(instance.user.group_name, instance.user.group_name.leader)
        assign_perm("rnapuzzles.view_submission", instance.user.group_name.leader, instance)

