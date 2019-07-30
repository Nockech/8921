import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

@Bot.event
async def on_ready():
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cosmic Background radiation'))

@Bot.command(pass_context = True)
async def help(ctx):
    main = discord.Embed(title= ":mailbox_with_mail:Sended! check pm", color= 0x39d0d6 )
    main.set_footer(text= f'Requested by: {ctx.message.author.name}')
    commands = discord.Embed(title= "", color= 0x3079ec )
    commands.add_field(name= ":page_facing_up: Regular commands :", value= '''
`/info <@user_name>` - info about user
`/inv` - send link to invite bot on your server
`/help` - send command list in pm
`/show` - enable screen demo in voice channel''')
    commands.add_field(name= "Administrator commands :" , value= '''
`/ban <@user_name>` - ban user
`/clear <messages amount>` - clear chat 
`/say <text>` - print text in embed
''')
    commands.set_image(url= "https://i.imgur.com/zSQVJHH.png")
    await ctx.send(embed= main)
    await ctx.message.author.send(embed= commands)
    await ctx.message.delete()

@Bot.command(pass_context = True)
async def info(ctx , user: discord.Member ):
    emb = discord.Embed(title= ":information_source:", color= 0x39d0d6  )
    if user.id == 399575084521488385:
        emb.add_field(name = "This is my owner!", value = "__ __", inline = False)
    ifbot = ""
    if user.bot == True:
        ifbot = "**BOT**"
    emb.add_field(name = "Name:" , value= f'{user.name} {ifbot}')
    stat = str(user.status)
    if stat == 'dnd':
        stat = 'do not disturb'
    emb.add_field(name = "Status:" , value= stat)
    if user.activity != None:
        emb.add_field(name = "Playing right now: " , value = user.activity)
    emb.add_field(name = "Joined server at: " , value = user.joined_at.strftime("%#A, %#d %B %Y, %I:%M") , inline = False)
    emb.add_field(name = "Created account at:" ,value = user.created_at.strftime("%#A, %#d %B %Y, %I:%M"))
    emb.set_thumbnail(url = user.avatar_url)
    emb.add_field(name = "Roles:" , value = (str(", \n").join([role.mention for role in user.roles]))[23:], inline = False)
    emb.set_image(url= "https://i.imgur.com/GgNIvmI.png")
    try:
        await ctx.send(embed= emb)
        await ctx.message.delete()
    except:
        err = discord.Embed(colour=0xdaf806, title="")
        err.add_field(name= ":x: Unable to execute",value="You must mention user nickname after this command")
        await ctxsend(embed= err)


@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def say(ctx):
    msg = discord.Embed(title="{}".format((ctx.message.content)[4:]), color= 0x39d0d6)
    msg.set_footer(text="© {}".format(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
    try:
        await ctx.send(embed=msg)
        await ctx.message.delete()
    except:
        await ctx.send("Type text after `/say`")

@Bot.command(pass_context = True)
async def inv(ctx):
    inv = discord.Embed(title = "", color= 0x3079ec )
    inv.set_author(name = "Click here to invite" , url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
    inv.set_footer(text = Bot.user.name , icon_url = Bot.user.avatar_url)
    main = discord.Embed(title= ":mailbox_with_mail: Sended! check pm", color= 0x39d0d6 )
    main.set_footer(text= f'Requested by: {ctx.message.author.name}')
    await ctx.send(embed = main)
    await ctx.message.author.send(embed= inv)
    await ctx.message.delete()

@Bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member,rsn="No reason given"):
    gg=discord.Permissions.is_superset(ctx.message.author.guild_permissions,user.guild_permissions)
    nope=discord.Embed(title="",color=0xdaf806)
    nope.add_field(name="No, it's my Creator!",value=user.name)
    bann=discord.Embed(title="",color=0xfc0202)
    bann.set_image(url="https://i.imgur.com/HaVYQIX.png")
    bann.add_field(name=f'User {user.name} was banned',value=f'Banned by: {ctx.message.author.name}\n Reason: {rsn}')
    dab = discord.Embed(title="Not enough permissions to ban: \n {user.name}",color=0xdaf806)
    if user.id == 399575084521488385:
        await ctx.send(embed=nope)
        await ctx.message.delete()
        #return
    if gg == True:
        await ctx.send(embed=bann)
        await user.ban()
    else:
        await ctx.send(embed=dab)
    await ctx.message.delete()

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def clear(ctx, amount= 10):
    if amount <= 10:
        now = "Dont waste my time"
    elif amount <= 50:
        now = "Thats all?"
    elif amount >= 90:
        now = "Big clear, buddy"
    elif amount >= 50:
        now = "Good cleaning"
    cln = discord.Embed(title= f'Messages cleared: {amount} .{now}', color= 0x39d0d6 )
    await ctx.channel.purge(limit = amount)
    await ctx.send(embed=cln)

@Bot.command(pass_contex= True)
async def show(ctx):
    await ctx.message.delete()
    try:
        Guild= ctx.message.guild.id
        channel= ctx.message.author.voice.channel.id
        show= discord.Embed(colour=0x39d0d6, title=':arrow_forward: Invite to watch:')
        show.add_field(name= f'{ctx.message.author.voice.channel.name} - {ctx.message.author.name}\'s demonstration', value= '[Click here]({})'.format(f'https://discordapp.com/channels/{Guild}/{channel}'))
        await ctx.send(embed= show)
    except AttributeError:
        no= discord.Embed(colour=0xdaf806, title="")
        no.add_field(name=":x: Unable to execute", value="You must be in voice channel to use this function")
        await ctx.send(embed= no)
token = os.environ.get('BOT_TOKEN')
Bot.run(str(token)) 
