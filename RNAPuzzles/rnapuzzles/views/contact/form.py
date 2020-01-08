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
        ask_question = kwargs.pop('ask', False)
        user = kwargs.pop('user', None)
        puzzle_id = kwargs.pop('puzzle_id', None)

        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-contactForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

        if ask_question:

            kwargs.update(initial={
                'from_email': user,
                'subject': '[Open puzzles: Puzzle {}] Question from user'.format(puzzle_id)
            })

            self.fields['from_email'].widget.attrs['readonly'] = True
            self.fields['subject'].widget.attrs['readonly'] = True

