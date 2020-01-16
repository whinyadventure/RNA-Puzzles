from random import random

import celery

from rnapuzzles.models import Submission, Score


@celery.task(name="spawn_tasks_for_metric_caluculation")
def spawn_tasks(submission):
    submission = Submission.objects.get(pk=submission)
    print("AaA")
    for metric in submission.challenge.puzzle_info.metrics.all():
        print(metric)
        calculate_score.delay(submission.pk, metric.pk)

@celery.task(name="calculate score")
def calculate_score(submission_pk, metric_pk):
    print(submission_pk, metric_pk)
    sub = Submission.objects.get(pk=submission_pk)
    res = random()
    object: Score = Score.objects.get_or_create(submission_id=submission_pk, challenge_id=sub.challenge.pk, metric_id=metric_pk, score=res, status=0)




