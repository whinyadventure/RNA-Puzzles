# rnapuzzles/forms/puzzles_forms.py

from django import forms
from django.forms import modelformset_factory, HiddenInput
from django.db.models import Q

from ..models.puzzles import *

import datetime


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


# TODO: rendered form dependent on current_status, validation of URLS
class PuzzleInfoForm(forms.ModelForm):

    class Meta:
        model = PuzzleInfo
        fields = ('description', 'sequence', 'publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url',
                  'pdb_file', 'img')

        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
        }

        error_messages = {
            'reference_url': {
                'invalid': "Invalid URL for reference.",
            },
            'pdb_url': {
                'invalid': "Invalid URL for PDB ID."
            },
            'pdb_file': {
                'invalid_extension': "Invalid extension of target 3D structure file."
            },
            'img': {
                'invalid_extension': "Invalid extension of target 3D structure graphic representation."
            },
        }

    def __init__(self, *args, **kwargs):
        hide_condition = kwargs.pop('hide_condition', False)

        super(PuzzleInfoForm, self).__init__(*args, **kwargs)

        if hide_condition:
            to_hide = ['publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url', 'pdb_file', 'img']
            for item in to_hide:
                self.fields[item].widget = HiddenInput()


class ChallengeForm(forms.ModelForm):
    instance = None

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
        self.instance = kwargs.pop('instance', None)

        super(ChallengeForm, self).__init__(*args, **kwargs)

        if required_puzzle:
            self.fields['puzzle_info'].required = True

    def clean(self):
        cleaned_data = super(ChallengeForm, self).clean()

        if self.fields['puzzle_info'].required:
            puzzle_info = cleaned_data.get('puzzle_info')

            if puzzle_info is None:
                self._errors['puzzle_info'] = self.error_class([u'Base challenge is required.'])

        start_date = datetime.date.fromisoformat(str(self.cleaned_data.get('start_date')))

        if self.instance.pk is None:
            if start_date < datetime.date.today():
                self._errors['start_date'] = self.error_class([u'The opening date cannot be in the past.'])
        else:
            if start_date < self.instance.created_at:
                self._errors['start_date'] = self.error_class([u'The opening date cannot be earlier than creation date.'])

        end_date = datetime.date.fromisoformat(str(cleaned_data.get('end_date')))

        if end_date <= start_date:
            self._errors['end_date'] = self.error_class([u'The closing date cannot be earlier or same as the opening date.'])

        return cleaned_data


class ChallengeFileForm(forms.ModelForm):

    class Meta:
        model = ChallengeFile
        fields = ['file', 'note']


FilesFormset = modelformset_factory(ChallengeFile, form=ChallengeFileForm, extra=1)
