from discord.ext import commands
import discord

#SAY
class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def say(self, ctx):
        if ctx.message.content[5:]:
            msg = discord.Embed(
                title = f'_«{ctx.message.content[5:]}»_', 
                color= 0x39d0d6)
            msg.set_footer(
                text = f'© {ctx.message.author.name}', 
                icon_url = ctx.message.author.avatar_url)
            await ctx.send(embed = msg)
        else :
            await ctx.send("Error! Type some text after `/say`")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(SayCog(bot))