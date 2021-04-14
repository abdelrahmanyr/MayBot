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
        elif member in [ctx.author.mention, "me", "myself"]:

            embed = discord.Embed(description = f"{emoji} **{ctx.message.author.name}** {verb_2} himself",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_image(url = random.choice(gifs))
        else:
            embed = discord.Embed(description = f"{emoji} | **{ctx.message.author.name}** {verb} {member}",
                                  color = discord.Colour.dark_red()
                                 )
            embed.set_image(url = random.choice(gifs))
        return embed

    @commands.command()
    async def fight(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/BLOhdU97BeDv2WRRti/giphy.gif",       #1
                "https://media.giphy.com/media/PajqfRMX30hBtgKqF0/giphy.gif",       #2
                "https://media.giphy.com/media/z9RDFpfeXeBAQoz7Ia/giphy.gif",       #3
                "https://media.giphy.com/media/VJ3ItCxd2zwJlIRzQ5/giphy.gif",       #4
                "https://media.giphy.com/media/QJiQc6XQMPUKDEXPFr/giphy.gif",       #5
                "https://media.giphy.com/media/8cWn0HSLA9y1tUgIk6/giphy.gif",       #6
                "https://media.giphy.com/media/wwfL6DcylpXnpSX3kK/giphy.gif",       #7
                "https://media.giphy.com/media/OjXngB124TpXCidFkN/giphy.gif",       #8
                "https://media.giphy.com/media/xZ6lafczLTaz4WxaTG/giphy.gif",       #9
                "https://media.giphy.com/media/4dVYiJ5mscFKjMBLua/giphy.gif"        #10
               ]

        embed = self.act(ctx, member, ":crossed_swords:", "fights", "fights", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def hug(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/1dhiqEvbGLKLqAa7hx/giphy.gif",       #1
                "https://media.giphy.com/media/AUJk6rDzwZc2olNAYX/giphy.gif",       #2
                "https://media.giphy.com/media/6RoLRaTqIzPqTXDFAf/giphy.gif",       #3
                "https://media.giphy.com/media/iHI2xEBBMmW375vlNj/giphy.gif",       #4
                "https://media.giphy.com/media/MFJdkbanrBljXlMRQy/giphy.gif",       #5
                "https://media.giphy.com/media/MuxRlhmbK3BxEE3MCz/giphy.gif",       #6
                "https://media.giphy.com/media/VR3XYlyEaSgF6dua3z/giphy.gif",       #7
                "https://media.giphy.com/media/22ikiUfzxhYy2CC0Xi/giphy.gif",       #8
                "https://media.giphy.com/media/5y0Hix0NVHzqKS0lj3/giphy.gif",       #9
                "https://media.giphy.com/media/63pQ3XzytCOtLBNfjv/giphy.gif",       #10
                "https://media.giphy.com/media/3X9ObZeRWOaltm0aaU/giphy.gif",       #11
                "https://media.giphy.com/media/2wQ7alRjhG3kY9uL5q/giphy.gif",       #12
                "https://media.giphy.com/media/IXkff06c1LvuXrG95w/giphy.gif",       #13
                "https://media.giphy.com/media/X7wZ41n66PWtW5hImr/giphy.gif",       #14
                "https://media.giphy.com/media/IVJVWQYyj16CNdCWmn/giphy.gif",       #15
                "https://media.giphy.com/media/98qlxqjXqBE8rQh9EQ/giphy.gif",       #16
                "https://media.giphy.com/media/MyWEnfYsfdq02N7PxR/giphy.gif",       #17
                "https://media.giphy.com/media/tiEQ1F8MrFgNnJI8bV/giphy.gif",       #18
                "https://media.giphy.com/media/1YrVRoPhSfbKsIHDaQ/giphy.gif",       #19
                "https://media.giphy.com/media/Awku1OLn1ZsVazioTe/giphy.gif"        #20
               ]
        embed = self.act(ctx, member, ":people_hugging:", "hugs", "hugs", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def sleep(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/SpajToJTAyuFU0GXDN/giphy.gif",       #1
                "https://media.giphy.com/media/hk8Epk9TVvsCyj8XVT/giphy.gif",       #2
                "https://media.giphy.com/media/8b5mRdK8dalVFyLCvR/giphy.gif",       #3
                "https://media.giphy.com/media/h7nIxcZlZsQhXGVm9m/giphy.gif",       #4
                "https://media.giphy.com/media/p694ppEoOztCCRyBb5/giphy.gif",       #5
                "https://media.giphy.com/media/atsX70LlSZyUnd2xHh/giphy.gif",       #6
                "https://media.giphy.com/media/KigYEljFltNtZtMjH7/giphy.gif",       #7
                "https://media.giphy.com/media/zgjAftzZbjVgoYASR7/giphy.gif",       #8
                "https://media.giphy.com/media/tm1pbMpAxCOOEpy6iC/giphy.gif",       #9
                "https://media.giphy.com/media/tm1pbMpAxCOOEpy6iC/giphy.gif",       #10
               ]
        embed = self.act(ctx, member, ":sleeping_accommodation:", "sleeps", "sleeps with", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def slap(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/iF50YPp3fwEl1QohZc/giphy.gif",       #1
                "https://media.giphy.com/media/OBsLisJ3I0H7W4cnGY/giphy.gif",       #2
                "https://media.giphy.com/media/Uou642KMOEEllknUdZ/giphy.gif",       #3
                "https://media.giphy.com/media/uIjQpTstEKruHOTc8h/giphy.gif",       #4
                "https://media.giphy.com/media/bwcZJTdPSlA2WLUbdT/giphy.gif",       #5
                "https://media.giphy.com/media/vThtVgF8CM675e8dUw/giphy.gif",       #6
                "https://media.giphy.com/media/Wcn03mErixaly1v3Rm/giphy.gif",       #7
                "https://media.giphy.com/media/dD08Mbh3dD8ofIJF1Q/giphy.gif",       #8
                "https://media.giphy.com/media/RSEiZIyJ6RMkXYqZfs/giphy.gif",       #9
                "https://media.giphy.com/media/QIxhNYBNWtpHInCQtQ/giphy.gif"        #10
               ]

        embed = self.act(ctx, member, ":punch:", "slaps", "slaps", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def eat(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/c1bz2TxTKQNSl6LSL4/giphy.gif",       #1
                "https://media.giphy.com/media/mRrs6Zlr9VTKEeZuRC/giphy.gif",       #2
                "https://media.giphy.com/media/prDheuNcfzYQX0SjYa/giphy.gif",       #3
                "https://media.giphy.com/media/EJOECpepWEuhNDyFqx/giphy.gif",       #4
                "https://media.giphy.com/media/Trm13p8piARVgsCYHy/giphy.gif",       #5
                "https://media.giphy.com/media/gaNoywoHm6ifcWn2Zl/giphy.gif",       #6
                "https://media.giphy.com/media/7pEBU6Pip4qS64ChGo/giphy.gif",       #7
                "https://media.giphy.com/media/zWidscD7UkCFxuIYyg/giphy.gif",       #8
                "https://media.giphy.com/media/rrQSQp1QvdHoDKmTXZ/giphy.gif",       #9
                "https://media.giphy.com/media/QpTHmjrIfoqYplLeVl/giphy.gif",       #10
                "https://media.giphy.com/media/uZ4g9h7SpRkc5gMk4h/giphy.gif",       #11
                "https://media.giphy.com/media/2l1TPIbEyTRjZi5wZY/giphy.gif",       #12
                "https://media.giphy.com/media/0kzPnZ8xHRuq69Q2Nn/giphy.gif",       #13
                "https://media.giphy.com/media/6bx4yewAIx77LUzFxC/giphy.gif",       #14
                "https://media.giphy.com/media/PMetBaPPSaWe9ZdfLE/giphy.gif",       #15
                "https://media.giphy.com/media/HMCProsvvw6vGcWXI1/giphy.gif",       #16
                "https://media.giphy.com/media/vV7PfUbGSMrdTMpGuQ/giphy.gif",       #17
                "https://media.giphy.com/media/R9oPOT93RnjOR71Vic/giphy.gif",       #18
                "https://media.giphy.com/media/UiwDrkpKSDHTOrvnPT/giphy.gif",       #19
                "https://media.giphy.com/media/UwFOIS3HtYPHHhXrYK/giphy.gif",       #20
                "https://media.giphy.com/media/jE8zRmZPhIECeizrO4/giphy.gif",       #21
                "https://media.giphy.com/media/J20IsodYMFpTpYs5GR/giphy.gif",       #22
                "https://media.giphy.com/media/SMbIdoLI0fQ95GiDQl/giphy.gif",       #23
                "https://media.giphy.com/media/wFlbVEdO8EB5npK0Dz/giphy.gif",       #24
                "https://media.giphy.com/media/ztCX1eA31m08XeYPqN/giphy.gif",       #25
                "https://media.giphy.com/media/J8viDdvM25H1nmeGof/giphy.gif",       #26
                "https://media.giphy.com/media/uV13PTCwgPORUnHQan/giphy.gif",       #27
                "https://media.giphy.com/media/TPSCQkQXkGLW6IZmLC/giphy.gif",       #28
                "https://media.giphy.com/media/b8aMV9SvYclzk1q8sE/giphy.gif",       #29
                "https://media.giphy.com/media/RBWAOjnwV98fyIIQlt/giphy.gif"        #30
               ]
        embed = self.act(ctx, member, ":ramen:", "eats", "eats", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def pat(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/oaHbYKKZKXzPlP0tVv/giphy.gif",       #1
                "https://media.giphy.com/media/i4la05Vy96Dt7Kbeks/giphy.gif",       #2
                "https://media.giphy.com/media/rHqM4aGWrjkWBBeeBG/giphy.gif",       #3
                "https://media.giphy.com/media/zaG1uyrhisset0J6Z5/giphy.gif",       #4
                "https://media.giphy.com/media/aaEGxd50vlsezlVLVv/giphy.gif",       #5
                "https://media.giphy.com/media/0riNaUmpAYzPWbQusl/giphy.gif",       #6
                "https://media.giphy.com/media/50EuqJ0rrmfxWkCUQk/giphy.gif",       #7
                "https://media.giphy.com/media/RcY34P516NDQp0jgMN/giphy.gif",       #8
                "https://media.giphy.com/media/XFwVUl21YiedB3lBMj/giphy.gif",       #9
                "https://media.giphy.com/media/7RIAM3GJEFegbhU32B/giphy.gif"        #10
               ]
        embed = self.act(ctx, member, ":pleading_face:", "pats", "pats", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def cry(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/zSoTFOinvxmY0Q9XmC/giphy.gif",       #1
                "https://media.giphy.com/media/PrZeRLzye6CX5yGN0d/giphy.gif",       #2
                "https://media.giphy.com/media/xXPNnDc6Idt7cbhPJB/giphy.gif",       #3
                "https://media.giphy.com/media/NnoONS016J70R6ZUED/giphy.gif",       #4
                "https://media.giphy.com/media/NWfbpjFIoTylVnn6wj/giphy.gif",       #5
                "https://media.giphy.com/media/6W8Oxugf8NR4EqeWt1/giphy.gif"        #6
               ]
        embed = self.act(ctx, member, ":droplet:", "cries", "cries with", gifs)
        await ctx.send(embed = embed)


    @commands.command()
    async def love(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/Yx8jb73BPEXwjDqwP0/giphy.gif",       #1
                "https://media.giphy.com/media/S7V09tdVyt8UXsp0Ky/giphy.gif",       #2
               ]
        embed = self.act(ctx, member, ":heart_decoration:", "loves", "loves", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def scream(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/Z2wLiZiCMHa3EdPHan/giphy.gif",       #1
                "https://media.giphy.com/media/fmH9KhjGvi5gbgaDZA/giphy.gif",       #2
                "https://media.giphy.com/media/l8j6CPLjobN1qD3VGF/giphy.gif"        #3
               ]
        embed = self.act(ctx, member, ":speaking_head:", "screams", "screames on", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def dance(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/pnLAs22edo0h6vxm9o/giphy.gif",       #1
                "https://media.giphy.com/media/CHthCphweq1jnwQksq/giphy.gif",       #2
                "https://media.giphy.com/media/2LYsjQzMiuxY7Np5Yt/giphy.gif"        #3
               ]
        embed = self.act(ctx, member, ":headphones:", "dances", "dances with", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def smile(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/TdZ97lI7oamh4MuLEm/giphy.gif",       #1
               ]
        embed = self.act(ctx, member, ":smile:", "smiles", "smiles for", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def tease(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/QQBcFbUKhDjVRLnsnW/giphy.gif",       #1
               ]
        embed = self.act(ctx, member, ":pinching_hand:", "teases", "teases", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def wink(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/7OxCzXojycfHGtZFNB/giphy.gif",       #1
               ]
        embed = self.act(ctx, member, ":wink:", "winks", "winks towards", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def kiss(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/KlNKbSkBXTbd5hXAR4/giphy.gif",       #1
               ]
        embed = self.act(ctx, member, ":kiss:", "kisses", "kisses", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def like(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/ELA7CjcR56mYM5qaHR/giphy.gif",       #1
                "https://media.giphy.com/media/HSKjntRTuRedapiSiE/giphy.gif"        #2
               ]
        embed = self.act(ctx, member, ":thumbsup:", "likes", "likes", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def blush(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/gU3Q3SgOxRZJvW7MAC/giphy.gif"        #1
               ]
        embed = self.act(ctx, member, ":flushed:", "blushes", "blushes because of", gifs)
        await ctx.send(embed = embed)

    @commands.command()
    async def shy(self, ctx, *, member = None):
        gifs = ["https://media.giphy.com/media/JjN45mysP9jzWkaK3z/giphy.gif"        #1
               ]
        embed = self.act(ctx, member, ":blush:", "feels shy", "feels shy because of", gifs)
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Roleplay(client))