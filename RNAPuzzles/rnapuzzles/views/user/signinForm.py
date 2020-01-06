from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext, ugettext_lazy as _

from ...models.user import CustomUser


class SiginForm(AuthenticationForm):

    username = None
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):

        self.request = kwargs['initial']['request']
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.username_field = CustomUser._meta.get_field(CustomUser.EMAIL_FIELD)

    def clean(self):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:

            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is not None:
                login(self.request, self.user_cache)
                self.confirm_login_allowed(self.user_cache)

            else:

                print("error")
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        pass
