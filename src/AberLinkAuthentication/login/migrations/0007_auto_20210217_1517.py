# Generated by Django 3.1.6 on 2021-02-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20210216_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='openidcuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='openidcuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]