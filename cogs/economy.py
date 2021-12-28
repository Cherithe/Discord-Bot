"""This file contains the cog for economy commands."""

import datetime
import discord

from datetime import datetime, timedelta
from discord.ext import commands

from datastore import data_store

def create_user(user: dict):
    """Checks if the user calling an economy command has a profile.
    If they do not, create a new user profile for them and append to global
    list of users.
    """

    data = data_store.get()
    users = data['users']
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {
            'money': 0,
            'daily': {
                'streak': 0,
                'last_claim': str((datetime.now() - timedelta(days=2)).timestamp()),
            }
        }
        data_store.set(data)
        print('A new user profile has been created for '
             f'{user} (id: {user.id})')
    return

def server_users(users: dict, ctx):
    """Returns a list of existing user profiles for all server members."""
    server_list = []
    for member in ctx.guild.members:
        user = users.get(f'{member.id}')
        if not user is None:
            user['id'] = f'{member.id}'
            server_list.append(user)
    return server_list


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='profile', help='Shows user profile of the mentioned user')
    async def profile(self, ctx):
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        else:
            await ctx.send('Try again, but this time just mention only one user. Thanks.')
            return
        create_user(user)
        data = data_store.get()
        profile = data['users'][f'{user.id}']
        embed = discord.Embed(title='USER PROFILE', description=f'{user}\'s user profile', color=discord.Color.blurple())
        embed.add_field(name = f'Account Balance:', value = f'{profile["money"]} coins', inline = False)
        embed.add_field(name = f'Inventory:', value = 'N/A', inline = False) # NOT YET IMPLEMENTED
        embed.set_footer(text=user.name, icon_url = user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='daily', help='Get your daily allowance!')
    async def daily(self, ctx):
        create_user(ctx.author)
        data = data_store.get()
        user = data['users'][f'{ctx.author.id}']
        now = datetime.now()
        delta = now - datetime.fromtimestamp(float(user['daily']['last_claim']))
        # Checks when the last allowance was collected.
        if delta < timedelta(hours=24):
            delta = 24 + (delta.seconds // -3600)
            await ctx.send('You already claimed your daily allowance for '
                            f'today. Be more patient! You have {str(delta)} hours remaining '
                            'until your next allowance can be collected.')
            return
        if delta < timedelta(hours=48):
            user['daily']['streak'] = str(int(user['daily']['streak']) + 1)
        else:
            user['daily']['streak'] = 0
        # Calculates allowance total and sends appropriate message.
        money = int(50 * (1 + 0.2 * int(user['daily']['streak'])))
        user['money'] = str(int(user['money']) + money)
        response = f'Thanks for stopping by! <@{ctx.author.id}> received {money} coins today.'
        if int(user['daily']['streak']) > 0:
            response += f' You\'re on a {user["daily"]["streak"]} day streak!\n\n'
            if int(user['daily']['streak']) > 5:
                 response += 'Are you addicted or something?'
            else:
                response += 'Keep it up!'
        user['daily']['last_claim'] = str(now.timestamp())
        data_store.set(data)
        await ctx.send(response)

    @commands.command(name='leaderboard', help='See the server rankings.')
    async def leaderboard(self, ctx):
        data = data_store.get()
        leaderboard = ''
        users = server_users(data['users'], ctx)
        for rank, user in enumerate(sorted(users, key=lambda x: x['money'])[:5]):
            name = await self.bot.fetch_user(user['id'])
            leaderboard += f"**#{rank + 1}** {name}: {user['money']} coins\n\n"
        if leaderboard == '':
            leaderboard = ('This server\'s leaderboard is empty! To get started with using economy commands and'
            ' earning currency, use !help economy.')
        embed = discord.Embed(title=f'LEADERBOARD', color=discord.Color.blurple())
        embed.add_field(name = f'Richest people on {ctx.guild.name}:', value = leaderboard, inline = False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
