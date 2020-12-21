import discord
import random
import os
import ksoftapi
from discord import Member
from discord.ext import commands
from discord.ext import tasks
from shortest import Shortest
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st = "67587c0f933aa8ab2e59377a14d0d315"

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ".", intents = intents)
client.remove_command("help")

#bot status
@client.event
async def on_ready():
    activity = discord.Game(name="Bohemian Rhapsody | .help", type=0)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("May is shredding")
    client.load_extension("cogs.music")
    client.load_extension("cogs.roleplay")
    client.load_extension("cogs.recommendations")
    print(f"Joined servers | {len(client.guilds)}:")
    for server in client.guilds:
        print(f"{client.guilds.index(server) + 1} - {server.name} - {server.owner}")

@client.command(aliases = ["Gift", "nitro", "Nitro"])
async def gift(ctx):
    embed = discord.Embed(title = "A WILD GIFT APPEARS!", colour = discord.Colour(0x43b581))
    embed.set_author(name = "Discord", icon_url = "https://logo-logos.com/wp-content/uploads/2018/03/Discord_icon.png")
    embed.add_field(name = "Nitro", value = "Expires in 48 hours")
    embed.set_thumbnail(url = "https://static.wikia.nocookie.net/discord/images/b/b8/Nitro_badge.png/revision/latest/scale-to-width-down/256?cb=20200615092656")
    embed.set_image(url = "https://i.imgur.com/7GlDJJE.png")
    embed.set_footer(text = f"{ctx.message.author} has recieved a gift", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)


#bot info commands
@client.command(aliases = ["Help"])
async def help(ctx):

    embed = discord.Embed(
        title = "About MayBot:",
        description = ":guitar: | MayBot is a multipurpose bot which can be used in moderating your server, playing music, having fun with friends, etc..\nBut the idea behind the bot name is the famous guitarist **Brian May** who was the guitarist for the Rock n' Roll band **Queen**. | :guitar: \n__**Check the list of the commands below:**__",
        colour = discord.Colour.dark_red()
    )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.add_field(name = ":information_source: | Bot Info Commands", value = "`help`, `aliases`, `ping`.", inline = False)
    embed.add_field(name = ":sparkles: | Special Commands", value = "`queen`, `short`, `vote`.")
    embed.add_field(name = ":tada: | Fun Commands", value = "`8ball`, `avatar`, `icon`, `kill`, `howmuch`, `say`, `cute`, `meme`.", inline = False)
    embed.add_field(name = ":performing_arts: | Roleplay Commands", value = "`blush`, `cry`, `dance`, `eat`, `fight`, `hug`, `kiss`, `like`, `love`, `scream`, `shy`, `slap`, `sleep`, `smile`, `tease`, `wink`.", inline = False)
    embed.add_field(name = ":musical_note: | Music Commands", value = "`connect`, `play`, `soundcloud`, `search`, `np`, `loop`, `equalizer`, `lyrics`, `volume`, `queue`, `shuffle`, `seek`, `pause`, `resume`, `move`, `skip`, `remove`, `skipto`, `clearqueue`, `stop`, `disconnect`. \n`album`, `artist`, `playlist`, `track`.", inline = False)
    embed.add_field(name = ":tools: | Moderation Commands", value = "`clear`, `mute`, `unmute`, `kick`, `ban`, `unban`.", inline = False)
    embed.set_footer(text = "Command Prefix is: ." )

    await ctx.send(embed = embed)

