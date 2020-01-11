from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from martor.fields import MartorFormField

from rnapuzzles.models import FaqModel


class Form(forms.ModelForm):

    success_url = ""

    title = forms.CharField()
    description = MartorFormField()

    helper = FormHelper()
    helper.form_id = 'Faq_form'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

    class Meta:
        model = FaqModel
        fields = ["title", "description"]
