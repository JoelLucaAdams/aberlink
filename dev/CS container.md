# Container for website and hosting

The container is responsible for hosting the website and back-end of the code for the project.  

Can ssh into container using `ssh joa38@mmp-joa38.dcs.aber.ac.uk`

It also has Samba installed, so can connect network shares to it:

`\\mmp-joa38.dcs.aber.ac.uk\joa38` (Your home directory) \
`\\mmp-joa38.dcs.aber.ac.uk\web`  (Apache web root directory, /var/www)

This machine isn't backed up so make sure you keep copies of anything important.

Thank you to Alun Jones [auj] for setting up a container called mmp-joa38.dcs.aber.ac.uk  

## Running Django in Apache 2.0

This proved to be harder than originally expected but the website is now hosted remotely on <http://mmp-joa38.dcs.aber.ac.uk> and is done using the Debian library `libapache2-mod-wsgi-py3`. I used the following video and article to setup Apache configurations:  

* YouTube video - <https://www.youtube.com/watch?v=boHX307pyQ4&ab_channel=ProfessionalCipher>
* Article version - <https://studygyaan.com/django/how-to-setup-django-applications-with-apache-and-mod-wsgi-on-ubuntu>
