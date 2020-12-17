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

    template_name = "rnapuzzles/user_new_password.html"
    model = CustomUser
    success_url = ""
    success_message = "Your password has been set. You may log in now."
    form_class = NewPasswordForm

    def get_object(self, queryset=None):
        return None

    def get_initial(self):
        self.initial.update({'request': self.request})
        self.initial.update({'uid': self.kwargs['uidb64']})
        self.initial.update({'token': self.kwargs['token']})
        return self.initial

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("home")
        return url
