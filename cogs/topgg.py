from discord import Colour
from discord.ext import commands, tasks
import discord
import json
import dbl


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc0Nzk2NTEyNTU5OTgyMTkxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyODcxNjgyfQ.rXjO968rh8zgJRgXJZr3GZzKw8JExp_vVtbB6l5x8Ts" 
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='nice', webhook_port=8080)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.bot.wait_until_ready()
        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            print(f"Posted server count ({server_count})")
        except Exception as e:
            print(f"Failed to post server count\n{type(e).__name__}: {e}")

    @tasks.loop(hours = 1)
    async def reminder(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(710341374188453898)
        message = channel.fetch_message(808091364196876288)
        reaction = message.reactions[0]
        users = [333639222395142175, 450446752068141057, 613452470966026250, 643075075100246046, 652627834417971239, 674729751604363284]
        print(users)
        embed = discord.Embed(title = "Vote Reminder", description = "Thanks for voting I really apprreciate this <3\n__**[Click here!](https://top.gg/bot/747965125599821914)**__\n`Note: If you want to cancel the reminder feel free to message the owner.`", colour = discord.Colour.dark_red())
        for user in users:
            user = self.bot.get_user(user)
            voted = await self.dblpy.get_user_vote(int(user.id))
            if voted == False:
                await user.send(embed = embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = int(data['user'])
        with open('vote.json', 'r') as f:
            votes = json.load(f)
        counts = list(votes)
        votes[str(user_id)] = 1
        
        if self.bot.get_user(user_id) in self.bot.get_guild(708891955232243792).members:
            if str(user_id) not in counts:
                with open('vote.json', 'w') as new:
                    json.dump(votes, new, indent = 4)

            else:
                with open('vote.json', 'r') as exist:
                    old = json.load(exist)
                old[str(user_id)] += 1

                with open('vote.json', 'w') as exist:
                    json.dump(old, exist, indent = 4)

        with open('vote.json', 'r') as f:
            votes_unsorted = json.load(f)
        votes = dict(sorted(votes_unsorted.items(),key=lambda x: x[1], reverse = True))
        channel = self.bot.get_channel(808047386052132885)
        message = await channel.fetch_message(808451136821788722)

        members = []
        for key in list(votes.keys()):
            member = await channel.guild.fetch_member(key)
            members.append(member)
        my_list = zip(list(members), list(votes.values()))
        content = "\n".join(f"{member.mention} **:** `{value}`" for member, value in my_list)
        embed = discord.Embed(title = "Votes Counter", description = content, colour = discord.Colour.dark_red())
        await message.edit(embed = embed)

    @commands.command()
    async def test(self, ctx, user):
        votes = await self.dblpy.get_user_vote(int(user))
        member = await ctx.guild.fetch_member(user)
        await ctx.send(f"{member.mention}: {votes}")
def setup(bot):
    bot.add_cog(TopGG(bot))
