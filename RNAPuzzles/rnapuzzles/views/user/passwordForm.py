from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ...models import CustomUser


class PasswordForm(SuccessMessageMixin, forms.ModelForm):

    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
        'password_mismatch': _("The two password fields didn't match.")
    }

    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']

    def clean_old_password(self):

        old_password = self.cleaned_data["old_password"]
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.request.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.request.user.save()
        return self.request.user

    class Meta:
        model = CustomUser
        fields = []