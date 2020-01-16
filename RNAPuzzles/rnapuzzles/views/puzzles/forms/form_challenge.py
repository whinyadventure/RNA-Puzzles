from django import forms
import datetime

from rnapuzzles.models import Challenge


class ChallengeForm(forms.ModelForm):

    instance = None

    class Meta:
        model = Challenge

        fields = ('puzzle_info', 'start_date', 'end_date', 'end_automatic')

        widgets = {
            'puzzle_info': forms.HiddenInput(),
<<<<<<< Updated upstream
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
=======

            'start_date': DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': next_full_hour().strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': next_full_hour().strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),

            'end_date': DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': (next_full_hour() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': (next_full_hour() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),

            'end_automatic': DateTimePicker(
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
            'start_date': 'Minimum open date is within next full hour.',
            'end_date': 'Default: 30 days after the opening date',
>>>>>>> Stashed changes
        }

    def __init__(self, *args, **kwargs):
        required_puzzle = kwargs.pop('required_puzzle', False)
        self.instance = kwargs.pop('instance', None)
        super(ChallengeForm, self).__init__(*args, **kwargs)

<<<<<<< Updated upstream
=======
        self.fields['start_date'].input_formats = [settings.DATETIME_INPUT_FORMATS]
        self.fields['end_date'].input_formats = [settings.DATETIME_INPUT_FORMATS]
        self.fields['end_automatic'].input_formats = [settings.DATETIME_INPUT_FORMATS]

>>>>>>> Stashed changes
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
