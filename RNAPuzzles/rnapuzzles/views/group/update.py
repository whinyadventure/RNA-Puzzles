from django.views.generic import UpdateView
from guardian.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from ...models import Group, CustomUser
from .form import Form


class Update(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    permission_required = "edit_group_description"
    model = Group
    success_message = "Successfully updated."
    success_url = ""
    form_class = Form

    def get_initial(self):
        self.initial.update({'request': self.request})

        return self.initial

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)

        if url == "":
            url = reverse("groups_list")

        return url

