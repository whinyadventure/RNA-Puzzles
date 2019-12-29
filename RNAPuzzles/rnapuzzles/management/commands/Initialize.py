from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import AnonymousUser
from guardian.models import Group
from guardian.shortcuts import assign_perm


class Command(BaseCommand):
    help = 'Initilize project. Creates Default group. Adds AnynomusUser do Default. Assign perm to view_newsmodel do Default group'

    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Defaults")
        if (not created and group is None):
            raise ValueError("Unable to create group")
        assign_perm("rnapuzzles.view_newsmodel", AnonymousUser())
        assign_perm("rnapuzzles.view_newsmodel", group)
