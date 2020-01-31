from django.test import TestCase, Client
from django.urls import reverse
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user

from rnapuzzles.models import CustomUser, ResourcesModel

#TODO hidden resources
class ResourcesView(TestCase):
    def setUp(self):
        self.author = CustomUser.objects.create_user(email="author@a.pl")
        self.user_without = CustomUser.objects.create(email="a@a.pl")
        self.user_with = CustomUser.objects.create(email="b@a.pl")
        self.user_object = CustomUser.objects.create(email="c@a.pl")
        self.user_tmp = CustomUser.objects.create(email="d@a.pl")
        self.resources = ResourcesModel.objects.create(title="Test", author=self.author)

        assign_perm("rnapuzzles.view_resourcesmodel", self.user_with)
        assign_perm("rnapuzzles.change_resourcesmodel", self.user_with)
        assign_perm("rnapuzzles.delete_resourcesmodel", self.user_with)
        assign_perm("rnapuzzles.add_resourcesmodel", self.user_with)

        assign_perm("rnapuzzles.view_resourcesmodel", self.user_object, self.resources)
        assign_perm("rnapuzzles.change_resourcesmodel", self.user_object, self.resources)
        assign_perm("rnapuzzles.delete_resourcesmodel", self.user_object, self.resources)

        self.client = Client()

    def test_list_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("resources_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("resources_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("resources_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 0)

    def test_view_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("resources_details", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("resources_details", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 302)

    def test_view_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("resources_details", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("resources_delete", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("resources_delete", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("resources_delete", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("resources_update", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("resources_update", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("resources_update", args=[self.resources.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("resources_new"))
        self.assertEqual(response.status_code, 200)

    def test_add_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("resources_new"))
        self.assertEqual(response.status_code, 403)

