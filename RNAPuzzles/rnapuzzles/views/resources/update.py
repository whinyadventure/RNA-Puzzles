from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import UpdateView
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import NewsModel, ResourcesModel
from rnapuzzles.views.news.form import Form


class Update(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    accept_global_perms = True
    permission_required = "rnapuzzles.change_resourcesmodel"
    model = ResourcesModel
    success_url = ""
    form_class = Form
    success_message = "Successfully updated."

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)

        if url == "":
            url = reverse("resources_list")

        return url
