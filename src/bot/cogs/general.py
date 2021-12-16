"""This file contains the cog for general commands."""

from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip', help='I mean... its a coinflip.')
    async def coinflip(self, ctx):
        """This function picks heads or tails and sends the result as a message.
        
        Return Value:
            - None
        """
        dice = ['The coin landed on heads!', 'The coin landed on tails!']
        response = random.choice(dice)
        await ctx.send(response)

    @commands.command(name='rate', help='Rates literally anything out of 10.')
    async def rate(self, ctx, subject):
        """This function rates the given subject out of 10 and sends the result
        as a message.

        Return Value:
            - None
        """
        rating = str(random.choice(range(0, 11)))
        response = f'I give {subject} a {rating}/10.'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(General(bot))