from django.db.models import Q
from django.views.generic import ListView
from guardian.mixins import PermissionListMixin

from rnapuzzles.models import ResourcesModel


class List(PermissionListMixin, ListView):

    permission_required = "rnapuzzles.view_resourcesmodel"
    model = ResourcesModel
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        try:
            q = self.request.GET["q"]
            queryset = queryset\
                .filter(Q(title__contains=q) | Q(description__contains=q))
        except:
            pass

        return queryset

