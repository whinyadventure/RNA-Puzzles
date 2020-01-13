from django.conf import settings
from django.db import models

from rnapuzzles.models import Challenge, CustomUser, Metric


class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)
    file = models.FileField(upload_to=settings.MEDIA_SUBMISSIONS)
    is_batch = models.BooleanField()
    status_choices = [
        ('SU', 'Submitted'),
        ('WA', 'Waiting'),
        ('EV', 'Evaluation'),
        ('IN', 'Invalid'),  # At least one metric failed
        ('SU', ' Success')  # All metrics calculated
    ]
    status = models.CharField(max_length=10, choices=status_choices)


class Score(models.Model):
    score = models.FloatField()
    error = models.CharField(max_length=50)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('submission', 'metric')
