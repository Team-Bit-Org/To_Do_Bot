import asyncio
from discord.ext import commands
from pymongo import MongoClient
import discord


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = MongoClient("mongodb://localhost:27017/").ToDo.user

    @commands.command(name="remove", aliases=["REMOVE", "delete", "DELETE"])
    async def remove_todo(self, ctx: commands.Context, *, todo_name):
        if not self.coll.find_one({"_id": str(todo_name)}):
            embed = discord.Embed(
                title="오류 발생",
                description=f"`{todo_name}`(이)라는 To Do를 찾을 수 없습니다.\nTo Do 이름을 바꾸고 다시 시도해주세요.",
                color=discord.Colour.red(),
            )
            return await ctx.send(embed=embed)
        else:
            check_remove = discord.Embed(
                title=f"정말로 {todo_name} To Do를 지우시겠습니까?",
                description=f"지우려면 아래 ✅ 이모지를 눌러주시고,\n지우지 않으시겠다면 ❎를 눌러주세요."
                f"\n\n시간 제한은 20초이며 20초가 초과될 경우 자동 취소됩니다.",
                color=discord.Colour.blurple(),
            )
            msg = await ctx.send(embed=check_remove)
            emojis = ["✅", "❎"]
            for i in emojis:
                await msg.add_reaction(str(i))

            def chck(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]

            try:
                reaction = await self.bot.wait_for(
                    "reaction_add", timeout=20, check=chck
                )
                if str(reaction[0].emoji) == "✅":
                    self.coll.delete_one({"_id": str(todo_name)})
                    embed = discord.Embed(
                        title="완료",
                        description=f"`{todo_name}` To Do를 삭제했습니다.",
                        color=discord.Colour.green(),
                    )
                    await ctx.send(embed=embed)
                else:
                    mm = await ctx.send(f"`{todo_name}` To Do 삭제를 취소했습니다.")
                    await msg.delete()
                    await ctx.message.delete()
                    await mm.delete()

            except asyncio.TimeoutError:
                await ctx.send("시간이 초과되었습니다.")
                await msg.delete()
                await ctx.message.delete()

    @commands.command(name="edit", aliases=["EDIT"])
    async def edit_todo(self, ctx: commands.Context, *, todo_name: str):
        if self.coll.find_one({"_id": str(todo_name)}):
            embed = discord.Embed(
                title="수정할 수 있는 To Do 설정",
                description="수정하고 싶은 To Do 설정의 번호를 입력해주세요.\n\n"
                "```md\n1. To Do 마감일 수정\n2. 마감 당일 안내 활성화 여부"
                "\n3. 작업 집중 메세지 활성화 여부\n4. To Do 완료 여부```",
                color=discord.Colour.blurple(),
            )
            await ctx.send(embed=embed)
            message = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            )
            content = message.content
            data = self.coll.find_one({"_id": str(todo_name)})
            emojis = ["✅", "❎"]  # 나중에 쓸 emoji 리스트
            if int(content) == 1:
                await ctx.send(
                    f'마감일을 몇일으로 다시 설정하시겠습니까?\n현재 저장된 마감일은 `{data["end_day"]}`입니다.'
                )
                message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
                content = message.content
                find = {"_id": str(todo_name)}
                set_data = {"$set": {"end_day": str(content)}}
                self.coll.update_one(find, set_data)
                embed = discord.Embed(
                    title="완료",
                    description=f"`{todo_name}` To Do의 마감일을 수정했습니다.",
                    color=discord.Colour.green(),
                )
                await ctx.send(embed=embed)
            elif int(content) == 2:
                if not data["alarm"]:
                    msg = await ctx.send(
                        f"마감 당일 안내를 활성화 하시려면 ✅를, 비활성화 하시려면 ❎를 눌러주세요.\n\n현재 마감 당일 안내는 비활성화 되어있습니다."
                    )
                    for i in emojis:
                        await msg.add_reaction(i)
                    try:

                        def chck(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis

                        reaction = await self.bot.wait_for(
                            "reaction_add", timeout=20, check=chck
                        )
                        if str(reaction[0].emoji) == emojis[0]:
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"alarm": True}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 마감 당일 안내를 활성화 했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 마감 당일 안내를 비활성화 했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)
                    except asyncio.TimeoutError:
                        await ctx.send("시간이 초과되었습니다.")
                if data["alarm"]:
                    msg = await ctx.send(
                        f"마감 당일 안내를 비활성화 하시려면 ✅를, 활성화 하시려면 ❎를 눌러주세요.\n\n현재 마감 당일 안내는 활성화 되어있습니다."
                    )
                    for i in emojis:
                        await msg.add_reaction(i)
                    try:

                        def chck(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis

                        reaction = await self.bot.wait_for(
                            "reaction_add", timeout=20, check=chck
                        )
                        if str(reaction[0].emoji) == emojis[0]:
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"alarm": False}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 마감 당일 안내를 비활성화 했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 마감 당일 안내를 활성화 했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)
                    except asyncio.TimeoutError:
                        await ctx.send("시간이 초과되었습니다.")
            elif int(content) == 3:
                if data["Concentration"] is not False:  # False 가 아니면 작업 집중 메세지를 받겠다고 저장됨
                    msg = await ctx.send(
                        "작업 집중 메세지를 비활성화 하시려면 ✅를, 메세지 전송 빈도를 바꾸시려면 ❎를 눌러주세요."
                    )
                    for i in emojis:
                        await msg.add_reaction(str(i))
                    try:

                        def chck(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis

                        reaction = await self.bot.wait_for(
                            "reaction_add", timeout=20, check=chck
                        )

                        if str(reaction[0].emoji) == str(emojis[0]):
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"Concentration": False}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 작업 집중 메세지 전송을 비활성화 했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)
                        elif str(reaction[1].emoji) == str(emojis[1]):
                            await ctx.send("바꾸려는 메세지 전송 빈도의 수를 5분 단위로 입력해주세요.")
                            message = await self.bot.wait_for(
                                "message",
                                check=lambda m: m.author == ctx.author
                                and m.channel == ctx.channel,
                            )
                            content = message.content
                            content = int(content) - 5
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"Concentration": str(content)}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 작업 집중 메세지 \n전송 빈도를 {int(content) + 5}분으로 설정했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)

                    except asyncio.TimeoutError:
                        await ctx.send("시간이 초과되었습니다.")
                else:
                    msg = await ctx.send('작업 집중 메세지를 활성화 하려면 ✅를 눌러주세요.')
                    await msg.add_reaction('✅')

                    def chck(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in emojis

                    reaction = await self.bot.wait_for(
                        "reaction_add", timeout=20, check=chck
                    )
                    if str(reaction[0].emoji) == emojis[0]:
                        await ctx.send("새로 설정하려는 메세지 전송 빈도의 수를 5분 단위로 입력해주세요.")
                        message = await self.bot.wait_for(
                            "message",
                            check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                        )
                        content = message.content
                        find = {"_id": str(todo_name)}
                        content = int(content) - 5
                        set_data = {"$set": {"Concentration": str(content)}}
                        self.coll.update_one(find, set_data)
                        embed = discord.Embed(
                            title="완료",
                            description=f"`{todo_name}` To Do의 작업 집중 메세지 \n전송 빈도를 {int(content) + 5}분으로 설정했습니다.",
                            color=discord.Colour.green(),
                        )
                        await ctx.send(embed=embed)

            elif int(content) == 4:
                if data["state"] is False:
                    msg = await ctx.send(
                        f"현재 {todo_name} To Do는 끝나지 않았습니다. 상태를 `완료`로 바꾸시려면 ✅를 눌러주세요."
                    )
                    await msg.add_reaction(str(emojis[0]))
                    try:

                        def chck(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis

                        reaction = await self.bot.wait_for(
                            "reaction_add", timeout=20, check=chck
                        )
                        if str(reaction[0].emoji) == str(emojis[0]):
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"state": True}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 완료 여부를 `완료`로 변경했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)

                    except asyncio.TimeoutError:
                        await ctx.send("시간이 초과되었습니다.")
                elif data["state"] is True:
                    msg = await ctx.send(
                        f"현재 {todo_name} To Do는 끝났습니다. 상태를 `미완료`로 바꾸시려면 ✅를 눌러주세요."
                    )
                    await msg.add_reaction(str(emojis[0]))
                    try:

                        def chck(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in emojis

                        reaction = await self.bot.wait_for(
                            "reaction_add", timeout=20, check=chck
                        )
                        if str(reaction[0].emoji) == str(emojis[0]):
                            find = {"_id": str(todo_name)}
                            set_data = {"$set": {"state": False}}
                            self.coll.update_one(find, set_data)
                            embed = discord.Embed(
                                title="완료",
                                description=f"`{todo_name}` To Do의 완료 여부를 `미완료`로 변경했습니다.",
                                color=discord.Colour.green(),
                            )
                            await ctx.send(embed=embed)

                    except asyncio.TimeoutError:
                        await ctx.send("시간이 초과되었습니다.")

    @commands.command(name='state')
    async def edit_todo_state(self, ctx, *, todo_name: str):
        if self.coll.find_one({"_id": str(todo_name)}):
            data = self.coll.find_one({"_id": str(todo_name)})
            emojis = ['✅', '❎']
            if not data['state']:
                msg = await ctx.send(
                    f"현재 {todo_name} To Do는 끝나지 않았습니다. 상태를 `완료`로 바꾸시려면 ✅를 눌러주세요."
                )
                await msg.add_reaction(emojis[0])
                try:

                    def chck(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in emojis

                    reaction = await self.bot.wait_for(
                        "reaction_add", timeout=20, check=chck
                    )
                    if str(reaction[0].emoji) == str(emojis[0]):
                        find = {"_id": str(todo_name)}
                        set_data = {"$set": {"state": True}}
                        self.coll.update_one(find, set_data)
                        embed = discord.Embed(
                            title="완료",
                            description=f"`{todo_name}` To Do의 완료 여부를 `완료`로 변경했습니다.",
                            color=discord.Colour.green(),
                        )
                        await ctx.send(embed=embed)

                except asyncio.TimeoutError:
                    await ctx.send("시간이 초과되었습니다.")

            elif data["state"]:
                msg = await ctx.send(
                    f"현재 {todo_name} To Do는 끝났습니다. 상태를 `미완료`로 바꾸시려면 ✅를 눌러주세요."
                )
                await msg.add_reaction(emojis[0])
                try:

                    def chck(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in emojis

                    reaction = await self.bot.wait_for(
                        "reaction_add", timeout=20, check=chck
                    )
                    if str(reaction[0].emoji) == str(emojis[0]):
                        find = {"_id": str(todo_name)}
                        set_data = {"$set": {"state": False}}
                        self.coll.update_one(find, set_data)
                        embed = discord.Embed(
                            title="완료",
                            description=f"`{todo_name}` To Do의 완료 여부를 `미완료`로 변경했습니다.",
                            color=discord.Colour.green(),
                        )
                        await ctx.send(embed=embed)

                except asyncio.TimeoutError:
                    await ctx.send("시간이 초과되었습니다.")


def setup(bot):
    bot.add_cog(Manage(bot))
