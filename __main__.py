from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
import asyncio
import discord
import os

load_dotenv()
coll = MongoClient("mongodb://localhost:27017/").ToDo.user
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
    if name is None:
        embed=discord.Embed(
            title="오류 발생", 
            description='올바른 사용법 : `!add "To Do 이름" "To Do 설명"', 
            color=discord.Colour.red()
        )
        return await ctx.send(embed=embed)

    elif os.path.isdir(f"./ToDo/{ctx.author.id}/"):
        with open(f"./ToDo/{ctx.author.id}/{name}.txt", "w", encoding="UTF-8") as f:
            f.write(str(content))

    else:
        os.mkdir(f'./ToDo/{ctx.author.id}/')
        with open(f"./ToDo/{ctx.author.id}/{name}.txt", "w", encoding="UTF-8") as f:
            f.write(str(content))

    e = discord.Embed(
        title="완료",
        description="To Do 등록이 완료되었습니다.\n마감일 등록이 필요하시다면 아래 이모지를 눌러주세요.",
        color=discord.Colour.green()
    )
    mmm = await ctx.send(embed=e)
    await mmm.add_reaction("🗓")
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "🗓"

    def text_check(m):
        return m.channel == ctx.channel and m.author.id == ctx.author.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
        embed = discord.Embed(
            title='작업 진행 중',
            description='작업이 진행중입니다.\n\n마감일 등록     : 🟥\n마감 당일 안내   : 🟥\n작업 집중 메세지 : 🟥',
            color=discord.Colour.blurple()
        )
        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
        msg = await ctx.send(embed=embed)
        embed = discord.Embed(
            title='작업 진행 중',
            description='작업이 진행중입니다.\n\n마감일 등록     : ⬛\n마감 당일 안내   : 🟥\n작업 집중 메세지 : 🟥',
            color=discord.Colour.blurple()
        )
        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
        await msg.edit(embed=embed)
        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
        await asyncio.sleep(1)
        await ctx.send('마감 일을 `YYYY/MM/DD` 형식으로 입력해주세요.\n예시 : 2021/06/26')

        desc = await bot.wait_for("message", timeout=60, check=text_check)
        date = desc.content

        embed = discord.Embed(
            title='작업 진행 중',
            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`\n마감 당일 안내   : 🟩\n작업 집중 메세지 : 🟥',
            color=discord.Colour.blurple()
        )
        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
        await msg.edit(embed=embed)

        msgs = await ctx.send('마감 당일 안내를 활성화 하시겠습니까?')
        embed = discord.Embed(
            title='작업 진행 중',
            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`\n마감 당일 안내   : ⬛\n작업 집중 메세지 : 🟥',
            color=discord.Colour.blurple()
        )
        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
        await msg.edit(embed=embed)

        emoji = ['✅', '❎']
        for i in emoji: await msgs.add_reaction(i)

        def check1(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emoji

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check1)
            if str(reaction.emoji) == emoji[0]:  # 마감 당일 안내 활성화
                with open('./alarm.txt', 'a', encoding="UTF-8") as f:
                    f.write(str(date) + '\n')

                embed = discord.Embed(
                    title='작업 진행 중',
                    description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟥',
                    color=discord.Colour.blurple()
                )
                embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                await msg.edit(embed=embed)
                await ctx.send('마감 당일 안내를 활성화 하였습니다.')
                await asyncio.sleep(0.5)
                msgss = await ctx.send('작업 집중 메세지를 활성화 하시겠습니까?')
                for i in emoji: await msgss.add_reaction(i)
                embed = discord.Embed(
                    title='작업 진행 중',
                    description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : ⬛',
                    color=discord.Colour.blurple()
                )
                embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                await msg.edit(embed=embed)
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check1)
                    if str(reaction.emoji) == emoji[0]:
                        await ctx.send('알림 빈도를 5분 단위, 그리고 숫자만 입력해주세요.')
                        descc = await bot.wait_for("message", timeout=60, check=text_check)
                        time = descc.content

                        embed = discord.Embed(
                            title='작업 진행 중',
                            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                        f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟩\n  - `{time}`분',
                            color=discord.Colour.blurple()
                        )
                        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                        await msg.edit(embed=embed)

                        embed = discord.Embed(
                            title='완료',
                            description='To Do 등록을 최종적으로 완료하였습니다.',
                            color=discord.Colour.green()
                        )
                        await mmm.edit(embed=embed)
                        await asyncio.sleep(3)
                        await msg.delete()
                    else:
                        await ctx.send('작업 집중 메세지를 비활성화 하였습니다.')
                        embed = discord.Embed(
                            title='작업 진행 중',
                            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                        f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟩\n  - 비활성화',
                            color=discord.Colour.blurple()
                        )
                        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                        await msg.edit(embed=embed)

                        embed = discord.Embed(
                            title='완료',
                            description='To Do 등록을 최종적으로 완료하였습니다.',
                            color=discord.Colour.green()
                        )
                        await mmm.edit(embed=embed)
                        await asyncio.sleep(3)
                        await msg.delete()
                except asyncio.TimeoutError:
                    await ctx.send('시간이 초과되었습니다.')

            else:  # 마감 당일 안내 비활성화
                embed = discord.Embed(
                    title='작업 진행 중',
                    description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟥',
                    color=discord.Colour.blurple()
                )
                embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                await msg.edit(embed=embed)
                await ctx.send('마감 당일 안내를 비활성화 하였습니다.')

                msgss = await ctx.send('작업 집중 메세지를 활성화 하시겠습니까?')
                for i in emoji: await msgss.add_reaction(i)
                embed = discord.Embed(
                    title='작업 진행 중',
                    description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : ⬛',
                    color=discord.Colour.blurple()
                )
                embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                await msg.edit(embed=embed)
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check1)
                    if str(reaction.emoji) == emoji[0]:  # 작업 집중 메세지 활성화
                        await ctx.send('알림 빈도를 5분 단위, 그리고 숫자만 입력해주세요.')
                        descc = await bot.wait_for("message", timeout=60, check=text_check)
                        time = descc.content

                        embed = discord.Embed(
                            title='작업 진행 중',
                            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                        f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟩\n  - `{time}`분',
                            color=discord.Colour.blurple()
                        )
                        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                        await msg.edit(embed=embed)

                        embed = discord.Embed(
                            title='완료',
                            description='To Do 등록을 최종적으로 완료하였습니다.',
                            color=discord.Colour.green()
                        )
                        await mmm.edit(embed=embed)
                        await asyncio.sleep(3)
                        await msg.delete()
                    else:  # 작업 집중 메세지 비활성화
                        await ctx.send('작업 집중 메세지를 비활성화 하였습니다.')
                        embed = discord.Embed(
                            title='작업 진행 중',
                            description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩'
                                        f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟩\n  - 비활성화',
                            color=discord.Colour.blurple()
                        )
                        embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                        await msg.edit(embed=embed)

                        embed = discord.Embed(
                            title='완료',
                            description='To Do 등록을 최종적으로 완료하였습니다.',
                            color=discord.Colour.green()
                        )
                        await mmm.edit(embed=embed)
                        await asyncio.sleep(3)
                        await msg.delete()

                except asyncio.TimeoutError:
                    await ctx.send('시간이 초과되었습니다.')
        except asyncio.TimeoutError:
            await ctx.send('시간이 초과되었습니다.')
    except asyncio.TimeoutError:
        await ctx.send("시간이 초과되었습니다.")


bot.run(os.getenv("TOKEN"))

