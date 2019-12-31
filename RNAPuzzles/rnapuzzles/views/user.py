from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from RNAPuzzles import settings
from ..models.user import CustomUser, Group
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.translation import ugettext, ugettext_lazy as _
from braces.views import LoginRequiredMixin

from ..tokens import account_activation_token


class CustomUserCreationForm(SuccessMessageMixin, UserCreationForm):
    username = None
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    new_group_name = forms.CharField(max_length=30, required=False)
    institution = forms.CharField(max_length=150, required=False)
    # group_name = forms.ChoiceField(required=False)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="")

    # user = CustomUser

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




class CustomUserLoginForm(AuthenticationForm):
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


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class SignupView(SuccessMessageMixin, CreateView):
    success_message = "Your account was successfully created. Pleas wait for confirmation email."

    template_name = "registration/signup.html"

    form_class = CustomUserCreationForm

    def get_success_url(self):
        return ""

    def get_success_url(self):
        return reverse('email_send')


class SigninView(FormView):
    template_name = "registration/login.html"
    success_url = "/"
    form_class = CustomUserLoginForm

    def get_initial(self):
        self.initial.update({'request': self.request})
        return self.initial


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile_detail.html"

    def get_object(self, **kwargs):
        return self.request.user

def get_member_count(group):
    return len([1 for x in group.customuser_set.all() if x.is_active])

class GroupsListView(ListView):
    model = Group
    template_name = "groups_list.html"


    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(GroupsListView, self).get_context_data(object_list=object_list, **kwargs)
        [setattr(x, "count",get_member_count(x)) for x in data["object_list"]]
        return data
    # def get_object(self, **kwargs):
    #    return self.request.user.group_name

class GroupDetail(DetailView):
    model = Group
    template_name = "group_detail.html"

    def get_context_data(self, **kwargs):
        data = super(GroupDetail, self).get_context_data(**kwargs)
        data["count"] = get_member_count(data["object"])


def logOut(request):
    logout(request)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        # return redirect('home')
        return render(request, 'rnapuzzles/email_confirmed.html')
    else:
        return render(request, 'rnapuzzles/email_invalid.html')

def email_send(request):
    return render(request, 'rnapuzzles/email_send.html')