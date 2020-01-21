from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from ...models.user import CustomUser, Group
from RNAPuzzles import settings
from ...tokens import account_activation_token


class SignupForm(SuccessMessageMixin, UserCreationForm):

    username = None
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    new_group_name = forms.CharField(max_length=30, required=False)
    institution = forms.CharField(max_length=150, required=False)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="")
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)

    class Meta:
        model = CustomUser
        exclude = ['username']
        fields = ('email', "first_name", "last_name", "role", "group_name", "new_group_name", "institution")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(),
                Column('first_name', css_class='form-group col-md-3 mb-0 offset-md-3'),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-3 mb-0 offset-md-3'),
                Column('role', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('institution', css_class='form-group col-md-3 mb-0 offset-md-3'),
                Column(
                    Row(
                        Column('group_name', css_class='form-group col-md-12 mb-0'),

                        css_class = 'form-row'
                    ),
                    Row(
                        Column('new_group_name', css_class='form-group col-md-12 mb-0'),

                        css_class='form-row'
                    ),
                    css_class= 'form-group col-md-3'

                ),

                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-3 mb-0 offset-md-3'),
                Column('password2', css_class='form-group col-md-3 mb-0'),
                css_class='form-row '
            ),
            Row(
                Column('captcha', css_class='form-group col-md-3 mb-0 offset-md-3'),
                Column(Submit('submit', 'Sign up', css_class="custom-button"), css_class='form-group col-md-2 mb-0 offset-md-2'),
                css_class='form-row align-items-center'
            )
        )

    def save(self, commit=True):
        user = None

        if self.cleaned_data['role'] == 1:  # organizer
            user = CustomUser(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=self.cleaned_data['role']
            )

            user.set_password(self.cleaned_data['password1'])

        elif self.cleaned_data['role'] == 2:  # participant
            print(self.cleaned_data['group_name'])
            group = Group.objects.get(group_name=self.cleaned_data['group_name'])
            user = group.customuser_set.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=self.cleaned_data['role'],
                institution=self.cleaned_data['institution']
            )

            user.save()
            group.save()

        elif self.cleaned_data['role'] == 3:  # leader
            print("lider")
            group = Group(group_name=self.cleaned_data['new_group_name'])
            group.save()
            user = group.customuser_set.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=self.cleaned_data['role'],
                institution=self.cleaned_data['institution']
            )

            group.leader = user
            group.contact = user.email

            user.save()
            group.save()

        if self.cleaned_data["role"] in [1, 2, 3]:
            user.set_password(self.cleaned_data['password1'])
            user.is_active = False
            user.save()
            current_site = settings.DOMAIN_URL
            mail_subject = 'Activate your RNA-PUZZLES account.'
            message = render_to_string('rnapuzzles/email_acc_active_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = self.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            print(email)

            return user.id

        return -1