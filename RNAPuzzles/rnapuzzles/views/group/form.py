from django import forms
from martor.fields import MartorFormField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from ...models import Group, CustomUser


class Form(forms.ModelForm):

    group_description = MartorFormField(required=False)

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        user = CustomUser.objects.get(id=self.request.user.id)
        group = Group.objects.get(group_name=kwargs['instance'])

        if not user.has_perm("name_group", group):
            self.fields["group_name"].widget = forms.HiddenInput()
            self.fields["contact"].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('group_name', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('contact', css_class='form-group col-md-4 mb-0 offset-md-4'),
                css_class='form-row '
            ),
            Row(
                Column('group_description', css_class='form-group'),
                css_class='form-row justify-content-center custom-martor'
            ),
            Row(
                Submit('submit', 'Save', css_class="custom-button"),
                css_class='form-row flex-d justify-content-center'
            )
        )

    class Meta:
        model = Group
        fields = ["group_name", "contact", "group_description"]
