import discord 
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import MemberConverter
import asyncio
import os
import json

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

global role_for_mute 
role_for_mute = 'muted'

#LVL SYSTEM
async def update_data(user_base, user):
    if not user in user_base:
        user_base[user] = {}
        user_base[user]['exp'] = 0
        user_base[user]['lvl'] = 0
        user_base[user]['bank'] = 0

async def add_exp(user_base, user, exp):
        user_base[user]['exp'] += exp

async def update_level(msg_channel, user_base, user):
    if user_base[user]['exp'] >= 15:
        user_base[user]['exp'] = 0
        user_base[user]['lvl'] += 1

        lvlup = discord.Embed(colour = 0x202225, title = "")
        lvlup.set_footer(
            text = f'{Bot.get_user(int(user)).name} advanced to the next lvl({user_base[user]["lvl"]})')
        await msg_channel.send(embed = lvlup)
        
@Bot.event
async def on_ready():
    #Bot.load_extension('cogs.music')
    await Bot.change_presence(status = discord.Status.idle, activity = discord.Game('Overwatch'))

@Bot.event
async def on_message(message):
    with open('data.json', 'r') as i:
        user_base = json.load(i)
    
    if not message.author.bot:
        await update_data(user_base, str(message.author.id))
        await add_exp(user_base, str(message.author.id), 1)
        await update_level(message.channel, user_base, str(message.author.id))
    
    with open('data.json', 'w') as i:
        json.dump(user_base, i)
    
    await Bot.process_commands(message)
    
#HELP
@Bot.command(pass_context = True)
async def help(ctx):
    hlp = discord.Embed(title = "", color = 0x3079ec)
    hlp.add_field(
        name = 'General commands: \n ** **',
        value = '''
        > /invite - sends the invite bot link in pm\n
        > /info - all information about user\n
        > /say [text] - shows the text in the quote
        ''')
    hlp.add_field(
        name = 'Moderation commands: \n ** **',
        value = f'''
        > /ban [@user] [reason] - bans the specified user\n
        > /unban [user_id - unbans user\n
        > /mute [@user] - gives user role named "{role_for_mute}" \n(make sure it exist on server)\n
        > /unmute [@user] - unmutes user\n
        > /clear [amount] - clears the specified number of messages
        ''')
    hlp.set_image(url = "https://i.imgur.com/zSQVJHH.png")

    main = discord.Embed(title = ":mailbox_with_mail: Sended! check pm", color = 0x39d0d6 )
    main.set_footer(text = f'Requested by: {ctx.message.author.name}')

    await ctx.send(embed = main)
    await ctx.message.author.send(embed = hlp)
    await ctx.message.delete()

#MUTE
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, user: discord.Member, time = 5, *rsn):
    shut = discord.Permissions.is_superset(ctx.message.author.guild_permissions, user.guild_permissions)
    role = discord.utils.get(ctx.message.guild.roles, name = role_for_mute)

    if shut:
        await user.add_roles(role)

        tm = f'{int(time)} min'
        time = float(time) * 60
        
        silent = discord.Embed(title = "", color = 0xfc0202)
        silent.add_field(
            name = f'{user.name} has been muted by {ctx.message.author.name}', 
            value = f'For time: {tm}\n Reason: {" ".join(rsn) if " ".join(rsn) else "No reason given"}')

        await ctx.send(embed = silent)
        await asyncio.sleep(time)
        await user.remove_roles(role)
    else:
        restrict = discord.Embed(title = f':warning: Not enough permissions to mute: \n {user.name}', color = 0xdaf806)
        await ctx.send(embed = restrict)

    await ctx.message.delete()
            
@mute.error
async def mute_handler(ctx, error):
    err = discord.Embed(colour = 0xdaf806, title = "")
    err.add_field(
        name = "Unable to execute!",
        value = "You must mention user nickname and pass correct time after this command")
    err.set_footer(
        text = f'Make sure server got role named "{role_for_mute}"')
    await ctx.send(embed = err)
    
#UNMUTE
@Bot.command(pass_context = True)
@commands.has_permissions(administrator=True)#
async def unmute(ctx, user):
    try:
        klap = discord.utils.get(ctx.message.guild.roles, name = role_for_mute)
        converter = MemberConverter()
        member = await converter.convert(ctx, user)
        emb = discord.Embed(title = f'Unmuted {member.name}. Take it slowly', color = 0xFF3861)

        await member.remove_roles(klap)
        await ctx.send(embed = emb)
    except:
        err = discord.Embed(colour = 0xdaf806, title = "")
        err.add_field(
            name = "Unable to execute!",
            value = "You must mention user nickname after this command")
        err.set_footer(
            text = f'Make sure server got role named "{role_for_mute}"')
        await ctx.send(embed = err)

#BAN
@Bot.command(pass_context = True)
@commands.has_permissions(ban_members = True)
async def ban(ctx, user, *rsn):
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
            value = f'** **\nBanned by {ctx.message.author.name}\n Reason: {" ".join(rsn) if " ".join(rsn) else "No reason given"}')
        await ctx.send(embed = bann)
        await user.ban()
    else:
        err = discord.Embed(colour = 0xdaf806, title = "")
        err.add_field(
            name = "Unable to execute!",
            value = "You have not enough permissions to ban this member")
        await ctx.send(embed = err)
            
#UNBAN
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, user_id):
    try:
        user = Bot.get_user(int(user_id))
        await ctx.guild.unban(user)
    except:
        err = discord.Embed(colour = 0xdaf806, title = "")
        err.add_field(
            name = "Unable to execute!",
            value = "You must mention banned user id after this command")
        err.set_footer(
            text = f'You can get banned users list by using "banlist" command')
        await ctx.send(embed = err)

#BANLIST
@Bot.command(pass_context = True)
async def banlist(ctx):
    banned_users = await ctx.guild.bans()
    banned_users = [i.user for i in banned_users]

    emb = discord.Embed(colour = 0xFF3861, title = "Banned users:")
    
    if not banned_users:
        emb.title = "There is no banned users on server"
        
    for i in banned_users:
        emb.add_field(
            name = f'{banned_users.index(i) + 1}. {str(i)}',
            value = f'{i.mention}; id: {str(i.id)}',
            inline = False)

    await ctx.send(embed = emb)
            
#INFO
@Bot.command(pass_context = True)
async def info(ctx, user: discord.Member = None):
    await ctx.message.delete()
    emb = discord.Embed(title = ":information_source:", color = 0x39d0d6)
    with open('data.json', 'r') as i:
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

#SAY
@Bot.command(pass_context = True)
async def say(ctx):
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

#INVITE
@Bot.command(pass_context = True)
async def invite(ctx):
    inv = discord.Embed(title = "", color = 0x3079ec )
    inv.set_author(
        name = "Click here to invite", 
        url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
    inv.set_footer(
        text = Bot.user.name + " BOT", 
        icon_url = Bot.user.avatar_url)

    main = discord.Embed(title = ":mailbox_with_mail: Sended! check pm", color = 0x39d0d6 )
    main.set_footer(text = f'Requested by: {ctx.message.author.name}')

    await ctx.send(embed = main)
    await ctx.message.author.send(embed = inv)
    await ctx.message.delete()

#CLEAR
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = None):
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

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token)) 
