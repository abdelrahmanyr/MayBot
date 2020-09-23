import discord
from discord.ext import commands
from discord import utils
import typing
import math
import lavalink
import wavelink
import asyncio
import aiohttp


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

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException("No channel to join. Please either specify a valid channel or join one.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f":gear: | Connecting to **`{channel.name}`**..")
        await player.connect(channel.id)

    @commands.command(aliases = ["p"])
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send(f":grey_question: | Could not find any songs with that query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f':play_pause: | **{str(tracks[0])}** has been added to the queue.')
        await player.play(tracks[0], replace = False)

    @commands.command()
    async def length(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        length = self.bot.wavelink.player.Track.length()
        await ctx.send(f"**{length}**")

    @commands.command()
    async def seek(self, ctx,* , position = 0):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(position = position * 1000)
        await ctx.send(f":fast_forward: | Your song has been seeked to **{position}** second.")

    @commands.command()
    async def skip(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.play()

    @commands.command()
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = True)
        await ctx.send(f":pause_button: | Player has been paused.")

    @commands.command()
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = False)
        await ctx.send(f":arrow_forward: | Player has been resumed.")

    @commands.command()
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.stop()
        await ctx.send(f":stop_button: | Player has stopped.")

    @commands.command(aliases = ["dc", "leave"])
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        await ctx.send(f":eject: | Disconnecting from **`{ctx.author.voice.channel.name}`**.")

def setup(client):
    client.add_cog(Music(client))
