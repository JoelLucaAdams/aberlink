# Generated by Django 3.1.6 on 2021-02-23 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210218_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discorduser',
            name='username',
        ),
    ]
