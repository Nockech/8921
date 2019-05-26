import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

global create, create_id 

create = 'создать пати 🔨'
create_id = 575710726459752460

@Bot.event
async def on_ready():
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cosmic Background radiation'))

@Bot.event
async def on_voice_state_update(member, before, after):
    global create
    guild = member.guild
    cat = discord.utils.get(member.guild.voice_channels, name= create)
    try:
        if after.channel.id == create_id:
            namechannel = '💻 ' + member.name + ' party'
            await guild.create_voice_channel(name= namechannel, category= cat.category)
            channel = discord.utils.get(member.guild.voice_channels, name= namechannel)
            channel = discord.utils.get(member.guild.voice_channels, name= namechannel)
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
`/clear <messages amount>` - clear chat 
`/say <text>` - print text in embed
''')
    commands.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await ctx.send(embed= commands)
    await ctx.message.delete()

@Bot.command(pass_context = True)
async def info(ctx , user: discord.Member ):  #member: discord.Member
    emb = discord.Embed(title= "{}".format(":information_source:"), color= 0x39d0d6  )
    if user.id == 399575084521488385:
        emb.add_field(name = "This is my owner!", value = "__ __", inline = False)
    ifbot = ""
    if user.bot == True:
        ifbot = str("**BOT**")
    emb.add_field(name = "Name:" , value= "{} {}".format(user.name,ifbot))
    stat = str(user.status)
    if stat == str("dnd"):
        stat = str("do not disturb")
    emb.add_field(name = "Status:" , value= stat)
    if user.activity != None:
        emb.add_field(name = "Playing right now: " , value = user.activity)
    emb.add_field(name = "Joined server at: " , value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M") , inline = False)
    emb.add_field(name = "Created account at:" ,value = user.created_at.strftime("%#A, %#d %B %Y, %I:%M"))
    emb.add_field(name = "Roles:" , value = (str(", ").join([role.mention for role in user.roles]))[23:], inline = False)
    emb.set_thumbnail(url = user.avatar_url)
    emb.set_image(url= "https://i.imgur.com/GgNIvmI.png")
    await ctx.send(embed= emb)
    await ctx.message.delete()


@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def say(ctx):
    msg = discord.Embed(title= "{}".format((ctx.message.content)[4:]), color= 0x39d0d6 )
    msg.set_footer(text= "{}".format(ctx.message.author.name))
    await ctx.send('',embed = msg)
    await ctx.message.delete()

@Bot.command(pass_context = True)
async def inv(ctx):
    inv = discord.Embed(title = "", color= 0x3079ec )
    inv.set_author(name = "Click here to invite" , url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
    inv.set_footer(text = Bot.user.name , icon_url = Bot.user.avatar_url)
    main = discord.Embed(title= "{} Sended! check pm".format(":mailbox_with_mail:"), color= 0x39d0d6 )
    main.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await ctx.send(embed = main)
    await ctx.message.author.send(embed= inv)
    await ctx.message.delete()

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def ban(ctx, user: discord.Member, time = None, reason = None):
    love = discord.Embed(title= "", color= 0xac5ae7 )
    love.add_field(name = "No, it's my Operator!" , value= user.name)
    bann = discord.Embed(title= "", color= 0xfc0202 )
    rsn = reason
    if reason == None:
        rsn = "No reason given"
    bann.add_field(name = ":no_entry_sign: Banned {}".format(rsn) , value= user.name)
    bann.set_footer(text= "Banned by: {} on time: days".format(ctx.message.author.name))
    if user.id == 399575084521488385:
        await ctx.send(embed = love)
        await ctx.message.delete()
    else :
        await ctx.send(embed= bann)
        await user.ban()
        await ctx.message.delete()

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def clear(ctx, amount= 100):
    if amount <= 10:
        now = "Dont waste my time"
    elif amount <= 50:
        now = "Thats all?"
    elif amount >= 90:
        now = "Big clear, buddy"
    elif amount >= 50:
        now = "Good cleaning"
    cln = discord.Embed(title= "Messages cleared: {} .{}".format(amount, now), color= 0x39d0d6 )
    await ctx.channel.purge(limit = amount)
    await ctx.send(embed=cln)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
