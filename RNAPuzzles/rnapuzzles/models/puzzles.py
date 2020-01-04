# rnapuzzles/models/puzzles.py
from django.db import models
from django.core.exceptions import ValidationError

from .user import CustomUser
import datetime
from six import text_type


def puzzle_dir_path(instance, filename):
    # file uploaded to MEDIA_ROOT/<puzzle_input.id>/<filename>
    return '{0}/puzzle_input/{1}'.format(instance.id, filename)

# pdb_file/img saved only through update, otherwise folder 'None' created


class PuzzleInfo(models.Model):
    description = models.CharField(verbose_name="Description", max_length=250, help_text='Maximum 250 characters.')
    sequence = models.TextField(verbose_name="RNA sequence (5' to 3')")
    publish_date = models.DateField(verbose_name='Target 3D structure publication date', blank=True, null=True)
    reference = models.CharField(verbose_name="Reference", max_length=500, help_text='Maximum 500 characters.', blank=True)
    reference_url = models.URLField(verbose_name="Reference URL", blank=True)
    pdb_id = models.CharField(verbose_name="PDB ID", max_length=4,
                              help_text='Maximum 4 characters (by PDB ID convention).', blank=True)
    pdb_url = models.URLField(verbose_name="PDB URL", blank=True)
    pdb_file = models.FileField(verbose_name="Target 3D structure file", upload_to=puzzle_dir_path,
                                help_text='Allowed types: .pdb, .cif', blank=True)
    img = models.ImageField(verbose_name="Target 3D structure graphic representation", upload_to=puzzle_dir_path,
                            help_text='Allowed file types: .jpg, .png', blank=True)

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

    def clean(self):
        if self.pk is None:
            if self.start_date < datetime.date.today():
                raise ValidationError('The opening date cannot be in the past.')
        else:
            if self.start_date < self.created_at:
                raise ValidationError('The opening date cannot be earlier than creation date.')
        if self.end_date <= self.start_date:
            raise ValidationError('The closing date cannot be earlier or same as the opening date.')

    def save(self, *args, **kwargs):
        if self.pk is None:
            # initialize current_status
            if self.start_date == datetime.date.today():
                self.current_status = 1
            else:
                self.current_status = 0

        self.full_clean()
        super(Challenge, self).save(*args, **kwargs)


def puzzle_challenge_dir_path(instance, filename):
    # file uploaded to MEDIA_ROOT/<puzzle_input.id>/<challenge.round/<filename>
    return '{0}/{1}/{2}'.format(instance.challenge.puzzle_info_id, instance.challenge.round, filename)


class ChallengeFile(models.Model):

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, editable=False)
    note = models.CharField(max_length=50, help_text='Information about file content. Maximum 50 characters.',
                            blank=True)
    file = models.FileField(upload_to=puzzle_challenge_dir_path, blank=True)

    def __str__(self):
        return 'challenge: %s file.id: %s' % (self.challenge_id, str(self.id))
