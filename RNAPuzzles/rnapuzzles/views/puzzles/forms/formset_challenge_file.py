from django import forms
from django.forms import modelformset_factory, inlineformset_factory, BaseInlineFormSet, BaseModelFormSet

from rnapuzzles.models import Challenge, ChallengeFile


class CurrentFilesFormSet(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(CurrentFilesFormSet, self).add_fields(form, index)

        if self.instance.current_status not in {0, 1}:
            form.fields['DELETE'].widget = forms.HiddenInput()


class ChallengeFileForm(forms.ModelForm):
    currently = forms.CharField(widget=forms.HiddenInput(), required=False, label='File')

    class Meta:
        model = ChallengeFile
        fields = ['currently', 'file', 'note']

    def __init__(self, *args, **kwargs):
        super(ChallengeFileForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['currently'].widget = forms.TextInput(attrs={'readonly': True,
                                                                     'value': self.instance.file.name})
            self.fields['file'].disabled = True
            self.fields['note'].widget.attrs['readonly'] = True


FilesFormsetEmpty = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=0)
FilesFormset = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=1)
CurrentFilesFormset = inlineformset_factory(Challenge, ChallengeFile, formset=CurrentFilesFormSet, form=ChallengeFileForm,
                                            extra=0, can_delete=True)
