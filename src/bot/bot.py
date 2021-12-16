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

# The words from BannedWords.txt which contain profanity and slurs to be
# filtered out.
with open('BannedWords.txt', 'r') as f:
    global banned_words
    banned_words = f.read().split()

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    """This function prints information out to standard output when
    the bot has established a connection to Discord.

    Arguments:
        - None

    Return Value:
        - None
    """

    global filterOn
    filterOn = False
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name} (id: {guild.id})\n')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    """This function sends a welcome message to members when they
    join a guild that the bot is currently active on.

    Arguments:
        - member (object): An object created under the Member class in Discord API.

    Return Value:
        - None
    """

    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my rad Discord server!\n'
    )

@bot.event
async def on_message(message):
    msg = message.content
    if filterOn:
        for word in banned_words:
            if word in msg:
                await message.delete()
                await message.channel.send("Dont use that word!")
    await bot.process_commands(message)

bot.run(TOKEN)