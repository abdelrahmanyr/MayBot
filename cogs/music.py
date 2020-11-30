import discord
from discord.ext import commands
from discord import utils
import typing
from typing import Union
import math
import random
import wavelink
import asyncio
import aiohttp
import datetime
import itertools
import random
import ksoftapi
import pprint
import time
from shortest import Shortest

st = "67587c0f933aa8ab2e59377a14d0d315"
kclient = ksoftapi.Client('ac8f0be3bfd40393c7c6aa58fb0c8c61de7f4064')

class Track(wavelink.Track):
    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.requester = kwargs.get('requester')

class MusicController:

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.previous = []

        self.volume = 100
        self.loop_state = "0"
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

            if self.loop_state == "1":
                song = self.previous[0]
            elif self.loop_state == "2":
                await self.queue.put(self.previous[0])
                song = await self.queue.get()
            else:
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

 

        if player.channel_id == ctx.author.voice.channel.id:

            if query.startswith("http"):
                tracks = await self.bot.wavelink.get_tracks(query)

                if isinstance(tracks, wavelink.player.TrackPlaylist):
                    tracks_p = tracks.tracks
                    playlist_duration = 0
                    for track_p in tracks_p:
                        track_p = Track(track_p.id, track_p.info, requester = ctx.author)
                        controller = self.get_controller(ctx)
                        await controller.queue.put(track_p)
                        playlist_duration += track_p.length
                    
                    
                    track_embed = discord.Embed(title = "Enqueued Playlist:",
                                                description = f":play_pause: | __**[{tracks.data['playlistInfo']['name']}]({query})**__",
                                                color = discord.Colour.dark_red()
                                               )
                    track_embed.add_field(name = "Number of Tracks", value = f"{len(tracks_p)}", inline = True)
                    track_embed.add_field(name = "Total Duration", value = f"`[{(datetime.timedelta(seconds = int(playlist_duration / 1000)))}]`", inline = True)
                    track_embed.add_field(name = "Playlist Player", value = f"{ctx.author.mention}")
                    await ctx.send(embed = track_embed)
                
                
                elif tracks[0].is_stream:
                    track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)
                    track.length = 0
                    controller = self.get_controller(ctx)
                    await controller.queue.put(track)
                    if player.is_playing:
                        embed = discord.Embed(title = "Enqueued Stream:",
                                        description = f":play_pause: | **{str(track)}**",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Stream Player", value = f"**{ctx.message.author.mention}**")

                    if not player.is_playing:
                        embed = discord.Embed(title = "Playing Stream:",
                                        description = f"**:play_pause: | {str(track)}**",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
                    await ctx.send(embed = embed)

                else:
                    track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

                    controller = self.get_controller(ctx)
                    await controller.queue.put(track)

                    if player.is_playing:
                        embed = discord.Embed(title = "Enqueued:",
                                        description = f":play_pause: | **{str(track)}**",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                        embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")

                    if not player.is_playing:
                        embed = discord.Embed(title = "Playing:",
                                        description = f"**:play_pause: | {str(track)}**",
                                        color = discord.Colour.dark_red()
                                        )
                        embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                        embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
                    await ctx.send(embed = embed)
                
                
            else:
                tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
                track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

            
                controller = self.get_controller(ctx)
                await controller.queue.put(track)
                

                if player.is_playing:
                    embed = discord.Embed(title = "Enqueued:",
                                    description = f":play_pause: | **{str(track)}**",
                                    color = discord.Colour.dark_red()
                                    )
                    embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                    embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")

                if not player.is_playing:
                    embed = discord.Embed(title = "Playing:",
                                    description = f"**:play_pause: | {str(track)}**",
                                    color = discord.Colour.dark_red()
                                    )
                    embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                    embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
                await ctx.send(embed = embed)
            if not tracks:
                return await ctx.send(f":grey_question: | No tracks found with this query.")

    @commands.command(aliases = ["Soundcloud", "SoundCloud", "scd", "Scd", "SCD"])
    async def soundcloud(self, ctx, *, query: str):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if player.channel_id == ctx.author.voice.channel.id:
            tracks = await self.bot.wavelink.get_tracks(f"scsearch:{query}")
            track = Track(tracks[0].id, tracks[0].info, requester = ctx.author)

            controller = self.get_controller(ctx)
            await controller.queue.put(track)
            if player.is_playing:
                embed = discord.Embed(title = "Enqueued:",
                                      description = f":play_pause: | **{str(track)}**",
                                      color = discord.Colour.dark_red()
                                     )
                embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")

            if not player.is_playing:
                embed = discord.Embed(title = "Playing:",
                                      description = f"**:play_pause: | {str(track)}**",
                                      color = discord.Colour.dark_red()
                                     )
                embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
            await ctx.send(embed = embed)

            if not tracks:
                return await ctx.send(f":grey_question: | No tracks found with this query.")

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
                              description = f"**:one: | {tracks[0]}** **`[{(datetime.timedelta(seconds = int(tracks[0].length / 1000)))}]`** \n:two: | **{tracks[1]}** **`[{(datetime.timedelta(milliseconds = int(tracks[1].length)))}]`** \n:three: | **{tracks[2]}** **`[{(datetime.timedelta(milliseconds = int(tracks[2].length)))}]`** \n:four: | **{tracks[3]}** **`[{(datetime.timedelta(milliseconds = int(tracks[3].length)))}]`** \n:five: | **{tracks[4]}** **`[{(datetime.timedelta(milliseconds = int(tracks[4].length)))}]`** \n:six: | **{tracks[5]}** **`[{(datetime.timedelta(milliseconds = int(tracks[5].length)))}]`** \n:seven: | **{tracks[6]}** **`[{(datetime.timedelta(milliseconds = int(tracks[6].length)))}]`**\n:eight: | **{tracks[7]}** **`[{(datetime.timedelta(milliseconds = int(tracks[7].length)))}]`** \n:nine: | **{tracks[8]}** **`[{(datetime.timedelta(milliseconds = int(tracks[8].length)))}]`** \n:keycap_ten: | **{tracks[9]}** **`[{(datetime.timedelta(milliseconds = int(tracks[9].length)))}]`**",
                              color = discord.Colour.dark_red()
                              )
            embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
            embed.set_footer(text = f"Requested by: {ctx.message.author} | Type the track number to play.", icon_url = ctx.message.author.avatar_url)

            await ctx.send(embed = embed)


            msg = await self.bot.wait_for('message', timeout = 20.0)
        

            controller = self.get_controller(ctx)

            track = Track(tracks[int(msg.content) - 1].id, tracks[int(msg.content) - 1].info, requester=ctx.author)

            await controller.queue.put(track)
            if player.is_playing:
                embed2 = discord.Embed(title = "Queued:",
                                description = f":play_pause: | **{str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed2.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed2.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")

            if not player.is_playing:
                embed2 = discord.Embed(title = "Now Playing:",
                                description = f"**:play_pause: | {str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed2.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed2.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
            await ctx.send(embed = embed2)



    @commands.command(aliases = ["Queen"])
    async def queen(self, ctx):

        playlist = await self.bot.wavelink.get_tracks("https://www.youtube.com/playlist?list=PLIexzKuu-if5FnrlmC0-cCxzLf1GPErAC")
        songs = list(playlist.tracks)
        song = random.choice(songs)
        track = Track(song.id, song.info, requester = ctx.author)


        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        if player.channel_id == ctx.author.voice.channel.id:

            await ctx.send(f":headphones: | I picked you a random queen song, have fun.", delete_after = 5)

            if player.is_playing:
                embed = discord.Embed(title = "Enqueued:",
                                description = f":play_pause: | **{str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")

            if not player.is_playing:
                embed = discord.Embed(title = "Playing:",
                                description = f"**:play_pause: | {str(track)}**",
                                color = discord.Colour.dark_red()
                                )
                embed.add_field(name = "Track Duration", value = f"**`[{(datetime.timedelta(seconds = int(track.length / 1000)))}]`**", inline = True)
                embed.add_field(name = "Track Player", value = f"**{ctx.message.author.mention}**")
            await ctx.send(embed = embed)
            controller = self.get_controller(ctx)
            await controller.queue.put(track)

    @commands.command(aliases = ["Nowplaying", "NowPlaying", "np", "Np", "NP" "now", "Now"])
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if not player.current:
            return await ctx.send(":question: | Nothing is currently playing, I guess you have to play a track first.")

        if player.current.is_stream:
            track_length = "0:00:00"
            track_position = "0:00:00"
            track_left = " ∞ "
            player_tracker = "🔴▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔴"
        else:
            track_length = datetime.timedelta(seconds = int(player.current.length / 1000))
            track_position = datetime.timedelta(seconds = int(player.position / 1000))
            time_left = int(player.current.length) - int(player.position)
            track_left = datetime.timedelta(seconds = int(time_left / 1000))
            ppp = player.position / player.current.length * 100
            if ppp >= 0:
                player_tracker = "🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #1
            if ppp >= 5:
                player_tracker = "▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #2
            if ppp >= 10:
                player_tracker = "▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #3
            if ppp >= 15:
                player_tracker = "▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #4
            if ppp >= 20:
                player_tracker = "▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #5
            if ppp >= 25:
                player_tracker = "▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬▬" #6
            if ppp >= 30:
                player_tracker = "▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬▬" #7
            if ppp >= 35:
                player_tracker = "▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬▬" #8
            if ppp >= 40:
                player_tracker = "▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬▬" #9
            if ppp >= 45:
                player_tracker = "▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬▬" #10
            if ppp >= 50:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬▬" #11
            if ppp >= 55:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬▬" #12
            if ppp >= 60:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬▬" #13
            if ppp >= 65:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬▬" #14
            if ppp >= 70:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬▬" #15
            if ppp >= 75:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬▬" #16
            if ppp >= 80:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬▬" #17
            if ppp >= 85:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬▬" #18
            if ppp >= 90:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘▬" #19
            if ppp == 100:
                player_tracker = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬🔘" #20

        if controller.loop_state == "1":
            loop_state = "Enabled"
        else:
            loop_state = "Disabled"

        embed = discord.Embed(title = "Now Playing:",
                              description = f":play_pause: | __**[{player.current.title}]({Shortest.get(player.current.uri, st)})**__ \n\n[{track_position} {player_tracker} {track_length}]",
                              color = discord.Colour.dark_red()
                              )
        embed.add_field(name = "Track Player", value = f"{player.current.requester.mention}")
        embed.add_field(name = "Time Left", value = f"`[{track_left}]`")
        embed.add_field(name = "Track Loop", value = f"{loop_state}")
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["Loop", "repeat", "Repeat"])
    async def loop(self,ctx, state : str = None):
        controller = self.get_controller(ctx)
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                try:
                    controller.previous.pop(0)
                except IndexError:
                    pass
                controller.previous.append(player.current)


                if controller.loop_state == "0" or state in ["queue", "Queue", "all", "All", "on", "On"]:
                    controller.loop_state = "2"
                    message = ":repeat: | Queue looping has been **enabled**."
                elif controller.loop_state == "2" or state in ["track", "Track", "one", "One", "current", "Current"]:
                    controller.loop_state = "1"
                    message = ":repeat_one: | Track looping has been **enabled**."
                elif controller.loop_state == "1" or state in ["off", "Off", "disable", "Disable", "stop", "Stop"]:
                    controller.loop_state = "0"
                    message = ":arrow_right: | Looping has been **disabled**."

                await ctx.send(message)
            else:
                await ctx.send(":question: | You have to play a track first.")

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
                             description = f"__**{first.name} - {first.artist}:**__ \n{first.lyrics}"[:2047],
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
        guild = ctx.guild

        upcoming = list(itertools.islice(controller.queue._queue, 0, None))

        tracks_list = '\n'.join(f"**{upcoming.index(song) + 1}** • **{str(song)}** **`[{(datetime.timedelta(seconds = int(song.length / 1000)))}]`**" for song in upcoming)
        if not player.current:
            await ctx.send(":question: | There are no tracks currently in the queue, you can add more tracks with the `play` command.")
        else:
            totald = player.current.length
            try:
                for song in upcoming:
                    totald += song.length
            except AttributeError:
                totald = player.current.track_length
            if controller.loop_state == "0":
                loop_state = "Disabled"
            elif controller.loop_state == "1":
                loop_state = "Track Looping"
            elif controller.loop_state == "2":
                loop_state = "Queue Looping"

        embed = discord.Embed(title=f"MayBot Queue:",
                              description = f"__**Upcoming Tracks | {len(upcoming)}**__ \n{tracks_list}"[:2047], 
                              colour = discord.Colour.dark_red())
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.add_field(name = f"Current Track", value = f"**- {player.current.title}** `[{(datetime.timedelta(seconds = int(player.current.length / 1000)))}]`", inline = False)
        embed.add_field(name = f"Total Duration", value =f"**[{(datetime.timedelta(seconds = int(totald / 1000)))}]**", inline = True)
        embed.add_field(name = f"Loop State", value = loop_state)
        embed.set_footer(text = f"{guild.name}'s queue", icon_url = guild.icon_url)

        await ctx.send(embed=embed)


    @commands.command(aliases = ["Shuffle", "mix", "Mix"])
    async def shuffle(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                if controller.queue.qsize() < 3:
                    return await ctx.send(":no_entry: | You need more than 3 tracks in your queue to shuffle.")
                else:
                    random.shuffle(controller.queue._queue)
                    await ctx.send(":twisted_rightwards_arrows: | Your queue has been shuffled.")
            else:
                await ctx.send(f":question: | You need to put more tracks in your queue to shuffle.")

    @commands.command(aliases = ["Equalizer", "eq", "Eq", "EQ"])
    async def equalizer(self, ctx: commands.Context, *, equalizer: str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_connected:
            return
        if player.channel_id == ctx.author.voice.channel.id:

            if player.current:
                if equalizer is None:
                    if player.equalizer.name == "flat":
                        eq_name = "default"
                    else:
                        eq_name = player.equalizer.name
                    await ctx.send(f":level_slider: | The currently applied equalizer is **{str(eq_name).capitalize()}**.")
                else:
                    eqs = {'default': wavelink.Equalizer.flat(),
                           'boost': wavelink.Equalizer.boost(),
                           'metal': wavelink.Equalizer.metal(),
                           'piano': wavelink.Equalizer.piano()}
            
                    eq = eqs.get(equalizer.lower(), None)

                    if not eq:
                        keys = list(eqs)
                        list_ = ", ".join(f"`{key.capitalize()}`" for key in keys)
                        return await ctx.send(f":no_entry: | You have entered a wrong equalizer name, currently available equalizers are:\n{list_}.")
                    await ctx.send(f":level_slider: | **{equalizer.capitalize()}** equalizer has been applied.")
                    await player.set_eq(eq)
            else:
                await ctx.send(f":question: | You can't apply an equializer without playing a song.")


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
                if player.current.is_stream:
                    await ctx.send(f":no_entry_sign: | You can't seek in a live stream.")
                else:
                    await ctx.send(f":fast_forward: | Your track has been seeked to **`[{(datetime.timedelta(milliseconds = int(position * 1000)))}]`**.")

    @commands.command(aliases = ["Skip", "s", "S"])
    async def skip(self, ctx, number : int = 1):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if player.channel_id == ctx.author.voice.channel.id:
            if player.current:
                await ctx.send(f":track_next: | The current track has been skipped.")
            if not player.is_playing:
                await ctx.send(f":question: | There is no current track to skip.")
            await player.stop()

    @commands.command(aliases = ["Clearqueue", "ClearQueue", "cq", "Cq", "CQ"])
    async def clearqueue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not player.current or not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't clear an empty queue.")
            else:
                await player.stop()
                controller.queue._queue.clear()
                await ctx.send(":wastebasket: | Your queue has been cleared.")

    @commands.command(aliases = ["Remove", "r", "R"])
    async def remove(self, ctx, number : int, number2 : int = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't remove an item from an empty queue.")
            else:
                if number == 0:
                    await player.stop()
                else:
                    value = controller.queue._queue[number - 1]
                    await ctx.send(f":track_next: | **{value.title}** has been removed.")
                    controller.queue._queue.remove(value)
            
    @commands.command(aliases = ["Skipto", "SkipTo", "st", "St", "ST"])
    async def skipto(self, ctx, number : int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't skip an item from an empty queue.")
            else:
                number = number - 1
                for n in range(number):
                    value = controller.queue._queue[0]
                    controller.queue._queue.remove(value)
                    time.sleep(0.001)
                await player.stop()
                await ctx.send(f":track_next: | Player has skipped to **{controller.queue._queue[0].title}**.")

    @commands.command(aliases = ["Move"])
    async def move(self, ctx, track : int, pos : int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)
        if player.channel_id == ctx.author.voice.channel.id:
            if not controller.queue._queue:
                await ctx.send(f":no_entry: | You can't move an item from an empty queue.")
            else:
                pos = pos - 1
                track = track - 1
                value = controller.queue._queue[track]
                controller.queue._queue.insert(pos, value)
                controller.queue._queue.remove(value)
                await ctx.send(f"**{value.title}** has been moved to position **{pos + 1}**")

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


    @commands.command(aliases = ["Stop", "sp", "Sp", "SP"])
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
