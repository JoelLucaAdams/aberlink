from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from AberLinkAuthentication.settings import config
from .auth import DiscordAuthenticationBackend, OpenIDCAuthenticationBackend
from .models import OpenIDCUser, DiscordUser
import requests
import json


def openidc_response(request):
    """
    Authenticates openidc user
    Returns redirect to '/oauth2/login' discord login page
    """
    metadata = request.META
    openidc_user = OpenIDCAuthenticationBackend().authenticate(request, user=metadata)
    login(request, openidc_user, backend='login.auth.OpenIDCAuthenticationBackend')
    # TODO: Should probably change to logging
    return redirect('/oauth2/login')


def discord_oauth2(request):
    """
    Returns redirect to discord login page
    """
    return redirect('https://discord.com/api/oauth2/authorize?client_id=807609453972422676&redirect_uri=https%3A%2F%2Fmmp-joa38.dcs.aber.ac.uk%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify')


#@login_required(login_url="/oauth2/login")
def get_authenticated_user(request):
    """
    Gets openidc user using discord user's foreign key
    Returns HTML page
    """
    openidc_user = OpenIDCUser.objects.get(username=request.user.username)
    discord_users = DiscordUser.objects.filter(openidc=openidc_user.id)
    context = {
        'openidc_user': openidc_user,
        'discord_users': discord_users,
        'title': 'Home',
    }
    return render(request, 'home.html', context)


def discord_oauth2_redirect(request):
    """
    Is the redirect from discord login and authenticates Discord user
    Returns redirect to 'auth/user/' authenticated user
    """
    # Exchange url code for discord users information
    discord_code = request.GET.get('code')
    user = exchange_code(discord_code)

    # gets openidc user using request.user.username
    openidc_user = OpenIDCUser.objects.get(username=request.user.username)
    discord_user = DiscordAuthenticationBackend().authenticate(request, user=user, openidc_user=openidc_user)
    # TODO: Should probably change to logging
    return redirect('/auth/user/')


def exchange_code(code: str):
    """
    Takes in code from discord redirect
    Returns discord user information in json
    """
    # Send request code to get access token 
    # https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-redirect-url-example
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

    # Use access token to get user information 
    # https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
    access_token = credentials['access_token']
    response = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user
