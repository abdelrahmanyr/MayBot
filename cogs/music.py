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
        self.bot = bot

        node = self.bot.wavelink.get_best_node()
        if not node:

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
            await self.bot.wavelink.initiate_node(host='0.0.0.0',
                                                  port=80,
                                                  rest_uri='http://0.0.0.0:2333',
                                                  password='youshallnotpass',
                                                  identifier='TEST',
                                                  region='us_central')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException("No channel to join. Please either specify a valid channel or join one.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f"Connecting to **`{channel.name}`**..")
        await player.connect(channel.id)

    @commands.command(aliases = ["p"])
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added **{str(tracks[0])}** to the queue.')
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
        await ctx.send(f"Seeked to **{position}**.")

    @commands.command()
    async def skip(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.play()

    @commands.command()
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = True)
        await ctx.send(f"Paused.")

    @commands.command()
    async def resume(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(pause = False)
        await ctx.send(f"Resumed.")

    @commands.command()
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.stop()
        await ctx.send(f"Stopped.")

    @commands.command(aliases = ["dc", "leave"])
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        await ctx.send(f"Disconnected.")

def setup(client):
    client.add_cog(Music(client))
