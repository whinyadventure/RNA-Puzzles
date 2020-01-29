from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from .user import CustomUser
import datetime
from six import text_type
import os


def puzzle_info_img_filename(instance, filename):
    return 'puzzle_{}_img{}'.format(instance.pk, os.path.splitext(filename)[1])


class PuzzleInfo(models.Model):

    description = models.CharField(verbose_name="Description", max_length=250)
    sequence = models.TextField(verbose_name="RNA sequence (5' to 3')")
    publish_date = models.DateTimeField(verbose_name='Target 3D structure publication date', blank=True, null=True)
    reference = models.TextField(verbose_name="Reference", blank=True)
    reference_url = models.URLField(verbose_name="Reference URL", blank=True)
    pdb_id = models.CharField(verbose_name="PDB ID", max_length=4, blank=True)
    pdb_url = models.URLField(verbose_name="PDB URL", blank=True)
    pdb_file = models.FileField(verbose_name="Target 3D structure file",
                                validators=[FileExtensionValidator(allowed_extensions=['pdb'])])
    img = models.ImageField(verbose_name="Target 3D structure graphic representation",
                            upload_to=puzzle_info_img_filename, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    metrics = models.ManyToManyField("rnapuzzles.Metric")

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


class Challenge(models.Model):

    CREATED = 0
    OPEN = 1
    EVALUATED = 2
    COMPLETED = 3

    round = models.IntegerField(default=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(verbose_name='Opening date')
    end_date = models.DateTimeField(verbose_name='Closing date for human category')
    end_automatic = models.DateTimeField(verbose_name='Closing date for server category')
    result_published = models.BooleanField(default=False)
    notification_email_send = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    puzzle_info = models.ForeignKey(PuzzleInfo, on_delete=models.CASCADE, blank=True, null=True)
    alignment = models.CharField(max_length=20, blank=True)
    class Meta:
        ordering = ['-puzzle_info', '-created_at']
        permissions = [
            ("metrics_challenge", "Run computation of metrics"),
        ]

    def __str__(self):
        if self.round == 1:
            return 'Puzzle %s' % self.puzzle_info_id
        else:
            return 'Puzzle %s-%s' % (self.puzzle_info_id, str(self.round))

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    @property
    def current_status(self):
        if timezone.now() < self.start_date:
            return self.CREATED

        if timezone.now() < self.end_date:
            return self.OPEN

        if not self.result_published:
            return self.EVALUATED

        return self.COMPLETED

    @property
    def current_status_label(self):
        if timezone.now() < self.start_date:
            return 'Created'

        if timezone.now() < self.end_date:
            return 'Open'

        if not self.result_published:
            return 'Evaluated'

        return 'Completed'

    @property
    def start_date_label(self):
        return self.__get_label('start_date')

    @property
    def end_date_label(self):
        return self.__get_label('end_date')

    @property
    def end_automatic_label(self):
        return self.__get_label('end_automatic')


class ChallengeFile(models.Model):

    note = models.CharField(max_length=50, help_text='Information about file content. Maximum 50 characters.', blank=True)
    file = models.FileField(blank=True)

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return 'challenge: %s file.id: %s' % (self.challenge, str(self.id))
