# rnapuzzles/views/Puzzles.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from ..forms.puzzles_forms import *


# TODO: add user object manipulation permissions

#TODO guardian
#@permission_required('auth.add_puzzleinfo', return_403=True)
def create_new(request):
    template_name = 'puzzles/new_challenge.html'

    if request.method == 'POST':
        puzzle_info_form = PuzzleInfoForm(request.POST,
                                          hide_condition=True)  # hide_condition hides form fields concerning yet unknown reference structure --> lookup in puzzles_forms.py
        challenge_form = ChallengeForm(request.POST)

        files_form = FilesFormset(request.POST, request.FILES)

        if puzzle_info_form.is_valid() and challenge_form.is_valid() and files_form.is_valid():
            puzzle_info = puzzle_info_form.save()
            challenge = challenge_form.save(commit=False)
            challenge.puzzle_info = puzzle_info
            # TODO: add author from current session
            # challenge.author = request.user
            challenge.save()

            for form in files_form:
                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

            # TODO: redirect to user's puzzles
            return redirect(reverse('open-puzzles'))

    else:
        puzzle_info_form = PuzzleInfoForm(hide_condition=True)
        challenge_form = ChallengeForm()
        files_form = FilesFormset(queryset=Challenge.objects.none())

    context = {'new': True, 'info_form': puzzle_info_form, 'challenge_form': challenge_form, 'files_form': files_form}

    return render(request, template_name, context)

#TODO guardian
#@permission_required('auth.add_puzzleinfo', return_403=True)
def create_next(request):
    template_name = 'puzzles/next_round.html'

    puzzle = None
    data = None

    select_form = SelectForm(None)  # base puzzle selection
    challenge_form = ChallengeForm(required_puzzle=True)  # required_puzzle enforces selecting Puzzle in the first form
    files_form = FilesFormset(queryset=Challenge.objects.none())

    if request.method == 'POST':

        if 'choose_base' in request.POST:  # distinguish form posted with button's name
            select_form = SelectForm(request.POST)

            if select_form.is_valid():
                puzzle = select_form.cleaned_data.get('choice')
                challenges = Challenge.objects.filter(puzzle_info=puzzle).order_by('round')

                data = []
                for challenge in challenges:
                    files = challenge.challengefile_set.all()
                    data.append((challenge, files))

        elif 'submit_form' in request.POST:
            challenge_form = ChallengeForm(request.POST,
                                           required_puzzle=True)  # choice from first form copied to hidden input in challange_form --> lookup createForm.js
            files_form = FilesFormset(request.POST, request.FILES)

            if challenge_form.is_valid() and files_form.is_valid():
                challenge = challenge_form.save(commit=False)
                puzzle = challenge_form.cleaned_data['puzzle_info']
                challenge.puzzle_info = puzzle
                challenge.round = puzzle.challenge_set.count() + 1
                # TODO: add author from current session
                # challenge.author = request.user
                challenge.save()

                for form in files_form:
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

                # TODO: redirect to user's puzzles
                return redirect(reverse('open-puzzles'))
            else:
                print('nynyny blad')
                # TODO: clean method in form for conditionally required field with raise error

    context = {'new': False, 'puzzle': puzzle, 'data': data,
               'select_form': select_form, 'challenge_form': challenge_form, 'files_form': files_form}

    return render(request, template_name, context)


def get_data(field, value):
    if field == 'current_status':
        challenges = Challenge.objects.filter(current_status=value)
    elif field == 'author':
        challenges = Challenge.objects.filter(author=value)
    data = []
    for challenge in challenges:
        puzzle_info = challenge.puzzle_info
        files = challenge.challengefile_set.all()
        data.append([puzzle_info, challenge, files])

    return data


def open_puzzles(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'
    context = {'list_name': name, 'data': get_data('current_status', 1)}

    return render(request, template_name, context)


def completed_puzzles(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'Results'
    context = {'list_name': name, 'data': get_data('current_status', 4)}

    return render(request, template_name, context)


# TODO: add to user menu 'My puzzles' option
def organizer_puzzles(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'My puzzles'
    context = {'list_name': name, 'data': get_data('author', request.user)}

    return render(request, template_name, context)

#TODO guardian
#@permission_required('auth.change_challenge', (Challenge, 'pk', 'pk'),return_403=True)
def update_challenge(request, pk):
    template_name = 'puzzles/update_challenge.html'

    challenge = Challenge.objects.get(pk=pk)
    challenge_form = ChallengeForm(request.POST or None, instance=challenge)
    files_form = FilesFormset(request.POST or None, request.FILES or None, queryset=challenge.challengefile_set.all())
    puzzle_info = challenge.puzzle_info

    if request.method == 'POST':
        if challenge_form.is_valid() and files_form.is_valid():
            challenge = challenge_form.save(commit=False)
            challenge.puzzle_info = puzzle_info
            challenge.save()

            for form in files_form:
                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()
            return redirect(reverse('open-puzzles'))
    else:
        challenge_form = ChallengeForm(instance=challenge)
        files_form = FilesFormset(queryset=challenge.challengefile_set.all())

    context = {'challenge_form': challenge_form, 'files_form': files_form}
    return render(request, template_name, context)

#TODO guardian
#@permission_required('auth.change_puzzleinfo', (, 'pk', 'pk'),return_403=True)
def update_puzzle(request, pk):
    template_name = 'puzzles/update_puzzle.html'
    info: PuzzleInfo = PuzzleInfo.objects.get(pk=pk)
    puzzle_info_form = PuzzleInfoForm(request.POST or None, instance=info)
    challenges = info.challenge_set.all()

    challenge_form = None
    files_form = None
    if len(challenges) == 1:
        challenge_form = ChallengeForm(request.POST or None, instance=challenges[0])
        files_form = FilesFormset(request.POST or None, request.FILES or None, queryset=challenges[0].challengefile_set.all())
    else:
        # Block reference file
        pass
    if request.method == 'POST':

        if puzzle_info_form.is_valid() and (challenge_form is None or challenge_form.is_valid() and
                                            (challenge_form is None or files_form.is_valid())):
            if challenge_form is not None:
                challenge = challenge_form.save(commit=False)
                challenge.puzzle_info = info
                challenge.save()

                for form in files_form:
                    if form.cleaned_data.get('file'):
                        file = form.save(commit=False)
                        file.challenge = challenge
                        file.save()

            puzzle_info_form.save()
            return redirect(reverse('open-puzzles'))

    context = {'info_form': puzzle_info_form, 'challenge_form': challenge_form, 'files_form': files_form}
    return render(request, template_name, context)
