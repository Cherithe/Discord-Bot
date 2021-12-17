"""This file contains the cog for general commands."""

from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip', help='I mean... its a coinflip.')
    async def coinflip(self, ctx):
        dice = ['The coin landed on heads!', 'The coin landed on tails!']
        response = random.choice(dice)
        await ctx.send(response)

    @commands.command(name='rate', help='Rates literally anything out of 10.')
    async def rate(self, ctx, subject):
        rating = random.choice(range(0, 11))
        response = f'I give {subject} a {str(rating)}/10.'
        if rating <= 2:
            response += ' Sorry but not really.'
        elif rating <= 4:
            response += ' I mean... could be worse.'
        elif rating <= 6:
            response += ' Not bad!'
        elif rating <= 8:
            response += ' Pretty good, ay?'
        else:
            response += ' Amazing!'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(General(bot))