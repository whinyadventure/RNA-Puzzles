from guardian.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from ...models.user import CustomUser


class Detail(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile_detail.html"

    def get_object(self, **kwargs):
        return self.request.user