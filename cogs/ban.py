from discord.ext import commands
import discord

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #BAN
    @commands.command(pass_context = True)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user, *rsn):
        await ctx.message.delete()

        try:
            converter = MemberConverter()
            user = await converter.convert(ctx, user)
            is_super = discord.Permissions.is_superset(ctx.message.author.guild_permissions, user.guild_permissions)
        except:
            err = discord.Embed(colour = 0xdaf806, title = "")
            err.add_field(
                name = "Unable to execute!",
                value = "You must mention user nickname after this command")
            await ctx.send(embed = err)
            return

        if user.id == 399575084521488385:
            nope = discord.Embed(title = "", color = 0x202225)
            nope.add_field(
                name = "No, it's my Creator!", 
                value = "Can't ban my master")
            await ctx.send(embed = nope)
        elif is_super:
            bann = discord.Embed(title = "", color = 0xfc0202)
            bann.set_image(url = "https://i.imgur.com/HaVYQIX.png")
            bann.set_thumbnail(url = user.avatar_url)
            bann.add_field(
                name = f'{user.name} has beeen banned',
                value = f'** **\nBanned by {ctx.message.author.name}\n Reason: {" ".join(rsn) if " ".join(rsn) else "No reason given"}')
            await ctx.send(embed = bann)
            await user.ban()
        else:
            err = discord.Embed(colour = 0xdaf806, title = "")
            err.add_field(
                name = "Unable to execute!",
                value = "You have not enough permissions to ban this member")
            await ctx.send(embed = err)
            
    #UNBAN
    @commands.command(pass_context = True)
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, user_id):
        try:
            user = self.bot.get_user(int(user_id))
            await ctx.guild.unban(user)
        except Exception as e:
            print(e)
            print(self.bot)
            err = discord.Embed(colour = 0xdaf806, title = "")
            err.add_field(
                name = "Unable to execute!",
                value = "You must mention banned user id after this command")
            err.set_footer(
                text = f'You can get banned users list by using "banlist" command')
            await ctx.send(embed = err)

    #BANLIST
    @commands.command(pass_context = True)
    async def banlist(self, ctx):
        banned_users = await ctx.guild.bans()
        banned_users = [i.user for i in banned_users]

        emb = discord.Embed(colour = 0xFF3861, title = "Banned users:")
    
        for i in banned_users:
            if (self.bot.get_user(int(i.id)) == None):
                pass
            else: 
                emb.add_field(
                    name = f'{banned_users.index(i) + 1}. {str(i)}',
                    value = f'{i.mention}; id: {str(i.id)}',
                    inline = False)

        if not('fields' in emb.to_dict()):
            emb.title = "There is no banned users on server"

        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(BanCog(bot))
