from django import forms
from django.conf import settings
from tempus_dominus.widgets import DateTimePicker
import os

from rnapuzzles.models import PuzzleInfo


class PuzzleInfoForm(forms.ModelForm):

    class Meta:
        model = PuzzleInfo

        fields = ('description', 'sequence', 'publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url',
                  'pdb_file', 'img')

        help_texts = {
            'description': 'Maximum 250 characters.',
            'reference': 'Publication referring to target 3D structure of the researched RNA molecule.',
            'pdb_id': 'Identifier of researched RNA molecule in Protein Data Bank. 4 characters by PBD convention.',
            'pdb_file': 'Allowed file extensions: .pdb, .cif',
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

        if self.instance.id:

            self.fields['publish_date'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'defaultDate': self.instance.publish_date.strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

        # current_status == 0
        to_hide = ['publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url', 'pdb_file', 'img']

        if current_status == 1:
            to_hide = ['description', 'sequence', 'publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url',
                       'pdb_file', 'img']

        elif current_status == 2:
            to_hide = ['description', 'sequence']

        elif current_status == 3:
            to_hide = ['description', 'sequence']
            required = ['publish_date', 'reference', 'reference_url', 'pdb_id', 'pdb_url', 'pdb_file', 'img']

            for item in required:
                self.fields[item].required = True

        for item in to_hide:
            self.fields[item].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(PuzzleInfoForm, self).clean()

        if 'pdb_file' in self.changed_data:

            pdb_file = cleaned_data['pdb_file']

            allowed_extensions = ['.pdb', '.cif']

            name, ext = os.path.splitext(pdb_file.name)

            if ext not in allowed_extensions:
                self._errors['pdb_file'] = self.error_class([u'Invalid extension of target 3D structure file.'])

        return cleaned_data



