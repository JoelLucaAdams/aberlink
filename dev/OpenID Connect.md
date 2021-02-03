# Using OpenID Connect on uni servers

The OpenID Connect service will be responsible for logging students in using their university credentials. Currently the `usertype` variable seems to be missing and needs fixing later down the line.  

Here are some example Apache settings for libapache2-mod-auth-openidc:

OIDCProviderMetadataURL https://openidc.dcs.aber.ac.uk/auth/realms/MMP-IMPACS/.well-known/openid-configuration \
OIDCClientID `MMP-IMPACS` \
OIDCRedirectURI `/oauth2callback` \
OIDCCryptoPassphrase `some-random-string-for-encrypting-cookies` \
OIDCScope `"openid basic"` \
OIDCRemoteUserClaim `preferred_username` \
OIDCSessionInactivityTimeout `86400`

Can replace `MMP-IMPACS` which is just for dcs with `MMP-Aber` for all aber students to use.

Thank you to Alun Jones [auj] for setting this up.  

There are a useful library for using this in Django found here: https://github.com/juanifioren/django-oidc-provider
