from django.views.generic.detail import DetailView
from ...models.user import Group


class Detail(DetailView):
    model = Group
    template_name = "group_detail.html"

    def get_member_count(group):
        return len([1 for x in group.customuser_set.all() if x.is_active])

    def get_context_data(self, **kwargs):
        data = super(Detail, self).get_context_data(**kwargs)
        data["count"] = self.get_member_count(data["object"])