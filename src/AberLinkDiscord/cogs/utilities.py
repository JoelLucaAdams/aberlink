import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import cog_ext, SlashContext
import time

guild_ids = [802212304216260661]

class Utilities(commands.Cog):
    """
    General Utilities
    """

    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    @cog_ext.cog_subcommand(base="utilities", name="ping", guild_ids=guild_ids)
    async def _ping(self, ctx: SlashContext):
        """
        Check latency and response time 
        """
        start_time = time.time()
        message = await ctx.send('🏓 pong. `DWSPz latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms`')
        end_time = time.time()
        await message.edit(content='🏓 pong. `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms` ' +
                                   '`Response time: ' + str(int((end_time - start_time) * 1000)) + 'ms`')

    #@commands.command()
    @cog_ext.cog_subcommand(base="utilities", name="source", guild_ids=guild_ids)
    async def _source(self, ctx: SlashContext):
        """
        Print a link to the source code
        """
        await ctx.send(content='This code is currently closed source\n'
                        'Created by `Joel Adams`\n https://github.com/JoelLucaAdams/aberlink')

    #@commands.command()
    @cog_ext.cog_subcommand(base="utilities", name="pog", guild_ids=guild_ids)
    async def _pog(self, ctx: SlashContext):
        '''
        Responds with a pogalitious message
        '''
        await ctx.send(content='certified poggers moment:tm:')

def setup(bot):
    bot.add_cog(Utilities(bot))
