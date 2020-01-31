from django.views.generic import DetailView
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import Submission


class Content(PermissionRequiredMixin, DetailView):
    return_403 = True
    accept_global_perms = True
    template_name = "rnapuzzles/submission_content.html"
    permission_required = "rnapuzzles.view_submission"
    model = Submission



