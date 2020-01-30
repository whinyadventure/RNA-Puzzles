from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from guardian.decorators import permission_required

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile, datetime
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from rnapuzzles.models import PuzzleInfo, Challenge
from rnapuzzles.views.contact.form import ContactForm
from RNAPuzzles import settings

@permission_required("rnapuzzles.view_puzzleinfo")
def list_open(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Open puzzles'

    n = timezone.now()
    challenges = Challenge.objects.filter(Q(end_date__gte=n) & Q(start_date__lte=n))

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
                send_mail(subject, message, from_email, settings.EMAIL_HOST_USER)
                messages.add_message(request, messages.SUCCESS, 'Mail was send.')

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect(reverse('open-puzzles'))

    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'list_name': name, 'data': data, 'page_obj': page_obj}

    return render(request, template_name, context)


@permission_required("rnapuzzles.view_puzzleinfo")
def list_completed(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'Completed puzzles'

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
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'list_name': name, 'data': data, 'page_obj': page_obj}

    return render(request, template_name, context)


@permission_required("rnapuzzles.view_puzzleinfo")
def list_organizer(request):

    template_name = 'puzzles/list_puzzles.html'
    name = 'My puzzles'

    challenges = Challenge.objects.filter(author=request.user)

    data = []

    for challenge in challenges:
        puzzle_info = PuzzleInfo.objects.get(id=challenge.puzzle_info_id)
        files = challenge.challengefile_set.all()
        data.append([puzzle_info, challenge, files])

    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'list_name': name, 'data': data, 'page_obj': page_obj}

    return render(request, template_name, context)