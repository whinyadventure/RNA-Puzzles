from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from ...models import CustomUser
from .resetForm import ResetForm


class PasswordReset(SuccessMessageMixin, FormView):

    template_name = "rnapuzzles/user_password_reset.html"
    model = CustomUser
    success_url = ""
    success_message = "Check your inbox. We've emailed you instructions for setting your password."
    form_class = ResetForm

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("home")
        return url
