import discord
import random
import math
import os
import datetime
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

client = commands.Bot(command_prefix = ".", intents = intents, case_insensitive = True)
client.remove_command("help")

#bot status
@client.event
async def on_ready():
    activity = discord.Activity(name = "Bohemian Rhapsody | .help",
                                type = discord.ActivityType.playing,
                               )
    await client.change_presence(status = discord.Status.online, activity = activity)
    print("May is shredding")
    client.load_extension("cogs.music")
    client.load_extension("cogs.roleplay")
    client.load_extension("cogs.recommendations")
    client.load_extension("cogs.topgg")
    print(f"Joined servers | {len(client.guilds)}:")
    for server in client.guilds:
        print(f"{client.guilds.index(server) + 1} - {server.name} - {server.owner} ({len(server.members)} Members)")


@client.command(aliases = ["nitro"])
async def gift(ctx):
    if ctx.message.author.id == 732612405858664458:
        await ctx.send(":robot: | A robot has been detected, no gift for you.")
    else:
        embed = discord.Embed(title = "A WILD GIFT APPEARS!", colour = discord.Colour(0x43b581))
        embed.set_author(name = "Discord", icon_url = "https://logo-logos.com/wp-content/uploads/2018/03/Discord_icon.png")
        embed.add_field(name = "Nitro", value = "Expires in 48 hours")
        embed.set_thumbnail(url = "https://static.wikia.nocookie.net/discord/images/b/b8/Nitro_badge.png/revision/latest/scale-to-width-down/256?cb=20200615092656")
        embed.set_image(url = "https://i.imgur.com/7GlDJJE.png")
        embed.set_footer(text = f"{ctx.message.author} has recieved a gift", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = embed)


#bot info commands
@client.command(description = "Returns a list of all commands or explains a specific command.",
                usage = "`.help\n.help [command]`"
               )
async def help(ctx, command_arg : str = None):

    commands = []
    for command in client.commands:
        commands.append(command.name)
    if command_arg is None:
        embed = discord.Embed(
            title = "About MayBot:",
            description = ":guitar: | MayBot is a multipurpose bot which can be used in moderating your server, playing music, having fun with friends, etc..\nBut the idea behind the bot name is the famous guitarist **Brian May** who was the guitarist for the Rock n' Roll band **Queen**. | :guitar: \n__**Check the list of the commands below:**__\nFor more inforamtion about a specific command, type `.help [command]`.",
            colour = discord.Colour.dark_red()
        )
        embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
        embed.add_field(name = ":information_source: | Bot Info Commands", value = "`help`, `aliases`, `ping`.", inline = False)
        embed.add_field(name = ":sparkles: | Special Commands", value = "`queen`, `vote`.")
        embed.add_field(name = ":tada: | Fun Commands", value = "`8ball`, `avatar`, `icon`, `kill`, `howmuch`, `say`, `cute`, `meme`.", inline = False)
        embed.add_field(name = ":performing_arts: | Roleplay Commands", value = "`blush`, `cry`, `dance`, `eat`, `fight`, `hug`, `kiss`, `like`, `love`, `pat`, `scream`, `shy`, `slap`, `sleep`, `smile`, `tease`, `wink`.", inline = False)
        embed.add_field(name = ":musical_note: | Music Commands", value = "`connect`, `play`, `soundcloud`, `search`, `np`, `loop`, `lyrics`, `lyricsgenius`, `⭐ equalizer`, `⭐ volume`, `⭐ nightcore`, `⭐ vapourwave`, `⭐ pitch`, `⭐ speed`, `queue`, `shuffle`, `seek`, `pause`, `resume`, `move`, `skip`, `remove`, `skipto`, `clearqueue`, `stop`, `disconnect`. \n\n`album`, `artist`, `playlist`, `track`.", inline = False)
        embed.add_field(name = ":tools: | Moderation Commands", value = "`clear`, `server`, `roles`, `mute`, `unmute`, `kick`, `ban`, `unban`.", inline = False)
        embed.set_footer(text = "Command Prefix is: ." )
        await ctx.send(embed = embed)


    elif command_arg.lower() in commands:
        command = client.get_command(command_arg.lower())
        if command.description == "":
            command.description = "No description needed."

        if command.usage is None:
            command.usage = f"`.{command.name}`"

        if command.cog_name == "roleplay":
            command.usage = f"`.{command.name}\n.{command.name} [member]`"
            command.description = f"Just a roleplay command."
        embed = discord.Embed(title = str(command.name.capitalize()),
                              colour = discord.Colour.dark_red(),
                             )
        embed.add_field(name = "Description", value = str(command.description), inline = False)
        embed.add_field(name = "Format", value = str(command.usage), inline = False)
        if command.aliases:
            aliases = " - ".join(f"{alias.capitalize()}" for alias in command.aliases)
            embed.add_field(name = "Aliases", value = aliases, inline = False)
        embed.add_field(name = "Instructions", value = "• **[ ]** explains the argument type.\n• **' '** is a literal argument.\n• **/** means one or other.\n• **( )** is not an argument but the input needed.")
        await ctx.send(embed = embed)
    else:
        await ctx.send(f":question: | Please either specify a command or type `.help` to understand how it works.")

