from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models.user import CustomUser
from django.views.generic.edit import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CustomUserCreationForm(UserCreationForm):
    username = None
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField( widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="")

    class Meta:
        model = CustomUser
        exclude = ['username']
        fields = ('email', "first_name", "last_name")




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

