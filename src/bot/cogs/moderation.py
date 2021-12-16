"""This file contains the cog for general commands."""

from discord.ext import commands
import bot

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='filter', help='A switch for the word filter')
    async def switch(self, ctx):
        if bot.filterOn:
            bot.filterOn = False
            response = 'Filter has been turned off.'
        else:
            bot.filterOn = True
            response = 'Filter has been turned on.'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Moderation(bot))