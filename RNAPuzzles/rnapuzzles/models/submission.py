from django.conf import settings
from django.db import models

from rnapuzzles.models import Challenge, CustomUser, Metric


class Submission(models.Model):
    SUBMITTED = 0
    EVALUATION = 1
    ERROR = 2
    SUCCESS = 3

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)
    label = models.CharField(max_length=10)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        (SUBMITTED, 'Submitted'),
        (EVALUATION, 'Evaluation'),
        (ERROR, 'Error'),  # At least one metric failed
        (SUCCESS, ' Success')  # All metrics calculated
    ]
    is_automatic = models.BooleanField()
    alignment = models.CharField(max_length=20, blank=True)
    status = models.SmallIntegerField(choices=status_choices, default=SUBMITTED)
    msg = models.TextField(blank=True)

    @staticmethod
    def get_last_submissions(challenge_pk):
        return Submission.objects.filter(challenge_id=challenge_pk).order_by('user', 'label', 'is_automatic',
                                                                             '-date').distinct('user', 'label',
                                                                                               'is_automatic')


class Score(models.Model):
    ERROR = 0
    SUCCESS = 1
    STATUS_CHOICES = (
        (ERROR, 'Error'),
        (SUCCESS, 'Success'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    score = models.FloatField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('submission', 'metric')
