from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import OpenIDCUser, DiscordUser
# Register your models here.

class DiscordUserChangeForm(forms.ModelForm):
    class Meta:
        model = DiscordUser
        fields = ('id', 'username', 'openidc')

class DiscordAdmin(UserAdmin):
    form = DiscordUserChangeForm

    list_display = ('id', 'username', 'openidc')
    list_filter = ('openidc',)
    fieldsets = (
        (None, {'fields': ('id', 'username', 'openidc')}),
    )
    readonly_fields = ('id', 'username', 'openidc')

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('id', 'username', 'openidc')
        })
    )
    search_fields = ('id', 'username', 'openidc',)
    ordering = ('id', 'username', 'openidc')
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        return False


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = OpenIDCUser
        fields = ('id', 'username', 'name', 'email', 'usertype', 'is_admin')

class UserAdmin(UserAdmin):
    form = UserChangeForm

    list_display = ('username', 'name', 'email', 'usertype', 'is_admin')
    list_filter = ('usertype',)
    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'usertype')}),
        #('Personal info', (None))),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    readonly_fields = ('username', 'name', 'email', 'usertype')

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'name', 'email', 'usertype')
        })
    )
    search_fields = ('email', 'name',)
    ordering = ('email',)
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(OpenIDCUser, UserAdmin)
admin.site.register(DiscordUser, DiscordAdmin)

admin.site.unregister(Group)