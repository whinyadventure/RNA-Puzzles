from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import ResourcesModel


class Delete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "rnapuzzles.delete_resourcesmodel"
    model = ResourcesModel
    success_url = "resources"
    success_message = "resources was deleted"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Delete, self).post(request, *args, **kwargs)

    def get_success_url(self, **kwargs):

        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("resources_list")
        return url
