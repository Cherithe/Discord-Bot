"""This file contains the cog for moderation commands."""

from discord.ext import commands

from datastore import data_store

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._filterOn = False
        # The words from BannedWords.txt which contain profanity and slurs to be
        # filtered out.
        with open('src/BannedWords.txt', 'r') as f:
            self._banned_words = f.read().split()

    @commands.Cog.listener()
    async def on_message(self, message):
        """This function deletes any messages containing banned words if the
        chat filter is turned on.
        Return Value:
            - None
        """

        msg = message.content
        data = data_store.get()
        guild = data['guilds'][f'{message.guild.id}']
        if guild['filter'] is True:
            for word in self._banned_words:
                if word in msg:
                    await message.delete()
                    await message.channel.send("Dont use that word!")

    @commands.has_permissions(administrator=True)
    @commands.command(name='filter', help='A switch for the word filter.')
    async def switch(self, ctx):
        data = data_store.get()
        guild = data['guilds'][f'{ctx.message.guild.id}']
        if guild['filter'] is True:
            guild['filter'] = False
            response = 'Filter has been turned off.'
        else:
            guild['filter'] = True
            response = 'Filter has been turned on.'
        await ctx.send(response)
        data_store.set(data)
    
    @commands.has_permissions(administrator=True)
    @commands.command(name='clean', help='Deletes a given number of messages.')
    async def clean(self, ctx, number):
        if number.isdigit() is False or int(number) <= 0:
            await ctx.send('Invalid number of messages to delete.')
            return
        await ctx.channel.purge(limit=(int(number) + 1))
        if int(number) > 100:
            await ctx.send('You sure about that?')
            return
        elif int(number) > 1:
            response = f'{number} messages have been deleted.'
        else:
            response = '1 message has been deleted. Happy?'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Moderation(bot))