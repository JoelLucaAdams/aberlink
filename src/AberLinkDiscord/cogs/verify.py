import discord
from discord.ext import commands
from discord.ext.commands import Context
from cogs import admin_roles, emojis
from AberLink import logger as logging
from postgresql import postgreSQL

def setup(bot):
    bot.add_cog(Verify(bot))

class Verify(commands.Cog):
    """
    Verification of aber users
    """

    @commands.command()
    async def verify(self, ctx: Context):
        """
        Confirms if user is verified or not
        """
        if postgreSQL.get_discord_user(ctx.message.author.id) is not None:
            verified = discord.utils.get(ctx.guild.roles, name='verified')
            user = ctx.message.author
            await user.add_roles(verified, reason='Assigning user the Verified role')
            await ctx.send("You are now verified with AberLink:tm:")
        else:
            await ctx.send("You have not been verified yet. Please visit to get verified: https://mmp-joa38.dcs.aber.ac.uk/")

    @commands.command(aliases=['b'])
    @commands.has_any_role(*admin_roles)
    @commands.bot_has_permissions(manage_roles=True, manage_messages=True, manage_channels=True)
    async def build(self, ctx: Context):
        """
        Sets up the server for verification
        """
        guild = ctx.message.guild
        everyone_role = discord.utils.get(ctx.guild.roles, name='@everyone')
        verified_role = discord.utils.get(ctx.guild.roles, name='verified')
        verify_channel = discord.utils.get(guild.channels, name='verify')
        verify_perms = discord.PermissionOverwrite()
        verified_role_perms = discord.Permissions(
            send_messages=True, read_messages=True, read_message_history=True, 
            change_nickname=True, embed_links=True, attach_files=True, 
            add_reactions=True, external_emojis=True, 
            connect=True, speak=True, stream=True, use_voice_activation=True
            )

        # Change permissions on @everyone role
        await everyone_role.edit(reason='Configuring everyone role for verify', permissions=discord.Permissions())
        await ctx.send('`@everyone` removed all permissions')
        
        # Create or modify verified role
        if verified_role:
            await verified_role.edit(reason='Updating old verified role', permissions=verified_role_perms)
            await ctx.send('`verified` role already exists, updating to match permissions...')
        else:
            verified_role = await guild.create_role(reason='Creating verified role', name='verified', permissions=verified_role_perms)
            await ctx.send('`verified` role created')
        
        # Gives the bot the verified role
        bot = await guild.fetch_member(ctx.bot.user.id)
        await bot.add_roles(verified_role)

        # Create or modify verify channel
        if verify_channel:
            await ctx.send('`verify` channel already exists, updating to match permissions...')
        else:
            verify_channel = await guild.create_text_channel('verify')
            await ctx.send('`verify` channel created')
            message = await verify_channel.send(f'Welcome to `{guild.name}`! If you are seeing this message then please type `!verify`')
            await message.pin()
        
        # Set permissions for roles in verify channel
        verify_perms.read_messages = True
        verify_perms.send_messages = True
        await verify_channel.set_permissions(everyone_role, overwrite=verify_perms)
        verify_perms.read_messages = False
        verify_perms.send_messages = False
        await verify_channel.set_permissions(verified_role, overwrite=verify_perms)


    @commands.command(aliases=['go'])
    async def get_openid(self, ctx: Context):
        """
        Returns the users' aber username
        """
        try:
            discord_user = postgreSQL.get_discord_user(ctx.message.author.id)
            message = postgreSQL.get_openid_user(discord_user["openidc_id"])
            await ctx.send(f'username: {message["username"]}')
        except TypeError:
            await ctx.send("You have not been verified yet. Please visit to get verified: https://mmp-joa38.dcs.aber.ac.uk/")
