"""This file contains the main framework for the Discord Bot to function."""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    """This function prints information out to standard output when
    the bot has established a connection to Discord.

    Return Value:
        - None
    """

    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name} (id: {guild.id})\n')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the permissions required to use this command.')

bot.run(TOKEN)