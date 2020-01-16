from django.db.models.signals import post_save
from django.dispatch import receiver

from rnapuzzles.models import Submission
from rnapuzzles.celery import spawn_tasks


@receiver(post_save, sender=Submission)
def post_save_challenge_change(sender, instance: Submission, *args, **kwargs):
    spawn_tasks(instance.pk)
