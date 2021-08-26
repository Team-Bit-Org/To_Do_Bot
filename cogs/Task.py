from discord.ext import commands
from discord.ext import tasks
from pymongo import MongoClient
import os


class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_alarm.start()
        self.coll = MongoClient("mongodb://localhost:27017/").ToDo.user

    @tasks.loop(minutes=5.0)
    async def check_alarm(self):
        for i in self.coll.find({}):
            if i["Concentration"] is not False:
                find = {"_id": str(i["_id"])}
                set_data = {"$inc": {"wait_minute": 5}}
                self.coll.update_one(find, set_data)
                if int(i["wait_minute"]) == int(i['Concentration']):
                    user = self.bot.get_user(int(i['author']))
                    find = {"_id": str(i["_id"])}
                    set_data = {"$set": {"wait_minute": 0}}
                    self.coll.update_one(find, set_data)
                    await user.send(f'안녕하세요, `{i["_id"]}` To Do 작업 집중 메세지입니다.')
                else:
                    continue
            else:
                continue

    @check_alarm.before_loop
    async def before_printer(self):
        print('Tasks check_alarm waiting..')
        await self.bot.wait_until_ready()
        print('Tasks check_alarm is start.')


def setup(bot):
    bot.add_cog(Task(bot))
    print("Cogs Tasks On Ready.")
