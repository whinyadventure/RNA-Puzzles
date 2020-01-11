from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from guardian.shortcuts import assign_perm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

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
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = CustomUser
        exclude = ['username']
        fields = ('email', "first_name", "last_name", "role", "group_name", "new_group_name", "institution")

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

            assign_perm("edit_group_description", user, group)
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

            assign_perm("edit_group_name", user, group)
            assign_perm("edit_group_description", user, group)
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