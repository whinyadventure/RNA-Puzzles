import datetime
import zipfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from rnapuzzles.utils import submission as util

from rnapuzzles.models import ResourcesModel, Submission, PuzzleInfo


class FormSingle(forms.ModelForm):
    label = forms.CharField(max_length=10, help_text="Label for submitted file")
    file = forms.FileField(help_text="*.pdb file")

    helper = FormHelper()
    helper.form_id = 'submission_form'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        self.objects = []
        self.pk = kwargs.pop('pk')
        self.user = kwargs.pop('user')
        super(FormSingle, self).__init__(*args, **kwargs)

    def clean(self):
        super(FormSingle, self).clean()
        self.content = self.cleaned_data["file"].read()
        util.validate_single(self.cleaned_data["file"].name, self.content, self.pk, self.cleaned_data["label"])

        return self.cleaned_data

    def save(self, commit=True):
        util.save_single(self.content, self.user, self.pk, self.cleaned_data["label"])

    class Meta:
        model = Submission
        fields = ["label","file"]


class FormBatch(forms.ModelForm):
    success_url = ""

    file = forms.FileField(help_text="Zip file with files named PuzzleCode_Label.pdb")


    helper = FormHelper()
    helper.form_id = 'submission_form'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        self.objects = []
        self.pk = kwargs.pop('pk')
        self.user = kwargs.pop('user')
        super(FormBatch, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(FormBatch, self).clean()
        util.validate_batch(self.cleaned_data["file"])
        return cleaned_data

    def save(self, commit=True):
        util.save_batch(self.cleaned_data["file"], self.user)

    class Meta:
        model = Submission
        fields = ["file"]
