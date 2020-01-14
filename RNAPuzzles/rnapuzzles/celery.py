from random import random

import celery

from rnapuzzles.models import Submission, Score


@celery.task(name="spawn_tasks_for_metric_caluculation")
def spawn_tasks(submission):
    submission = Submission.objects.get(pk=submission)
    for metric in submission.challenge.puzzle_info.metrics.all():
        calculate_score.delay(submission.pk, metric.pk)

@celery.task(name="calculate score")
def calculate_score(submission_pk, metric_pk):
    print(submission_pk, metric_pk)

    res = random()
    object: Score = Score.objects.get_or_create(submission_id=submission_pk, metric_id=metric_pk, score=res, status=0)




