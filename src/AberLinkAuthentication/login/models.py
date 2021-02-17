from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .managers import DiscordUserOAuth2Manager


class OpenIDCUserManager(BaseUserManager):
    def create_user(self, user, password=None):
        new_user = self.model(
            username = user['OIDC_CLAIM_preferred_username'],
            name = user['OIDC_CLAIM_name'],
            email = user['OIDC_CLAIM_email'],
            usertype = user['OIDC_CLAIM_usertype']
        )
        if user['OIDC_CLAIM_usertype'] == "staff":
            new_user.is_staff = True
            new_user.is_admin = True

        new_user.set_password(None)
        new_user.save(using=self._db)
        return new_user

class OpenIDCUser(AbstractBaseUser):
    objects = OpenIDCUserManager()

    class usertypes(models.TextChoices):
        STAFF = "staff"
        UNDERGRAD = "undergrad"

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=30)
    usertype = models.CharField(max_length=50, choices=usertypes.choices)
    last_login = models.DateTimeField(null=True)
    password = None
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'id'
    #EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'email', 'usertype']
    
    def has_perm(self, perm, obj=None):
        if self.usertype == "staff":
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        if self.usertype == "staff":
            return True
        else:
            return False

    @property
    def is_staff(self):
        return self.is_admin
    
    def __str__(self):
        return "{} username: {}".format(self.__class__.__name__, self.username)

'''class StaffManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(usertype=OpenIDCUser.usertypes.STAFF)

class UndergradManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(usertype=OpenIDCUser.usertypes.UNDERGRAD)

class Staff(OpenIDCUser):
    objects = StaffManager()

    class Meta:
        proxy = True

class Undergrad(OpenIDCUser):
    objects = UndergradManager()

    class Meta:
        proxy = True'''


class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True)
    openidc = models.ForeignKey(OpenIDCUser, on_delete=models.CASCADE, related_name='aber_id')

    def is_authenticated(self, request):
        return True

    def is_active(self, request):
        return False

    def is_staff(self, request):
        return False

    def has_perm(self, perm):
        return False

    def has_module_perms(self, app_label):
        return False

    def __str__(self):
        return "{} id: {}".format(self.__class__.__name__, self.id)
