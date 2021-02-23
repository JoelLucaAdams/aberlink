from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser, OpenIDCUser
from django.utils import timezone 

class DiscordAuthenticationBackend(BaseBackend):

    def authenticate(self, request, user, openidc_user) -> DiscordUser:
        try:
            DiscordUser.objects.filter(id=user['id']).update(last_login=timezone.now())
            return DiscordUser.objects.get(id=user['id'])
        except DiscordUser.DoesNotExist:
            print("User not in database... adding Discord user")
            DiscordUser.objects.create_user(user, openidc_user)
            return DiscordUser.objects.get(id=user['id'])

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None

class OpenIDCAuthenticationBackend(BaseBackend):

    def authenticate(self, request, user) -> OpenIDCUser:
        try:
            return OpenIDCUser.objects.get(username=user['OIDC_CLAIM_preferred_username'])
        except OpenIDCUser.DoesNotExist:
            print("User not in database... adding OpenIDC user")
            OpenIDCUser.objects.create_user(user)
            return OpenIDCUser.objects.get(username=user['OIDC_CLAIM_preferred_username'])

    def get_user(self, user_id):
        try:
            return OpenIDCUser.objects.get(pk=user_id)
        except OpenIDCUser.DoesNotExist:
            return None