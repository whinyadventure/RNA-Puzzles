from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.contrib import messages

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile
from rnapuzzles.views.contact.form import ContactForm


def list_open(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'

    challenges = Challenge.objects.filter(current_status=1)

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

    return render(request, template_name, context)


def list_completed(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Completed puzzles'

    challenges = Challenge.objects.filter(current_status=4)

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

    return render(request, template_name, context)


def list_organizer(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'My puzzles'

    challenges = Challenge.objects.filter(author=request.user)

    data = []

    for challenge in challenges:
        puzzle_info = PuzzleInfo.objects.get(id=challenge.puzzle_info_id)
        files = challenge.challengefile_set.all()
        data.append([puzzle_info, challenge, files])

    context = {'list_name': name, 'data': data}

    return render(request, template_name, context)