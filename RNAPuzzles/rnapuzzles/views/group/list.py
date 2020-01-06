from django.views.generic.list import ListView
from ...models.user import Group
from .detail import Detail


class List(ListView):
    model = Group
    template_name = "groups_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(List, self).get_context_data(object_list=object_list, **kwargs)
        [setattr(x, "count", Detail.get_member_count(x)) for x in data["object_list"]]
        return data