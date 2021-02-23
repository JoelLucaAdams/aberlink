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

class UserAdmin(UserAdmin):
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

admin.site.register(OpenIDCUser, UserAdmin)
admin.site.register(DiscordUser, DiscordAdmin)

admin.site.unregister(Group)