from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import Submission


class Detail(PermissionRequiredMixin, DetailView):
    accept_global_perms = True
    permission_required = "rnapuzzles.view_submission"
    model = Submission

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            return HttpResponseRedirect(reverse("submission_user_list"))

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)



