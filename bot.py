import discord
import random
import lavalink
from discord import Member
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = ".")
client.remove_command("help")

#bot status
@client.event
async def on_ready():
    activity = discord.Game(name="Bohemian Rhapsody", type=0)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("May is shredding")
    client.load_extension("cogs.music")


#bot info commands
@client.command()
async def help(ctx):

    embed = discord.Embed(
        title = "About MayBot:",
        description = ":guitar: Maybot is a multipurpose bot which can be used in Moderating your server, play music, having fun with friends, etc..\nBut the idea behind the bot name is the famous guitarist **Brian May** who was the guitarist for the Rock n Roll band **Queen**. :guitar: \n Check the list of the commands below:",
        colour = discord.Colour.dark_red()
    )
    embed.set_author(name = "MayBot", icon_url = "https://mir-s3-cdn-cf.behance.net/project_modules/disp/38c9468957365.560c6217e00fd.jpg")
    embed.add_field(name = "Bot Info Commands", value = "`help`, `ping`", inline = False)
    embed.add_field(name = "Fun Commands", value = "`8ball`, `avatar`, `kill`", inline = False)
    embed.add_field(name = "Music Commands", value = "`connect`, `play`, `length`, `seek`, `skip`, `pause`, `resume`, `stop`, `disconnect`", inline = False)
    embed.add_field(name = "Moderation Commands", value = "`clear`, `mute`, `unmute`, `kick`, `ban`, `unban`", inline = False)
    embed.set_footer(text = "Command Prefix is ." )

    await ctx.send(embed = embed)


@client.command(aliases = ["Ping"])
async def ping(ctx):
    await ctx.send(f"Picking speed ?!\n{round(client.latency * 1000)} ms")


#fun commands
@client.command(aliases = ["8ball", "8Ball"])
async def _8ball(ctx, *, question ):
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
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"{random.choice(responses)}")

@client.command(aliases = ["Kill"])
async def kill(ctx, *, member : discord.Member):
    responses = [f"`{ctx.message.author.name}` killed `{member.name}` with a flying guitar.",
                 f"`{ctx.message.author.name}` played heavy metal for `{member.name}` until death.",
                 f"`{ctx.message.author.name}` played heavy metal for `{member.name}` until death."
                ]
    await ctx.send(f"{random.choice(responses)}")

@client.command(aliases = ["Avatar"])
async def avatar(ctx, *, member : discord.Member):
    embed = discord.Embed(colour = discord.Colour.dark_red()
    )
    embed.set_author(name = member, icon_url = member.avatar_url)
    embed.set_image(url = member.avatar_url)
    embed.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    await ctx.send(embed = embed)

#management commands
@client.command(aliases = ["Clear"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)


@client.command(aliases = ["Kick"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member):
    await member.kick()
    await ctx.send(f"{member} has been kicked.")

@client.command(aliases = ["Ban"])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member):
    await member.ban()
    await ctx.send(f"{member} has been banned.")

@client.command(aliases = ["Unban"])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.name}#{user.discriminator} has been unbanned.")
            return

@client.command(aliases = ["Mute"])
@commands.has_permissions(manage_roles = True)
async def mute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted.")

@client.command(aliases = ["Unmute"])
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, *, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been unmuted.")

client.run(osenviron["token"])
