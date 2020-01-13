from django.core.files.base import ContentFile
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from guardian.shortcuts import assign_perm, remove_perm

from rnapuzzles.models import ChallengeFile, PuzzleInfo, Challenge

import os
import io
import zipfile


@receiver(post_save, sender=ChallengeFile)
def post_save_compression(sender, instance, *args, **kwargs):

    challenge_id = str(instance.challenge.pk)
    file_id = str(instance.pk)

    zip_filename = 'challenge_{0}_file_{1}.zip'.format(challenge_id, file_id)
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    if instance.file.path != zip_path:
        file = instance.file
        filename = file.name

        with file.open('rb') as f:
            file_content = f.read()

        in_memory_zip = io.BytesIO()

        with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(filename, file_content)

        zip_file_content = ContentFile(in_memory_zip.getvalue())

        file.save(zip_filename, zip_file_content, save=True)

        file.storage.delete(filename)


@receiver(post_delete, sender=ChallengeFile)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.file.delete(save=False)


@receiver(post_save, sender=PuzzleInfo)
def post_save_puzzleinfo_creation(sender, instance: PuzzleInfo, *args, **kwargs):
    if kwargs.get("created", False):
        assign_perm("rnapuzzles.delete_puzzleinfo", instance.author, instance)

@receiver(post_save, sender=Challenge)
def post_save_challenge_change(sender, instance: Challenge, *args, **kwargs):
        if(instance.current_status != 0):
            remove_perm("rnapuzzles.delete_puzzleinfo", instance.puzzle_info.author, instance.puzzle_info)

        if(instance.current_status != 4):
            assign_perm("rnapuzzles.change_puzzleinfo", instance.puzzle_info.author, instance.puzzle_info)


