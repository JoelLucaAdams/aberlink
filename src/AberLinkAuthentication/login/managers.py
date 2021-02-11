from django.contrib.auth import models

class DiscordUserOAuth2Manager(models.UserManager):

    def create_new_discord_user(self, user, openidc_user):
        discord_username = '%s#%s' % (user['username'], user['discriminator']) 
        new_user = self.create(
            id=user['id'],
            username=discord_username,
            openidc=openidc_user
        )
        return new_user

class OpenIDCUserManager(models.UserManager):

    def create_new_openidc_user(self, user):
        new_user = self.create(
            username = user['OIDC_CLAIM_preferred_username'],
            name = user['OIDC_CLAIM_name'],
            email = user['OIDC_CLAIM_email'],
            usertype = user['OIDC_CLAIM_usertype']
        )
        return new_user
        