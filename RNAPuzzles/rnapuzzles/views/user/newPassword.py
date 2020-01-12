from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render

from ...models import CustomUser
from .newPasswordForm import NewPasswordForm
from ...tokens import password_reset_token


class NewPassword(SuccessMessageMixin, UpdateView):

    template_name = "rnapuzzles/user_password_update.html"
    model = CustomUser
    success_url = ""
    success_message = "Successfully updated. You can login with Your new password."
    form_class = NewPasswordForm

    def get_initial(self):
        print("sialalala")
        self.initial.update({'request': self.request})
        self.initial.update({'uid': self.uidb64})
        self.initial.update({'token': self.token})
        return self.initial

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("home")
        return url
