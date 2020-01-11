from django import forms
from django.forms import HiddenInput

from rnapuzzles.models import PuzzleInfo


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
