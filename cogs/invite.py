from discord.ext import commands
import discord

#INVITE
class InviteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def invite(self, ctx):
        inv = discord.Embed(title = "", color = 0x3079ec )
        inv.set_author(
            name = "Click here to invite", 
            url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
        inv.set_footer(
            text = self.bot.user.name + " BOT", 
            icon_url = self.bot.user.avatar_url)

        main = discord.Embed(title = ":mailbox_with_mail: Sended! check pm", color = 0x39d0d6 )
        main.set_footer(text = f'Requested by: {ctx.message.author.name}')

        await ctx.send(embed = main)
        await ctx.message.author.send(embed = inv)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(InviteCog(bot))