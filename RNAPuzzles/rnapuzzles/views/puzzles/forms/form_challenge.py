from django import forms
import datetime

from rnapuzzles.models import Challenge


class ChallengeForm(forms.ModelForm):

    instance = None

    class Meta:
        model = Challenge

        fields = ('puzzle_info', 'start_date', 'end_date')

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

        start_date = self.cleaned_data.get('start_date')

        if self.instance.pk is None:
            if start_date < datetime.date.today():
                self._errors['start_date'] = self.error_class([u'The opening date cannot be in the past.'])
        else:
            if start_date < self.instance.created_at:
                self._errors['start_date'] =\
                    self.error_class([u'The opening date cannot be earlier than creation date.'])

        end_date = cleaned_data.get('end_date')

        if end_date <= start_date:
            self._errors['end_date'] =\
                self.error_class([u'The closing date cannot be earlier or same as the opening date.'])

        return cleaned_data
