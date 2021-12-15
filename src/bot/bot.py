import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name} (id: {guild.id})\n')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my rad Discord server!\n'
    )

@bot.event
async def on_message(message):
    # Add stuff here - Message listener
    await bot.process_commands(message)

@bot.command(name='coinflip', help='I mean... its a coinflip.')
async def roll(ctx):
    dice = ['The coin landed on heads!', 'The coin landed on tails!']
    response = random.choice(dice)
    await ctx.send(response)

bot.run(TOKEN)