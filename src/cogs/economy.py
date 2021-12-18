"""This file contains the cog for economy commands."""

import datetime
from datetime import datetime, timedelta
from discord.ext import commands

from datastore import data_store

def find_user(user_id):
    print("HI")
    data = data_store.get()
    users = data['users']
    user = next((user for user in users
                     if user_id == user['user_id']), None)
    if user is None:
        users.append({
            'user_id': user_id,
            'money': 0,
            'streak': 0,
            'last_claim': str(datetime.min.timestamp()),
        })
        data_store.set(data)
    return {'data': data, 'user': user}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='daily', help='Get your daily allowance!')
    async def daily(self, ctx):
        data = find_user(ctx.message.author.id)
        user = data['user']
        now = datetime.now()
        delta = now - datetime.fromtimestamp(float(data['last_claim']))
        if delta < timedelta(hours=24):
            await ctx.send('You already claimed your daily allowance for '
                            'today. Be more patient!')
            return

        if delta < timedelta(hours=48):
            user['streak'] += 1
        else:
            user['streak'] = 0
        money = 50 * (1 + 0.2 * user['streak'])
        user['money'] += money
        response = f'Thanks for stopping by. {user.mention} received {money} coins today.'
        if user['streak'] > 0:
            response += f'\nThey are on a {user["streak"]} day streak!'
        data_store.set(data['data'])

def setup(bot):
    bot.add_cog(Economy(bot))