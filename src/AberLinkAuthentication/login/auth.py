from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser, OpenIDCUser

class DiscordAuthenticationBackend(BaseBackend):

    def authenticate(self, request, user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) == 0:
            print("User not in database... adding Discord user")
            new_user = DiscordUser.objects.create_new_discord_user(user)
            print(new_user)
            return new_user
        return find_user

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None

class OpenIDCAuthenticationBackend(BaseBackend):

    def authenticate(self, request, user) -> OpenIDCUser:
        find_user = OpenIDCUser.objects.filter(username=user['OIDC_CLAIM_preferred_username'])
        if len(find_user) == 0:
            print("User not in database... adding OpenIDC user")
            new_user = OpenIDCUser.objects.create_new_openidc_user(user)
            print(new_user)
            return new_user
        return find_user

    def get_user(self, user_id):
        try:
            return OpenIDCUser.objects.get(pk=user_id)
        except OpenIDCUser.DoesNotExist:
            return None