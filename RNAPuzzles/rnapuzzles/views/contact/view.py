from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

from RNAPuzzles import settings
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
                m = "Message from: "+ from_email+ "\n" \
                                                  "Subject: "+subject+"\n" \
                                                                      "Message:\n" \
                                                                      +message
                send_mail("Contact message from: "+from_email, m, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                messages.add_message(request, messages.SUCCESS, 'Message has been sent successfully!')

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect(reverse("contact"))

    return render(request, "rnapuzzles/contact_form.html", {'form': form})
