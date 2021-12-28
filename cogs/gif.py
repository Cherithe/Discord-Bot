"""This file contains the cog for greeting commands."""

import json
import os

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TENOR_KEY = os.getenv('TENOR_KEY')

class Gif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """This function sends a welcome message to members when they
        join a guild that the bot is currently active on.

        Return Value:
            - None
        """

        await member.create_dm()
        await member.dm_channel.send(
             f'Hi {member.name}, welcome to {member.guild.name}! This server is'
            ' powered by PLACEHOLDER_NAME. To get more information about'
            ' PLACEHOLDER_NAME and it\'s functions, type !help in any channel.'
        )

    @commands.command(name='hi', help='Replies to the user with a GIF.')
    async def hi(self, ctx):
        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(title='GREETINGS', description='Hello to you too!', color=discord.Color.blurple())
            response = await session.get(f'https://api.tenor.com/v1/search?q=hello&key={TENOR_KEY}&limit=30')
            data = json.loads(await response.text())
            gif_choice = random.randint(0,29)
            embed.set_image(url=data['results'][gif_choice]['media'][0]['mediumgif']['url'])
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(name='gif', help='Returns GIF based on keyword.')
    async def gif(self, ctx, keyword = None):
        async with aiohttp.ClientSession() as session:
            if keyword is None:
                embed = discord.Embed(title='DUDE', description=f'You need to add a keyword.', color=discord.Color.blurple())
                response = await session.get(f'https://api.tenor.com/v1/search?q=disappointment&key={TENOR_KEY}&limit=30')
            else:
                embed = discord.Embed(title='BEHOLD', description=f'Here is a gif of {keyword}.', color=discord.Color.blurple())
                response = await session.get(f'https://api.tenor.com/v1/search?q={keyword}&key={TENOR_KEY}&limit=30')

            data = json.loads(await response.text())
            gif_choice = random.randint(0,29)
            embed.set_image(url=data['results'][gif_choice]['media'][0]['mediumgif']['url'])
        await session.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Gif(bot))
