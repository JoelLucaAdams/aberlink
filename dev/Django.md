# Django web framework

## Motivation

Django has been chosen for this project as I have a good working knowledge of Python and will be writing the front-end in Python so having both use the same language makes it easier to work with. Django also scales very well when working on larger projects, incorporates a good backend database and login system. Documentation for Django: <https://docs.djangoproject.com/en/3.1/>

A series of videos on using Django in Python:

* 4hr Django crash course tutorial - <https://www.youtube.com/watch?v=F5mRW0jo-U4&ab_channel=freeCodeCamp.org>
* Using multiple signin methods in Django - <https://www.youtube.com/watch?v=eXyTlHhHb3U&ab_channel=DevDungeon>
* Using Discord OAuth2 with Django Ep. 1 - <https://www.youtube.com/watch?v=Cr-jxZ1TsuE&ab_channel=AnsontheDeveloper>

## Django deleting old sessions

`$ python3 manage.py shell` \
`>>> from django.contrib.sessions.models import Session` \
`>>> Session.objects.all().delete()`

## favicon usage

1. First upload an image to <https://favicon.io/favicon-converter/> and download the folder. 
2. Then copy the `favicon.ico` file over to the `src/AberLinkAuthentication/static/admin/img/` and delete the old `favicon.ico`.
3. The rest of the website should update with the new icon but if there are any issues please check or update the `src/AberLinkAuthentication/templates`.
