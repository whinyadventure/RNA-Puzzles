from django.test import TestCase, Client
from django.urls import reverse
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user

from rnapuzzles.models import CustomUser, NewsModel

#TODO hidden news
class NewsView(TestCase):
    def setUp(self):

        self.user_without = CustomUser.objects.create(email="a@a.pl")
        self.user_with = CustomUser.objects.create(email="b@a.pl")
        self.user_object = CustomUser.objects.create(email="c@a.pl")
        self.user_tmp = CustomUser.objects.create(email="d@a.pl")
        self.news = NewsModel.objects.create(title="Test", author=self.user_tmp)

        assign_perm("rnapuzzles.view_newsmodel", self.user_with)
        assign_perm("rnapuzzles.change_newsmodel", self.user_with)
        assign_perm("rnapuzzles.delete_newsmodel", self.user_with)
        assign_perm("rnapuzzles.add_newsmodel", self.user_with)

        assign_perm("rnapuzzles.view_newsmodel", self.user_object, self.news)
        assign_perm("rnapuzzles.change_newsmodel", self.user_object, self.news)
        assign_perm("rnapuzzles.delete_newsmodel", self.user_object, self.news)

        self.client = Client()

    def test_list_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("news_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("news_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_list_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("news_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["object_list"]) == 1)

    def test_view_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("news_details", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("news_details", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("news_details", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("news_delete", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("news_delete", args=[self.news.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("news_delete", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("news_update", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("news_update", args=[self.news.pk]))
        self.assertEqual(response.status_code, 302)

    def test_update_object(self):
        self.client.force_login(self.user_object)
        response = self.client.get(reverse("news_update", args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_with(self):
        self.client.force_login(self.user_with)
        response = self.client.get(reverse("news_new"))
        self.assertEqual(response.status_code, 200)

    def test_add_without(self):
        self.client.force_login(self.user_without)
        response = self.client.get(reverse("news_new"))
        self.assertEqual(response.status_code, 403)

