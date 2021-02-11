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

## Useful data to return

```python
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
```
