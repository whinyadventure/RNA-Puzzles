from django.test import TestCase, Client
from django.urls import reverse
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user

from rnapuzzles.models import CustomUser, Group as CustomGroup


class GroupView(TestCase):
    def setUp(self):
        self.user_without = CustomUser.objects.create(email="a@a.pl")
        self.user_with = CustomUser.objects.create(email="b@a.pl")
        self.user_object = CustomUser.objects.create(email="c@a.pl")

        self.group = CustomGroup.objects.create(group_name="Test")

        assign_perm("rnapuzzles.delete_group", self.user_with)
        assign_perm("rnapuzzles.add_group", self.user_with)

        assign_perm("rnapuzzles.change_group", self.user_object, self.group)
        assign_perm("rnapuzzles.delete_group", self.user_object, self.group)

        self.client = Client()

    def test_list_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("groups_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("groups_list"))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("groups_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 0)

    def test_view_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("group_detail", args=[self.group.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("group_detail", args=[self.group.pk]))
        self.assertEqual(response.status_code, 403)

    def test_view_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("group_detail", args=[self.group.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("group_update", args=[self.group.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("group_update", args=[self.group.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("group_update", args=[self.group.pk]))
        self.assertEqual(response.status_code, 200)
