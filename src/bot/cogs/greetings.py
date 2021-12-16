"""This file contains the cog for greeting commands."""

import aiohttp
import discord
from discord.ext import commands
import json

class Greetings(commands.Cog):
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

    @commands.command(name='hi', help='Replies to the user.')
    async def hi(self, ctx):
        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(title="GREETINGS", description="Hello to you too!", color=discord.Color.blurple())
            response = await session.get(f'https://api.tenor.com/v1/search?q=hello&api_key={}&limit=30')
            data = json.loads(await response.text())
            gif_choice = random.randint(0,29)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
        await session.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Greetings(bot))