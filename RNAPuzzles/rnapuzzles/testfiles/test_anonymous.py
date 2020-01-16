

from django.test import TestCase
from guardian.utils import get_anonymous_user

from rnapuzzles.models import CustomUser, Group


class AnonymousPermissions(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group_name="Test")
        self.group2 = Group.objects.create(group_name="Test2")
        self.Anonymous :CustomUser = get_anonymous_user()


    def test_Anonymous_permissions_newsmodel(self):
        """Check default permissions of Anonymous for NewsModel"""
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.view_newsmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.add_newsmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.delete_newsmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_newsmodel"))


    def test_Anonymous_permissions_puzzleinfo(self):
        """Check default permissions of Anonymous for PuzzleInfo"""
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.view_puzzleinfo"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.add_puzzleinfo"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.delete_puzzleinfo"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_puzzleinfo"))

    def test_Anonymous_permissions_group(self):
        """Check default permissions of Anonymous for Group"""

        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.view_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.add_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.delete_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_group", self.group2))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_group", self.group))

        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.name_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.name_group", self.group2))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.name_group", self.group))

        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.accept_group"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.accept_group", self.group2))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.accept_group", self.group))

        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.contact_group"))
        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.contact_group", self.group2))
        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.contact_group", self.group))

        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.description_group"))
        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.description_group", self.group2))
        #self.assertFalse(self.Anonymous.has_perm("rnapuzzles.description_group", self.group))

    def test_Anonymous_permissions_resources(self):
        """Check default permissions of Anonymous for Resources"""
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.view_resourcesmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.add_resourcesmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.delete_resourcesmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_resourcesmodel"))


    def test_Anonymous_permissions_faq(self):
        """Check default permissions of Anonymous for Faq"""
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.view_faqmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.add_faqmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.delete_faqmodel"))
        self.assertFalse(self.Anonymous.has_perm("rnapuzzles.change_faqmodel"))
