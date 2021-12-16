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

class Greetings(commands.Cog):
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
            f'Hi {member.name}, welcome to my rad Discord server!\n'
        )

    @commands.command(name='hi', help='Replies to the user with a gif.')
    async def hi(self, ctx):
        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(title="GREETINGS", description="Hello to you too!", color=discord.Color.blurple())
            response = await session.get(f'https://api.tenor.com/v1/search?q=hello&key={TENOR_KEY}&limit=30')
            data = json.loads(await response.text())
            gif_choice = random.randint(0,29)
            embed.set_image(url=data['results'][gif_choice]['media'][0]['mediumgif']['url'])
        await session.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Greetings(bot))