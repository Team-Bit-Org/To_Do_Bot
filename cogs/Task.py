from discord.ext import commands
from discord.ext import tasks
import os


class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_alarm.start()

    @tasks.loop(minutes=5.0)
    async def check_alarm(self):
        with open('../count.txt', 'r', encoding="UTF-8") as f:
            ff = f.readlines()

        with open('../count.txt', 'w', encoding="UTF-8") as f:
            asdf = int(ff[0]) + 5
            f.write(str(asdf))

        todo_listdir = os.listdir('./ToDo/')

        for i in todo_listdir:
            l = os.listdir(f'./ToDo/{i}/')
            for ii in l:
                with open(f'./ToDo/{i}/{ii}/information.txt', 'r', encoding="UTF-8") as f:
                    ff = f.readlines()
                for iii in ff:
                    ff.remove(iii)
                    ff.append(iii.strip())
                if int(ff[2]) == int(asdf):
                    user = self.bot.get_user(int(i))
                    await user.send(f'<@{i}> 님 To Do `{ii}` 작업 집중 메세지입니다!')
                else:
                    continue

    @check_alarm.before_loop
    async def before_check_alarm(self):
        print('check_alarm task wait..')
        await self.bot.wait_until_ready()
        print('check_alarm task is ready.')


def setup(bot):
    bot.add_cog(Task(bot))
    print('Cogs Tasks On Ready.')