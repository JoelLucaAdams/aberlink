from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests
import json

def pancakes(request):
    return HttpResponse(str(request.META))
    ''' # example of Json response usage
    metadata = request.META
    return JsonResponse({
        'username': metadata['OIDC_CLAIM_preferred_username'],
        'name': metadata['OIDC_CLAIM_name'],
        'family name': metadata['OIDC_CLAIM_family_name'],\
    })
    '''

def discord_oauth2(request):
    return redirect('https://discord.com/api/oauth2/authorize?client_id=807609453972422676&redirect_uri=https%3A%2F%2Fmmp-joa38.dcs.aber.ac.uk%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify')

def discord_oauth2_redirect(request):
    discord_code = request.GET.get('code')
    user = exchange_code(discord_code)
    return JsonResponse(user)

def exchange_code(code: str):
    # For information on docs see here https://discord.com/developers/docs/topics/oauth2

    # Send request code to get access token https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-redirect-url-example
    data = {
        'client_id': '807609453972422676',
        'client_secret': 'LF7HoTviVqlwaKv2ndTUe5qQnafSH4Ag',
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
