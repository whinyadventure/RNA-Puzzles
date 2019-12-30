from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import UpdateView
from guardian.mixins import PermissionRequiredMixin

from rnapuzzles.models import NewsModel, FaqModel
from rnapuzzles.views.news.form import Form


class Update(PermissionRequiredMixin, SuccessMessageMixin,  UpdateView):
    permission_required = "rnapuzzles.change_faqmodel"
    model = FaqModel
    success_url = ""
    form_class = Form
    success_message = "Successfully updated."

    def get_success_url(self):
        url = self.request.POST.get('next', self.success_url)
        if (url == ""):
            url = reverse("faq_list")
        return url

