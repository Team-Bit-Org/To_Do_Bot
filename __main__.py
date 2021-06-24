from discord.ext import command
import disord
from pymongo import MongoClient
import os

coll = MongoClient("mongodb://localhost:27017").ToDo.user


bot = commands.Bot(
    command_prefix="-",
    help_command=None,
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print(f"{bot.user} is Ready.")


@bot.command(name="add")
async def _todo_add(ctx, name=None, content=None):
    if name == None:
        embed=discord.Embed(
            title="오류 발생", 
            description='올바른 사용법 : `!add "To Do 이름" "To Do 설명"', 
            color=discord.Colour.red()
        )
        await ctx.send(embed=embed)
    elif os.path.isdir(f"./ToDo/{ctx.author.id}/"):
        with open("./ToDo/{ctx.author.id}/{name}.txt", "w", encoding="UTF-8") as f:
            f.write(str(content))
