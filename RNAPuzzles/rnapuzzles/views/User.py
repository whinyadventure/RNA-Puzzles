from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from ..models.user import CustomUser, Group
from django.views.generic.edit import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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
            user.save()
            return user.id
        return -1

#class CustomUserLoginForm(AuthenticationForm):
 #   username = None
  #  email = forms.EmailField( widget = forms.TextInput(attrs = {'placeholder': 'Email'}))


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class SignupView(CreateView):
    template_name = "form.html"
    success_url = ""
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return ""


class SigninView(CreateView):
    template_name = "form.html"
    success_url = ""
    form_class = AuthenticationForm()

    def get_success_url(self):
        return ""
