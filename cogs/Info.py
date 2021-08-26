from discord.ext import commands
from EZPaginator import Paginator
from pymongo import MongoClient
import discord


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = MongoClient("mongodb://localhost:27017/").ToDo.user

    @commands.command(name='list', aliases=['List'])
    async def info_todos(self, ctx):
        if not self.coll.find_one({"author": str(ctx.author.id)}):
            embed = discord.Embed(
                title='오류 발생',
                description='등록한 To Do가 없습니다.\n`-add "To Do Name" "To Do description` 명령어를 사용해보세요.',
                color=discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        juststr = []
        embeds = []  # embeds list
        plz_wait = await ctx.send('잠시만 기다려주세요. 처리 중입니다.')
        for i in self.coll.find({"author": str(ctx.author.id)}):
            if i['_id'] in juststr:
                continue
            juststr.append(i["_id"])

        for i in juststr:
            data = self.coll.find_one({"_id": str(i)})
            if data['Concentration'] is not False:  # 작업 집중 메세지 빈도
                if data['alarm']:  # 마감 당일 안내 신청함
                    if data['state']:  # To Do 끝났음
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                            설명 : {data["content"]}\n마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `{int(data["Concentration"]) + 5}분`\n
                            마감 당일 안내 : `활성화`\nTo Do 끝남
                                         """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                    else:  # To Do 안끝남
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                                        설명 : {data["content"]}\n
                                        마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `{int(data["Concentration"]) + 5}분`\n
                                        마감 당일 안내 : `활성화`\nTo Do 끝나지 않음
                                        """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                else:  # 마감 당일 안내 신청 안함
                    if data['state']:  # To Do 끝났음
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                            설명 : {data["content"]}\n
                            마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `{int(data["Concentration"]) + 5}분`\n
                            마감 당일 안내 : `비활성화`\nTo Do 끝남
                                         """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                    else:  # To Do 안끝남
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                                        설명 : {data["content"]}\n
                                        마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `{int(data["Concentration"]) + 5}분`\n
                                        마감 당일 안내 : `비활성화`\nTo Do 끝나지 않음
                                        """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
            else:  # 작업 집중 메세지 신청 안함
                if data['alarm']:  # 마감 당일 안내 신청함
                    if data['state']:  # To Do 끝났음
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                            설명 : {data["content"]}\n
                            마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `설정하지 않음`\n
                            마감 당일 안내 : `활성화`\nTo Do 끝남
                                         """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                    else:  # To Do 안끝남
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                                        설명 : {data["content"]}\n
                                        마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `설정하지 않음`\n
                                        마감 당일 안내 : `활성화`\nTo Do 끝나지 않음
                                        """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                else:  # 마감 당일 안내 신청 안함
                    if data['state']:  # To Do 끝났음
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                            설명 : {data["content"]}\n
                            마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `설정하지 않음`\n
                            마감 당일 안내 : `비활성화`\nTo Do 끝남
                                         """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
                    else:  # To Do 안끝남
                        embed = discord.Embed(
                            title=f'{i}',
                            description=f"""
                                        설명 : {data["content"]}\n
                                        마감일 : `{data["end_day"]}`\n작업 집중 메세지 전송 빈도 : `설정하지 않음`\n
                                        마감 당일 안내 : `비활성화`\nTo Do 끝나지 않음
                                        """,
                            color=discord.Colour.blurple()
                        )
                        embeds.append(embed)
        msg = await ctx.send(embed=embeds[0])
        await plz_wait.delete()
        await Paginator(
            bot=self.bot, message=msg, embeds=embeds, only=ctx.author
        ).start()


def setup(bot):
    bot.add_cog(Info(bot))
