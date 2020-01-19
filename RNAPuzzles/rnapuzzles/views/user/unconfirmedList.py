from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from guardian.mixins import PermissionRequiredMixin
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from ...models.user import CustomUser
from RNAPuzzles import settings


class UnconfirmedList(PermissionRequiredMixin, ListView):

    accept_global_perms = True
    permission_required = "rnapuzzles.accept_group"
    model = CustomUser
    template_name = "rnapuzzles/user_unconfirmed_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(UnconfirmedList, self).get_context_data(object_list=object_list, **kwargs)
        data['object_list'] = data['object_list'].filter(email_confirmed=True, is_authorised=False, is_disabled=False )
        if self.request.user.role == 3:
            data['object_list'] = data['object_list'].filter(group_name=self.request.user.group_name)
        print(self.request)
        return data

    def user_confirm(request, pk):
        if request.user.has_perm("rnapuzzles.accept_group"):
            user = CustomUser.objects.get(pk=pk)
            user.is_authorised = True

            current_site = settings.DOMAIN_URL
            mail_subject = 'Your RNA-PUZZLES account is active now.'
            message = render_to_string('rnapuzzles/email_active_account.html', {
                'user': user,
            })

            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            print(email)
            user.save()

            return HttpResponseRedirect("/accounts/unconfirmed")
        else:
            return render(request, 'home.html')

    def user_reject(request, pk):
        if request.user.has_perm("rnapuzzles.accept_group"):
            user = CustomUser.objects.get(pk=pk)
            user.is_disabled = True

            current_site = settings.DOMAIN_URL
            mail_subject = 'Your RNA-PUZZLES account was disabled.'
            message = render_to_string('rnapuzzles/email_disable_account.html', {
                'user': user,
            })

            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            print(email)
            user.save()
            return HttpResponseRedirect("/accounts/unconfirmed")
        else:
            return render(request, 'home.html')