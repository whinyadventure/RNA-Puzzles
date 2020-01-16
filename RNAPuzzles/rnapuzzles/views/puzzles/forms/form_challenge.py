from django import forms
from datetime import datetime, timedelta
from django.conf import settings
from tempus_dominus.widgets import DateTimePicker

from tempus_dominus.widgets import DateTimePicker

from rnapuzzles.models import Challenge, settings


def next_full_hour(created_at=None):
    if created_at:
        return created_at.replace(second=0, minute=0) + timedelta(hours=1)
    else:
        return datetime.today().replace(microsecond=0, second=0, minute=0) + timedelta(hours=1)


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge

        fields = ('puzzle_info', 'start_date', 'end_date', 'end_automatic')

        widgets = {
            'puzzle_info': forms.HiddenInput(),

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

        }

    def __init__(self, *args, **kwargs):
        required_puzzle = kwargs.pop('required_puzzle', False)

        super(ChallengeForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].input_formats = [settings.DATETIME_INPUT_FORMATS]
        self.fields['end_date'].input_formats = [settings.DATETIME_INPUT_FORMATS]

        self.fields['end_automatic'].input_formats = [settings.DATETIME_INPUT_FORMATS]


        if required_puzzle:
            self.fields['puzzle_info'].required = True

        if self.instance.id:

            self.fields['start_date'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': self.instance.created_at.strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': self.instance.start_date.strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['end_date'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': (self.instance.created_at + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': self.instance.end_date.strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['start_date'].help_text = 'Minimum available open date is challenge creation date.'
            self.fields['end_date'].help_text = ''

            to_hide = []

            if self.instance.current_status == 1:
                to_hide = ['start_date']

            elif self.instance.current_status in {2, 3}:
                to_hide = ['start_date', 'end_date']

            for item in to_hide:
                self.fields[item].disabled = True

    def clean(self):
        cleaned_data = super(ChallengeForm, self).clean()

        if self.fields['puzzle_info'].required:
            puzzle_info = cleaned_data.get('puzzle_info')

            if puzzle_info is None:
                self._errors['puzzle_info'] = self.error_class([u'Base challenge is required.'])

        start_date = cleaned_data.get('start_date')

        if self.instance.pk is None:

            if start_date < datetime.today():
                self._errors['start_date'] = self.error_class([u'Opening date cannot be in the past.'])
        else:

            if start_date < self.instance.created_at:
                self._errors['start_date'] =\
                    self.error_class([u'Opening date cannot be earlier than the creation date.'])

        end_date = cleaned_data.get('end_date')

        if end_date <= start_date:
            self._errors['end_date'] =\
                self.error_class([u'Closing date cannot be earlier or same as the opening date.'])

        return cleaned_data
