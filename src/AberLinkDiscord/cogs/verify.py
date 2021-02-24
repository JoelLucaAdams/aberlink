import discord
from discord.ext import commands
from discord.ext.commands import Context
from cogs import admin_roles, emojis
from AberLink import logger as logging

def setup(bot):
    bot.add_cog(Verify(bot))

class Verify(commands.Cog):
    """
    Verification of aber users
    """

