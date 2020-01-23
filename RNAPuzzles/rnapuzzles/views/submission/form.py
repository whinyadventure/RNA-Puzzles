import datetime
import zipfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from rnapuzzles.utils import submission as util

from rnapuzzles.models import ResourcesModel, Submission, PuzzleInfo


class Form(forms.ModelForm):
    success_url = ""

    file = forms.FileField(help_text="Help text")

    helper = FormHelper()
    helper.form_id = 'submission_form'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        self.objects = []
        self.pk = kwargs.pop('pk')
        self.user = kwargs.pop('user')
        super(Form, self).__init__(*args, **kwargs)

    def clean(self):
        super(Form, self).clean()

        if util.is_batch(self.cleaned_data["file"].name):
            self.pk = None
            util.validate_batch(self.cleaned_data["file"])

        else:
            self.content = self.cleaned_data["file"].read()
            util.validate_single(self.cleaned_data["file"].name, self.content, self.pk)

        return self.cleaned_data

    def save(self, commit=True):
        if util.is_batch(self.cleaned_data["file"].name):
            util.save_zip(self.cleaned_data["file"], self.user)
        else:
            util.save_single(self.cleaned_data["file"].name, self.content, self.user,
                             self.pk)

    class Meta:
        model = Submission
        fields = ["file"]
