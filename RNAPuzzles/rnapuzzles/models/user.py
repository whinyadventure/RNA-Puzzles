import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Group(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(_('group name'), primary_key=True, unique = True, max_length = 30, blank = False)
    group_description = models.TextField(blank=True)
    #TODO leader ???

    def __str__(self):
        return self.group_name

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
      (1, 'organizer'),
      (2, 'participant'),
      (3, 'group leader')
    )

    username = None
    email = models.EmailField(_('email address'), unique = True)
    first_name = models.CharField(_('first name'), max_length = 30, blank = False)
    last_name = models.CharField(_('last name'), max_length = 30, blank = False)
    institution = models.CharField(_('institution'), max_length = 150, blank = True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank = False)
    group_name = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True)    #TODO "on_delete"???
    user_description = models.TextField(_('user description'), blank = True)
    id_active = False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name, last_name, role, group_name]

    objects = UserManager()





