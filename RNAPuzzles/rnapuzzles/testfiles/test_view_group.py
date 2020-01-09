from django.test import TestCase, Client
from django.urls import reverse
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user

from rnapuzzles.models import Group, CustomUser, FaqModel


class FaqView(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group_name="Test")
        self.user_without = CustomUser.objects.create(email="a@a.pl")
        self.user_with = CustomUser.objects.create(email="b@a.pl")
        self.user_object = CustomUser.objects.create(email="c@a.pl")

        self.faq = FaqModel.objects.create(title="Test")

        assign_perm("rnapuzzles.view_faqmodel", self.user_with)
        assign_perm("rnapuzzles.change_faqmodel", self.user_with)
        assign_perm("rnapuzzles.delete_faqmodel", self.user_with)
        assign_perm("rnapuzzles.add_faqmodel", self.user_with)

        assign_perm("rnapuzzles.view_faqmodel", self.user_object, self.faq)
        assign_perm("rnapuzzles.change_faqmodel", self.user_object, self.faq)
        assign_perm("rnapuzzles.delete_faqmodel", self.user_object, self.faq)

        self.client = Client()

    def test_list_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("faq_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("faq_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("faq_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 0)

    def test_view_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("faq_details", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("faq_details", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 302)

    def test_view_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("faq_details", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("faq_delete", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("faq_delete", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("faq_delete", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("faq_update", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("faq_update", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("faq_update", args=[self.faq.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("faq_new"))
        self.assertEqual(response.status_code, 200)

    def test_add_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("faq_new"))
        self.assertEqual(response.status_code, 403)

