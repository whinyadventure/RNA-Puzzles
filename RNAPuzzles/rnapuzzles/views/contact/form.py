from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        challenge = kwargs.pop('challenge', None)
        list_name = kwargs.pop('list', None)

        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-contactForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

        if user:

            if challenge.round == 1:
                puzzle_public_id = 'Puzzle {}'.format(challenge.puzzle_info.id)
            else:
                puzzle_public_id = 'Puzzle {}-{}'.format(challenge.puzzle_info.id, challenge.round)

            if list_name == 'Open puzzles':
                subject = '[Open puzzles: ' + puzzle_public_id + '] Question from ' + str(user)
            else:
                subject = '[Completed puzzles: ' + puzzle_public_id + '] Question from ' + str(user)

            self.fields['from_email'].initial = user.email
            self.fields['from_email'].widget.attrs['readonly'] = True

            self.fields['subject'].initial = subject
            self.fields['subject'].widget.attrs['readonly'] = True

