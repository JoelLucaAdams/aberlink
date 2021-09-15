"""Provides verification for users in servers and builds server for verification

on_member_join() checks if user is verified when they join the server, otherwise sends message to verify
verify() manual version on previous function but manually checks if user is verified
verifyAlumni() sends message telling alumni to message aft about getting verified
build() modifies the server for verification, creating new text channels and roles
getOpenID() gets database information on OpenID account and linked Discord accounts for current user
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Discord bot"
__deprecated__ = False

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.errors import CommandInvokeError, BadArgument, MissingAnyRole, BotMissingPermissions
from discord.utils import get
from AberLink import WEBSITE

from cogs import admin_roles, emojis, shelve_file
from AberLink import logger as logging
from .db import PostgreSQL

from time import time
import shelve
import asyncio

def setup(bot):
    bot.add_cog(Verify(bot))


def check_shelve_file(serverName: int):
    """
    Checks if the server has set the auto roles to false
    """
    with shelve.open(shelve_file) as db:
        if str(serverName) in db:
            data = db[str(serverName)]
            return data

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
        await ctx.send(f'You have not been verified yet. Please visit {WEBSITE} to get verified (Aber VPN is required off campus)')
        return
    return user


class Verify(commands.Cog):
    """
    Verification of Aberystwyth University students
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(manage_nicknames=True, manage_roles=True)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Triggered when a new member joins the guild and gives them the verified role
        """
        verified = get(member.guild.roles, name='verified')
        verify_channel = get(member.guild.channels, name='verify')
        db_discord_user = PostgreSQL.get_discord_user(member.id)
        # Checks if the verified role exists, if it doesn't a DM is sent to the server owner to configure it
        if verified is None:
            await verify_channel.send(f'{member.guild.owner.mention} The verified role doesn\'t exist in the server `{member.guild.name}`. Please type `!build` in one of the text channels in that server')
            return

        # Checks if the user exists in the database, if it doesn't a DM is sent to the user to tell them to get verified
        if db_discord_user is None:
            await verify_channel.send(f'{member.mention} You have not been verified yet. Please visit {WEBSITE} to get verified (VPN is required)')
            return
            
        db_openid_user = PostgreSQL.get_openid_user(db_discord_user["openidc_id"])
        email = db_openid_user["username"]
        await member.add_roles(verified, reason='Assigning user the verified role')

        if check_shelve_file(member.guild.id):
            await member.edit(nick=f'{member.name} [{email}]', reason="Changing users\'s nickname")
        

    @commands.bot_has_permissions(manage_nicknames=True, manage_roles=True)
    @commands.command(aliases=['v'])
    async def verify(self, ctx: Context):
        """
        Confirms if user is verified or not
        """
        verified = await check_verify_role(ctx)
        db_discord_user = await check_discord_user(ctx)
        if verified is None or db_discord_user is None:
            return
        db_openid_user = PostgreSQL.get_openid_user(db_discord_user["openidc_id"])
        email = db_openid_user["username"]
        user = ctx.message.author
        await user.add_roles(verified, reason='Assigning user the verified role')
        await ctx.send("You are now verified with AberLink")
         
        if check_shelve_file(ctx.guild.id):
            await user.edit(nick=f'{user.name} [{email}]', reason="Changing users\'s nickname")

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            # Gets the preious message and if it is from the bot then it knows user has been verified so sends second error
            prev_message = await ctx.channel.history(limit=1).flatten()
            if prev_message[0].author.id != os.getenv('DISCORD_CLIENT_ID'):
                await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} My role permissions aren\'t working correctly. Please open the `server settings`, navigate to the `Roles` panel and drag the `AberLink role` to the top of the list. It may also be because I can\'t change your nickname because you have higher permissions than me (e.g you are the server owner)')
            else:
                await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} I can\'t change your nickname because you have higher permissions than me (e.g you are the server owner)')
        else:
            await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} {error}')


    @commands.command(aliases=['va'])
    async def verifyAlumni(self, ctx: Context):
        """
        Verifies alumni of the university
        """
        embed = Embed(description='Unfortunately we can\'t automatically verify Alumni so please send an email to `afc@aber.ac.uk` including your discord name (e.g `JohnSmith#1234`) and we will add you. Include your name and if possible the year you graduated. It may take a day or two to do this if we are busy.', colour=discord.Color.red())
        await ctx.send(embed=embed)


    @commands.command(aliases=['b'])
    @commands.has_any_role(*admin_roles)
    @commands.bot_has_permissions(manage_roles=True, manage_messages=True, manage_channels=True)
    async def build(self, ctx: Context):
        """
        Sets up the server for verification
        """
        # Simulates that the bot is typing to visually show user command is being processed
        async with ctx.typing(): 
            start_time = time()
            description= f'{emojis["discord"]} Configuring `{ctx.guild.name}` for verification...\n'

            guild = ctx.message.guild
            bot_role = get(ctx.guild.roles, name='AberLink')
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

            #make sure that the bots position is above that of verification
            bot_role.edit(position=2)

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
                verified_role.edit(position=1)
                description += f'{int((time() - start_time) * 1000)}ms: `verified` role created\n'
            
            # Gives the bot the verified role
            bot = await guild.fetch_member(ctx.bot.user.id)
            await bot.add_roles(verified_role)

            # Create or modify verify channel
            if verify_channel is not None:
                description += f'{int((time() - start_time) * 1000)}ms: `verify` channel already exists, updating to match permissions...\n'
                message = await verify_channel.send(f'Welcome to `{guild.name}`! If you are seeing this message then please type `!verify`')
                await message.pin()
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

    @build.error
    async def build_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} My role permissions aren\'t working correctly. Please open the `server settings`, navigate to the `Roles` panel and drag the `AberLink` role to the top of the list')
        elif isinstance(error, MissingAnyRole):
            await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} {error}. Please create and assign one of these roles to yourself')
        else:
            await ctx.send(f'{emojis["aberlink_error"]}{ctx.author.mention} {error}')

    @commands.command(aliases=['go'])
    async def getOpenID(self, ctx: Context):
        """
        Displays the linked Aberystwyth and Discord accounts
        """
        discord_user = await check_discord_user(ctx)
        if discord_user is None:
            return

        message = PostgreSQL.get_openid_user(discord_user["openidc_id"])
        accounts = PostgreSQL.get_discord_accounts(discord_user["openidc_id"])

        embed = Embed(title='Aber details', colour=discord.Color.gold())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='Name', value=message["name"], inline=False)
        embed.add_field(name='Email', value=message["email"], inline=False)
        embed.add_field(name='Last login', value=message["last_login"].strftime("%G-%m-%d %X"), inline=False)

        users = ""
        for index, _ in enumerate(accounts):
            users += f'<@{accounts[index]["id"]}> - last login: {accounts[index]["last_login"].strftime("%G-%m-%d %X")}\n'
        embed.add_field(name='Linked Discord accounts', value=f'{users}', inline=False)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('🗑️')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '🗑️'

        try:
            await ctx.bot.wait_for('reaction_add', check=check, timeout=60.0)
            await msg.delete()
        except asyncio.TimeoutError:
            await msg.clear_reaction('🗑️')
            pass
