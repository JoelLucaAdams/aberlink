from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def pancakes(request):
    return HttpResponse("HAHA, it worked! Hello " + str(request.META['OIDC_CLAIM_preferred_username']))

