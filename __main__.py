from discord.ext import commands
from pymongo import MongoClient
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
coll = MongoClient("mongodb://localhost:27017/").ToDo.user


@bot.event
async def on_ready():
    for i in coll.find({}):
        find = {"_id": str(i["_id"])}
        set_data = {"$set": {"wait_minute": 0}}
        coll.update_one(find, set_data)
    for i in os.listdir('./cogs/'):
        if i.endswith('.py'):
            bot.load_extension(f'cogs.{i.replace(".py", "")}')
        else:
            continue
    bot.load_extension('jishaku')
    print('jishaku is ready.')
    await asyncio.sleep(1)
    print(f"{bot.user} is Ready.\n")


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title='오류 발생',
        description=f'```py\n{type(error)}: {error}```',
        color=discord.Colour.red()
    )
    await ctx.send(embed=embed)
    chn = bot.get_channel(812947799456743455)
    await chn.send(embed=embed)


bot.run("TOKEN", reconnect=True)
