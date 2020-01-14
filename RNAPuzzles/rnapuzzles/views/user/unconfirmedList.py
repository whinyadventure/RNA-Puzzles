from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from guardian.mixins import PermissionRequiredMixin
from django.urls import reverse

from ...models.user import CustomUser


class UnconfirmedList(PermissionRequiredMixin, ListView):

    permission_required = "rnapuzzles.accept_group"
    model = CustomUser
    template_name = "rnapuzzles/user_unconfirmed_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(UnconfirmedList, self).get_context_data(object_list=object_list, **kwargs)
        data['object_list'] = data['object_list'].filter(is_authorised = False, is_disabled = False )
        if(self.request.user.role == 3):
            data['object_list'] = data['object_list'].filter(group_name = self.request.user.group_name)
        print(self.request)
        return data

    def user_confirm(request, pk):
        user = CustomUser.objects.get(pk=pk)
        user.is_authorised = True
        user.save()
        return HttpResponseRedirect("/accounts/unconfirmed")

    def user_reject(request, pk):
        user = CustomUser.objects.get(pk=pk)
        user.is_disabled = True
        user.save()
        return HttpResponseRedirect("/accounts/unconfirmed")