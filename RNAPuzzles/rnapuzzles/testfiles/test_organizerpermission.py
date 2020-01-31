

from django.test import TestCase

from rnapuzzles.models import CustomUser


class OrganizerPermissions(TestCase):
    def setUp(self):
        self.organizer:CustomUser = CustomUser.objects.create(email="a@a.pl", role=1)


    def test_organizer_permissions_newsmodel(self):
        """Check default permissions of organizer for NewsModel"""
        self.assertTrue(self.organizer.has_perm("rnapuzzles.view_newsmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.add_newsmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_newsmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_newsmodel"))


    def test_organizer_permissions_puzzleinfo(self):
        """Check default permissions of organizer for PuzzleInfo"""
        self.assertTrue(self.organizer.has_perm("rnapuzzles.view_puzzleinfo"))
        self.assertTrue(self.organizer.has_perm("rnapuzzles.add_puzzleinfo"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_puzzleinfo"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_puzzleinfo"))

    def test_organizer_permissions_challenge(self):
        """Check default permissions of organizer for PuzzleInfo"""
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_challenge"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_challenge"))


    def test_organizer_permissions_group(self):
        """Check default permissions of organizer for Group"""
        self.assertTrue(self.organizer.has_perm("rnapuzzles.view_group"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.add_group"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_group"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_group"))

    def test_organizer_permissions_resources(self):
        """Check default permissions of organizer for Resources"""
        self.assertTrue(self.organizer.has_perm("rnapuzzles.view_resourcesmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.add_resourcesmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_resourcesmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_resourcesmodel"))


    def test_organizer_permissions_faq(self):
        """Check default permissions of organizer for Faq"""
        self.assertTrue(self.organizer.has_perm("rnapuzzles.view_faqmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.add_faqmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.delete_faqmodel"))
        self.assertFalse(self.organizer.has_perm("rnapuzzles.change_faqmodel"))
