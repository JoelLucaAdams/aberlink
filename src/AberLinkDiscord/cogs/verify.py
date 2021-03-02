import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from cogs import admin_roles, emojis
from AberLink import logger as logging
from .db import PostgreSQL

from time import time

def setup(bot):
    bot.add_cog(Verify(bot))

async def check_verify_role(ctx: Context):
        """
        Checks if the verified role exists in the guild
        """
        verified = get(ctx.guild.roles, name='verified')
        if verified is None:
            await ctx.send(f'{ctx.guild.owner.mention} the verified role doesn\'t exist. Please type `!build` to configure the server for verification')
            return
        return verified

async def check_discord_user(ctx: Context):
    """
    Checks if user exists in the database
    """
    user = PostgreSQL.get_discord_user(ctx.message.author.id)
    if user is None:
        await ctx.send("You have not been verified yet. Please visit https://mmp-joa38.dcs.aber.ac.uk/ to get verified")
        return
    return user

class Verify(commands.Cog):
    """
    Verification of aber users
    """

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Triggered when a new member joins the guild and gives them the verified role
        """
        verified = get(member.guild.roles, name='verified')
        user = PostgreSQL.get_discord_user(member.id)
        # Checks if the verified role exists, if it doesn't a DM is sent to the server owner to configure it
        if verified is None:
            dm_channel = await member.guild.owner.create_dm()
            await dm_channel.send(f'{member.guild.owner.mention} the verified role doesn\'t exist in the server `{member.guild.name}`. Please type `!build` in one of the text channels in that server')
            return

        # Checks if the user exists in the database, if it doesn't a DM is sent to the user to tell them to get verified
        if user is None:
            dm_channel = await member.create_dm()
            await dm_channel.send("You have not been verified yet. Please visit https://mmp-joa38.dcs.aber.ac.uk/ to get verified")
            return
            
        await member.add_roles(verified, reason='Assigning user the verified role')
    

    @commands.command()
    async def verify(self, ctx: Context):
        """
        Confirms if user is verified or not
        """
        verified = await check_verify_role(ctx)
        db_user = await check_discord_user(ctx)
        if verified is None or db_user is None:
            return
        user = ctx.message.author
        await user.add_roles(verified, reason='Assigning user the verified role')
        await ctx.send("You are now verified with AberLink:tm:")

    @commands.command(aliases=['va'])
    async def verify_alumni(self, ctx: Context):
        """
        Verifies alumni of the university
        """
        await ctx.send('Unfortunately we can\'t automatically verify Alumni so please send an email to `afc@aber.ac.uk` including your discord name (e.g `JohnSmith#1234`) and we will add you. Include your name and if possible the year you graduated. It may take a day or two to do this if we are busy.')


    @commands.command(aliases=['b'])
    @commands.has_any_role(*admin_roles)
    @commands.bot_has_permissions(manage_roles=True, manage_messages=True, manage_channels=True)
    async def build(self, ctx: Context):
        """
        Sets up the server for verification
        """
        start_time = time()
        description= f'{emojis["discord"]} Configuring `{ctx.guild.name}` for verification...\n'

        guild = ctx.message.guild
        everyone_role = get(ctx.guild.roles, name='@everyone')
        verified_role = get(ctx.guild.roles, name='verified')
        verify_channel = get(guild.channels, name='verify')
        verify_perms = discord.PermissionOverwrite()
        verified_role_perms = discord.Permissions(
            send_messages=True, read_messages=True, read_message_history=True, 
            change_nickname=True, embed_links=True, attach_files=True, 
            add_reactions=True, external_emojis=True, 
            connect=True, speak=True, stream=True, use_voice_activation=True
            )

        # Change permissions on @everyone role
        await everyone_role.edit(reason='Configuring everyone role for verify', permissions=discord.Permissions())
        description += f'{int((time() - start_time) * 1000)}ms: `@everyone` removed all permissions\n'
        # {int((end_time - start_time) * 1000)}
        
        # Create or modify verified role
        if verified_role is not None:
            await verified_role.edit(reason='Updating old verified role', permissions=verified_role_perms)
            description += f'{int((time() - start_time) * 1000)}ms: `verified` role already exists, updating to match permissions...\n'
        else:
            verified_role = await guild.create_role(reason='Creating verified role', name='verified', permissions=verified_role_perms)
            description += f'{int((time() - start_time) * 1000)}ms: `verified` role created\n'
        
        # Gives the bot the verified role
        bot = await guild.fetch_member(ctx.bot.user.id)
        await bot.add_roles(verified_role)

        # Create or modify verify channel
        if verify_channel is not None:
            description += f'{int((time() - start_time) * 1000)}ms: `verify` channel already exists, updating to match permissions...\n'
        else:
            verify_channel = await guild.create_text_channel('verify')
            description += f'{int((time() - start_time) * 1000)}ms: `verify` channel created\n'
            message = await verify_channel.send(f'Welcome to `{guild.name}`! If you are seeing this message then please type `!verify`')
            await message.pin()
        
        # Set permissions for roles in verify channel
        verify_perms.read_messages = True
        verify_perms.send_messages = True
        verify_perms.read_message_history = True
        await verify_channel.set_permissions(everyone_role, overwrite=verify_perms)
        verify_perms.read_messages = False
        verify_perms.send_messages = False
        await verify_channel.set_permissions(verified_role, overwrite=verify_perms)
        description += f'{emojis["aberlink"]} This server is now setup for verification!'
        embed = Embed(description=description, colour=discord.Colour.green())
        await ctx.send(embed=embed)


    @commands.command(aliases=['go'])
    async def get_openid(self, ctx: Context):
        """
        Returns the users' aber username
        """
        discord_user = await check_discord_user(ctx)
        if discord_user is None:
            return
        message = PostgreSQL.get_openid_user(discord_user["openidc_id"])
        await ctx.send(f'username: {message["username"]}')
