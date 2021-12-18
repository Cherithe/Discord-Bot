"""This file contains the cog for economy commands."""

from datetime import datetime
from discord.ext import commands

from datastore import data_store

def find_user(user_id):
    data = data_store.get()
    users = data['users']
    user = next((user for user in users
                     if user_id == user['user_id']), None)
    if user is None:
        users.append({
            'user_id': user_id,
            'money': 0,
            'streak': 0,
            'last_claim': datetime(),
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

        data_store.set(data)

def setup(bot):
    bot.add_cog(Economy(bot))