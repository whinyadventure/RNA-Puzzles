from django.http import HttpResponse
from django.shortcuts import render

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile
#from rnapuzzles.views import ContactForm


def list_open(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'
    # email_form = ContactForm(ask=True, user=request.user, puzzle_id=)
    context = {'list_name': name, 'data': get_data('current_status', 1)}

    return render(request, template_name, context)


def list_completed(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Completed puzzles'
    context = {'list_name': name, 'data': get_data('current_status', 4)}

    return render(request, template_name, context)


# TODO: add to user menu 'My puzzles' option
def list_organizer(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'My puzzles'
    context = {'list_name': name, 'data': get_data('author', request.user)}

    return render(request, template_name, context)


def get_data(field, value):

    challenges = None

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


def file_download(request, pk):

    challenge_file = ChallengeFile.objects.get(pk=pk)
    file_content = open(challenge_file.file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % challenge_file.file.name

    return response