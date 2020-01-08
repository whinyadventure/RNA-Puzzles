from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

from rnapuzzles.views.contact.form import ContactForm


def contactView(request):

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Mail was send.')

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect(reverse("contact"))

    return render(request, "rnapuzzles/contact_form.html", {'form': form})