@client.command(description = "Returns a list of commands' aliases.",
                usage = "`.aliases`"
               )
async def aliases(ctx):

    embed = discord.Embed(
        title = "Commands aliases and abbreviations:",
        description = "Commands aliases if exist.",
        colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = "MayBot 🎸", icon_url = client.user.avatar_url)
    embed.add_field(name = ":tada: | Fun Commands", value = "• **8Ball:** `8b`. \n• **Avatar:** `av`. \n• **ServerIcon:** `serveravatar`, `icon`. \n• **HowMuch:** `how`.", inline = False)
    embed.add_field(name = ":musical_note: | Music Commands", value = " • **Connect:** `join`, `c`. \n• **Play:** `p`. \n• **SoundCloud:** `scd`. \n• **Search:** `sc`. \n• **NowPlaying:** `now`, `np`. \n• **Lyrics:** `ls`. \n• **LyricsGenius:** `lsg`. \n• **Repeat:** `loop`. \n• **Equalizer:** `eq`. \n• **Volume:** `vol`. \n• **Queue:** `q`. \n• **Shuffle:** `mix`. \n• **Skip:** `s`. \n• **Remove:** `r`. \n• **ClearQueue:** `cq`. \n• **Stop:** `st`. \n• **Disconnect:** `leave`, `dc`.", inline = False)
    embed.set_footer(text = "Command Prefix is: .")

    await ctx.send(embed = embed)

@client.command(description = "Returns the client latency.",
                usage = "`.ping`"
               )
async def ping(ctx):
    await ctx.send(f":question: | __**Picking speed ?!**__\n:gear: | {round(client.latency * 1000)} ms.")

@client.command(aliases = ["short"],
                description = "Shortens a URL by using shorte.st platform.",
                usage = "`.shorten [URL]`"
               )
async def shorten(ctx, url : str = None):
    pass
    if url is None:
        url = "https://www.youtube.com/watch?v=bR-gZQLO26w"
    try:
        short = Shortest.get(url, st)
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

@client.command(description = "Returns an embed containing the links of bot's profiles which allows voting",
                usage = "`.vote`"
               )
async def vote(ctx):
    embed = discord.Embed(title = "Vote",
                          description = f":ballot_box: | Vote for me at __**[top.gg](https://top.gg/bot/747965125599821914)**__ or at __**[discordbotlist.com](https://discord.ly/maybot)**__.",          
                          colour = discord.Colour.dark_red()
                         )
    await ctx.send(embed = embed)


#fun commands
@client.command(name = "8ball", aliases = ["8b"],
                description = "Gives a random answer for a yes/no question.",
                usage = "`.8ball [question]`"
               )
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

@client.command(description = "Returns a weird death for the member specified.",
                usage = "`.kill [member]`"
               )
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

@client.command(aliases = ["av"],
                description = "Returns the mentioned member's avatar, if a member was not mentioned then returns the avatar of the message author.",
                usage = "`.avatar\n.avatar [member]`"
               )
