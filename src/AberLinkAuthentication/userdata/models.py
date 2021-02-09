from django.db import models
from django.db.models.fields import IntegerField

# Documentation for models.Model https://docs.djangoproject.com/en/3.1/ref/models/fields/

class UserData(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    discriminator = IntegerField()
    last_login = models.DateTimeField()