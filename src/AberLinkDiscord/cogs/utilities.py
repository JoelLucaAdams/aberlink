import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
#from discord_slash import cog_ext, SlashContext
from time import time

# test server guild
#guild_ids = [802212304216260661]

class Utilities(commands.Cog):
    """
    General Utilities
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #@cog_ext.cog_subcommand(base="utilities", name="ping", guild_ids=guild_ids)
    async def ping(self, ctx: Context):
        """
        Check latency and response time 
        """
        start_time = time()
        message = await ctx.send('🏓 pong `DWSPz latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms`')
        end_time = time()
        await message.edit(content='🏓 pong `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms` ' +
                                   '`Response time: ' + str(int((end_time - start_time) * 1000)) + 'ms`')

    @commands.command()
    #@cog_ext.cog_subcommand(base="utilities", name="source", guild_ids=guild_ids)
    async def source(self, ctx: Context):
        """
        Link to the source code
        """
        await ctx.send('This code is currently closed source\n'
                        'Created by `Joel Adams` https://github.com/JoelLucaAdams/aberlink')

    @commands.command()
    #@cog_ext.cog_subcommand(base="utilities", name="pog", guild_ids=guild_ids)
    async def pog(self, ctx: Context):
        '''
        Responds with a pogalitious message
        '''
        await ctx.send('certified poggers moment:tm:')

def setup(bot):
    bot.add_cog(Utilities(bot))
