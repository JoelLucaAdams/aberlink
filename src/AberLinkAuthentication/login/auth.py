"""Responsible for authentication and login of Discord and OpenID Connect (Aberystwyth) accounts

DiscordAuthenticationBackend() trys to authenticate Discord accounts against database or creates new account
OpenIDCAuthenticationBackend() trys to authenticate OpenID Connect (Aberystwyth) accounts against database or creates new account
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Django website"
__deprecated__ = False

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