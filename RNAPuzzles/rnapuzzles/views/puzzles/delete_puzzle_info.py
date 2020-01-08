from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.urls import reverse

from rnapuzzles.models import PuzzleInfo


class PuzzleInfoDelete(DeleteView):

    template_name = 'puzzles/puzzle_delete.html'
    model = PuzzleInfo
    success_message = "Puzzle was deleted"

    def post(self, request, *args, **kwargs):

        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(PuzzleInfoDelete, self).post(request, *args, **kwargs)

    def puzzle_id(self):
        return self.kwargs['pk']

    def get_success_url(self):
        return reverse('organizer-puzzles')
