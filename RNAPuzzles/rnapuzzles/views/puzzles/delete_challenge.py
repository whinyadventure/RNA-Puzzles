from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.urls import reverse

from rnapuzzles.models import Challenge


class ChallengeDelete(DeleteView):

    model = Challenge
    template_name = 'puzzles/puzzle_delete.html'
    success_message = "Puzzle was deleted"

    def post(self, request, *args, **kwargs):

        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(ChallengeDelete, self).post(request, *args, **kwargs)

    def puzzle_id(self):
        challenge = Challenge.objects.get(pk=self.kwargs['pk'])
        puzzle_id = str(challenge.puzzle_info_id) + '-' + str(challenge.round)
        return puzzle_id

    def get_success_url(self):
        return reverse('organizer-puzzles')
