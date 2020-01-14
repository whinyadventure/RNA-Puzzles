from django.shortcuts import render, redirect
from django.urls import reverse

from rnapuzzles.models import PuzzleInfo, Challenge
from .forms import *


#TODO guardian
#@permission_required('auth.change_puzzleinfo', (, 'pk', 'pk'),return_403=True)
def update_puzzle_info(request, pk):

    template_name = 'puzzles/update_puzzle.html'

    challenge = Challenge.objects.get(pk=pk)
    puzzle = challenge.puzzle_info

    puzzle_id = 'Puzzle {0}'.format(puzzle.id)

    puzzle_info_form = PuzzleInfoForm(request.POST or None, request.FILES or None, current_status=challenge.current_status, instance=puzzle)
    challenge_form = ChallengeForm(request.POST or None, instance=challenge)

    current_files_form = CurrentFilesFormset(request.POST or None, request.FILES or None, instance=challenge)

    files_form = FilesFormsetEmpty(request.POST or None, request.FILES or None, queryset=Challenge.objects.none())

    if challenge.current_status in {0, 1}:
        files_form = FilesFormset(request.POST or None, request.FILES or None, queryset=Challenge.objects.none())

    if request.method == 'POST':

        if puzzle_info_form.is_valid() and challenge_form.is_valid()\
                and current_files_form.is_valid() and files_form.is_valid():

            puzzle = puzzle_info_form.save()
            challenge = challenge_form.save(commit=False)
            challenge.puzzle_info = puzzle
            challenge.save()

            current_files_form.save()

            for form in files_form:

                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

            return redirect(reverse('organizer-puzzles'))

    context = {'puzzle_id': puzzle_id, 'puzzle_info_form': puzzle_info_form, 'challenge_form': challenge_form,
               'current_files_form': current_files_form, 'files_form': files_form}

    return render(request, template_name, context)

#TODO guardian
#@permission_required('auth.change_challenge', (Challenge, 'pk', 'pk'),return_403=True)
def update_challenge(request, pk):

    template_name = 'puzzles/update_challenge.html'

    challenge = Challenge.objects.get(pk=pk)
    puzzle = challenge.puzzle_info
    previous_rounds = puzzle.challenge_set.all().order_by('round')

    data = []

    for single in previous_rounds:
        if single.pk != challenge.pk:
            files = single.challengefile_set.all()
            data.append((single, files))

    puzzle_id = 'Puzzle {0}-{1}'.format(puzzle.id, challenge.round)

    challenge_form = ChallengeForm(request.POST or None, instance=challenge)

    current_files_form = CurrentFilesFormset(request.POST or None, request.FILES or None, instance=challenge)

    files_form = FilesFormset(request.POST or None, request.FILES or None, queryset=Challenge.objects.none())

    if request.method == 'POST':

        if challenge_form.is_valid() and current_files_form.is_valid() and files_form.is_valid():

            challenge = challenge_form.save(commit=False)
            challenge.puzzle_info = puzzle
            challenge.save()

            current_files_form.save()

            for form in files_form:

                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

            return redirect(reverse('organizer-puzzles'))

    context = {'puzzle_id': puzzle_id, 'puzzle': puzzle, 'data': data, 'challenge_form': challenge_form,
               'current_files_form': current_files_form, 'files_form': files_form}

    return render(request, template_name, context)


