from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from guardian.mixins import LoginRequiredMixin
from django.urls import reverse

from .updateForm import Form
from ...models import CustomUser


class Update(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = "rnapuzzles/user_update.html"
    model = CustomUser
    success_url = ""
    success_message = "Successfully updated."
    form_class = Form

    def get_object(self, **kwargs):
        return self.request.user

    def get_initial(self):
        self.initial.update({'request': self.request})

        return self.initial

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)

        if url == "":
            url = reverse("user_detail")

        return url
