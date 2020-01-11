from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from guardian.mixins import LoginRequiredMixin
from django.urls import reverse


from .passwordForm import PasswordForm
from ...models import CustomUser


class PasswordUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "rnapuzzles/user_password_update.html"
    model = CustomUser
    success_url = ""
    success_message = "Successfully updated. You can login with Your new password."
    form_class = PasswordForm

    def get_object(self, **kwargs):
        return self.request.user

    def get_initial(self):
        self.initial.update({'request': self.request})
        return self.initial

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("home")
        return url
