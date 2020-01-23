from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from rnapuzzles.models import ResourcesModel
from rnapuzzles.views.resources.form import Form


class Create(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    permission_required = "rnapuzzles.add_resourcesmodel"
    success_url = ""
    model = ResourcesModel
    form_class = Form
    success_message = "resources was created successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('resources_details', args=(self.object.pk,))
