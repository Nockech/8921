#Under rework now
import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import json

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

global role_for_mute 
role_for_mute = 'muted'

#LVL SYSTEM INIT
async def update_data(user_base, user):
    if not user in user_base and not str(Bot.user.id):
        user_base[user] = {}
        user_base[user]['exp'] = 0
        user_base[user]['lvl'] = 0

async def add_exp(user_base, user, exp):
    user_base[user]['exp'] += exp

async def update_level(channel, user_base, user):
    if user_base[user]['exp'] >= 15:
        user_base[user]['exp'] = 0
        user_base[user]['lvl'] += 1
        await channel.send(f'Ebal nichers')

        
@Bot.event
async def on_ready():
    await Bot.change_presence(status = discord.Status.idle, activity = discord.Game('with 0 users((')) # Very sad((

@Bot.event
async def on_message(message):
    with open('data.json', 'r') as i:
        user_base = json.load(i)
    
    await update_data(user_base, str(message.author.id))
    await add_exp(user_base, str(message.author.id), 1)
    await update_level(message.channel, user_base, str(message.author.id))
    
    with open('data.json', 'w') as i:
        json.dump(user_base, i)
        

@Bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def mute(ctx, user: discord.Member, time="indefinite term", rsn="No reason given"):
    shut = discord.Permissions.is_superset(ctx.message.author.guild_permissions,user.guild_permissions)
    restrict = discord.Embed(title=f':warning: Not enough permissions to mute: \n {user.name}',color=0xdaf806)
    role = discord.utils.get(ctx.message.guild.roles, name=role_for_mute)
    await ctx.message.delete()
    if shut:
        await user.add_roles(role)
        if time == "indefinite term":
            pass
        else:
            tm = float(time)*60
            time = f'{time} min'
            pass
        silent = discord.Embed(title="",color=0xfc0202)
        silent.add_field(name=f'User `{user.name}` has been muted by `{ctx.message.author.name}`', value=f'for time: `{time}`\n Reason: `{rsn}`')
        await ctx.send(embed=silent)
        await asyncio.sleep(tm)
        await user.remove_roles(role)
    else:
        await ctx.send(embed=restrict)
    
@Bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    klap = discord.utils.get(ctx.message.guild.roles, name=role_for_mute)
    await user.remove_roles(klap)
    await ctx.send(f'Unmuted `{user.name}`')

@Bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member,rsn="No reason given"):
    god = discord.Permissions.is_superset(ctx.message.author.guild_permissions,user.guild_permissions)
    nope = discord.Embed(title="", color=0xdaf806)
    nope.add_field(name="No, it's my Creator!", value=user.name)
    bann = discord.Embed(title="", color=0xfc0202)
    bann.set_image(url="https://i.imgur.com/HaVYQIX.png")
    bann.add_field(name=f'User `{user.name}` has beeen banned', value=f'Banned by: `{ctx.message.author.name}`\n Reason: `{rsn}`')
    dab = discord.Embed(title=f':warning: Not enough permissions to ban: \n {user.name}',color=0xdaf806)
    if user.id == 399575084521488385:
        await ctx.send(embed=nope)
        await ctx.message.delete()
    elif god:
        await ctx.send(embed=bann)
        await user.ban()
    else:
        await ctx.send(embed=dab)
    await ctx.message.delete()

#INFO
@Bot.command(pass_context = True)
async def info(ctx, user: discord.Member = None):
    await ctx.message.delete()
    emb = discord.Embed(title=":information_source:", color=0x39d0d6)

    try:
        emb.add_field(
            name = "Name:",
            value = f'{user.name} {"**BOT**" if user.bot else ""}')
    except:
        err = discord.Embed(colour=0xdaf806, title="")
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
            name = f'{str(user.activity.type)[13:]} right now: ', 
            value = user.activity.name,
            inline = False)

    emb.add_field(
        name = "Joined server at: ", 
        value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M"), 
        inline = False)
    emb.add_field(
        name = "Created account at:", 
        value = user.created_at.strftime("%#A, %#d %B %Y, %I:%M"))
    emb.add_field(
        name="Roles:", 
        value = (str(", ").join([role.mention for role in user.roles]))[23:], 
        inline = False)
    emb.set_thumbnail(url = user.avatar_url)
    emb.set_image(url = "https://i.imgur.com/GgNIvmI.png")

    await ctx.send(embed = emb)


#SAY
@Bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def say(ctx):
    if ctx.message.content[4:]:
        msg = discord.Embed(
            title = f'{ctx.message.content[4:]}', 
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
    inv = discord.Embed(title = "", color= 0x3079ec )
    inv.set_author(
        name = "Click here to invite", 
        url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
    inv.set_footer(
        text = Bot.user.name + " BOT", 
        icon_url = Bot.user.avatar_url)

    main = discord.Embed(title= ":mailbox_with_mail: Sended! check pm", color= 0x39d0d6 )
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

        cln = discord.Embed(title = f'Messages cleared: {amount}. {now}', color= 0xFF3861)
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = cln)
    except:
        err = discord.Embed(colour=0xdaf806, title="")
        err.add_field(
            name = "Unable to execute!",
            value = "You must indicate the number of messages after this command")

        await ctx.send(embed = err)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token)) 
