from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import requests
import json
from AberLinkAuthentication.settings import config
from .auth import DiscordAuthenticationBackend, OpenIDCAuthenticationBackend
from .models import OpenIDCUser, DiscordUser

def openidc_response(request):
    metadata = request.META
    openidc_user = OpenIDCAuthenticationBackend.authenticate(OpenIDCAuthenticationBackend, request, user=metadata)
    openidc_user = list(openidc_user).pop()
    login(request, openidc_user, backend='login.auth.OpenIDCAuthenticationBackend')
    # TODO: Should probably change to logging
    return redirect('/oauth2/login')

def discord_oauth2(request):
    return redirect('https://discord.com/api/oauth2/authorize?client_id=807609453972422676&redirect_uri=https%3A%2F%2Fmmp-joa38.dcs.aber.ac.uk%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify')

@login_required(login_url="/oauth2/login")
def get_authenticated_user(request):
    discord_user = DiscordUser.objects.filter(id=request.user.id).values()
    discord_user = list(discord_user).pop()
    openidc_user = OpenIDCUser.objects.filter(id=discord_user['openidc_id']).values()
    openidc_user = list(openidc_user).pop()
    return JsonResponse({
        "Discord": {
            "id": discord_user['id'],
            "username": discord_user['username'],
            'last_login': discord_user['last_login'],
            'openidc_id': discord_user['openidc_id']
        },
        "OpenIDC": {
            'id': openidc_user['id'],
            'username': openidc_user['username'],
            'name': openidc_user['name'],
            'email': openidc_user['email'],
            'usertype': openidc_user['usertype'],
            'last_login': openidc_user['last_login']
        }
    })

def discord_oauth2_redirect(request):
    discord_code = request.GET.get('code')
    openidc_user = OpenIDCUser.objects.get(username=request.user.username)
    user = exchange_code(discord_code)
    discord_user = DiscordAuthenticationBackend.authenticate(DiscordAuthenticationBackend, request, user=user, openidc_user=openidc_user)
    discord_user = list(discord_user).pop()
    login(request, discord_user, backend='login.auth.DiscordAuthenticationBackend')
    # TODO: Should probably change to logging
    print(user)
    return redirect('/auth/user')

def exchange_code(code: str):
    # Send request code to get access token https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-redirect-url-example
    data = {
        'client_id': '807609453972422676',
        'client_secret': config['DISCORD_CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://mmp-joa38.dcs.aber.ac.uk/oauth2/login/redirect',
        'scope': 'identify'
    }
    headers = {
        'content_type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    credentials = response.json()

    # Use access token to get user information https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    access_token = credentials['access_token']
    response = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user
