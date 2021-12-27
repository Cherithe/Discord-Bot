import asyncio

import discord
import youtube_dl

from discord.ext import commands

from datastore import data_store

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

async def play_next(self, ctx):
    data = data_store.get()
    queue = data['guilds'][f'{ctx.message.guild.id}']['queue']
    vc = ctx.message.guild.voice_client
    # Pops the first item from the queue
    video_data = queue.pop(0)
    player = await YTDLSource.from_url(video_data['title'], loop=self.bot.loop, stream=True)
    data_store.set(data.keys())
    await ctx.send(f'**Now playing:** {player.title} **[{video_data["duration"]}]**')
    print(f'Now playing in {ctx.guild.name} (id: {ctx.guild.id}): {player.title} [{video_data["duration"]}]')
    vc.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(self, ctx), self.bot.loop))

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return {'player': cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), 'duration': data['duration']}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Joins the voice channel you are currently in.')
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send('You must be connected to a voice channel to use this command.')
        voice_channel = ctx.author.voice.channel
        # Checks if the bot_id is in the list of user_ids connected to the author's voice channel.
        if 919765855435366490 in ctx.author.voice.channel.voice_states.keys():
            return await ctx.send('I am already connected to your voice channel. Check again!')
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            ctx.voice_client

    @commands.command(name='leave', help='Disconnects bot from the voice channel if connected.')
    async def leave(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send('You must be connected to a voice channel to use this command.')
        elif ctx.guild.voice_client not in self.bot.voice_clients:
            await ctx.send('I am not connected to any channels.')
        else:
            await ctx.voice_client.disconnect()
            await ctx.message.add_reaction("👋")

    @commands.command(name='play', help='Plays audio of the YouTube video that best matches the given keyword/url.')
    async def play(self, ctx, *, url):
        data = data_store.get()
        queue = data['guilds'][f'{ctx.message.guild.id}']['queue']
        vc = ctx.message.guild.voice_client
        if vc.is_playing():
            video_data = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            # If the video is longer than 35 minutes, cancel download and return with error message.
            if video_data['duration'] > 2100:
                await ctx.send('Sorry, but the video you are trying to pla'
                                   'y is longer than 35 minutes. Try using !pl'
                                   'ay again but this time with a video of a s'
                                   'horter length.')
                return
            player = video_data['player']
            duration = f'{str(int(video_data["duration"]) // 60)}:{"%02d" % (int(video_data["duration"]) % 60)}'
            await ctx.send(f'**Added:** {format(player.title)} **[{duration}]** at position {str(len(queue) + 1)} in queue.')
            queue.append({'title': player.title, 'duration': duration})
        else:
            async with ctx.typing():
                video_data = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                if video_data['duration'] > 2100:
                    await ctx.send('Sorry, but the video you are trying to pla'
                                   'y is longer than 35 minutes. Try using !pl'
                                   'ay again but this time with a video of a s'
                                   'horter length.')
                    return
                player = video_data['player']
                duration = f'{str(int(video_data["duration"]) // 60)}:{"%02d" % (int(video_data["duration"]) % 60)}'
                queue.append({'title': player.title, 'duration': duration})
                vc.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(self, ctx), self.bot.loop))
            await ctx.send(f'**Now playing:** {player.title} **[{duration}]**')
            print(f'Now playing in {ctx.guild.name} (id: {ctx.guild.id}): {player.title} [{duration}]')
            # Removes the first item from the queue
            queue.pop(0)
        data_store.set(data)

    @commands.command(name='pause', help='Pauses any audio playing from the bot.')
    async def pause(self, ctx):
        vc = ctx.message.guild.voice_client
        vc.pause()
        await ctx.send('Bot is paused.')

    @commands.command(name='resume', help='Resumes playing audio if paused.')
    async def resume(self, ctx):
        vc = ctx.message.guild.voice_client
        vc.resume()
        await ctx.send('Bot has resumed playing.')

    @commands.command(name='stop', help='Stops any audio playing from bot and clears queue.')
    async def stop(self, ctx):
        data = data_store.get()
        queue = data['guilds'][f'{ctx.message.guild.id}']['queue']
        queue.clear()
        data_store.set(data)
        vc = ctx.message.guild.voice_client
        vc.stop()
        await ctx.send('Bot has stopped playing.')

    @commands.command(name='skip', help='Skips the current-playing song.')
    async def skip(self, ctx):
        vc = ctx.message.guild.voice_client
        vc.pause()
        await ctx.send('Skipped.')
        await play_next(self, ctx)

    @commands.command(name='clear', help='Clears the existing queue.')
    async def stop(self, ctx):
        data = data_store.get()
        queue = data['guilds'][f'{ctx.message.guild.id}']['queue']
        queue.clear()
        data_store.set(data)
        vc = ctx.message.guild.voice_client
        vc.stop()
        await ctx.send('Bot has stopped playing.')

    @commands.command(aliases=['q'], help='Prints the currently queued songs.')
    async def queue(self, ctx):
        data = data_store.get()
        queue = data['guilds'][f'{ctx.message.guild.id}']['queue']
        queue_list = ''
        duration_list = ''
        for count, item in enumerate(queue, 1):
            queue_list += f'**[{count}]**:    {item["title"]}\n\n'
            duration_list += f'**[{item["duration"]}]**\n\n'
            if len(item['title']) > 65:
                duration_list += '\n'
        if queue_list == '':
            queue_list = 'The queue is currently empty! Add more songs using !play.'
        embed = discord.Embed(title=f'QUEUE', color=discord.Color.blurple())
        embed.add_field(name = f'Up next:', value = queue_list, inline = True)
        if duration_list != '':
            embed.add_field(name = '\u200b', value = duration_list, inline = True)
        await ctx.send(embed=embed)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')
                raise commands.CommandError('Author not connected to a voice channel.')

def setup(bot):
    bot.add_cog(Music(bot))