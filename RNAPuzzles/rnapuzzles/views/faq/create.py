from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from rnapuzzles.models import FaqModel
from rnapuzzles.views.faq.form import Form


class Create(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "rnapuzzles.add_faqmodel"
    success_url = ""
    model = FaqModel
    form_class = Form
    success_message = "FAQ was created successfully."


    def get_success_url(self):
        return reverse('faq_details', args=(self.object.pk,))
