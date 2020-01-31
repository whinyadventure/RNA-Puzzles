import os

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from guardian.utils import get_anonymous_user

from ..views.faq import Form


class FaqForm(TestCase):

    def setUp(self):
        self.proper = {"title":"title", "description":"description"}

        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']

    def test_proper(self):
        form = Form(self.proper)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        del self.proper["title"]
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

    def test_missing_description(self):
        del self.proper["description"]
        form = Form(self.proper)
        self.assertFalse(form.is_valid())

    def test_long_title(self):
        self.proper["title"] = "0"*101
        form = Form(self.proper)
        self.assertFalse(form.is_valid())