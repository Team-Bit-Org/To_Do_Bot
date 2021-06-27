from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
bot = commands.Bot(
    command_prefix="-",
    help_command=None,
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    for i in os.listdir('./cogs/'):
        if i.endswith('.py'):
            bot.load_extension(f'cogs.{i.replace(".py", "")}')
        else:
            continue
    bot.load_extension('jishaku')
    print('jishaku is ready.')
    await asyncio.sleep(1)
    print(f"\n{bot.user} is Ready.\n")


bot.run(os.getenv("TOKEN"), reconnect=True)