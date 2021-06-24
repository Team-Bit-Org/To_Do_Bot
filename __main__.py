from discord.ext import command
import disord

bot = commands.Bot(
    command_prefix="-",
    help_command=None,
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print(f"{bot.user} is Ready.")

