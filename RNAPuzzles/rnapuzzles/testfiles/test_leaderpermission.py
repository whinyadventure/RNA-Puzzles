

from django.test import TestCase

from rnapuzzles.models import CustomUser, Group


class LeaderPermissions(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group_name="Test")
        self.group2 = Group.objects.create(group_name="Test2")
        self.leader:CustomUser = CustomUser.objects.create(email="a@a.pl", role=3, group_name=self.group)


    def test_leader_permissions_newsmodel(self):
        """Check default permissions of leader for NewsModel"""
        self.assertTrue(self.leader.has_perm("rnapuzzles.view_newsmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.add_newsmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.delete_newsmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_newsmodel"))


    def test_leader_permissions_puzzleinfo(self):
        """Check default permissions of leader for PuzzleInfo"""
        self.assertTrue(self.leader.has_perm("rnapuzzles.view_puzzleinfo"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.add_puzzleinfo"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.delete_puzzleinfo"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_puzzleinfo"))

    def test_leader_permissions_group(self):
        """Check default permissions of leader for Group"""
        self.assertTrue(self.leader.has_perm("rnapuzzles.view_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.add_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.delete_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_group", self.group2))
        self.assertTrue(self.leader.has_perm("rnapuzzles.change_group", self.group))

        self.assertFalse(self.leader.has_perm("rnapuzzles.name_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.name_group", self.group2))
        self.assertTrue(self.leader.has_perm("rnapuzzles.name_group", self.group))

        self.assertFalse(self.leader.has_perm("rnapuzzles.accept_group"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.accept_group", self.group2))
        self.assertTrue(self.leader.has_perm("rnapuzzles.accept_group", self.group))


    def test_leader_permissions_resources(self):
        """Check default permissions of leader for Resources"""
        self.assertTrue(self.leader.has_perm("rnapuzzles.view_resourcesmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.add_resourcesmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.delete_resourcesmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_resourcesmodel"))


    def test_leader_permissions_faq(self):
        """Check default permissions of leader for Faq"""
        self.assertTrue(self.leader.has_perm("rnapuzzles.view_faqmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.add_faqmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.delete_faqmodel"))
        self.assertFalse(self.leader.has_perm("rnapuzzles.change_faqmodel"))
