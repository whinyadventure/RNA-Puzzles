from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from ..models.user import CustomUser, Group
from django.http import HttpResponse
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect



class CustomUserCreationForm(UserCreationForm):
    username = None
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    new_group_name = forms.CharField(max_length=30, required=False)
    institution = forms.CharField(max_length=150, required=False)
    #group_name = forms.ChoiceField(required=False)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="")
        #user = CustomUser

    class Meta:
        model = CustomUser
        exclude = ['username']
        fields = ('email', "first_name", "last_name", "role",  "group_name", "new_group_name", "institution")

    def save(self, commit=True):
        if self.cleaned_data['role'] == 1:          #organizer
            user = CustomUser(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role = self.cleaned_data['role']
            )
            user.set_password(self.cleaned_data['password1'])
            user.save()
            return user.id
        elif self.cleaned_data['role'] == 2:        #participant
            print(self.cleaned_data['group_name'])
            group = Group.objects.get(group_name=self.cleaned_data['group_name'])
            user = group.customuser_set.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=self.cleaned_data['role'],
                institution = self.cleaned_data['institution']
            )
            user.set_password(self.cleaned_data['password1'])
            user.save()
            return user.id
        elif self.cleaned_data['role'] == 3:        #leader
            print("lider")
            group = Group(group_name = self.cleaned_data['new_group_name'])
            group.save()
            user = group.customuser_set.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role=self.cleaned_data['role'],
                institution = self.cleaned_data['institution']
            )
            user.set_password(self.cleaned_data['password1'])
            user.save()
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


class SignupView(CreateView):
    template_name = "registration/signup.html"
    success_url = ""
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return ""

class SigninView(FormView):

    template_name = "registration/login.html"
    success_url = "/"
    form_class = CustomUserLoginForm

    def get_initial(self):
        self.initial.update({ 'request': self.request })
        return self.initial

class ProfileView(LoginRequiredMixin, DetailView):

    model = CustomUser
    template_name = "profile_detail.html"

    def get_object(self, **kwargs):
        return self.request.user

class GroupsListView(ListView):

    model = Group
    template_name = "groups_list.html"



    #def get_object(self, **kwargs):
    #    return self.request.user.group_name


def logOut(request):
    logout(request)

