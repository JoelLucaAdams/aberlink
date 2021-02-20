import os

import logging

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
from cogs.utilities import Utilities
from discord_slash import SlashCommand

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Initialise the Bot object with an accessible help Command object
#helpCommand = DefaultHelpCommand()

bot = commands.Bot(
    command_prefix="!",
    #help_command=helpCommand
    intents=discord.Intents.all(),
)

#client = discord.Client(intents=discord.Intents.all())

slash = SlashCommand(bot, sync_commands=True)

# Setup the General cog with the help command
#generalCog = Utilities()
bot.add_cog(Utilities(bot))
#helpCommand.cog = generalCog


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
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(error)
        await ctx.send('Lmao, you broke something')
    elif isinstance(error, commands.errors.BadArgument):
        print(error)
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send('I\'ve not accounted for this error type... ngl I didn\'t expect you to get this far')
        logging.error(error)

# Start the bot
bot.run(TOKEN)
