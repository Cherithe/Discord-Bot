"""This file contains the cog for music commands."""

from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Joins the voice channel you are currently in.')
    async def join(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send('You must be connected to a voice channel first.')
        elif ctx.guild.voice_client in self.bot.voice_clients:
            await ctx.send('I am already connected to a channel.')
        else:
            channel = voice_state.channel
            await channel.connect()

    @commands.command(name='leave', help='Leaves voice channel if in one.')
    async def leave(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send('You must be connected to a voice channel to use this command.')
        elif ctx.guild.voice_client not in self.bot.voice_clients:
            await ctx.send('I am not connected to any channels.')
        else:
            await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(Music(bot))