import os
import subprocess
import zipfile
from random import random

import celery
import tempfile

import xmltodict

from rnapuzzles.models import Submission, Score, PuzzleInfo, Metric


@celery.task(name="spawn_tasks_for_metric_caluculation")
def spawn_tasks(submission):
    submission = Submission.objects.get(pk=submission)
    rnaqua_metrics.delay(submission.pk)

@celery.task(name="calculate score")
def rnaqua_metrics(submission_pk):
    task_id = str(rnaqua_metrics.request.id)
    sub:Submission = Submission.objects.get(pk=submission_pk)
    sub.status = sub.EVALUATION
    sub.save()
    puzzle: PuzzleInfo = sub.challenge.puzzle_info


    with tempfile.TemporaryDirectory() as directory:
        submitted_path = os.path.join(directory, "submitted.pdb")
        ref_path = os.path.join(directory, "ref.pdb")
        output_path = os.path.join(directory, "out.xml")
        with open(submitted_path, "w") as file:
            file.write(sub.content)
        with open(ref_path, "w") as file:
            file.write(puzzle.pdb_file.read().decode("utf-8"))

        print(subprocess.run(["java", "-jar", "../rnaqua.jar", "--command", "ALL-SCORES-AT-ONCE", "-s",submitted_path, "-r",ref_path, "-o",output_path]))

        with open(output_path, "r") as file:
            res_rnaqua = file.read()
            out_dict = xmltodict.parse(res_rnaqua)
            print(out_dict['comprehensiveScores']["structure"])
            root = out_dict['comprehensiveScores']["structure"]

            if(root["description"]["errors"]):
                sub.status = sub.ERROR
                sub.msg = res_rnaqua
                sub.save()
                return 1

            infs_metrics = ["wc", "nwc", "stacking", "all"]
            no_infs_metrics = ["rmsd", "di", "p-value", "clashscore"]

            for m in infs_metrics:

                value = root["infs"][m]
                metric = Metric.objects.get(code="infs_"+m)
                score, _ = Score.objects.get_or_create(submission_id=sub.pk, challenge_id=sub.challenge.puzzle_info_id, metric_id=metric.pk, score=value, status=Score.SUCCESS)
                score.save()


            for m in no_infs_metrics:

                value = root[m]
                metric = Metric.objects.get(code=m)
                score, _ = Score.objects.get_or_create(submission_id=sub.pk,
                                                       challenge_id=sub.challenge.puzzle_info_id,
                                                       metric_id=metric.pk, score=value, status=Score.SUCCESS)
                score.save()
        sub.status = sub.SUCCESS
        sub.msg = res_rnaqua
        sub.save()
        return 0
    # except:
    #     sub.status = sub.ERROR
    #     sub.error_msg = "Internal Error"
    #     sub.save()
    #     return 1



    # print(submission_pk, metric_pk)
    # sub = Submission.objects.get(pk=submission_pk)
    # res = random()
    # object: Score = Score.objects.get_or_create(submission_id=submission_pk, challenge_id=sub.challenge.pk, metric_id=metric_pk, score=res, status=0)




