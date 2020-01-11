# from django.test import TestCase, Client
# from django.urls import reverse
# from guardian.shortcuts import assign_perm
# from guardian.utils import get_anonymous_user
#
# from rnapuzzles.models import CustomUser, NewsModel, PuzzleInfo
#
#
# class PuzzleView(TestCase):
#     def setUp(self):
#
#         self.user_without = CustomUser.objects.create(email="a@a.pl")
#         self.user_with = CustomUser.objects.create(email="b@a.pl")
#         self.news = PuzzleInfo.objects.create(description="Test", sequence="ABCD")
#
#         assign_perm("rnapuzzles.view_puzzleinfo", self.user_with)
#         assign_perm("rnapuzzles.change_puzzleinfo", self.user_with)
#         assign_perm("rnapuzzles.delete_puzzleinfo", self.user_with)
#         assign_perm("rnapuzzles.add_puzzleinfo", self.user_with)
#         self.client = Client()
#
#     def test_list_with(self):
#         self.client.force_login(self.user_with)
#         response = self.client.get(reverse("open-puzzles"))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse("completed-puzzles"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_list_without(self):
#         self.client.force_login(self.user_without)
#         response = self.client.get(reverse("open-puzzles"))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse("completed-puzzles"))
#         self.assertEqual(response.status_code, 200)
#     # TODO
#     # def test_view_with(self):
#     #     self.client.force_login(self.user_with)
#     #     response = self.client.get(reverse("news_details", args=[self.news.pk]))
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_view_without(self):
#     #     self.client.force_login(self.user_without)
#     #     response = self.client.get(reverse("news_details", args=[self.news.pk]))
#     #     self.assertEqual(response.status_code, 200)
#
#
#     def test_delete_with(self):
#         self.client.force_login(self.user_with)
#         response = self.client.get(reverse("puzzle-info-delete", args=[self.news.pk]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_delete_without(self):
#         self.client.force_login(self.user_without)
#         response = self.client.get(reverse("puzzle-info-delete", args=[self.news.pk]))
#         self.assertEqual(response.status_code, 302)
#
#     def test_update_with(self):
#         self.client.force_login(self.user_with)
#         response = self.client.get(reverse("update-puzzle-info", args=[self.news.pk]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_update_without(self):
#         self.client.force_login(self.user_without)
#         response = self.client.get(reverse("update-puzzle-info", args=[self.news.pk]))
#         self.assertEqual(response.status_code, 302)
#
#
#     def test_add_with(self):
#         self.client.force_login(self.user_with)
#         response = self.client.get(reverse("create-new"))
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.get(reverse("create-next"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_add_without(self):
#         self.client.force_login(self.user_without)
#         response = self.client.get(reverse("news_new"))
#         self.assertEqual(response.status_code, 403)
#
#         response = self.client.get(reverse("news_next"))
#         self.assertEqual(response.status_code, 403)
#
