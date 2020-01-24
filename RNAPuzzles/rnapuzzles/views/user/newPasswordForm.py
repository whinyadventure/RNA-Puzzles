from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from ...models import CustomUser
from ...tokens import password_reset_token

class NewPasswordForm(SuccessMessageMixin, forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")
    }

    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        self.uid = force_text(urlsafe_base64_decode(kwargs['initial']['uid']))
        self.token = kwargs['initial']['token']

        try:
            self.user = CustomUser.objects.get(pk=self.uid)
        except:
            self.user = None
        self.linkvalid = True
        if not(self.user is not None and default_token_generator.check_token(self.user, self.token)):
            self.linkvalid = False
            #return HttpResponseRedirect("/")
    def clean(self):
        clean_data = super(NewPasswordForm, self).clean()
        if not (self.user is not None and default_token_generator.check_token(self.user, self.token)):
            return HttpResponseRedirect("/")
        return clean_data
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('newpassword1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.request.user

    class Meta:
        model = CustomUser
        fields = []