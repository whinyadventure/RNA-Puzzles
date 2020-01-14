from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from rnapuzzles.models import Submission
from rnapuzzles.views.submission.form import Form


class Create(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    permission_required = "rnapuzzles.add_submission"
    success_url = ""
    model = Submission
    form_class = Form
    success_message = "resources was created successfully."

    def get_form_kwargs(self):
        kwargs = super(Create, self).get_form_kwargs()
        if('pk' in self.kwargs):
            kwargs['pk'] = self.kwargs["pk"]
        else:
            kwargs['pk'] = None
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('submission_user_list')
