from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
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
