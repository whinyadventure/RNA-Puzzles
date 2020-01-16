from django.db.models import Q
from django.http import HttpResponse
<<<<<<< Updated upstream
from django.shortcuts import render

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile
#from rnapuzzles.views import ContactForm
=======
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.contrib import messages
from guardian.decorators import permission_required

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile, datetime
from rnapuzzles.views.contact.form import ContactForm
>>>>>>> Stashed changes

@permission_required("rnapuzzles.view_puzzleinfo")
def list_open(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'
<<<<<<< Updated upstream
    # email_form = ContactForm(ask=True, user=request.user, puzzle_id=)
    context = {'list_name': name, 'data': get_data('current_status', 1)}
=======
    n = datetime.datetime.now()
    challenges = Challenge.objects.filter(Q(end_date__gte=n)|Q(start_date__lte=n))

    data = []

    for challenge in challenges:
        puzzle_info = PuzzleInfo.objects.get(id=challenge.puzzle_info_id)
        files = challenge.challengefile_set.all()
        email_form = ContactForm(user=request.user, challenge=challenge, list=name)

        data.append([puzzle_info, challenge, files, email_form])

    if request.method == 'POST':
        email_form = ContactForm(request.POST)

        if email_form.is_valid():
            from_email = email_form.cleaned_data['from_email']
            subject = email_form.cleaned_data['subject']
            message = email_form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Mail was send.')

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect(reverse('open-puzzles'))

    context = {'list_name': name, 'data': data}
>>>>>>> Stashed changes

    return render(request, template_name, context)

@permission_required("rnapuzzles.view_puzzleinfo")
def list_completed(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Completed puzzles'
    context = {'list_name': name, 'data': get_data('current_status', 4)}

<<<<<<< Updated upstream
    return render(request, template_name, context)
=======
    challenges = Challenge.objects.filter(result_published=True)

    data = []

    for challenge in challenges:
        puzzle_info = PuzzleInfo.objects.get(id=challenge.puzzle_info_id)
        files = challenge.challengefile_set.all()
        email_form = ContactForm(user=request.user, challenge=challenge, list=name)

        data.append([puzzle_info, challenge, files, email_form])

    if request.method == 'POST':
        email_form = ContactForm(request.POST)

        if email_form.is_valid():
            from_email = email_form.cleaned_data['from_email']
            subject = email_form.cleaned_data['subject']
            message = email_form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Mail was send.')
>>>>>>> Stashed changes


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