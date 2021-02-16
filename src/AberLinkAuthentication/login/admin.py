from django.contrib import admin
from .models import OpenIDCUser, DiscordUser, Staff, Undergrad
# Register your models here.

admin.site.register(OpenIDCUser)
admin.site.register(DiscordUser)
admin.site.register(Staff)
admin.site.register(Undergrad)