from discord.ext import commands
import discord
import asyncio
import os


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    async def _todo_add(self, ctx, name=None, content=None):
        if name is None:
            embed = discord.Embed(
                title="오류 발생",
                description='올바른 사용법 : `!add "To Do 이름" "To Do 설명"',
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)

        elif os.path.isdir(f"./ToDo/{ctx.author.id}/"):
            os.chdir(f'./ToDo/{ctx.author.id}/')
            if os.path.isdir(f"./{name}/"):
                with open(f"./{name}/content.txt", "w", encoding="UTF-8") as f:
                    f.write(str(content))
                with open(f"./{name}/information.txt", "w", encoding="UTF-8") as f:
                    f.write('0')
                    f.seek(0)
                    f.truncate()
            else:
                os.mkdir(f'./{name}/')
                with open(f"./{name}/content.txt", "w", encoding="UTF-8") as f:
                    f.write(str(content))
                with open(f"./{name}/information.txt", "w", encoding="UTF-8") as f:
                    f.write('0')
                    f.seek(0)
                    f.truncate()

        else:
            os.mkdir(f'./ToDo/{ctx.author.id}/')
            os.mkdir(f'./ToDo/{ctx.author.id}/{name}/')
            with open(f"./ToDo/{ctx.author.id}/{name}/content.txt", "w", encoding="UTF-8") as f:
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
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
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
            await asyncio.sleep(0.5)
            m = await ctx.send('마감 일을 `YYYY/MM/DD` 형식으로 입력해주세요.\n예시 : 2021/06/26')

            descs = await self.bot.wait_for("message", timeout=60, check=text_check)
            date = descs.content

            await m.delete()
            await descs.delete()

            embed = discord.Embed(
                title='작업 진행 중',
                description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`\n마감 당일 안내   : 🟥\n작업 집중 메세지 : 🟥',
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
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check1)
                if str(reaction.emoji) == emoji[0]:  # 마감 당일 안내 활성화
                    with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                        f.write('True\n')

                    embed = discord.Embed(
                        title='작업 진행 중',
                        description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`'
                                    f'\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟥',
                        color=discord.Colour.blurple()
                    )
                    embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                    await msg.edit(embed=embed)
                    await ctx.send('마감 당일 안내를 활성화 하였습니다.', delete_after=1.0)
                    await msgs.delete()
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
                    try:  # 작업 집중 메세지 활성화 - 비활성화 선택
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check1)
                        if str(reaction.emoji) == emoji[0]:  # 작업 집중 메세지 활성화
                            message2 = await ctx.send('알림 빈도를 5분 단위, 그리고 숫자만 입력해주세요.')
                            descc = await self.bot.wait_for("message", timeout=60, check=text_check)
                            time = descc.content
                            with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                                f.write(f'{str(time)}\n')

                            await msgss.delete()
                            await descc.delete()

                            embed = discord.Embed(
                                title='작업 완료',
                                description=f'To Do 등록이 완료되었습니다.\n아래는 저장된 설정입니다.\n\n마감일 등록     : 🟩'
                                            f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟩\n  - `{time}`분',
                                color=discord.Colour.green()
                            )
                            embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                            await msg.edit(embed=embed)
                            await message2.delete()
                            await mmm.delete()
                        else:
                            with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                                f.write(f'False\n')
                            await ctx.send('작업 집중 메세지를 비활성화 하였습니다.', delete_after=2.0)
                            embed = discord.Embed(
                                title='작업 완료',
                                description=f'To Do 등록이 완료되었습니다.\n아래는 저장된 설정입니다.\n\n마감일 등록     : 🟩'
                                            f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 활성화\n작업 집중 메세지 : 🟩\n  - 비활성화',
                                color=discord.Colour.blurple()
                            )
                            embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                            await msg.edit(embed=embed)
                            await msgss.delete()
                            await mmm.delete()
                    except asyncio.TimeoutError:
                        await ctx.send('시간이 초과되었습니다.')

                else:  # 마감 당일 안내 비활성화
                    with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                        f.write(f'False\n')
                    embed = discord.Embed(
                        title='작업 진행 중',
                        description=f'작업이 진행중입니다.\n\n마감일 등록     : 🟩\n  - `{date}`'
                                    f'\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟥',
                        color=discord.Colour.blurple()
                    )
                    embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                    await msg.edit(embed=embed)
                    await msgs.delete()
                    await ctx.send('마감 당일 안내를 비활성화 하였습니다.', delete_after=2.0)

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
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check1)
                        if str(reaction.emoji) == emoji[0]:  # 작업 집중 메세지 활성화
                            msgmsg = await ctx.send('알림 빈도를 5분 단위, 그리고 숫자만 입력해주세요.')
                            descc = await self.bot.wait_for("message", timeout=60, check=text_check)
                            time = descc.content
                            with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                                f.write(f'{str(time)}\n')
                            await msgmsg.delete()
                            await msgss.delete()
                            await descc.delete()

                            embed = discord.Embed(
                                title='작업 완료',
                                description=f'To Do 등록이 완료되었습니다.\n아래는 저장된 설정입니다.\n\n마감일 등록     : 🟩'
                                            f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟩\n  - `{time}`분',
                                color=discord.Colour.green()
                            )
                            embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                            await msg.edit(embed=embed)

                            await mmm.delete()
                        else:  # 작업 집중 메세지 비활성화
                            await ctx.send('작업 집중 메세지를 비활성화 하였습니다.', delete_after=1.0)
                            with open(f"./ToDo/{ctx.author.id}/{name}/information.txt", "a", encoding="UTF-8") as f:
                                f.write(f'False\n')
                            await mmm.delete()
                            await msgss.delete()
                            embed = discord.Embed(
                                title='작업 완료',
                                description=f'To Do 등록이 완료되었습니다.\n아래는 저장된 설정입니다.\n\n마감일 등록     : 🟩'
                                            f'\n  - `{date}`\n마감 당일 안내   : 🟩\n  - 비활성화\n작업 집중 메세지 : 🟩\n  - 비활성화',
                                color=discord.Colour.green()
                            )
                            embed.set_footer(text='⬛ - 작업 진행중 ㅣ 🟥 - 작업 미진행 ㅣ 🟩 - 작업 완료')
                            await msg.edit(embed=embed)

                    except asyncio.TimeoutError:
                        await ctx.send('시간이 초과되었습니다.')
            except asyncio.TimeoutError:
                await ctx.send('시간이 초과되었습니다.')
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과되었습니다.")


def setup(bot):
    bot.add_cog(Add(bot))
