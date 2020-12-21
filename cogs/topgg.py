from discord.ext import commands, tasks

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


def setup(bot):
    bot.add_cog(TopGG(bot))