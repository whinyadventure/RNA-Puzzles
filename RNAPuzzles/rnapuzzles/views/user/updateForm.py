from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from ...models import CustomUser


class Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        if self.request.user.role == 1:
            self.fields["institution"].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('last_name', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row '
            ),
            Row(
                Column('institution', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row '
            ),
            Row(
                Submit('submit', 'Save', css_class="custom-button"),
                css_class='form-row flex-d justify-content-center'
            )

        )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "institution"]