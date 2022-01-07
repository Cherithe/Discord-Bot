"""This file contains the cog for general commands."""

import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import random

from datastore import data_store

load_dotenv()
POGWALL = os.getenv('POGWALL')

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
        # Adds flavour statements depending on the rating given.
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
    async def eight_ball(self, ctx, *, query = None):
        if query is None:
            await ctx.send('Even a magician can\'t see the future if you don\'t'
                           ' give them anything to work with.')
            return
        # If the statement given does not end with a question mark, raise an error.
        if query[-1] != '?':
            await ctx.send('So... are we going to be here all day or are you going to ask me a question?')
            print(type(query[-1]))
            print(query[-1])
            return
        responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
             'Don\'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
             'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.',
             'Yes.', 'Yes, definitely.', 'You may rely on it.']
        response = random.choice(responses)
        await ctx.send(response)

    @commands.command(name='pfp', help='Blows up the profile picture of mentioned user.')
    async def pfp(self, ctx):
        # If no user is mentioned, then set user to the author of the sent command.
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        # If ctx.message.mentions contains more than one user, raise an error.
        else:
            await ctx.send('Try again, but this time just mention only one user. Thanks.')
            return
        embed = discord.Embed(title=f'WOW', description=f"{user}'s profile picture", color=discord.Color.blurple())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='merge', help='Combines the profile pictures of two users.')
    async def merge(self, ctx):
        # If no user is mentioned, then set user to the author of the sent command.
        if len(ctx.message.mentions) == 2:
            user1 = ctx.message.mentions[0]
            user2 = ctx.message.mentions[1]
        # If ctx.message.mentions contains more than one user, raise an error.
        else:
            await ctx.send('You must mention two users to use this command')
            return

        asset1 = user1.avatar_url_as(size=128)
        asset2 = user2.avatar_url_as(size=128)
        data1 = BytesIO(await asset1.read())
        data2 = BytesIO(await asset2.read())
        pfp1 = Image.open(data1)
        pfp2 = Image.open(data2)
        pfp1 = pfp1.crop((0, 0, 128, 64))
        pfp2.paste(pfp1)
        with BytesIO() as image_binary:
            pfp2.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(name='moustache', help='Gives your guy a cool moustache.')
    async def moustache(self, ctx):
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        # If ctx.message.mentions contains more than one user, raise an error.
        else:
            await ctx.send('Try again, but this time just mention only one user. Thanks.')
            return

        moustache = Image.open("src/images/moustache.png")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp.paste(moustache, (25, 50), moustache)
        with BytesIO() as image_binary:
            pfp.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(name='lick', help='Yummo.')
    async def lick(self, ctx):
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        # If ctx.message.mentions contains more than one user, raise an error.
        else:
            await ctx.send('Try again, but this time just mention only one user. Thanks.')
            return

        crazy_square = Image.open("src/images/Crazy_Square.png")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp.paste(crazy_square, (80, 70), crazy_square)
        with BytesIO() as image_binary:
            pfp.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(name='history', help='Finds all recent messages which contain keyword.')
    async def history(self, ctx, *, keywords = None):
        if keywords is None:
            await ctx.send('This command must be entered with a keyword!')
        page = ''
        pages = []
        # Returns the recent channel history as one long list.
        messages = await ctx.channel.history(limit=200).flatten()
        self = True
        msg_count = 0
        for msg in messages:
            if keywords in msg.content and not self:
                if msg_count >= 5:
                    msg_count = 0
                    pages.append(page)
                    page = ''
                timestamp = msg.created_at.strftime("%d/%m/%Y")
                page += f"{msg.author} at {timestamp}: {msg.content}\n{msg.jump_url}\n\n"
                msg_count += 1
            self = False

        pages.append(page)
        if pages[0] == '':
            await ctx.send("There were no messages with the given keyword found!")
            return

        page_len = len(pages)
        embed = discord.Embed(title=f'HISTORY', color=discord.Color.blurple())
        embed.add_field(name=f'Recent messages with "{keywords}":\n\nPage 1 out of {page_len}', value=pages[0], inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⬅")
        await msg.add_reaction("➡")

        index = 0
        # Hangs on after the history embed has been sent to check for user reactions.
        # Acts as a scrolling mechanism for the pages for recent history, and times out after 1 minute.
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅", "➡"]

        while True:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "➡" and index != page_len:
                    index += 1
                    new_embed = discord.Embed(title=f'HISTORY', color=discord.Color.blurple())
                    new_embed.add_field(name=f'Recent messages with "{keywords}":\n\nPage {index + 1} out of {page_len}', value=pages[index], inline=False)
                    await msg.edit(embed=new_embed)
                    await msg.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⬅" and index > 0:
                    index -= 1
                    new_embed = discord.Embed(title=f'HISTORY', color=discord.Color.blurple())
                    new_embed.add_field(name=f'Recent messages with "{keywords}":\n\nPage {index + 1} out of {page_len}', value=pages[index], inline=False)
                    await msg.edit(embed=new_embed)
                    await msg.remove_reaction(reaction, user)

                else:
                    await msg.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await ctx.send("The history page has timed out.")
                break

    @commands.command(name='pogwall', help='It\'s a... distraction of sorts.')
    async def pogwall(self, ctx):
        await ctx.message.add_reaction("🇵")
        await ctx.message.add_reaction("🇴")
        await ctx.message.add_reaction("🇬")
        # Loops 4 times, sending 25 :pogwall: emotes per line. There is a delay
        # on Discord if more than 4 lines are attempted to be sent at once.
        for _ in range(4):
            await ctx.send(25 * f'{POGWALL}')

    @commands.command(name='tag', help='Tags the mentioned user with a curse.')
    async def tag(self, ctx):
        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        # If ctx.message.mentions does not contain one user, raise an error.
        else:
            await ctx.send('Try again, but this time mention only one user. Thanks.')
            return
        data = data_store.get()
        guild = data['guilds'][f'{ctx.message.guild.id}']
        if f'{user.id}' == guild['tagged_user']:
            await ctx.send('The mentioned user is already tagged!')
            return
        response = ''
        if f'{user.id}' == f'{self.bot.user.id}':
            response += 'You do realise it doesn\'t work like that right? '
            user = ctx.message.author.id
        guild['tagged_user'] = f'{user.id}'
        response += f'<@{user.id}> has been tagged!'
        await ctx.send(response)
        

    @commands.Cog.listener()
    async def on_message(self, message):
        """This function will react to the tagged user anytime they send a 
        message in the guild.

        Return Value:
            - None
        """

        data = data_store.get()
        guild = data['guilds'][f'{message.guild.id}']
        if f'{message.author.id}' == guild['tagged_user']:
            reaction_list = ["🗿", "💀", "🤡", "🖕", "🙅", "🤢", "🤥", "🤷", "🤣", "😂", "🤪", "💩"]
            reaction = random.choice(reaction_list)
            await message.add_reaction(reaction)

def setup(bot):
    bot.add_cog(General(bot))
