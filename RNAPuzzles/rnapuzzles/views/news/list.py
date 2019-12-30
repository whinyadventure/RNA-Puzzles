from django.db.models import Q
from django.views.generic import ListView
from guardian.mixins import PermissionListMixin

from guardian.utils import get_anonymous_user
from rnapuzzles.models import NewsModel


class List(PermissionListMixin, ListView):

    permission_required = "rnapuzzles.view_newsmodel"
    model = NewsModel
    paginate_by = 5

    def get_queryset(self, **kwargs):
        anno = get_anonymous_user()
        print(self.request.user)
        print(self.request.user.has_perm("rnapuzzles.add_newsmodel"))
        print(anno)
        print(anno.has_perm("rnapuzzles.add_newsmodel"))
        queryset = super().get_queryset()
        try:
            q = self.request.GET["q"]
            queryset = queryset.filter(
                Q(title__contains=q) | Q(description__contains=q)
            )
        except:
            pass
        if not self.request.user.is_staff:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    Q(author=self.request.user) | Q(public=True)
                )
            else:
                queryset = queryset.filter(
                    Q(public=True)
                )

        return queryset

