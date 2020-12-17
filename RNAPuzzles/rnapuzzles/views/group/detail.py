from django.views.generic.detail import DetailView
from django.db.models import Q
from guardian.mixins import PermissionRequiredMixin

from ...models.user import Group, CustomUser


class Detail(DetailView):
    model = Group
    template_name = "group_detail.html"
    pk_url_kwarg = "pk"
    return_403 = True

    @staticmethod
    def get_member_count(group):
        return len([1 for x in group.customuser_set.all() if x.is_active])

    @staticmethod
    def get_members(group):
        return CustomUser.objects.filter( ~Q(role = 3), group_name = group)

    def get_context_data(self, **kwargs):
        data = super(Detail, self).get_context_data(**kwargs)
        setattr(data["object"], "members", list(Detail.get_members(data["object"])))

        return data
