from django.db.models import Q
from django.views.generic import ListView
from guardian.mixins import PermissionListMixin

from guardian.utils import get_anonymous_user
from rnapuzzles.models import NewsModel


class List(ListView):
    model = NewsModel
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        try:
            q = self.request.GET["q"]
            queryset = queryset\
                .filter(Q(title__contains=q) | Q(description__contains=q))

        except:
            pass

        if not self.request.user.is_staff:

            if self.request.user.is_authenticated:
                queryset = queryset\
                    .filter(Q(author=self.request.user) | Q(public=True))
            else:
                queryset = queryset\
                    .filter(Q(public=True))

        return queryset

