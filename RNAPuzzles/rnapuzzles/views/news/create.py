from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from rnapuzzles.models import NewsModel
from rnapuzzles.views.news.form import Form


class Create(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    permission_required = "rnapuzzles.add_newsmodel"
    success_url = ""
    model = NewsModel
    form_class = Form
    success_message = "News was created successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('news_details', args=(self.object.pk,))
