import discord
from discord.ext import commands
from discord import utils
import typing
from typing import Union
import math
import wavelink
import asyncio
import aiohttp
import datetime
import itertools
import random
import ksoftapi

kclient = ksoftapi.Client('ac8f0be3bfd40393c7c6aa58fb0c8c61de7f4064')

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 100
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player = self.bot.wavelink.get_player(self.guild_id)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song)
            self.now_playing = await self.channel.send(f":play_pause: | __Now playing:__ **{song}** **`[{(datetime.timedelta(seconds = int(song.length / 1000)))}]`**.")

            await self.next.wait()

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}


        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot = self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        node = await self.bot.wavelink.initiate_node(host = "127.0.0.1",
                                                     port = 2333,
                                                     rest_uri = "http://127.0.0.1:2333",
                                                     password = "youshallnotpass",
                                                     identifier = "TEST",
                                                     region = "south_africa")
        node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller


    @commands.command(name='connect', aliases = ["Connect", "c", "join", "Join"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(":question: | No channel to join, Type the desired channel's name or join one.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.send(f":gear: | Connecting to **`{channel.name}`**..", delete_after = 5)

        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel
    
    @commands.command(aliases = ["Play", "p", "P"])
    async def play(self, ctx, *, query: str):
       player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if query.startswith("http"):
            tracks = await self.bot.wavelink.get_tracks(query)
            if isinstance(tracks, wavelink.player.TrackPlaylist):
                await ctx.send(f":play_pause: | {len(tracks.tracks)} tracks has been added.")
                tracks = tracks.tracks[0]
                controller = self.get_controller(ctx)
                await controller.queue.put(tracks)

        else:
            tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")

        if not tracks:
            return await ctx.send(f":grey_question: | No tracks found with this query.")

 

        if player.channel_id == ctx.author.voice.channel.id:

            track = tracks[0]

            controller = self.get_controller(ctx)
            await controller.queue.put(track)

            if player.is_playing:
                embed = discord.Embed(title = "Queued:",
                                description = f":play_pause: | **{str(tracks[0])}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = ":1234: | Track duration", value = f"**`[{(datetime.timedelta(seconds = int(tracks[0].length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")

            if not player.is_playing:
                embed = discord.Embed(title = "Now Playing:",
                                description = f"**:play_pause: | {str(tracks[0])}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = "Track duration", value = f"**`[{(datetime.timedelta(seconds = int(tracks[0].length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")
            await ctx.send(embed = embed)

    @commands.command(aliases = ["Search", "sc", "Sc", "SC"])
    async def search(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")

        if not tracks:
            return await ctx.send(f":grey_question: | No tracks found with this query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)



        if player.channel_id == ctx.author.voice.channel.id:


            embed = discord.Embed(title = "Search Results:",
                              description = f"**:one: | {tracks[0]}** **`[{(datetime.timedelta(milliseconds = int(tracks[0].length)))}]`** \n :two: | **{tracks[1]}** **`[{(datetime.timedelta(milliseconds = int(tracks[1].length)))}]`** \n :three: | **{tracks[2]}** **`[{(datetime.timedelta(milliseconds = int(tracks[2].length)))}]`** \n :four: | **{tracks[3]}** **`[{(datetime.timedelta(milliseconds = int(tracks[3].length)))}]`** \n :five: | **{tracks[4]}** **`[{(datetime.timedelta(milliseconds = int(tracks[4].length)))}]`** \n :six: | **{tracks[5]}** **`[{(datetime.timedelta(milliseconds = int(tracks[5].length)))}]`** \n :seven: | **{tracks[6]}** **`[{(datetime.timedelta(milliseconds = int(tracks[6].length)))}]`**\n :eight: | **{tracks[7]}** **`[{(datetime.timedelta(milliseconds = int(tracks[7].length)))}]`** \n :nine: | **{tracks[8]}** **`[{(datetime.timedelta(milliseconds = int(tracks[8].length)))}]`** \n :keycap_ten: | **{tracks[9]}** **`[{(datetime.timedelta(milliseconds = int(tracks[9].length)))}]`**",
                              color = discord.Colour.dark_red()
                              )
            embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
            embed.set_footer(text = f"Requested by {ctx.message.author} | Type the track number to play.", icon_url = ctx.message.author.avatar_url)

            await ctx.send(embed = embed)

            msg = await self.bot.wait_for('message', timeout = 20.0)
        

            controller = self.get_controller(ctx)

            track = tracks[int(msg.content) - 1]

            await controller.queue.put(track)
            if player.is_playing:
                embed2 = discord.Embed(title = "Queued:",
                                description = f":play_pause: | **{str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed2.add_field(name = "Track duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed2.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")

            if not player.is_playing:
                embed2 = discord.Embed(title = "Now Playing:",
                                description = f"**:play_pause: | {str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed2.add_field(name = "Track duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed2.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")
            await ctx.send(embed = embed2)



    @commands.command(aliases = ["Queen"])
    async def queen(self, ctx):

        playlist = await self.bot.wavelink.get_tracks("https://www.youtube.com/watch?v=gphz_5PEHsk&list=PLIexzKuu-if5FnrlmC0-cCxzLf1GPErAC")
        songs = playlist.tracks
        track = random.choice(songs)

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if player.channel_id == ctx.author.voice.channel.id:


            controller = self.get_controller(ctx)
            await ctx.send(f":headphones: | I picked you a random queen song, have fun.", delete_after = 5)

            if player.is_playing:
                embed = discord.Embed(title = "Queued:",
                                description = f":play_pause: | **{str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = "Track duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")
                embed.set_image(url = track.thumb)


            if not player.is_playing:
                embed = discord.Embed(title = "Now Playing:",
                                description = f"**:play_pause: | {str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = "Track duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track player", value = f"**{ctx.message.author.mention}**")
                embed.set_image(url = track.thumb)
            await ctx.send(embed = embed)
            await controller.queue.put(track)

    @commands.command(aliases = ["Nowplaying", "NowPlaying", "np", "Np", "NP" "now", "Now"])
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send(":question: | Nothing is currently playing, I guess you have to play a track first.")

        embed = discord.Embed(title = "Now Playing:",
                              description = f":abc: | __**[{player.current.title}]({player.current.uri})**__ \n :left_right_arrow: | `[{(datetime.timedelta(seconds = int(player.position / 1000)))} / {(datetime.timedelta(seconds = int(player.current.length / 1000)))}]`",
                              color = discord.Colour.dark_red()
                              )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["Lyrics"])
    async def lyrics(self, ctx, *, query : str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if query is None:
            query = str(player.current)
        if query == 'None':
            await ctx.send(f":question: | Please either play a song or write its name.")
        try:
            if query != "None":
                results = await kclient.music.lyrics(query)
        except ksoftapi.NoResults:
            await ctx.send(":question: | No lyrics found for this query")
        else:
            first = results[0]

        embed = discord.Embed(title = "Lyrics:",
                             description = f"__**{first.name} - {first.artist}:**__ \n {first.lyrics}"[:2047],
                             color = discord.Colour.dark_red()          
                             )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.set_image(url = first.album_art)
        embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["Queue", "q", "Q"])
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        upcoming = list(itertools.islice(controller.queue._queue, 0, None))

        tracks_list = '\n'.join(f"**{upcoming.index(song) + 1}** • **{str(song)}** **`[{(datetime.timedelta(milliseconds = int(song.length)))}]`**" for song in upcoming)


        embed = discord.Embed(title=f"MayBot Queue:",
                             description = f"__**Upcoming Tracks | {len(upcoming)}**__ \n {tracks_list}"[:2047], 
                             colour = discord.Colour.dark_red())

        if not player.current:
            await ctx.send(":question: | There are no tracks currently in the queue, you can add more tracks with the `play` command.")

        guild = ctx.guild
        totald = player.current.length
        for song in upcoming:
            totald += song.length

        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.add_field(name = f"Current Track", value = f"**- {player.current.title}** `[{(datetime.timedelta(milliseconds = int(player.current.length)))}]`", inline = True)
        embed.add_field(name = f"Total Duration", value =f"**[{(datetime.timedelta(milliseconds = int(totald)))}]**")
        embed.set_footer(text = f"{guild.name}'s queue", icon_url = guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(aliases = ["Volume", "vol", "Vol"])
    async def volume(self, ctx, *, vol: int = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if vol is None:
            await ctx.send(f":loud_sound: | The current player volume is `{player.volume}`.")
        if player.channel_id == ctx.author.voice.channel.id:

            controller = self.get_controller(ctx)

            vol = max(min(vol, 1000), 0)
            controller.volume = vol

            await ctx.send(f":loud_sound: | Setting the player volume to `{vol}`.")
            await player.set_volume(vol)

    @commands.command(aliases = ["Seek"])
    async def seek(self, ctx,* , position = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            await player.seek(position = position * 1000)

            if not player.is_playing:
                await ctx.send(f":question: | Nothing is currently playing.")

            if player.is_playing:
                await ctx.send(f":fast_forward: | Your track has been seeked to **`[{(datetime.timedelta(milliseconds = int(position * 1000)))}]`**.")

    @commands.command(aliases = ["Skip", "s", "S"])
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                await ctx.send(f":track_next: | The current track has been skipped.")
            if not player.is_playing:
                await ctx.send(f":question: | There is no current track to skip.")
            await player.stop()

    @commands.command(aliases = ["Pause"])
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if not player.is_paused:
                await ctx.send(f":pause_button: | Player has been paused.")
            await player.set_pause(pause = True)

    @commands.command(aliases = ["Resume"])
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.is_paused:
                await ctx.send(f":arrow_forward: | Player has been resumed.")
            await player.set_pause(pause = False)


    @commands.command(aliases = ["Stop", "st", "St"])
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            try:
                del self.controllers[ctx.guild.id]
            except KeyError:
                await player.disconnect()
                return await ctx.send(":question: | There was no controller to stop.")

            await player.destroy()
            await player.disconnect()
            await ctx.send(f":stop_button: | Player has stopped and disconnected.")

    @commands.command(aliases = ["Disconnect", "dc", "DC", "Dc", "leave", "Leave"])
    async def disconnect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            channel = ctx.author.voice.channel

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.channel_id == ctx.author.voice.channel.id:
            if player.is_connected:
                await ctx.send(f":eject: | Disconnecting from **`{channel.name}`**.")
            await player.disconnect()

def setup(client):
    client.add_cog(Music(client))
