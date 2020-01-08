from django import forms
from django.forms import modelformset_factory

from rnapuzzles.models import ChallengeFile


class ChallengeFileForm(forms.ModelForm):

    class Meta:
        model = ChallengeFile
        fields = ['file', 'note']

    def __init__(self, *args, **kwargs):
        super(ChallengeFileForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['file'].widget = forms.widgets.TextInput(attrs={'readonly': True})
            self.fields['note'].widget.attrs['readonly'] = True


FilesFormset = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=1)
CurrentFilesFormset = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=0, can_delete=True)
