from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from guardian.shortcuts import assign_perm, remove_perm

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile


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

        else:
            if obj.img:
                obj.img.delete(save=False)

        if instance.pdb_file:
            if not obj.pdb_file == instance.pdb_file:
                obj.pdb_file.delete(save=False)
                obj.pdb_file = instance.pdb_file


@receiver(post_delete, sender=PuzzleInfo)
def puzzle_info_post_delete(sender, instance, *args, **kwargs):
    instance.img.delete(save=False)
    instance.pdb_file.delete(save=False)


@receiver(post_delete, sender=ChallengeFile)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.file.delete(save=False)


@receiver(post_save, sender=PuzzleInfo)
def post_save_puzzleinfo_creation(sender, instance: PuzzleInfo, *args, **kwargs):
    if kwargs.get("created", False):
        assign_perm("rnapuzzles.delete_puzzleinfo", instance.author, instance)
        #assign_perm("rnapuzzles.change_puzzleinfo", instance.author, instance)


@receiver(post_save, sender=Challenge)
def post_save_challenge_change(sender, instance: Challenge, *args, **kwargs):
    if kwargs.get("created", False):
        assign_perm("rnapuzzles.metrics_challenge", instance.author, instance)
        assign_perm("rnapuzzles.change_challenge", instance.author, instance)
        assign_perm("rnapuzzles.delete_challenge", instance.author, instance)

    if instance.current_status != 0:
        remove_perm("rnapuzzles.delete_puzzleinfo", instance.puzzle_info.author, instance.puzzle_info)
        remove_perm("rnapuzzles.delete_challenge", instance.author, instance)

    if instance.current_status == 3:
        #remove_perm("rnapuzzles.change_puzzleinfo", instance.puzzle_info.author, instance.puzzle_info)
        remove_perm("rnapuzzles.change_challenge", instance.author, instance)

