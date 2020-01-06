# rnapuzzles/models/puzzles.py

from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings

import os
import io
from .user import CustomUser
import datetime
import zipfile
from six import text_type


# TODO: test extention validators, move validation to forms
class PuzzleInfo(models.Model):
    description = models.CharField(verbose_name="Description", max_length=250, help_text='Maximum 250 characters.')
    sequence = models.TextField(verbose_name="RNA sequence (5' to 3')")
    publish_date = models.DateField(verbose_name='Target 3D structure publication date', blank=True, null=True)
    reference = models.CharField(verbose_name="Reference", max_length=500, help_text='Maximum 500 characters.', blank=True)
    reference_url = models.URLField(verbose_name="Reference URL", blank=True)
    pdb_id = models.CharField(verbose_name="PDB ID", max_length=4,
                              help_text='Maximum 4 characters (by PDB ID convention).', blank=True)
    pdb_url = models.URLField(verbose_name="PDB URL", blank=True)
    pdb_file = models.FileField(verbose_name="Target 3D structure file", help_text='Allowed types: .pdb, .cif',
                                validators=[FileExtensionValidator(allowed_extensions=['pdb', 'cif'])], blank=True)
    img = models.ImageField(verbose_name="Target 3D structure graphic representation", help_text='Allowed file types: .jpg, .png',
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])], blank=True)

    class Meta:
        verbose_name = 'Puzzle Information'

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    @property
    def description_label(self):
        return self.__get_label('description')

    @property
    def sequence_label(self):
        return self.__get_label('sequence')

    @property
    def publish_date_label(self):
        return self.__get_label('publish_date')

    @property
    def reference_label(self):
        return self.__get_label('reference')

    @property
    def reference_url_label(self):
        return self.__get_label('reference_url')

    @property
    def pdb_id_label(self):
        return self.__get_label('pdb_id')

    @property
    def pdb_url_label(self):
        return self.__get_label('pdb_url')

    @property
    def pdb_file_label(self):
        return self.__get_label('pdb_file')

    @property
    def img_label(self):
        return self.__get_label('img')

    def __str__(self):
        return 'Puzzle %s' % (str(self.id))

    def clean(self):
        if self.publish_date:
            if self.publish_date < datetime.date.today():
                raise ValidationError('The date cannot be in the past.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(PuzzleInfo, self).save(*args, **kwargs)


# TODO: write auto-run script updating Challenge current_status at certain occasions
'''
    'Created'/'Open' --> during instance initial saving to db
    'Under modeling' --> changed by auto-run script triggered by reaching end_date irl
    'Evaluated' --> changed when evaluation of models comes to an end
    'Completed' --> changed when auto-run script triggered by current_status='Evaluated' will detect all fields filled;
                    otherwise: generate an email to challenge's author with a plea to fill remaining fields,
                               run the script whenever the challenge instance has been updated
    
    Proposal regarding editing: make all optional fields required if current_status='Evaluated'                               
'''


class Challenge(models.Model):

    STATUS_TYPE = (
        (0, 'Created'),
        (1, 'Open'),
        (2, 'Under modeling'),
        (3, 'Evaluated'),
        (4, 'Completed')
    )

    round = models.IntegerField(default=1, editable=False)
    created_at = models.DateField(auto_now_add=True)
    start_date = models.DateField(verbose_name='Opening date')
    end_date = models.DateField(verbose_name='Closing date')
    current_status = models.IntegerField(choices=STATUS_TYPE, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    puzzle_info = models.ForeignKey(PuzzleInfo, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-puzzle_info', '-created_at']

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    @property
    def start_date_label(self):
        return self.__get_label('start_date')

    @property
    def end_date_label(self):
        return self.__get_label('end_date')

    def __str__(self):
        return 'puzzle_info: %s challenge.id: %s' % (self.puzzle_info_id, str(self.id))

    def save(self, *args, **kwargs):
        if self.pk is None:
            # initialize current_status
            if self.start_date == datetime.date.today():
                self.current_status = 1
            else:
                self.current_status = 0

        super(Challenge, self).save(*args, **kwargs)


class ChallengeFile(models.Model):

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, editable=False)
    note = models.CharField(max_length=50, help_text='Information about file content. Maximum 50 characters.', blank=True)
    file = models.FileField(blank=True)

    def __str__(self):
        return 'challenge: %s file.id: %s' % (self.challenge_id, str(self.id))


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
