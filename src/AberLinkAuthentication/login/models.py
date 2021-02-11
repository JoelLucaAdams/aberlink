from django.db import models
from .managers import DiscordUserOAuth2Manager, OpenIDCUserManager

# Create your models here.

class OpenIDCUser(models.Model):
    objects = OpenIDCUserManager()

    username = models.CharField(max_length=40)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=30)
    usertype = models.CharField(max_length=50)
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self, request):
        return True

    '''def __str__(self):
        return "{} username: {}".format(self.__class__.__name__, self.username)'''


class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True)
    openidc = models.ForeignKey(OpenIDCUser, on_delete=models.CASCADE, related_name='aber_id')

    def is_authenticated(self, request):
        return True

    '''def __str__(self):
        return "{} id: {}".format(self.__class__.__name__, self.id)'''
