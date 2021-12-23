"""This file contains the cog for general commands."""

import discord
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
    async def rate(self, ctx, subject = None):
        if subject is None:
            await ctx.send('You need to give me a subject to rate, man.')
            return
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

    @commands.command(name='8ball', help='Gives a burning response to your burning question.')
    async def eight_ball(self, ctx, *, arg = None):
        if arg is None:
            await ctx.send('Even a magician can\'t see the future if you don\'t'
                           ' give them anything to work with.')
            return
        if arg[-1] != '?':
            await ctx.send('So... are we going to be here all day or are you going to ask me a question?')
            print(type(arg[-1]))
            print(arg[-1])
            return
        responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
             'Don\'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
             'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.',
             'Yes.', 'Yes, definitely.', 'You may rely on it.']
        response = random.choice(responses)
        await ctx.send(response)

    @commands.command(name='pfp', help='Blows up the profile picture of mentioned user.')
    async def pfp(self, ctx):
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            await ctx.send('Try again, but this time just mention only one user. Thanks.')
            return
        embed = discord.Embed(title=f'WOW', description=f"{user}'s profile picture", color=discord.Color.blurple())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='history', help='Finds all recent messages which contain keyword')
    async def history(self, ctx, *, keywords = None):
        if keywords is None:
            await ctx.send('This command must be entered with a keyword!')
        history_list = ''
        messages = await ctx.channel.history(limit=200).flatten()
        self = True
        for msg in messages:
            if keywords in msg.content and not self:
                history_list += f"{msg.author}: {msg.content}\n{msg.jump_url}\n\n"

            self = False

        if history_list == '':
            await ctx.send("There were no messages with the given keyword found!")
        else:
            embed = discord.Embed(title=f'History', color=discord.Color.blurple())
            embed.add_field(name = f'Recent messages with "{keywords}":', value = history_list, inline = False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))