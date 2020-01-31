from django import forms
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

from tempus_dominus.widgets import DateTimePicker

from rnapuzzles.models import Challenge, settings


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge

        fields = ('puzzle_info', 'start_date', 'end_date', 'end_automatic')

        widgets = {
            'puzzle_info': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        required_puzzle = kwargs.pop('required_puzzle', False)

        super(ChallengeForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].input_formats = settings.DATETIME_INPUT_FORMATS
        self.fields['end_date'].input_formats = settings.DATETIME_INPUT_FORMATS
        self.fields['end_automatic'].input_formats = settings.DATETIME_INPUT_FORMATS

        if required_puzzle:
            self.fields['puzzle_info'].required = True

        if not self.instance.id:
            now = timezone.localtime(timezone.now())
            self.fields['start_date'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': (now + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': (now + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M'),
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
                    'minDate': (now + timedelta(days=1, minutes=30)).strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': (now + timedelta(days=30, minutes=30)).strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['end_automatic'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                    'minDate': (now + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M'),
                    'defaultDate': (now + timedelta(days=2, minutes=30)).strftime('%Y-%m-%d %H:%M'),
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['start_date'].help_text = 'Default: half an hour from now'
            self.fields['end_date'].help_text = 'Default: 30 days after default opening date'
            self.fields['end_automatic'].help_text = 'Default: 2 days after default opening date'

        else:

            self.fields['start_date'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
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
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['end_automatic'].widget = DateTimePicker(
                options={
                    'format': 'DD-MM-YYYY HH:mm',
                    'pickSeconds': False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )

            self.fields['start_date'].help_text = 'Minimum available opening date is challenge creation date.'
            self.fields['end_date'].help_text = ''
            self.fields['end_automatic'].help_text = ''

            disable = []

            if self.instance.current_status == 1:
                disable = ['start_date', 'end_automatic']

            elif self.instance.current_status >= 2:
                disable = ['start_date', 'end_date', 'end_automatic']

            for item in disable:
                self.fields[item].disabled = True

    def clean(self):

        cleaned_data = super(ChallengeForm, self).clean()

        if self.fields['puzzle_info'].required:
            puzzle_info = cleaned_data.get('puzzle_info')

            if puzzle_info is None:
                self._errors['puzzle_info'] = self.error_class([u'Base challenge is required.'])

        start_date = cleaned_data.get('start_date')

        if self.instance.pk is None:

            if start_date < timezone.now():
                self._errors['start_date'] = self.error_class([u'Opening date cannot be in the past.'])
        else:

            if start_date < self.instance.created_at:
                self._errors['start_date'] =\
                    self.error_class([u'Opening date cannot be earlier than the creation date.'])

        end_date = cleaned_data.get('end_date')

        if end_date <= start_date:
            self._errors['end_date'] =\
                self.error_class([u'Closing date cannot be earlier or same as the opening date.'])

        end_automatic = cleaned_data.get('end_automatic')

        if end_automatic <= start_date or end_automatic >= end_date:
            self._errors['end_automatic'] =\
                self.error_class([u"Closing date for server prediction category must be within range of opening and closing dates."])

        return cleaned_data
