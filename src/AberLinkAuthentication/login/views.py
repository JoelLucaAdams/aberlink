from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import json
from AberLinkAuthentication.settings import config

def openidc_response(request):
    # Prints to terminal for debugging
    # TODO: Should probably change to loggin
    print(str(request.META))
    '''
    return HttpResponse(str(request.META))
    ''' # example of Json response usage
    metadata = request.META
    return JsonResponse({
        'OIDC_CLAIM_preferred_username': metadata['OIDC_CLAIM_preferred_username'],
        'OIDC_CLAIM_name': metadata['OIDC_CLAIM_name'],
        'OIDC_CLAIM_family_name': metadata['OIDC_CLAIM_family_name'],
        'OIDC_CLAIM_email': metadata['OIDC_CLAIM_email'],
        'OIDC_CLAIM_usertype': metadata['OIDC_CLAIM_usertype'],
        'OIDC_CLAIM_aud': metadata['OIDC_CLAIM_aud'],
        'OIDC_access_token': metadata['OIDC_access_token'],
        'OIDC_CLAIM_iat': metadata['OIDC_CLAIM_iat'],
        'OIDC_CLAIM_exp': metadata['OIDC_CLAIM_exp'],
        'HTTP_HOST': metadata['HTTP_HOST'],
        'REQUEST_URI': metadata['REQUEST_URI'],
        'DOCUMENT_ROOT': metadata['DOCUMENT_ROOT'],
        'REQUEST_SCHEME': metadata['REQUEST_SCHEME'],
        'SERVER_ADDR': metadata['SERVER_ADDR'],
        'SERVER_PORT': metadata['SERVER_PORT'],
        'REMOTE_ADDR': metadata['REMOTE_ADDR'],
        'SERVER_PROTOCOL': metadata['SERVER_PROTOCOL'],
        'REQUEST_METHOD': metadata['REQUEST_METHOD'],
    })

def discord_oauth2(request):
    return redirect('https://discord.com/api/oauth2/authorize?client_id=807609453972422676&redirect_uri=https%3A%2F%2Fmmp-joa38.dcs.aber.ac.uk%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify')

@login_required(login_url="/oauth2/login")
def get_authenticated_user(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "username": user.username
    })

def discord_oauth2_redirect(request):
    discord_code = request.GET.get('code')
    user = exchange_code(discord_code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
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
