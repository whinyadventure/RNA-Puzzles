from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from rnapuzzles.models import Submission
from rnapuzzles.views.submission.form import FormBatch


class CreateBatch(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    return_403 = True
    accept_global_perms = True

    permission_required = "rnapuzzles.add_submission"
    success_url = ""
    model = Submission
    form_class = FormBatch
    success_message = "resources was created successfully."

    def get_form_kwargs(self):
        kwargs = super(CreateBatch, self).get_form_kwargs()
        if('pk' in self.kwargs):
            kwargs['pk'] = self.kwargs["pk"]
        else:
            kwargs['pk'] = None
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('submission_user_list')
