from django.contrib.auth import models

class DiscordUserOAuth2Manager(models.UserManager):

    def create_new_discord_user(self, user):
        discord_username = '%s#%s' % (user['username'], user['discriminator']) 
        new_user = self.create(
            id=user['id'],
            username=discord_username
        )
        return new_user
        