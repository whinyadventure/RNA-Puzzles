from django.db.models import Q
from django.views.generic import ListView
from guardian.mixins import PermissionListMixin

from rnapuzzles.models import ResourcesModel, Submission


class List(PermissionListMixin, ListView):

    permission_required = "rnapuzzles.view_submission"
    model = Submission
    ordering = ["-date"]

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        try:
            queryset = queryset\
                .filter(user=self.request.user)
        except:
            pass

        return queryset
