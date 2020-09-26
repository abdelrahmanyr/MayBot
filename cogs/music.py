import discord
from discord.ext import commands
from discord import utils
import typing
import math
import lavalink
import wavelink
import asyncio
import aiohttp
import datetime


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot = self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='south_africa')

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

    @commands.command(aliases = ["Play", "p"])
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send(f":grey_question: | Could not find any songs with that query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f':play_pause: | **{str(tracks[0])}** **`[{(datetime.timedelta(milliseconds = int(tracks[0].length)))}]`** has been added to the queue.')
        await player.play(tracks[0], replace = False)

    @commands.command(aliases = ["Nowplaying", "NowPlaying", "np", "Np", "NP" "now", "Now"])
    async def nowplaying(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        embed = discord.Embed(title = f"{player.current.title}",
                              description = f":left_right_arrow: | `[{(datetime.timedelta(seconds = int(player.position / 1000)))} / {(datetime.timedelta(milliseconds = int(player.current.length)))}]`",
                              color = discord.Colour.dark_red()
                              )
        embed.set_author(name = "MayBot 🎸", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text = f"{ctx.message.author}", icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["Seek"])
    async def seek(self, ctx,* , position = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(position = position * 1000)
        await ctx.send(f":fast_forward: | Your track has been seeked to **`[{(datetime.timedelta(milliseconds = int(position * 1000)))}]`**.")

    @commands.command()
    async def skip(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.play()

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
        await player.stop()
        await ctx.send(f":stop_button: | Player has stopped.")

    @commands.command(aliases = ["Disconnect", "dc", "DC", "Dc" "leave", "Leave"], )
    async def disconnect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            channel = ctx.author.voice.channel

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        await ctx.send(f":eject: | Disconnecting from **`{channel.name}`**.")

def setup(client):
    client.add_cog(Music(client))
