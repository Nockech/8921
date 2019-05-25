import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

global create

global create, create_id 

create = 'test'
create_id = '557569433191710720'

@Bot.event
async def on_ready():
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cosmic Background radiation'))

@Bot.event
async def on_voice_state_update(member, before, after):
    global create, create_id
    guild = member.guild
    cat = discord.utils.get(member.guild.voice_channels, name= create)
    try:
        if after.channel.id == create_id:
            namechannel = '💻 ' + member.name + ' party'
            await guild.create_voice_channel(name= namechannel, category= cat.category)
            channel = discord.utils.get(member.guild.voice_channels, name= namechannel)
            channel_id = channel.id
            overwrite = discord.PermissionOverwrite()
            overwrite.manage_channels = True
            await channel.set_permissions(member, overwrite=overwrite)
            await asyncio.sleep(0.1)
            await member.edit(voice_channel= channel)
            status = True
            while status:
                if len(channel.members) == 0:
                    await asyncio.sleep(20)
                    await channel.delete()
                    status = False
    except AttributeError:
        pass

@Bot.command(pass_context = True)
async def help(ctx):
    commands = discord.Embed(title= "", color= 0x3079ec )
    commands.add_field(name= "{} All commands :".format(":page_facing_up:") , value= '''
`/info <@user_name>` - info about user
`/inv` - send link to invite bot on your server
`/help` - send command list in pm
''')
    commands.add_field(name= "{}Administrator commands :".format(":page_facing_up:") , value= '''
`/ban <@user_name>` - ban user
`/rainon/!rainoff` - on/off rainbow role
`/clear <messages amount>` - clear chat 
`/say <text>` - print text in embed
''')
    commands.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await ctx.send(embed= commands)

@Bot.command(pass_context = True)
async def info(ctx , user: discord.Member ):  #member: discord.Member
    emb = discord.Embed(title= "{}".format(":information_source:"), color= 0x39d0d6  )
    ifbot = ""
    if user.bot == True:
        ifbot = str("**BOT**")
    emb.add_field(name = "Name:" , value= "{} {}".format(user.name,ifbot))
    if user.id == '399575084521488385':
        emb.add_field(text = "This is my owner!" , value = "__g __")
    stat = str(user.activity)
    if stat == str("dnd"):
        stat = str("do not disturb")
    emb.add_field(name = "Status:" , value= stat)
    if user.activity != None:
        emb.add_field(name = "Playing right now: " , value = user.activity, inline = False)
    emb.add_field(name = "Joined server at: " , value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M") , inline = False)
    emb.add_field(name = "Created account at:" ,value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M"))
    emb.add_field(name = "Roles:" , value = (str(", ").join([role.mention for role in user.roles]))[23:], inline = False)
    emb.set_thumbnail(url = user.avatar_url)
    emb.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await ctx.send(embed= emb)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def say(ctx):
    msg = discord.Embed(title= "{}".format((ctx.message.content)[4:]), color= 0x39d0d6 )
    msg.set_footer(text= "{}".format(ctx.message.author.name))
    await ctx.send('',embed = msg)



token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
