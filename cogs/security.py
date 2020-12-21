import discord
from discord.ext import commands
from discord import utils
import json

class Recommendations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 748737636751114251:
            with open('security.json', 'r') as f:
                check = json.load(f)
            check[str(message.author)] = "mute"
            if str(message.content).lower in ["die"]:
                await message.channel.send("done")

def setup(client):
    client.add_cog(Recommendations(client))