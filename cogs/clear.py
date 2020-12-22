from discord.ext import commands
import discord

#CLEAR
class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount = None):
        if amount is None:
            amount = 10
        try:
            amount = int(amount)

            if amount <= 10:
                now = "Done"
            elif amount <= 50:
                now = "Thats all?"
            elif amount >= 90:
                now = "Big clear, buddy"
            elif amount >= 50:
                now = "Good cleaning"

            cln = discord.Embed(title = f'Messages cleared: {amount}. {now}', color = 0xFF3861)
            await ctx.channel.purge(limit = amount)
            await ctx.send(embed = cln)
        except:
            err = discord.Embed(colour = 0xdaf806, title = "")
            err.add_field(
                name = "Unable to execute!",
                value = "You must indicate the number of messages after this command")

            await ctx.send(embed = err)

def setup(bot):
    bot.add_cog(ClearCog(bot))