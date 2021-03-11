from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
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
    openidc_user = OpenIDCAuthenticationBackend().authenticate(request, user=request.META)
    login(request, openidc_user, backend='login.auth.OpenIDCAuthenticationBackend')

    if request.method == 'POST':
        try:
            discord_id = request.POST.get("discord_id")
            DiscordUser.objects.filter(id=discord_id).delete()
        except KeyError:
            pass
    # TODO: Should probably change to logging
    discord_users = DiscordUser.objects.filter(openidc=openidc_user.id)
    context = {
        'openidc_user': openidc_user,
        'discord_users': discord_users,
        'title': 'Home',
    }
    return render(request, 'home.html', context)

def deleted_user(request):
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        OpenIDCUser.objects.filter(username=request.user.username).delete()
    context = {
        'title': 'Deleted user data'
    }
    return render(request, 'deleted_data.html', context)

def discord_oauth2(request):
    """
    Returns redirect to discord login page
    """
    return redirect('https://discord.com/api/oauth2/authorize?client_id=807609453972422676&redirect_uri=https%3A%2F%2Fmmp-joa38.dcs.aber.ac.uk%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify')


def get_authenticated_user(request):
    """
    Gets openidc user using discord user's foreign key
    Returns JSON response for debugging
    """
    openidc_user = OpenIDCUser.objects.get(username=request.user.username)
    discord_users = DiscordUser.objects.filter(openidc=openidc_user.id)
    json_object = {
        "OpenIDC": {
            'id': openidc_user.id,
            'username': openidc_user.username,
            'name': openidc_user.name,
            'email': openidc_user.email,
            'usertype': openidc_user.usertype,
            'last_login': openidc_user.last_login
        }
    }
    for index, user in enumerate(discord_users):
        user = {f"Discord_{index}": {
            "id": user.id,
            'last_login': user.last_login,
            'openidc_id': user.openidc_id
            }
        }
        json_object.update(user)
        
    return JsonResponse(json_object)


def discord_oauth2_redirect(request):
    """
    Is the redirect from discord login and authenticates Discord user
    Returns redirect to '/'
    """
    # Exchange url code for discord users information
    discord_code = request.GET.get('code')

    # Attempts to get user to sign in, if they do not they are redirected back to the home page
    try:
        user = exchange_code(discord_code)
    except PermissionDenied:
        return redirect('/')

    # gets openidc user using request.user.username
    openidc_user = OpenIDCUser.objects.get(username=request.user.username)
    DiscordAuthenticationBackend().authenticate(request, user=user, openidc_user=openidc_user)
    # TODO: Should probably change to logging
    return redirect('/')


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

    # attempts to get acccess token, if the user cancels the rquest then raises a permission denied error
    try:
        # Use access token to get user information 
        # https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
        access_token = credentials['access_token']
    except KeyError:
        raise PermissionDenied()

    response = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user

def privacy_policy_view(request):
    """
    Returns a HTML render of the privacy policy
    """
    context = {
        'title': 'Privacy Policy'
    }
    return render(request, 'privacy_policy.html', context)