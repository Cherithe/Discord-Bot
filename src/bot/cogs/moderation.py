"""This file contains the cog for moderation commands."""

from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name='filter', help='A switch for the word filter')
    async def switch(self, ctx):
        if self.bot.filterOn:
            self.bot.filterOn = False
            response = 'Chat filter has been turned off.'
        else:
            self.bot.filterOn = True
            response = 'Chat filter has been turned on.'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Moderation(bot))