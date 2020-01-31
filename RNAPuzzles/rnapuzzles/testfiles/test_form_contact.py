import os

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from guardian.utils import get_anonymous_user

from ..views.contact import ContactForm as Form


class ContactForm(TestCase):

    def setUp(self):
        self.proper = {"from_email": "adam.nowak@example.com", "subject": "subject", "message": "message",
                       'g-recaptcha-response': 'a'}

        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']

    def test_proper(self):
        form = Form(self.proper)
        self.assertTrue(form.is_valid())

    def test_missing_from_email(self):
        del self.proper["from_email"]
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

    def test_missing_message(self):
        del self.proper["message"]
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

    def test_missing_subject(self):
        del self.proper["subject"]
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        self.proper["from_email"] = "a@"
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

