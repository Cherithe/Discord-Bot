"""This file contains the cog for economy commands."""

import datetime
from datetime import datetime, timedelta
from discord.ext import commands

from datastore import data_store

def create_user(user):
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

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='daily', help='Get your daily allowance!')
    async def daily(self, ctx):
        create_user(ctx.author)
        data = data_store.get()
        user = data['users'][f'{ctx.author.id}']
        now = datetime.now()
        delta = now - datetime.fromtimestamp(float(user['daily']['last_claim']))
        if delta < timedelta(hours=24):
            await ctx.send('You already claimed your daily allowance for '
                            'today. Be more patient!')
            return
        if delta < timedelta(hours=48):
            user['daily']['streak'] = int(user['daily']['streak']) + 1
        else:
            user['daily']['streak'] = 0
        money = int(50 * (1 + 0.2 * int(user['daily']['streak'])))
        user['money'] = int(user['money']) + money
        response = f'Thanks for stopping by. <@{ctx.author.id}> received {str(money)} coins today.'
        if int(user['daily']['streak']) > 0:
            response += f'\nThey are on a {user["daily"]["streak"]} day streak!'
        user['daily']['last_claim'] = str(now.timestamp())
        data_store.set(data)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Economy(bot))