import discord
from discord.ext import commands
from discord.ext.commands import Context

from cogs import admin_roles, emojis
from AberLink import logger as logging
from AberLink import WEBSITE
from .db import PostgreSQL

from datetime import datetime
import requests

def setup(bot):
    bot.add_cog(Here(bot))

class Here(commands.Cog):
    """
    Marking attendance of students during Discord practicals
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h'])
    async def here(self, ctx: Context):
        """
        Marks the student as present in the practical
        """
        await ctx.message.delete()
        dm_channel = await ctx.author.create_dm()
        discord_user = PostgreSQL.get_discord_user(ctx.author.id)
        url = 'https://integration.aber.ac.uk/joa38/submit.php'

        # Gets openid user from Discord id
        if discord_user is None:
            await dm_channel.send(f'You have not been verified yet. Please visit {WEBSITE} to get verified')
            return
        openid_user = PostgreSQL.get_openid_user(discord_user["openidc_id"])

        # getting request from API endpoint
        data = {'username': openid_user["username"]}
        api_response = requests.post(url, json=data).json()

        # If evaluates to true send user message with timestamp
        if eval(api_response["status_updated"].title()):
            current_time = datetime.now()
            current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
            await dm_channel.send(f'Your attendance in the server `{ctx.guild.name}` has been recorded for the module: `{api_response["module_code"]}` with timestamp: `{current_time}`')
        else:
            await dm_channel.send('Your attendance has not been recorded for this practical. If you believe this is incorrect please contact your module coordinator.')
