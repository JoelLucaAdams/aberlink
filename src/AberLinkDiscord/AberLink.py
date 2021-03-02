import os

import logging

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
#from discord_slash import SlashCommand
from cogs import emojis

import psycopg2

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('HOST')
DB_PORT = os.getenv('PORT')

try:
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
except psycopg2.OperationalError as err:
    print(f'Error connecting to database. Error: {err}')
    raise

print(f'Connected to PSQL database: {conn}')

# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()

bot = commands.Bot(
    command_prefix="!",
    help_command=helpCommand,
    intents=discord.Intents.all(),
)

#client = discord.Client(intents=discord.Intents.all())
#slash = SlashCommand(bot, sync_commands=True)

# load cogs
bot.load_extension('cogs.utilities')
bot.load_extension('cogs.verify')
bot.load_extension('cogs.i_am_here')

# Setup the General cog with the help command
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
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(f'{emojis["aberlink_error"]} {error}')
    elif isinstance(error, commands.errors.BadArgument):
        print(error)
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send('I\'ve not accounted for this error type... ngl I didn\'t expect you to get this far')
        logging.error(error)

# Start the bot
bot.run(TOKEN)
