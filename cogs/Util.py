from discord.ext import commands
import discord


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['도움말', '도움', '명령어'])
    async def help_cmd(self, ctx: commands.Context):
        embed = discord.Embed(
            title="To Do Bot Help",
            description='',
            color=discord.Colour.blurple()
        )
        embed.add_field(
            name='To Do',
            value='`-add "To Do Name" "To Do description"`\n`-edit [To Do Name]`\n`-remove [To Do Name]'
                  '`\n`-state [To Do Name]`\n`-list`',
            inline=False
        )
        embed.add_field(
            name='Util',
            value=f'`-help`\n`-invite`\n`-dev`',
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name='invite')
    async def invitebot(self, ctx):
        embed = discord.Embed(
            title='Invite Link',
            description='[Click Here](https://discord.com/api/oauth2/authorize?client_id='
                        '851092913537548348&permissions=273472&scope=bot)',
            color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='dev')
    async def developers(self, ctx):
        embed = discord.Embed(
            title='Developer',
            description='땅콩#0516 (443734180816486441)',
            color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Util(bot))