async def avatar(ctx, *, member : discord.Member = None):
    if member is None:
        member = ctx.message.author
    url = str(member.avatar_url)
    short = url
    embed = discord.Embed(description = f"**• Avatar link:** __[Link]({short})__",
                          colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = member, icon_url = member.avatar_url)
    embed.set_image(url = member.avatar_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(aliases = ["servericon", "serveravatar", "serverav", "avatar server"],
                description = "Returns the server's icon.",
                usage = "`.icon`"
               )
async def icon(ctx):
    guild = ctx.guild
    url = str(guild.icon_url)
    short = url
    embed = discord.Embed(description = f"**• Icon link:** __[Link]({short})__",
                          colour = discord.Colour.dark_red()
                         )
    embed.set_author(name = guild.name, icon_url = guild.icon_url)
    embed.set_image(url = guild.icon_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(description = "Gives a magnified emoji",
                usage = "`.emoji [emoji]`")
async def emoji(ctx, emoji : discord.Emoji):
    embed = discord.Embed(title = "Emoji",
                          color = discord.Colour.dark_red())
    embed.set_image(url = emoji.url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ["how"],
                description = "Rates how much an adjective describes a member.",
                usage = "`.howmuch [member] [adjective]`"
               )
async def howmuch(ctx, member : discord.Member = None, *, adjective):
    if member is None:
        await ctx.send(":question: | Please mention a specified member.")
    percentage = list(range(0, 101))
    embed = discord.Embed(title = f"Red Special rates how much {adjective} you are:",
                          description = f":1234: | `{member.name}` is {random.choice(percentage)}% {adjective}.",
                          colour = discord.Colour.dark_red())

    embed.set_author(name = member, icon_url = member.avatar_url)
    embed.set_footer(text = f"Requested by: {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

@client.command(description = "Repeats your message.",
                usage = "`.say [message]`"
               )
async def say(ctx, *, message = None):
    if message is None:
        await ctx.send(f":question: | I have nothing to say")
    elif message is not None:
        await ctx.send(message)
        await ctx.message.delete()

@client.command(description = "Repeats your message but with a loudspeaker emoji.",
                usage = "`.announce [message]`"
               )
async def announce(ctx, *, message = None):
    if message is None:
        await ctx.send(f":question: | I have nothing to say")
    elif message is not None:
        await ctx.send(f":loudspeaker: | {message}")
        await ctx.message.delete()

@client.command(description = "Returns a random meme from Reddit.",
                usage = "`.meme`"
               )
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

@client.command(description = "Returns a random cute picture from Reddit.",
                usage = "`.cute`"
               )
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


# Moderation Commands
@client.command(aliases = ["guild"])
async def server(ctx):
    server = ctx.guild
    members = []
    bots = []
    for member in server.members:
        if member.bot:
            bots.append(member)
        else:
            members.append(member)
    creation_date = server.created_at.strftime(f"%Y/%m/%d | %I:%M:%S %p (UTC)")
    tt_emoji = client.get_emoji(799371392033620013)
    vt_emoji = client.get_emoji(799371392486866984)
    boost_emoji = client.get_emoji(799372040942387213)
    if ctx.guild.owner.color == discord.Colour.default():
        color = discord.Colour.dark_red()
    else:
        color = ctx.guild.owner.color
    embed = discord.Embed(title = "Server Info",
                          description = server.description,
                          colour = color
                         )
    embed.set_author(name = server.name, icon_url = server.icon_url)
    embed.add_field(name = "ID", value = f":id: | `{server.id}`")
    embed.add_field(name = "Owner", value = f":crown: | {server.owner.mention}")
    embed.add_field(name = "Creation", value = f":calendar_spiral: | `{creation_date}`")
    embed.add_field(name = "Members", value = f":busts_in_silhouette: | `{len(server.members)}` Total Members\n:bust_in_silhouette: | `{len(members)}` Persons\n:robot: | `{len(bots)}` Bots", inline = False)
    embed.add_field(name = "Channels", value = f":file_folder: | `{len(server.categories)}` Categories\n{tt_emoji} | `{len(server.text_channels)}` Text Channels\n{vt_emoji} | `{len(server.voice_channels)}` Voice Channels", inline = False)
    if server.system_channel:
        top_channels = f":gear: | {server.system_channel.mention} - System"
        embed.add_field(name = "Top Channels", value = top_channels)
    if server.system_channel and server.public_updates_channel:
        top_channels += f"\n:earth_americas: | {server.public_updates_channel.mention} - Public"
    if server.system_channel and server.afk_channel:
        top_channels += f"\n:speech_left: | {server.afk_channel.mention} - AFK"
    
    if server.features:
        embed.add_field(name = "Features", value = "\n".join(f":star: | {str(feature).capitalize()}" for feature in server.features))
    embed.add_field(name = "Boost", value = f"{boost_emoji} | `{server.premium_subscription_count}` Boosts • Level `{server.premium_tier}` • `{len(server.premium_subscribers)}` Boosters", inline = False)
    embed.add_field(name = "Roles", value = f":tools: | `{len(server.roles)}` Roles")
    embed.add_field(name = "Emojis", value = f":grinning: | `{len(server.emojis)}`/`{server.emoji_limit}` Emojis")
    embed.add_field(name = "Region", value = f":earth_africa: | *{server.region}*")
    embed.set_image(url = server.banner_url)

    await ctx.send(embed = embed)

@client.command()
async def roles(ctx):
    real_roles = ctx.guild.roles
    roles = []
    page = 0
    total_pages = math.ceil(len(real_roles) / 50)
    if ctx.guild.owner.color == discord.Colour.default():
        color = discord.Colour.dark_red()
    else:
        color = ctx.guild.owner.color
    if len(real_roles) > 50:
        for role in real_roles:
            roles.append(role)
            if len(roles) == 50:
                final = "\n".join(f"{r.mention} `--> {len(r.members)} Members`"for r in roles)
                page += 1
                embed = discord.Embed(title = "Server Roles",
                                      description = final,
                                      colour = color)
                embed.set_footer(text = f"Page {page} / {total_pages}")
                await ctx.send(embed = embed)
                roles = []
    else:
        roles = "\n".join(f"{r.mention} `--> {len(r.members)} Members`"for r in real_roles)
        embed = discord.Embed(title = "Server Roles",
                      description = roles,
                      colour = color)
        embed.set_footer(text = "Page 1 /1")
        await ctx.send(embed = embed)
    if 0 < len(roles) < 50:
            final = "\n".join(f"{r.mention} `--> {len(r.members)} Members`"for r in roles)
            embed2 = discord.Embed(title = "Server Roles",
                                  description = final,
                                  colour = color)
            embed2.set_footer(text = f"Page {page + 1} / {total_pages}")

            await ctx.send(embed = embed2)

@client.command(usage = "`.user`\n`.user [user]`")
async def user(ctx, user : discord.User = None):
    if user is None:
        user = ctx.author
    if not user:
        user = client.get_user(user)

    try:
        member = await ctx.guild.fetch_member(user.id)
        color = member.color
    except discord.errors.NotFound:
        color = discord.Colour.dark_red()

    bot_emoji = client.get_emoji(799399189170618368)
    at_symbol = client.get_emoji(799400469712863263)
    staff_emoji = client.get_emoji(799401143109025832)
    partner_emoji = client.get_emoji(799403821549879301)
    hunter_emoji = client.get_emoji(799404591845867630)
    hunter2_emoji = client.get_emoji(799407703708532756)
    bravery_emoji = client.get_emoji(799371392290258984)
    brilliance_emoji = client.get_emoji(799371394856517664)
    balance_emoji = client.get_emoji(799371393610940427)
    supporter_emoji = client.get_emoji(799406898226790411)
    dev_emoji = client.get_emoji(799407971125690388)

    mention = f"{user.mention} "
    if user.bot:
        mention += f"{bot_emoji} "
    if user.public_flags.staff:
        mention += f"{staff_emoji} "
    if user.public_flags.partner:
        mention += f"{partner_emoji} "
    if user.public_flags.bug_hunter:
        mention += f"{hunter_emoji} "
    if user.public_flags.hypesquad_bravery:
        mention += f"{bravery_emoji} "
    if user.public_flags.hypesquad_brilliance:
        mention += f"{brilliance_emoji} "
    if user.public_flags.hypesquad_balance:
        mention += f"{balance_emoji} "
    if user.public_flags.early_supporter:
        mention += f"{supporter_emoji} "
    if user.public_flags.bug_hunter_level_2:
        mention += f"{hunter2_emoji} "
    if user.public_flags.verified_bot_developer:
        mention += f"{dev_emoji} "
            
    creation_date = user.created_at.strftime(f"%Y/%m/%d | %I:%M:%S %p (UTC)")
    creation_since = (datetime.datetime.now() - user.created_at).days
    
    def tf(x):
        if 365 > x > 30:
            process = int(round(x / 30))
            number = f"{process} months ago"
        elif x > 365:
            process = int(round(x / 365))
            number = f"{process} years ago"
        else:
            number = f"{x} days ago"
        return number

    embed = discord.Embed(title = "User Info",
                          colour = color,
                         )
    embed.set_author(name = str(user), icon_url = user.avatar_url)
    embed.set_thumbnail(url = user.avatar_url)
    embed.add_field(name = "User", value = f"{at_symbol} | {mention} ")
    embed.add_field(name = "ID", value = f":id: | `{user.id}`", inline = False)
    embed.add_field(name = "Account Creation", value = f":calendar_spiral: | `{creation_date}` • `{tf(creation_since)}`", inline = False)

    try:
        member = await ctx.guild.fetch_member(user.id)
        roles = ", ".join(f"{role.mention}" for role in member.roles)
        join = member.joined_at.strftime(f"%Y/%m/%d | %I:%M:%S %p (UTC)")
        join_since = (datetime.datetime.now() - member.joined_at).days
        embed.add_field(name = "Server Joining", value = f":calendar: | `{join}` • `{tf(join_since)}`")
        embed.add_field(name = "Roles", value = f":tools: | {roles}", inline = False)
    except:
        pass
    await ctx.send(embed = embed)

    

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member):
    await member.kick()
    await ctx.send(f":wave: | {member} has been kicked.")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member):
    await member.ban()
    await ctx.send(f":wave: | {member} has been banned.")

@client.command()
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

@client.command()
@commands.has_permissions(manage_roles = True)
async def mute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f":mute: | {member.mention} has been muted.")

@client.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f":sound: | {member.mention} has been unmuted.")

client.run("NzQ3OTY1MTI1NTk5ODIxOTE0.X0Wizg.eCMYgg1dcel92InAj-lHJt_Jjss")
