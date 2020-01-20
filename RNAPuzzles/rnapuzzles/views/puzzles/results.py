from django.shortcuts import redirect, render
from django.urls import reverse
from guardian.decorators import permission_required

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile


@permission_required("rnapuzzles.view_puzzleinfo")
def results(request, pk):

    template_name = 'puzzles/challenge_results.html'
    name = 'Results'

    challenge = Challenge.objects.get(pk=pk)
    puzzle = PuzzleInfo.objects.get(pk=challenge.puzzle_info.pk)
    files = challenge.challengefile_set.all()

    context = {'list_name': name, 'puzzle': puzzle, 'challenge': challenge, 'files': files}

    return render(request, template_name, context)
