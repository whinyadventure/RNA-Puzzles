from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from rnapuzzles.models import Challenge


# TODO: add user object manipulation permissions
def create_new(request):

    template_name = 'puzzles/new_challenge.html'

    if request.method == 'POST':
        puzzle_info_form = PuzzleInfoForm(request.POST, hide_condition=True)    # hide_condition hides form fields concerning yet unknown reference structure --> lookup in puzzles_forms.py
        challenge_form = ChallengeForm(request.POST)
        files_form = FilesFormset(request.POST, request.FILES)

        if puzzle_info_form.is_valid() and challenge_form.is_valid() and files_form.is_valid():
            puzzle_info = puzzle_info_form.save()

            challenge = challenge_form.save(commit=False)
            challenge.puzzle_info = puzzle_info
            challenge.author = request.user
            challenge.save()

            for form in files_form:

                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

            return redirect(reverse('organizer-puzzles'))

    else:
        puzzle_info_form = PuzzleInfoForm(hide_condition=True)
        challenge_form = ChallengeForm()
        files_form = FilesFormset(queryset=Challenge.objects.none())

    context = {'new': True, 'info_form': puzzle_info_form, 'challenge_form': challenge_form, 'files_form': files_form}

    return render(request, template_name, context)


def create_next(request):

    template_name = 'puzzles/next_round.html'

    puzzle = None
    data = None

    select_form = SelectForm(None)  # base puzzle selection
    challenge_form = ChallengeForm(required_puzzle=True)    # required_puzzle enforces selecting Puzzle in the first form
    files_form = FilesFormset(queryset=Challenge.objects.none())

    if request.method == 'POST':

        if 'choose_base' in request.POST:   # distinguish form posted with button's name
            select_form = SelectForm(request.POST)

            if select_form.is_valid():
                puzzle = select_form.cleaned_data.get('choice')
                challenges = Challenge.objects.filter(puzzle_info=puzzle).order_by('round')

                data = []

                for challenge in challenges:
                    files = challenge.challengefile_set.all()
                    data.append((challenge, files))

        elif 'submit_form' in request.POST:
            challenge_form = ChallengeForm(request.POST, required_puzzle=True)  # choice from first form copied to hidden input in challange_form --> lookup createForm.js
            files_form = FilesFormset(request.POST, request.FILES)

            if challenge_form.is_valid() and files_form.is_valid():
                challenge = challenge_form.save(commit=False)

                puzzle = challenge_form.cleaned_data['puzzle_info']

                challenge.puzzle_info = puzzle
                challenge.round = puzzle.challenge_set.count() + 1
                challenge.author = request.user
                challenge.save()

                for form in files_form:
                    if form.cleaned_data.get('file'):
                        file = form.save(commit=False)
                        file.challenge = challenge
                        file.save()

                return redirect(reverse('organizer-puzzles'))

    context = {'new': False, 'puzzle': puzzle, 'data': data,
               'select_form': select_form, 'challenge_form': challenge_form, 'files_form': files_form}

    return render(request, template_name, context)