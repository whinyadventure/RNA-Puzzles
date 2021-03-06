from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from ...models.user import CustomUser


class SigninForm(AuthenticationForm):

    error_messages = {
        'user_unconfirmed': _("Confirm email before sign in."),
        'user_inactive': _("Your account is not accepted by member."),
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
    }

    username = None
    password = None
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email"]

    def __init__(self, request=None, *args, **kwargs):
        self.request = kwargs['initial']['request']
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.username_field = CustomUser._meta.get_field(CustomUser.EMAIL_FIELD)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row '
            ),
            Row(
                Submit('submit', 'Sign in', css_class="custom-button"),
                css_class='form-row flex-d justify-content-center'
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)

            if self.user_cache is not None:
                login(self.request, self.user_cache)
                self.confirm_login_allowed(self.user_cache)

            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        user = CustomUser.objects.get(email=email)

        if not user.email_confirmed:
            raise forms.ValidationError(
               self.error_messages['user_unconfirmed'],
                code='user_unconfirmed',
                )
            return email

        if not user.is_authorised:
            raise forms.ValidationError(
               self.error_messages['user_inactive'],
                code='user_inactive',
                )

        return email

    def confirm_login_allowed(self, user):
        pass
