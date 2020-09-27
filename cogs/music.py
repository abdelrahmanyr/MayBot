import discord
from discord.ext import commands
from discord import utils
import typing
from typing import Union
import math
import lavalink
import wavelink
import asyncio
import aiohttp
import datetime
import itertools

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
            await player.play(song, replace = False)
            self.now_playing = await self.channel.send(f":play_pause: | __Now playing:__ **{song}** **`[{(datetime.timedelta(milliseconds = int(song.length)))}]`**.")

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
        node = await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='south_africa')
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
                raise discord.DiscordException("No channel to join. Please either specify a valid channel or join one.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f":gear: | Connecting to **`{channel.name}`**..")
        await player.connect(channel.id)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel


    @commands.command(aliases = ["Play", "p", "P"])
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send(f":grey_question: | Could not find any songs with that query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        track = tracks[0]

        controller = self.get_controller(ctx)
        await controller.queue.put(track)
        await ctx.send(f":notes: | **{str(tracks[0])}** **`[{(datetime.timedelta(milliseconds = int(tracks[0].length)))}]`** has been added to the queue.")



    @commands.command(aliases = ["Nowplaying", "NowPlaying", "np", "Np", "NP" "now", "Now"])
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.current:
            return await ctx.send(":question: | Nothing is currently playing, I guess you have to play a track first.")

        embed = discord.Embed(title = "Now Playing:",
                              description = f":abc: | **{player.current.title}**. \n :left_right_arrow: | `[{(datetime.timedelta(seconds = int(player.position / 1000)))} / {(datetime.timedelta(milliseconds = int(player.current.length)))}]`",
                              color = discord.Colour.dark_red()
                              )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text = f"{ctx.message.author}", icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["Queue", "q", "Q"])
    async def queue(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        embed = discord.Embed(title=f"MayBot Queue:" , description = "",colour = discord.Colour.dark_red())
        upcoming = list(itertools.islice(controller.queue._queue, 0, 50))

        tracks_list = '\n'.join(f"• **{str(song)}** **`[{(datetime.timedelta(milliseconds = int(song.length)))}]`**" for song in upcoming)


        if not player.current or not controller.queue._queue:
            await ctx.send(":question: | There are no tracks currently in the queue or playing, you can add more tracks with the `play` command.")

        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.add_field(name = f"Upcoming Tracks | {len(upcoming)}", value = f"{tracks_list}", inline = False)
        embed.add_field(name = f"Currently playing tracks", value = f"**- {player.current.title}** `[{(datetime.timedelta(milliseconds = int(player.current.length)))}]`", inline = False)
        embed.set_footer(text = f"{ctx.message.author}", icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases = ["Volume", "vol", "Vol"])
    async def volume(self, ctx, *, vol: int):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        controller = self.get_controller(ctx)

        vol = max(min(vol, 1000), 0)
        controller.volume = vol

        await ctx.send(f":loud_sound: | Setting the player volume to `{vol}`.")
        await player.set_volume(vol)

    @commands.command(aliases = ["Seek"])
    async def seek(self, ctx,* , position = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(position = position * 1000)

        if not player.is_playing:
            await ctx.send(f":question: | Nothing is currently playing.")

        await ctx.send(f":fast_forward: | Your track has been seeked to **`[{(datetime.timedelta(milliseconds = int(position * 1000)))}]`**.")

    @commands.command(aliases = ["Skip", "s", "S"])
    async def skip(self, ctx, number = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.stop()
        await ctx.send(f":track_next: | The current track has been skipped.")

    @commands.command(aliases = ["Pause"])
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = True)
        await ctx.send(f":pause_button: | Player has been paused.")

    @commands.command(aliases = ["Resume"])
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = False)
        await ctx.send(f":arrow_forward: | Player has been resumed.")

    @commands.command(aliases = ["Stop", "st", "St"])
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            await ctx.send(":question: | Nothing is currently playing, you can use `disconnect` command to disconnect the bot from your voice channel" )

        if player.is_playing:
            await player.stop()
            await player.disconnect()
            await ctx.send(f":stop_button: | Player has stopped and disconnected.")

    @commands.command(aliases = ["Disconnect", "dc", "DC", "Dc" "leave", "Leave"], )
    async def disconnect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            channel = ctx.author.voice.channel

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        await ctx.send(f":eject: | Disconnecting from **`{channel.name}`**.")

def setup(client):
    client.add_cog(Music(client))
