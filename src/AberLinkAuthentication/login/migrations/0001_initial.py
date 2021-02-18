# Generated by Django 3.1.6 on 2021-02-18 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpenIDCUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=30)),
                ('usertype', models.CharField(choices=[('staff', 'Staff'), ('undergrad', 'Undergrad')], max_length=50)),
                ('last_login', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('last_login', models.DateTimeField(null=True)),
                ('openidc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aber_id', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('objects', login.models.DiscordUserOAuth2Manager()),
            ],
        ),
    ]
