from discord.ext import commands
import discord
import os.path as path
import json

#INFO
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def info(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        emb = discord.Embed(title = ":information_source:", color = 0x39d0d6)

        one_up = path.abspath(path.join('data.json' ,"./."))
        with open(one_up, 'r') as i:
            user_base = json.load(i)

        try:
            emb.add_field(
                name = "Name:",
                value = f'{user} {"**BOT**" if user.bot else ""}')
        except:
            err = discord.Embed(colour = 0xdaf806, title = "")
            err.add_field(
                name = "Unable to execute!",
                value = "You must mention user nickname after this command")
            await ctx.send(embed = err)
            return

        emb.add_field(
            name = "Status:", 
            value = 'do not disturb' if str(user.status) == 'dnd' else str(user.status))

        if user.activity != None and str(user.activity.type) != 'ActivityType.custom':
            emb.add_field(
                name = f'{(str(user.activity.type)[13:]).capitalize()} right now: ', 
                value = user.activity.name,
                inline = False)

        emb.add_field(
            name = "Joined server at: ", 
            value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M").capitalize(), 
            inline = False)
        emb.add_field(
            name = "Created account at:", 
            value = user.created_at.strftime("%#A, %#d %B %Y, %I:%M").capitalize())
        emb.add_field(
            name="Roles:", 
            value = (str(", ").join([role.mention for role in user.roles]))[23:], 
            inline = False)

        if str(user.id) in user_base:
            db_user = user_base[str(user.id)]
            emb.add_field(
                name = f'Lvl {db_user["lvl"]} user, {15 - db_user["exp"]} exp left to the next lvl', 
                value = "** **")

        emb.set_thumbnail(url = user.avatar_url)
        emb.set_image(url = "https://i.imgur.com/GgNIvmI.png")

        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(HelpCog(bot))