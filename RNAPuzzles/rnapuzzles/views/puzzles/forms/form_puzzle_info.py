from django import forms
from django.conf import settings
from tempus_dominus.widgets import DateTimePicker
import os

from rnapuzzles.models import PuzzleInfo


class PuzzleInfoForm(forms.ModelForm):

    class Meta:
        model = PuzzleInfo

        fields = ('description', 'sequence', 'pdb_file', 'publish_date', 'reference', 'reference_url', 'pdb_id',
                  'pdb_url', 'img')

        widgets = {
            'publish_date': DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )
        }

        help_texts = {
            'description': 'Maximum 250 characters.',
            'sequence': 'Allowed characters in sequence: [A, U, G, C, -]',
            'reference': 'Publication referring to target 3D structure of the researched RNA molecule.',
            'pdb_id': 'Identifier of researched RNA molecule in Protein Data Bank. 4 characters by PBD convention.',
            'pdb_file': 'Allowed file extensions: .pdb',
            'img': 'Allowed img extensions: .jpg, .png',
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
        current_status = kwargs.pop('current_status', 0)
        super(PuzzleInfoForm, self).__init__(*args, **kwargs)

        self.fields['publish_date'].input_formats = [settings.DATETIME_INPUT_FORMATS]

        if current_status in {0, 1}:
            to_hide = ['publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url', 'img']

            for item in to_hide:
                self.fields[item].widget = forms.HiddenInput()

        if current_status != 0:
            readonly = ['description', 'sequence']

            for item in readonly:
                self.fields[item].widget.attrs['readonly'] = True

            self.fields['pdb_file'].disabled = True

    def clean(self):
        cleaned_data = super(PuzzleInfoForm, self).clean()

        if 'sequence' in self.changed_data:

            rna_alphabet = set('AUCG-')
            seq = set(cleaned_data['sequence'])

            if seq - rna_alphabet:
                self._errors['sequence'] = self.error_class([u'Invalid RNA sequence input.'])

        return cleaned_data
