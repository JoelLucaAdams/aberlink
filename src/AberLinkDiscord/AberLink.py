"""Initialise and setup Discord bot in server

1. Connects to the PostgreSQL database
2. Initialises the Discord bot
3. Loads all commands from cogs files

on_ready() displays message when the bot has joined the server
on_command_error() handles error messages for all files
on_guild_join() called when the bot joins a new Discord server
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Discord bot"
__deprecated__ = False

import os
import logging
import shelve

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
#from pretty_help import PrettyHelp, Navigation
#from discord_slash import SlashCommand
from cogs import emojis, shelve_file
from cogs.db import PostgreSQL

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBSITE = os.getenv('WEBSITE_URL')

# Initialise the database connection
PostgreSQL.connect()

# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()
#helpCommand = PrettyHelp()

bot = commands.Bot(
    command_prefix="!",
    help_command=helpCommand,
    intents=discord.Intents.all(),
    case_insensitive=True
)

#client = discord.Client(intents=discord.Intents.all())
#slash = SlashCommand(bot, sync_commands=True)

# load cogs
bot.load_extension('cogs.utilities')
bot.load_extension('cogs.verify')
bot.load_extension('cogs.here')
bot.load_extension('cogs.help')

# Setup the General cog with the help command

#nav = Navigation('⬆️', '⬇️')
#bot.help_command = PrettyHelp(navigation=nav, color=discord.Color.dark_green())
generalCog = bot.get_cog("Utilities")
helpCommand.cog = generalCog

@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))


@bot.event
async def on_command_error(ctx, error):
    """
    Handle the Error message in a nice way.
    """
    # Ignores any further errors if custom command has an on_error function
    if hasattr(ctx.command, 'on_error'):
            return
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(f'{emojis["aberlink_error"]} {error}')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'{emojis["aberlink_error"]} {error}')
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send('I\'ve not accounted for this error type... ngl I didn\'t expect you to get this far')
        logging.error(error)

@bot.event
async def on_guild_join(guild):
    """
    Automatically adds server to shelve file on join
    """
    with shelve.open(shelve_file) as db:
            db[str(guild.id)] = True
    
    verify_channel = discord.utils.get(guild.channels, name='verify')
    if verify_channel is not None:
        ctx = verify_channel
    else:
        ctx = await guild.create_text_channel('verify')

    await ctx.send(embed=discord.Embed(description=f'Hello and welcome to AberLink {emojis["aberlink"]}. Before we carry on we need to setup a few things! \n' 
                    '• Open the server settings page and navigate to the roles tab. Then move the `AberLink` role to the top of the list\n'
                    '• In the same panel add a new role called `Lecturer` and give yourself the role\n'
                    '• Finally type the `!build` command to setup verification for the server', colour=discord.Colour.green()))
    """
    general_channel = get(guild.channels, name='verify')

    if general_channel is not None:
        ctx = general_channel
    else:
        ctx = await guild.create_text_channel('verify')

    msg = await ctx.send('Would you like AberLink to automatically configure server roles and verification?')
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

    def check(_, user):
        return user != msg.author

    reaction, _ = await msg.bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        Lecturer_role = await guild.create_role(reason='Creating lecturer role', name='lecturer', permissions=discord.Permissions.advanced())
    elif str(reaction.emoji) == '👎':
        await msg.delete()
        await ctx.send('Please make sure to setup verification using the `!build` and configure the server roles necessary.')
        """

# Start the bot
bot.run(TOKEN)
