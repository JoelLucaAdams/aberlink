from django.contrib.auth import models

class DiscordUserOAuth2Manager(models.UserManager):

    def create_user(self, user, openidc_user):
        discord_username = '%s#%s' % (user['username'], user['discriminator']) 
        new_user = self.create(
            id=user['id'],
            username=discord_username,
            openidc=openidc_user
        )
        return new_user
        