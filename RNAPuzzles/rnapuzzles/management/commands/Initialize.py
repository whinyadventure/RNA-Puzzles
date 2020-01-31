from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import AnonymousUser
from guardian.models import Group
from guardian.shortcuts import assign_perm

