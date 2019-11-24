from django.contrib import admin

# Register your models here.
from django.db import models as dbModels
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from martor.widgets import AdminMartorWidget
from .models import CustomUser, NewsModel

from django.apps import apps


models = apps.get_models()



@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class MarkdownModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        dbModels.TextField: {'widget': AdminMartorWidget},
    }
admin.site.register(NewsModel, MarkdownModelAdmin)