import json

from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from ...models import CustomUser
from RNAPuzzles import settings
from ...tokens import password_reset_token


class ResetForm(SuccessMessageMixin, forms.Form):

    error_messages = {
        'email_incorrect': _("Please enter a correct email.")
    }

    email = forms.EmailField(label=_("Email"), widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    def clean_email(self):
        try:
            user = CustomUser.objects.get(email=self.cleaned_data['email'])
        except(CustomUser.DoesNotExist):
            raise forms.ValidationError(
                self.error_messages['email_incorrect'],
                code='email_incorrect',
            )
        return self.cleaned_data

    def save(self, commit=True):
        print("save")
        user = CustomUser.objects.get(email=self.cleaned_data['email'])
        current_site = settings.DOMAIN_URL
        mail_subject = 'Activate your RNA-PUZZLES account.'
        message = render_to_string('rnapuzzles/email_acc_active_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': password_reset_token.make_token(user),
        })

        to_email = self.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )

        email.send()
        print(email)

        return True

    def reset(request):
        if request.method == "POST":
            form = ResetForm(request.POST)
            email = form.data['email']
            user = CustomUser.objects.get(email=email)
            current_site = settings.DOMAIN_URL
            mail_subject = 'Activate your RNA-PUZZLES account.'
            message = render_to_string('rnapuzzles/email_password_reset.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            print(email)

            return HttpResponseRedirect("/")


    class Meta:
        model = CustomUser
        fields = ["email"]