"""Responsible for displaying information on Admin pages such as tables on 
   linked accounts and what data can be added or deleted

DiscordUserChangeForm() which information to display in Discord users table
DiscordAdmin() which information can be displayed in Discord users table and what can be edited/changed
UserChangeForm() which information to display in table OpenID Connect (Aberystwyth) users
OpenIDCAdmin() which information can be edited/changed on OpenID Connect (Aberystwyth) users table
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Django website"
__deprecated__ = False

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import OpenIDCUser, DiscordUser

class DiscordUserChangeForm(forms.ModelForm):
    class Meta:
        model = DiscordUser
        fields = ('id', 'last_login', 'openidc')

class DiscordAdmin(UserAdmin):
    form = DiscordUserChangeForm

    list_display = ('id', 'last_login', 'openidc')
    list_filter = ('openidc',)
    fieldsets = (
        (None, {'fields': ('id', 'last_login', 'openidc')}),
    )
    readonly_fields = ('id', 'last_login', 'openidc')

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('id', 'last_login', 'openidc')
        })
    )
    search_fields = ('id', 'last_login', 'openidc',)
    ordering = ('id', 'last_login', 'openidc')
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        return False


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = OpenIDCUser
        fields = ('id', 'username', 'name', 'email', 'usertype', 'is_admin', 'last_login')

class OpenIDCAdmin(UserAdmin):
    form = UserChangeForm

    list_display = ('username', 'name', 'email', 'usertype', 'is_admin', 'last_login')
    list_filter = ('usertype',)
    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'usertype', 'last_login')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    readonly_fields = ('username', 'name', 'email', 'usertype', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'name', 'email', 'usertype', 'last_login')
        })
    )
    search_fields = ('email', 'name',)
    ordering = ('email', 'last_login',)
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(OpenIDCUser, OpenIDCAdmin)
admin.site.register(DiscordUser, DiscordAdmin)

admin.site.unregister(Group)