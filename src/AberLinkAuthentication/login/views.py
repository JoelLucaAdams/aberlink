"""Responsible for displaying webpages and dealing with requests in Django

openidc_response() authenticates user accounts and default home page
discord_oauth2() redirects users to Discord login portal
get_authenticated_user() returns JSON object containing information on user account and linked Discord accounts
discord_oauth2_redirect() gets information from discord login page and authenticates user
exchange_code() makes request to Discord to get a users information
get_discord_users() returns json array of linked Discord accounts based on queryset
deleted_user() deletes user data and displays webpage confirming it
privacy_policy_view() displays privacy policy page
about_major_project_view() displays about this project page
error_400_view(), error_403_view(), error_404_view() and error_500_view() display error webpages
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Django website"
__depricated__ = False

from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth import login
from django.db.models.query import QuerySet
from AberLinkAuthentication.settings import config
from .auth import DiscordAuthenticationBackend, OpenIDCAuthenticationBackend
from .models import OpenIDCUser, DiscordUser
import requests


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
    
    # Queries Discord to get users information and then sends to template
    discord_users_info = get_discord_users(discord_users)

    # Get account from url if exists
    new_authenticated_discord_account = request.GET.get('account')

    context = {
        'openidc_user': openidc_user,
        'discord_users': discord_users,
        'title': 'Home',
        'discord_user_info': discord_users_info,
        'new_authenticated_account': new_authenticated_discord_account,
    }
    return render(request, 'home.html', context)

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
        },
        "discord_accounts": []
    }
    for user in discord_users:
        user = {
            "id": user.id,
            'last_login': user.last_login,
            'openidc_id': user.openidc_id
            }
        json_object["discord_accounts"].append(user)
        
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
    return redirect(f'/?account={user["id"]}')


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
        'redirect_uri': f'{config["WEBSITE_URL"]}oauth2/login/redirect',
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

    response = requests.get('https://discord.com/api/v8/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user


def get_discord_users(discord_users: QuerySet):
    """
    uses bot authorisation to get Discord users' info
    Returns list of Discord users
    """
    json_response = {}
    for discord_user in discord_users:
        response = requests.get(f'https://discord.com/api/v8/users/{discord_user.id}', headers={
        'Authorization': f'Bot {config["DISCORD_TOKEN"]}'
        })
        user = response.json()
        user = {user["id"] : response.json()}
        json_response.update(user)
    return json_response

def deleted_user(request):
    """
    Displays the deleted user page and removes user from database (uses CASCADE)
    """
    if request.method == 'POST':
        try:
            request.POST.get('user_id')
            OpenIDCUser.objects.filter(username=request.user.username).delete()
        except KeyError:
            pass
    context = {
        'title': 'Deleted user data'
    }
    return render(request, 'deleted_data.html', context)

def privacy_policy_view(request):
    """
    Returns a HTML render of the privacy policy
    """
    context = {
        'title': 'Privacy Policy'
    }
    return render(request, 'privacy_policy.html', context)

def about_major_project_view(request):
    """
    Returns a HTML render of the major project webpage
    """
    context = {
        'title': 'Major Project'
    }
    return render(request, 'major_project.html', context)

def error_400_view(request, exception):
    """
    returns the error 400 page
    """
    context = {
        'title': 'Error 400'
    }
    return render(request, '400.html', context)

def error_403_view(request, exception):
    """
    returns the error 403 page
    """
    context = {
        'title': 'Error 403'
    }
    return render(request, '403.html', context)

def error_404_view(request, exception):
    """
    returns the error 404 page
    """
    context = {
        'title': 'Error 404'
    }
    return render(request, '404.html', context)

def error_500_view(request):
    """
    returns the error 500 page
    """
    context = {
        'title': 'Error 500'
    }
    return render(request, '500.html', context)