from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from rnapuzzles.models import Challenge as ChallengeModel, PuzzleInfo, Submission, Score


class Challenge(DetailView):
    model = ChallengeModel
    template_name = "rnapuzzles/score_table.html"

    def get_submissions(self):
        return Submission.get_last_submissions(self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(Challenge, self).get_context_data(**kwargs)
        context["all"] = True
        return context

    def get(self, request, *args, **kwargs):

        try:
            self.object: ChallengeModel = self.get_object()
        except Http404:
            # redirect here
            return HttpResponseRedirect(reverse("completed-puzzles"))

        # if not self.object.result_published:
        #      return HttpResponseRedirect(reverse("completed-puzzles"))

        puzzle = self.object.puzzle_info


        submissions = self.get_submissions()
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

class ChallengeAutomatic(Challenge):
    def get_submissions(self):
        submissions = super(ChallengeAutomatic, self).get_submissions()
        return submissions.filter(is_automatic=True)

    def get_context_data(self, **kwargs):
        context = super(ChallengeAutomatic, self).get_context_data(**kwargs)
        context["all"] = False
        context["in_silico"] = True
        return context

class ChallengeUser(Challenge):
    def get_submissions(self):
        submissions = super(ChallengeUser, self).get_submissions()
        return submissions.filter(is_automatic=False)


    def get_context_data(self, **kwargs):
        context = super(ChallengeUser, self).get_context_data(**kwargs)
        context["all"] = False
        context["in_vivo"] = True
        return context

