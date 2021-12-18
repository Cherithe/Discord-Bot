"""This file contains the cog for moderation commands."""
# NOTE: NEED TO TEST WHETHER THIS BREAKS ON USE WITH MULTIPLE GUILDS: IF THIS
# IS AN ISSUE, THEN IMPLEMENTATION CAN BE CHANGED TO USE DATASTORE

from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._filterOn = False
        # The words from BannedWords.txt which contain profanity and slurs to be
        # filtered out.
        with open('BannedWords.txt', 'r') as f:
            self._banned_words = f.read().split()

    @commands.Cog.listener()
    async def on_message(self, message):
        """This function deletes any messages containing banned words if the
        chat filter is turned on.
        Return Value:
            - None
        """

        msg = message.content
        if self._filterOn is True:
            for word in self._banned_words:
                if word in msg:
                    await message.delete()
                    await message.channel.send("Dont use that word!")

    @commands.has_permissions(administrator=True)
    @commands.command(name='filter', help='A switch for the word filter.')
    async def switch(self, ctx):
        if self._filterOn:
            self._filterOn = False
            response = 'Filter has been turned off.'
        else:
            self._filterOn = True
            response = 'Filter has been turned on.'
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Moderation(bot))