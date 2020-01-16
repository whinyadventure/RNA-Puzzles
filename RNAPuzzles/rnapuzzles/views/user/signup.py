from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .signupForm import SignupForm
from ...models.user import CustomUser
from ...tokens import account_activation_token


class Signup(SuccessMessageMixin, CreateView):

    success_message = "Your account was successfully created. Pleas wait for confirmation email."
    template_name = "registration/signup.html"
    form_class = SignupForm

    def get_success_url(self):
        return reverse('email_send')

    def activate(request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.email_confirmed = True
            user.save()

            return render(request, 'rnapuzzles/email_confirmed.html')
        else:
            return render(request, 'rnapuzzles/email_invalid.html')

    def email_send(request):
        return render(request, 'rnapuzzles/email_send.html')