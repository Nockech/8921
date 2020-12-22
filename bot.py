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
    Bot.load_extension('cogs.ban')
    Bot.load_extension('cogs.info')
    Bot.load_extension('cogs.say')
    Bot.load_extension('cogs.clear')
    Bot.load_extension('cogs.invite')
    
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

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token)) 
