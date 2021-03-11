"""AberLinkAuthentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
    path('', views.openidc_response, name='Home'),
    path('deleted/', views.deleted_user, name='User-data-deleted'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy-policy'),
    # JSON response with user data for debugging
    path('auth/user/', views.get_authenticated_user, name='logged-in-accounts'),
    path('admin/', admin.site.urls, name='Admin'),  
    # Responsible for discord login
    path('oauth2/login', views.discord_oauth2, name='Discord-login'),
    path('oauth2/login/redirect', views.discord_oauth2_redirect, name='Discord-response'),
]
