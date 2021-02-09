from discord import Colour
from discord.ext import commands, tasks
import discord
import json

import dbl


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc0Nzk2NTEyNTU5OTgyMTkxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA3MjAwMjAzfQ.hGwo5VrTEK59x-YID8lVLUtdWXLEYD8RfJK6b8t2f4I" 
        self.dblpy = dbl.DBLClient(self.bot, self.token)
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
        channel = self.bot.get_channel(710341374188453898)
        message = channel.fetch_message(808091364196876288)
        reaction = message.reactions[0]
        users = await reaction.users().flatten()
        embed = discord.Embed(title = "Vote Reminder", description = "Thanks for voting I really apprreciate this <3\n__**[Click here!](https://top.gg/bot/747965125599821914)**__", colour = discord.Colour.dark_red())
        for user in users:
            if self.dblpy.get_user_vote(user.id) is False:
                await user.send(embed = embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = data['user']

        with open('vote.json', 'r') as f:
            votes = json.load(f)
        counts = list(votes)
        votes[str(user_id)] = 0
        
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
            votes = json.load(f)


        channel = self.bot.get_channel(808047386052132885)
        message = channel.fetch_messages(808451136821788722)
        member = channel.guild.fetch_member()
        my_list = zip(list(votes.keys), list(votes.values))
        content = "\n".join(f"{channel.guild.fetch_member(key).mention} : {value}" for key, value in my_list)
        embed = discord.Embed(title = "Votes Counter", description = content, colour = discord.Colour.dark_red())
        await message.edit(embed = embed)


def setup(bot):
    bot.add_cog(TopGG(bot))