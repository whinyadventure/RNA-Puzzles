from django import forms
from django.forms import modelformset_factory, HiddenInput
from django.db.models import Q

from ..models.puzzles import *


# get last round of each puzzle_info and filter only completed
class SelectForm(forms.Form):
    choice = forms.ModelChoiceField(label='Choose base challenge', required=True,
                                    queryset=PuzzleInfo.objects
                                    .filter(id__in=Challenge.objects
                                            .filter(Q(id__in=Challenge.objects
                                                      .order_by('puzzle_info', '-round')
                                                      .distinct('puzzle_info'))
                                                    & Q(current_status=4))
                                            .values('puzzle_info_id')))


class PuzzleInfoForm(forms.ModelForm):

    class Meta:
        model = PuzzleInfo
        fields = ('description', 'sequence', 'publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url',
                  'pdb_file', 'img')
        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        hide_condition = kwargs.pop('hide_condition', False)
        super(PuzzleInfoForm, self).__init__(*args, **kwargs)
        if hide_condition:
            to_hide = ['publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url', 'pdb_file', 'img']
            for item in to_hide:
                self.fields[item].widget = HiddenInput()


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ['puzzle_info', 'start_date', 'end_date']
        widgets = {
            'puzzle_info': forms.HiddenInput(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        required_puzzle = kwargs.pop('required_puzzle', False)
        super(ChallengeForm, self).__init__(*args, **kwargs)
        if required_puzzle:
            self.fields['puzzle_info'].required = True


class ChallengeFileForm(forms.ModelForm):

    class Meta:
        model = ChallengeFile
        fields = ['file', 'note']


FilesFormset = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=1)
