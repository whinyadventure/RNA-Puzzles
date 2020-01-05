from django import forms

from ...models import CustomUser


class Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        if self.request.user.role == 1:
            self.fields["institution"].widget = forms.HiddenInput()

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "institution"]