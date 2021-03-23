# Building the project

## Setting up Apache2

1. `sudo apt install apache2 -y` - Install apache2

2. `sudo cp ~/aberlink/config/aberlink.conf /etc/apache2/sites-available/` - copy the config file to the directory

3. Edit the file to match the file structure, below is an example of what to change the settings to:

```shell
<VirtualHost *:80>
        ServerName discord.dcs.aber.ac.uk
        ServerAlias discord.dcs.aber.ac.uk
        ServerAdmin cs-support@aber.ac.uk
        DocumentRoot /home/joel/aberlink/src/

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

4. `sudo a2ensite aberlink` - Enable the website

5. Go to `sudo nano /etc/apache2/apache2.conf` and add the following:

```shell
<Directory /home/joa38/aberlink/src/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```

## Setting up SSL

1. Install the certbot package: `sudo apt intall certbot`

2. Run this command to create the SSL certificates: `sudo certbot certonly --webroot -w ~/aberink -d discord.dcs.aber.ac.uk`

3. `sudo a2enmod rewrite` - Enable the rewrite mod for website redirect

4. `sudo a2enmod ssl` - Enable the ssl mod for SSL to work on the website

5. `source /etc/apache2/envvars` - fixes errors in apache2

6. Open the conf file again (e.g. `aberlink.conf`) and change it match the domain name:

```shell
<VirtualHost *:443>
        ServerAdmin cs-support@aber.ac.uk
        serverName discord.dcs.aber.ac.uk
        ServerAlias discord.dcs.aber.ac.uk
        DocumentRoot /home/joa38/aberlink/src/AberLinkAuthentication

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        Alias /static /home/joa38/aberlink/src/AberLinkAuthentication/static
        <Directory /home/joa38/aberlink/src/AberLinkAuthent/static>
                Require all granted
        </Directory>

        <Directory /home/joa38/aberlink/src/AberLinkAuthentication/AberLinkAuthentication>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        <Directory /home/joa38/aberlink/src/AberLinkAuthentication>
                Options Indexes FollowSymLinks
                AllowOverride None
                Require all granted
                Allow from all
        </Directory>

        <Location />
                AuthType openid-connect
                Require valid-user
        </Location>

        WSGIScriptAlias / /home/joa38/aberlink/src/AberLinkAuthentication/AberLinkAuthentication/wsgi.py
        WSGIDaemonProcess django_app python-path=/home/joa38/aberlink/src/AberLinkAuthentication python-home=/home/joa38/aberlink/src/AberLinkAuthentication/venv
        WSGIProcessGroup django_app

        SSLEngine on
        SSLCertificateFile /etc/letsencrypt/live/discord.dcs.aber.ac.uk/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/discord.dcs.aber.ac.uk/privkey.pem
        SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
</VirtualHost>

```

7. `sudo apachectl restart` - Restart Apache2 to enable the new mods
