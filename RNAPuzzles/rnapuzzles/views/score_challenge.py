from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from rnapuzzles.models import Challenge as ChallengeModel, PuzzleInfo, Submission, Score


class Challenge(DetailView):
    model = ChallengeModel
    template_name = "rnapuzzles/score_table.html"

    def get(self, request, *args, **kwargs):

        try:
            self.object: ChallengeModel = self.get_object()
        except Http404:
            # redirect here
            return HttpResponseRedirect(reverse("completed-puzzles"))
        #TODO
        # if not self.object.result_published:
        #     return HttpResponseRedirect(reverse("completed-puzzles"))

        puzzle = self.object.puzzle_info
        print(puzzle.metrics.all())

        submissions = Submission.objects.filter(challenge=self.object).order_by('user', '-date').distinct('user')
        res = []
        metrics_list = []
        for metric in puzzle.metrics.all():
            metrics_list.append(metric.name)

        for s in submissions:
            m = []
            for metric in puzzle.metrics.all():
                try:
                    m.append(s.score_set.get(metric=metric))
                except:
                    m.append(None)
            setattr(s,"scores", m)

            res.append(s)

        context = self.get_context_data()
        context["object_list"] = res
        context["metric_list"] = metrics_list
        return self.render_to_response(context)
