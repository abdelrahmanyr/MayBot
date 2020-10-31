import discord
from discord.ext import commands
from discord import utils
import typing
from typing import Union
import math
import random
import json

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def fight(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/8wCfapg.gif",
                "https://i.imgur.com/B98zccD.gif",
                "https://i.imgur.com/XmLfmtn.gif",
                "https://i.imgur.com/CZPvwvG.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":crossed_swords: | **{ctx.message.author.name}** fights",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:crossed_swords: | {ctx.message.author.name}** fights **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def hug(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/HcKQj08.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":people_hugging: | **{ctx.message.author.name}** hugs someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:people_hugging: | {ctx.message.author.name}** hugs **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def sleep(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/bvM8axY.gif",
                "https://i.imgur.com/XMP7Xmc.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":sleeping_accommodation: | **{ctx.message.author.name}** sleeps",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:sleeping_accommodation: | {ctx.message.author.name}** sleeps with **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def slap(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/91jLS0i.gif",
                "https://i.imgur.com/HYByYDK.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":punch: | **{ctx.message.author.name}** slaps someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:punch: | {ctx.message.author.name}** slaps **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def eat(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/GzKy2gG.gif",
                "https://i.imgur.com/47oeUKx.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":ramen: | **{ctx.message.author.name}** eats",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:ramen: | {ctx.message.author.name}** eats with **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def cry(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/B7nJJyv.gif",
                "https://i.imgur.com/2rVFc1z.gif",
                "https://i.imgur.com/dlkaJMM.gif",
                "https://i.imgur.com/TDn36JZ.gif",
                "https://i.imgur.com/3tsTERP.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":droplet: | **{ctx.message.author.name}** cries",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:droplet: | {ctx.message.author.name}** cries with **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)


    @commands.command()
    async def love(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/qfDWAHI.gif",
                "https://i.imgur.com/tCjS60Q.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":heart_decoration: | **{ctx.message.author.name}** feels love",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:heart_decoration: | {ctx.message.author.name}** feels love with **{member.name}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def scream(self, ctx, *, member : discord.Member = None):
        gifs = ["https://i.imgur.com/juZi43k.gif",
                "https://i.imgur.com/e2ylwI6.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":speaking_head: | **{ctx.message.author.name}** screams",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:speaking_head: | {ctx.message.author.name}** screams on **{member.name}**'s face",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Roleplay(client))