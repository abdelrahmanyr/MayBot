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
    async def fight(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:crossed_swords: | {ctx.message.author.name}** fights **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def hug(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/HcKQj08.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":people_hugging: | **{ctx.message.author.name}** hugs someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:people_hugging: | {ctx.message.author.name}** hugs **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def sleep(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:sleeping_accommodation: | {ctx.message.author.name}** sleeps with **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def slap(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:punch: | {ctx.message.author.name}** slaps **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def eat(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:ramen: | {ctx.message.author.name}** eats with **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def cry(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/B7nJJyv.gif",
                "https://i.imgur.com/2rVFc1z.gif",
                "https://i.imgur.com/dlkaJMM.gif",
                "https://i.imgur.com/TDn36JZ.gif",
                "https://i.imgur.com/3tsTERP.gif",
                "https://i.imgur.com/avSyzin.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":droplet: | **{ctx.message.author.name}** cries",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:droplet: | {ctx.message.author.name}** cries with **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)


    @commands.command()
    async def love(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:heart_decoration: | {ctx.message.author.name}** feels love with **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def scream(self, ctx, *, member = None):
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
            embed = discord.Embed(description = f"**:speaking_head: | {ctx.message.author.name}** screams on **{member}**'s face",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def dance(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/ffcJgcu.gif",
                "https://i.pinimg.com/originals/03/d0/3f/03d03facff90fbce9005ae02a58ddfd1.gif",
                "https://i.imgur.com/TFbDSGP.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":headphones: | **{ctx.message.author.name}** dances",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:headphones: | {ctx.message.author.name}** dances with **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def smile(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/ZghhEUs.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":smile: | **{ctx.message.author.name}** smiles",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:smile: | {ctx.message.author.name}** smiles for **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)


    @commands.command()
    async def tease(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/G98bIDh.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":pinching_hand: | **{ctx.message.author.name}** teases someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:pinching_hand: | {ctx.message.author.name}** teases **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def wink(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/I1AVFZS.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":wink: | **{ctx.message.author.name}** winks",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:wink: | {ctx.message.author.name}** winks towards **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def kiss(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/RK916ug.gif",
               ]
        if member is None:
            embed = discord.Embed(description = f":wink: | **{ctx.message.author.name}** kisses someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:wink: | {ctx.message.author.name}** kisses **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def like(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/xezCm8i.gif",
                "https://media1.tenor.com/images/bc7f6147063085d89b403cb96de6f883/tenor.gif?itemid=4973579"
               ]
        if member is None:
            embed = discord.Embed(description = f":thumbsup: | **{ctx.message.author.name}** likes",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:thumbsup: | {ctx.message.author.name}** likes **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def blush(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/f8vEHcV.gif",               ]
        if member is None:
            embed = discord.Embed(description = f":flushed: | **{ctx.message.author.name}** blushes",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:flushed: | {ctx.message.author.name}** blushes because of **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)

    @commands.command()
    async def shy(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/KIfA9af.gif"
               ]
        if member is None:
            embed = discord.Embed(description = f":blush: | **{ctx.message.author.name}** is shy",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"**:blush: | {ctx.message.author.name}** is shy because of **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
            embed.set_image(url = random.choice(gifs))
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Roleplay(client))