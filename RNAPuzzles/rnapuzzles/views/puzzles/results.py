from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from guardian.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import PuzzleInfo, ChallengeFile, Submission
from rnapuzzles.models import Challenge as ChallengeModel

# @permission_required("rnapuzzles.view_puzzleinfo")
# def results(request, pk):
#
#     template_name = 'puzzles/challenge_results.html'
#     name = 'Results'
#
#     challenge = Challenge.objects.get(pk=pk)
#     puzzle = PuzzleInfo.objects.get(pk=challenge.puzzle_info.pk)
#     files = challenge.challengefile_set.all()
#
#     context = {'list_name': name, 'puzzle': puzzle, 'challenge': challenge, 'files': files}
#
#     return render(request, template_name, context)


class ChallengeAll(DetailView):
    model = ChallengeModel
    template_name = 'puzzles/challenge_results.html'

    def get_permission_object(self):
        return self.get_object().puzzle_info

    def get_submissions(self):
        return Submission.get_last_submissions(self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(ChallengeAll, self).get_context_data(**kwargs)
        context['challenge'] = self.get_object()
        context['puzzle'] = PuzzleInfo.objects.get(pk=self.object.puzzle_info.pk)
        context['files'] = self.object.challengefile_set.all()
        context["list_name"] = "Results"
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
        print(puzzle.metrics.all())

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


class ChallengeAutomatic(ChallengeAll):
    def get_submissions(self):
        submissions = super(ChallengeAutomatic, self).get_submissions()
        return submissions.filter(is_automatic=True)

    def get_context_data(self, **kwargs):
        context = super(ChallengeAutomatic, self).get_context_data(**kwargs)
        context["all"] = False
        context["in_silico"] = True
        return context


class ChallengeUser(ChallengeAll):
    def get_submissions(self):
        submissions = super(ChallengeUser, self).get_submissions()
        return submissions.filter(is_automatic=False)

    def get_context_data(self, **kwargs):
        context = super(ChallengeUser, self).get_context_data(**kwargs)
        context["all"] = False
        context["in_vivo"] = True
        return context

