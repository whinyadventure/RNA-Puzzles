from django.core.files.base import ContentFile
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile

import os
import io
import zipfile


@receiver(pre_save, sender=PuzzleInfo)
def puzzle_info_pre_save(sender, instance, *args, **kwargs):

    try:
        obj = sender.objects.get(pk=instance.pk)

    except sender.DoesNotExist:
        pass

    else:
        if instance.img:
            if not obj.img == instance.img:
                obj.img.delete(save=False)
                obj.img = instance.img

        if instance.pdb_file:

            zip_filename = 'puzzle_{}_target_structure.zip'.format(instance.pk)
            zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

            if os.path.exists(zip_path):

                if not instance.pdb_file.name == zip_filename:
                    os.remove(zip_path)

            if not instance.pdb_file.name == zip_filename:

                file = instance.pdb_file
                filename = file.name

                with file.open('rb') as f:
                    file_content = f.read()

                in_memory_zip = io.BytesIO()

                with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(filename, file_content)

                zip_file_content = ContentFile(in_memory_zip.getvalue())
                file.save(zip_filename, zip_file_content, save=True)


# TODO: current_status=4 if all fields filled and challenge's current_status==3
@receiver(post_save, sender=PuzzleInfo)
def puzzle_info_post_save(sender, instance, *args, **kwargs):
    pass


@receiver(post_delete, sender=PuzzleInfo)
def puzzle_info_post_delete(sender, instance, *args, **kwargs):
    instance.img.delete(save=False)
    instance.pdb_file.delete(save=False)


@receiver(post_save, sender=Challenge)
def challenge_post_save(sender, instance, *args, **kwargs):

    if instance.current_status == 3:
        puzzle = instance.puzzle_info

        if puzzle.is_fully_filled:
            instance.current_status = 4


@receiver(post_save, sender=ChallengeFile)
def challenge_file_post_save(sender, instance, *args, **kwargs):

    if instance.file:

        challenge_id = str(instance.challenge.pk)
        file_id = str(instance.pk)

        zip_filename = 'challenge_{0}_file_{1}.zip'.format(challenge_id, file_id)

        if not instance.file.name == zip_filename:

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
