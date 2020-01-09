from django.test import TestCase, Client
from django.urls import reverse
from guardian.utils import get_anonymous_user

from rnapuzzles.models import Group, CustomUser


class AnonymousPermissions(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group_name="Test")
        self.anonymous: CustomUser = get_anonymous_user()
        self.parcitipant: CustomUser = CustomUser.objects.create(email="a@a.pl", role=2, group_name=self.group)
        self.leader: CustomUser = CustomUser.objects.create(email="b@a.pl", role=3, group_name=self.group)
        self.organizer: CustomUser = CustomUser.objects.create(email="c@a.pl", role=1)
        self.client = Client()

    def test_anonymous_200(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_parcitipant_200(self):
        self.client.force_login(self.parcitipant)
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_leader_200(self):
        self.client.force_login(self.leader)
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_organizer_200(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
