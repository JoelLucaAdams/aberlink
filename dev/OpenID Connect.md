# Using OpenID Connect on uni servers

The OpenID Connect service will be responsible for logging students in using their university credentials.

## Configuration

Here are some example Apache settings for `libapache2-mod-auth-openidc`:

OIDCProviderMetadataURL <https://openidc.dcs.aber.ac.uk/auth/realms/MMP-IMPACS/.well-known/openid-configuration> \
OIDCClientID `MMP-IMPACS` \
OIDCRedirectURI `/oauth2callback` \
OIDCCryptoPassphrase `some-random-string-for-encrypting-cookies` \
OIDCScope `"openid basic"` \
OIDCRemoteUserClaim `preferred_username` \
OIDCSessionInactivityTimeout `86400`

Can replace `MMP-IMPACS` which is just for dcs with `MMP-Aber` for all aber students to use.  

~~There are a useful library for using this in Django found here: <https://github.com/juanifioren/django-oidc-provider>~~ Replaced with the Apache library for openidc `libapache2-mod-auth-openidc`

## Usertypes

staff      - includes retired staff, visiting staff etc \
postgrad   - both taught and research \
undergrad  - undergrads (this one's straightforward, at least!) \
office     - role accounts shared within an office \
conted     - Continuing Education courses (may not exist any more) \
summer     - Summer School courses \
web        - Web site owner role accounts \
temporary  - Other temporary accounts assigned by IS \
unknown    - If we receive a new, unrecognised card type

Hopefully you won't see "unknown". I try to keep an eye on what we receive from IS and try to assign unknowns to some other category.

Thank you to Alun Jones [auj] for setting this up.
