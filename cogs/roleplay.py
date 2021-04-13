import discord
from discord.ext import commands
from discord import utils
import random
import json

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def act(self, ctx, member, emoji, verb, verb_2, gifs : list):
        if member is None:
            embed = discord.Embed(description = f"{emoji} | **{ctx.message.author.name}** {verb_2} someone",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_image(url = random.choice(gifs))
        elif member == ctx.author:
            embed = discord.Embed(description = f"{emoji} **{ctx.message.author.name}** {verb_2} himself")
            embed.set_image(url = random.choice(gifs))

        else:
            embed = discord.Embed(description = f"{emoji} | {ctx.message.author.name}** {verb} **{member}**",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_image(url = random.choice(gifs))
        return embed

    @commands.command()
    async def fight(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/8wCfapg.gif",
                "https://static.wikia.nocookie.net/c4d798a2-b26f-415a-a038-94c5902200af",
                "https://i.imgur.com/XmLfmtn.gif",
                "https://i.imgur.com/CZPvwvG.gif",
               ]

        embed = self.act(ctx, member, ":crossed_swords:", "fights", "fights", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def hug(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/HcKQj08.gif",
               ]
        embed = self.act(ctx, member, ":people_hugging:", "hugs", "hugs", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def sleep(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/bvM8axY.gif",
                "https://i.imgur.com/XMP7Xmc.gif"
               ]
        embed = self.act(ctx, member, ":sleeping_accommodation:", "sleeps", "sleeps with", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def slap(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/91jLS0i.gif",
                "https://i.imgur.com/HYByYDK.gif"
               ]

        embed = self.act(ctx, member, ":punch:", "slaps", "slaps", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def eat(self, ctx, *, member = None):
        gifs = ["https://64.media.tumblr.com/7eb8a1771bae88561344652b1254cabc/tumblr_nt6bvlhzhk1u9u50eo2_500.gif",   #1
                "https://i.pinimg.com/originals/7c/3c/a8/7c3ca802cd4140aa1e6b153a5b625d7b.gif",                      #2
                "https://cdn.discordapp.com/attachments/708133938253791275/830935351639670844/image0.gif",           #3
                "https://cdn.discordapp.com/attachments/708133938253791275/830935352063426560/image2.gif",           #4
                "https://cdn.discordapp.com/attachments/708133938253791275/830935352529256488/image3.gif",           #5
                "https://cdn.discordapp.com/attachments/708133938253791275/830935353325125652/image7.gif",           #6
                "https://cdn.discordapp.com/attachments/708133938253791275/830935353661587466/image8.gif",           #7
                "https://cdn.discordapp.com/attachments/708133938253791275/830935357922476063/image0.gif",           #8
                "https://cdn.discordapp.com/attachments/708133938253791275/830935358374936606/image2.gif",           #9
                "https://cdn.discordapp.com/attachments/708133938253791275/830935358765531176/image4.gif",           #10
                "https://cdn.discordapp.com/attachments/708133938253791275/830935358971183193/image5.gif",           #11
                "https://cdn.discordapp.com/attachments/708133938253791275/830935359197020230/image6.gif",           #12
                "https://media.discordapp.net/attachments/708133938253791275/830935359416172544/image7.gif",         #13
                "https://media.discordapp.net/attachments/708133938253791275/830935359793266698/image9.gif",         #14
                "https://media.discordapp.net/attachments/708133938253791275/830935416416239677/image1.gif",         #15
                "https://media.discordapp.net/attachments/708133938253791275/830935416566710323/image2.gif",         #16
                "https://media.discordapp.net/attachments/708133938253791275/830935416818499604/image3.gif",         #17
                "https://media.discordapp.net/attachments/708133938253791275/830935418253213706/image7.gif",         #18
                "https://media.discordapp.net/attachments/708133938253791275/830935418701742141/image8.gif",         #19
                "https://media.discordapp.net/attachments/708133938253791275/830935418949992508/image9.gif",         #20
                "https://media.discordapp.net/attachments/708133938253791275/830935486754455562/image0.gif",         #21
                "https://media.discordapp.net/attachments/708133938253791275/830935486948179978/image1.gif",         #22
                "https://media.discordapp.net/attachments/708133938253791275/830935487492390912/image2.gif",         #23
                "https://media.discordapp.net/attachments/708133938253791275/830935487707086848/image3.gif",         #24
                "https://media.discordapp.net/attachments/708133938253791275/830937401907609630/image0.gif",         #25
                "https://media.discordapp.net/attachments/708133938253791275/830937402205798461/image1.gif",         #26
                "https://media.discordapp.net/attachments/708133938253791275/830937402440155176/image2.gif",         #27
                "https://media.discordapp.net/attachments/708133938253791275/830937402977419334/image3.gif",         #28
                "https://media.discordapp.net/attachments/708133938253791275/830937403367227402/image4.gif",         #29
                "https://media.discordapp.net/attachments/708133938253791275/830937403766079569/image6.gif"          #30
               ]
        embed = self.act(ctx, member, ":ramen:", "eats", "eats", gifs)
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
        embed = self.act(ctx, member, ":droplet:", "cries", "cries with", gifs)
        await ctx.send(embed = embed)


    @commands.command()
    async def love(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/qfDWAHI.gif",
                "https://i.imgur.com/tCjS60Q.gif",
               ]
        embed = self.act(ctx, member, ":heart_decoration:", "loves", "loves", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def scream(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/juZi43k.gif",
                "https://i.imgur.com/e2ylwI6.gif",
               ]
        embed = self.act(ctx, member, ":speaking_head:", "screams", "screames on", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def dance(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/ffcJgcu.gif",
                "https://i.pinimg.com/originals/03/d0/3f/03d03facff90fbce9005ae02a58ddfd1.gif",
                "https://i.imgur.com/TFbDSGP.gif"
               ]
        embed = self.act(ctx, member, ":headphones:", "dances", "dances with", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def smile(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/ZghhEUs.gif",
               ]
        embed = self.act(ctx, member, ":smile:", "smiles", "smiles for", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def tease(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/G98bIDh.gif",
               ]
        embed = self.act(ctx, member, ":pinching_hand:", "teases", "teases", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def wink(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/I1AVFZS.gif",
               ]
        embed = self.act(ctx, member, ":wink:", "winks", "winks towards", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def kiss(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/RK916ug.gif",
               ]
        embed = self.act(ctx, member, ":kiss:", "kisses", "kisses", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def like(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/xezCm8i.gif",
                "https://media1.tenor.com/images/bc7f6147063085d89b403cb96de6f883/tenor.gif?itemid=4973579"
               ]
        embed = self.act(ctx, member, ":thumbsup:", "likes", "likes", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def blush(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/f8vEHcV.gif"]
        embed = self.act(ctx, member, ":flushed:", "blushes", "blushes because of", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def shy(self, ctx, *, member = None):
        gifs = ["https://i.imgur.com/KIfA9af.gif"]
        embed = self.act(ctx, member, ":blush:", "feels shy", "feels shy because of", gifs)
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Roleplay(client))