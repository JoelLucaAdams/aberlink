import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
#from discord_slash import cog_ext, SlashContext
from cogs import admin_roles

from time import time
import asyncio

# test server guild
#guild_ids = [802212304216260661]

# use \:emote: to get
emojis = {'aberlink': '<:AberLink:813468686647033936>', 'discord': '<:discord:814098231142514697>'}

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
        
        embed = Embed(description='Created and maintained by `Joel Adams` for his major project', colour=discord.Colour.green())
        embed.add_field(name=f'{emojis["aberlink"]} Repository (closed source):', 
                        value='https://github.com/JoelLucaAdams/aberlink', inline=False)
        embed.add_field(name=f'{emojis["discord"]} Discord server (suggestions or feedback):', 
                        value='https://discord.gg/b3EdxVK', inline=False)
        await ctx.send(embed=embed)
        #await ctx.send(content='Created and maintained by `Joel Adams` for a major project\n'
                                #f'{emojis["aberlink"]} Repository (closed source): <https://github.com/JoelLucaAdams/aberlink>\n'
                                #f'{emojis["discord"]} Discord server (suggestions or feedback): https://discord.gg/b3EdxVK')

    @commands.command()
    #@cog_ext.cog_subcommand(base="utilities", name="pog", guild_ids=guild_ids)
    async def pog(self, ctx: Context):
        '''
        Responds with a pogalitious message
        '''
        await ctx.send('certified poggers moment:tm:')

    @commands.command(aliases=['cm'])
    @commands.has_any_role(*admin_roles)
    @commands.bot_has_permissions(manage_messages=True)
    async def clearMessages(self, ctx: Context):
        """
        *Warning* Clears all messages in a channel
        that are less than 14 days old
        """
        msg = await ctx.send('Are you sure you want to clear messages?')
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        def check(_, user):
            return user == ctx.message.author

        reaction, _ = await ctx.bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '👍':
            #logging.info('{0}: #{1} messages cleared by {2}'.format(ctx.guild, ctx.channel.name, ctx.message.author))
            counter = await ctx.channel.purge()
            msg = await ctx.channel.send(f'Success! Messages deleted: `{len(counter)}`, this message will delete in 5 seconds')
            await asyncio.sleep(5)
            await msg.delete()
        elif str(reaction.emoji) == '👎':
            await ctx.send('Messages have not been cleared')

def setup(bot):
    bot.add_cog(Utilities(bot))
