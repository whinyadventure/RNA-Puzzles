from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.urls import reverse
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import PuzzleInfo

#TODO block if len(puzzleInfo.challenge_set) != 1 or one challenge is oppened
class PuzzleInfoDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "rnapuzzle.delete_puzzleinfo"
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
