from django.contrib import admin
from .models import OpenIDCUser, DiscordUser
# Register your models here.

admin.site.register(OpenIDCUser)
admin.site.register(DiscordUser)