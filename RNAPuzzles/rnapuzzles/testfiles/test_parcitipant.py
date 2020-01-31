

from django.test import TestCase

from rnapuzzles.models import CustomUser, Group


class ParcitipantPermissions(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group_name="Test")
        self.group2 = Group.objects.create(group_name="Test2")
        self.parcitipant :CustomUser = CustomUser.objects.create(email="a@a.pl", role=2, group_name=self.group)


    def test_parcitipant_permissions_newsmodel(self):
        """Check default permissions of parcitipant for NewsModel"""
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.add_newsmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.delete_newsmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_newsmodel"))


    def test_parcitipant_permissions_puzzleinfo(self):
        """Check default permissions of parcitipant for PuzzleInfo"""
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.add_puzzleinfo"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.delete_puzzleinfo"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_puzzleinfo"))

    def test_parcitipant_permissions_group(self):
        """Check default permissions of parcitipant for Group"""

        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.add_group"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.delete_group"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_group"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_group", self.group2))
        self.assertTrue(self.parcitipant.has_perm("rnapuzzles.change_group", self.group))

        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.name_group"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.name_group", self.group2))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.name_group", self.group))

        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.accept_group"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.accept_group", self.group2))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.accept_group", self.group))

        #self.assertFalse(self.parcitipant.has_perm("rnapuzzles.contact_group"))
        #self.assertFalse(self.parcitipant.has_perm("rnapuzzles.contact_group", self.group2))
        #self.assertFalse(self.parcitipant.has_perm("rnapuzzles.contact_group", self.group))

        #self.assertFalse(self.parcitipant.has_perm("rnapuzzles.description_group"))
        #self.assertFalse(self.parcitipant.has_perm("rnapuzzles.description_group", self.group2))
        #self.assertTrue(self.parcitipant.has_perm("rnapuzzles.description_group", self.group))

    def test_parcitipant_permissions_resources(self):
        """Check default permissions of parcitipant for Resources"""
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.add_resourcesmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.delete_resourcesmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_resourcesmodel"))


    def test_parcitipant_permissions_faq(self):
        """Check default permissions of parcitipant for Faq"""
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.add_faqmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.delete_faqmodel"))
        self.assertFalse(self.parcitipant.has_perm("rnapuzzles.change_faqmodel"))