@client.command(aliases = ["Aliases"])
async def aliases(ctx):

    embed = discord.Embed(
        title = "Commands aliases and abbreviations:",
        description = "Commands aliases if exist.",
        colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.add_field(name = ":tada: | Fun Commands", value = "• **8Ball:** `8b`. \n• **Avatar:** `av`. \n• **ServerIcon:** `serveravatar`, `icon`. \n• **HowMuch:** `how`.", inline = False)
    embed.add_field(name = ":musical_note: | Music Commands", value = " • **Connect:** `join`, `c`. \n• **Play:** `p`. \n• **SoundCloud:** `scd`. \n• **Search:** `sc`. \n• **NowPlaying:** `now`, `np`. \n• **Repeat:** `loop`. \n• **Equalizer:** `eq`. \n• **Volume:** `vol`. \n• **Queue:** `q`. \n• **Shuffle:** `mix`. \n• **Skip:** `s`. \n• **Remove:** `r`. \n• **ClearQueue:** `cq`. \n• **Stop:** `st`. \n• **Disconnect:** `leave`, `dc`.", inline = False)
    embed.set_footer(text = "Command Prefix is: .\nCapitalizations at first letter is allowed")

    await ctx.send(embed = embed)

@client.command(aliases = ["Ping"])
async def ping(ctx):
    await ctx.send(f":question: | __**Picking speed ?!**__\n:gear: | {round(client.latency * 1000)} ms.")

@client.command(aliases = ["Shorten", "short", "Short"])
async def shorten(ctx, url : str = None):
    if url is None:
        url = "https://www.youtube.com/watch?v=bR-gZQLO26w"
    try:
        short = urle.sou
    except ValueError:
        raise await ctx.send(":question: | Pass a valid url.")

    embed = discord.Embed(title = "Shortened Link",
                          description = f":link: | __{short}__",
                          colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.add_field(name = "Why do I have to pass through an advertisement page ?", value = "The bot services are completely free and it's the only way to support the developer \n__Note:__ if you didn't shorten a link you will be redirected to some cool song, have fun!")
    embed.add_field(name = "What do I benefit from using this command ?", value = "Having a short url instead of a long messy one.")
    embed.add_field(name = "Wanna try the same things and earn money ?", value = f"__[Click the link and join now.](http://join-shortest.com/ref/15860a2afd?user-type=new)__")
    embed.set_footer(text = f"Shortened by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ["Vote"])
async def vote(ctx):
    embed = discord.Embed(title = "Vote",
                          description = f":ballot_box: | Vote for me at __**[top.gg](https://top.gg/bot/747965125599821914)**__ or at __**[discordbotlist.com](https://discord.ly/maybot)**__.",          
                          colour = discord.Colour.dark_red()
                         )
    await ctx.send(embed = embed)


#fun commands
@client.command(aliases = ["8ball", "8Ball", "8b", "8B"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My guitar says no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f":8ball: | {random.choice(responses)}")

@client.command(aliases = ["Kill"])
async def kill(ctx, *, member : discord.Member):
    author = ctx.message.author
    deaths = [f"`{author.name}` killed `{member.name}` with a flying guitar.",
             f"`{author.name}` played black metal for `{member.name}` until death.",
             f"`{member.name}` battled `{author.name}` but he died falling out of the stage.",
             f"`{member.name}` died with an unknown cause of death, but a broken guitar string was found in his room",
             f"While playing Fortnite `{member.name}` died out of cringe.",
             f"`{author.name}` punched `{member.name}`, the murder weapon is unknown but a message beside the body saying __**I am inevitable**__.",
             f"`{author.name}` planted TNT in `{member.name}`'s piano.",
             f"`{author.name}` threw `{member.name}` out. \n**`{member.name}` was An impostor!** \n**VICTORY**",
             f"`{author.name}` killed `{member.name}` with a pointed tongue. \n**`{author.name}` was The impostor!** \n**DEFEAT**"
             ]
    await ctx.send(f":crossed_swords: | {random.choice(deaths)}")

@client.command(aliases = ["Avatar", "av", "Av","AV"])
async def avatar(ctx, *, member : discord.Member = None):
    if member is None:
        member = ctx.message.author
    url = str(member.avatar_url)
    short = urle.sou
    embed = discord.Embed(description = f"**• Avatar link:** __[Link]({short})__",
                          colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = member, icon_url = member.avatar_url)
    embed.set_image(url = member.avatar_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(aliases = ["Icon", "servericon", "ServerIcon", "Servericon", "serveravatar", "ServerAvatar", "Serveravatar", "serverav", "ServerAv", "Server AV"])
async def icon(ctx):
    guild = ctx.guild
    url = str(guild.icon_url)
    short = urle.sou
    embed = discord.Embed(description = f"**• Icon link:** __[Link]({short})__",
                          colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = guild.name, icon_url = guild.icon_url)
    embed.set_image(url = guild.icon_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(aliases = ("Howmuch", "HowMuch", "how", "How"))
async def howmuch(ctx, adjective, *, member : discord.Member = None):
    if member is None:
        await ctx.send(":question: | Please mention a specified member.")
    percentage = list(range(0, 101))
    embed = discord.Embed(title = f"Red Special rates how much {adjective} you are:",
                          description = f":1234: | `{member.name}` is {random.choice(percentage)}% {adjective}.",
                          colour = discord.Colour.dark_red())

    embed.set_author(name = member, icon_url = member.avatar_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(aliases = ["Say"])
async def say(ctx, *, message = None):
    if message is None:
        await ctx.send(f":question: | I have nothing to say")
    elif message is not None:
        await ctx.send(f":loudspeaker: | {message}")
        await ctx.message.delete()

@client.command(aliases = ["Meme"])
async def meme(ctx):
    kclient = ksoftapi.Client("ac8f0be3bfd40393c7c6aa58fb0c8c61de7f4064")
    meme = await kclient.images.random_meme()
    embed = discord.Embed(description = f"**[{meme.title}]({meme.source})**",
                          color = discord.Colour.dark_red()
                         )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.set_image(url = meme.image_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ["Cute"])
async def cute(ctx):
    kclient = ksoftapi.Client("ac8f0be3bfd40393c7c6aa58fb0c8c61de7f4064")
    cute = await kclient.images.random_aww()
    embed = discord.Embed(description = f"**[{cute.title}]({cute.source})**",
                          color = discord.Colour.dark_red()
                         )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.set_image(url = cute.image_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)




#moderation commands
@client.command(aliases = ["Clear"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)


@client.command(aliases = ["Kick"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member):
    await member.kick()
    await ctx.send(f":wave: | {member} has been kicked.")

@client.command(aliases = ["Ban"])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member):
    await member.ban()
    await ctx.send(f":wave: | {member} has been banned.")

@client.command(aliases = ["Unban"])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f":handshake: | {user.name}#{user.discriminator} has been unbanned.")
            return

@client.command(aliases = ["Mute"])
@commands.has_permissions(manage_roles = True)
async def mute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f":mute: | {member.mention} has been muted.")

@client.command(aliases = ["Unmute"])
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f":sound: | {member.mention} has been unmuted.")

client.run("NzQ3OTY1MTI1NTk5ODIxOTE0.X0Wizg.eCMYgg1dcel92InAj-lHJt_Jjss")
