# rnapuzzles/views/Puzzles.py

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DeleteView

from ..forms.puzzles_forms import *


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
            # TODO: add author from current session
            #challenge.author = request.user
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
                # TODO: add author from current session
                # challenge.author = request.user
                challenge.save()

                for form in files_form:
                    file = form.save(commit=False)
                    file.challenge = challenge
                    file.save()

                # TODO: redirect to user's puzzles
                return redirect(reverse('open-puzzles'))

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
        puzzle_info = PuzzleInfo.objects.get(id=challenge.puzzle_info_id)
        files = challenge.challengefile_set.all()
        data.append([puzzle_info, challenge, files])

    return data


def list_open(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'
    context = {'list_name': name, 'data': get_data('current_status', 1)}

    return render(request, template_name, context)


def list_completed(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'Results'
    context = {'list_name': name, 'data': get_data('current_status', 4)}

    return render(request, template_name, context)


# TODO: add to user menu 'My puzzles' option
def list_organizer(request):
    template_name = 'puzzles/list_puzzles.html'
    name = 'My puzzles'
    context = {'list_name': name, 'data': get_data('author', request.user)}

    return render(request, template_name, context)


def file_download(request, pk):
    challenge_file = ChallengeFile.objects.get(pk=pk)
    file_content = open(challenge_file.file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % challenge_file.file.name

    return response


def edit(request, pk):
    template_name = 'puzzles/puzzle_edit.html'

    challenge_input = Challenge.objects.get(pk=pk)
    puzzle_input = PuzzleInfo.objects.get(pk=challenge_input.puzzle_info.pk)
    files_input = challenge_input.challengefile_set.all()

    puzzle_info_form = PuzzleInfoForm(request.POST or None, instance=puzzle_input)
    challenge_form = ChallengeForm(request.POST or None, instance=challenge_input)

    if puzzle_info_form.is_valid() and challenge_form.is_valid():
        return redirect(reverse('open-puzzles'))

    puzzle_display_id = 'Puzzle ' + str(puzzle_input.id)
    context = {'puzzle_display_id': puzzle_display_id, 'info_form': puzzle_info_form, 'challenge_form': challenge_form}

    return render(request, template_name, context)


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

    # TODO: redirect to user's puzzles
    def get_success_url(self):
        return reverse('open-puzzles')


class ChallengeDelete(DeleteView):
    template_name = 'puzzles/puzzle_delete.html'
    model = Challenge
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

    # TODO: redirect to user's puzzles
    def get_success_url(self):
        return reverse('open-puzzles')



