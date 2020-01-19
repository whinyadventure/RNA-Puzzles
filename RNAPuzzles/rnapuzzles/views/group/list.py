from django.views.generic.list import ListView
from ...models.user import Group
from .detail import Detail
from guardian.mixins import PermissionRequiredMixin


class List(PermissionRequiredMixin, ListView):

    PermissionRequiredMixin.accept_global_perms = True
    permission_required = "rnapuzzles.view_group"
    model = Group
    template_name = "groups_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(List, self).get_context_data(object_list=object_list, **kwargs)
        [setattr(x, "count", Detail.get_member_count(x)) for x in data["object_list"]]

        return data
