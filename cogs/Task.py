from discord.ext import commands
from discord.ext import tasks


class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_alarm.start()

    @tasks.loop(minutes=5)
    async def check_alarm(self):