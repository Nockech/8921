import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import youtube_dl
import asyncio
from itertools import cycle
import os

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')
global rain
global come
rain = True
come = 'just_come'

players = {}
queues = {}
join_role = "new"

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@Bot.event
async def on_ready():
    await Bot.change_presence(game = discord.Game(name = "/help", type = 2))
    print("No errors , great job")
    print("Bot is online")

@Bot.command(pass_context = True)
async def join(ctx):
    jn = discord.Embed(title= "", color= 0x39d0d6  )
    jn.add_field(name = ":white_check_mark: Joined" , value= "waiting for commands")
    chnl = ctx.message.author.voice.voice_channel
    await Bot.say(embed= jn)
    await Bot.delete_message(ctx.message)
    await Bot.join_voice_channel(chnl)

@Bot.command(pass_context = True)
async def leave(ctx):
    lv = discord.Embed(title= "" , color = 0x39d0d6)
    lv.add_field(name= ":negative_squared_cross_mark: Disconnected" , value = "see ya next time!") 
    server = ctx.message.server
    voice_client = Bot.voice_client_in(server)
    await Bot.say(embed= lv)
    await Bot.delete_message(ctx.message)
    await voice_client.disconnect()

@Bot.command(pass_context = True)
async def play(ctx,url):
    server = ctx.message.server
    voice_client = Bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, ytdl_options={'default_search': 'auto'}, after= lambda : check_queue(server.id))
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await Bot.say('Added to queue')
    players[server.id] = player
    player.start()

@Bot.event
async def on_member_join(member):
    global come
    role = discord.utils.get(member.server.roles, name = come )
    await Bot.add_roles(member, role)
    await Bot.send_message(ctx.message.server)

@Bot.command(pass_context = True)
async def help(ctx):
    commands = discord.Embed(title= "", color= 0x3079ec )
    commands.add_field(name= "{} All commands :".format(":page_facing_up:") , value= '''
`/info <@user_name>` - info about user
`/glyph` - sends my glyph in warframe ^w^
`/inv` - send link to invite bot on your server
`/join`, `!play <url>`, `!pause`, `!stop`, `!leave` -
music commands(still under development)
`/helphere` - sends help in server chat
''')
    commands.add_field(name= "{}Administrator commands :".format(":page_facing_up:") , value= '''
`/ban <@user_name>` - ban user
`/rainon/!rainoff` - on/off rainbow role
`/clear <messages amount>` - clear chat 
` `
''')
    commands.set_footer(text= "in developing", icon_url = Bot.user.avatar_url )
    chat = discord.Embed(title= "{} Sended! check pm".format(":mailbox_with_mail:"), color= 0x39d0d6 )
    chat.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await Bot.delete_message(ctx.message)
    await Bot.send_message(ctx.message.author, embed= commands)
    await Bot.say(embed= chat)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def helphere(ctx):
    commands = discord.Embed(title= "", color= 0x3079ec )
    commands.add_field(name= "{} All commands :".format(":page_facing_up:") , value= '''
`/info <@user_name>` - info about user
`/hello` - say hello to bot:upside_down:
`/glyph` - sends my glyph in warframe ^w^
`/inv` - send link to invite bot on your server
`/join`, `!play <url>`, `!pause`, `!stop`, `!leave` -
music commands(still under development)
''')
    commands.add_field(name= "{}Administrator commands :".format(":page_facing_up:") , value= '''
`/ban <@user_name>` - ban user
`/rainon/!rainoff` - on/off rainbow role
`/clear <messages amount>` - clear chat 
''')
    await Bot.say(embed= commands)

@Bot.command(pass_context = True)
async def info(ctx, user: discord.User):
    emb = discord.Embed(title= "{}".format(":information_source:"), color= 0x39d0d6  )
    emb.add_field(name = "Name:" , value= user.name, inline = False)
    emb.add_field(name = "Status:" , value= user.status, inline = False)
    emb.add_field(name = "Joined at: " , value = str(user.joined_at)[:16], inline = False)
    if user.game != None:
        emb.add_field(name = "Playing right now: " , value = user.game, inline = False)
    emb.add_field(name = "Id:" , value= user.id, inline = False)
    emb.add_field(name = "Created account at:" , value = str(user.created_at)[:16], inline = False)
    emb.add_field(name = "Roles:" , value = ", ".join([role.name for role in user.roles]), inline = False)
    emb.set_thumbnail(url = user.avatar_url)
    emb.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await Bot.delete_message(ctx.message)
    await Bot.say(embed= emb)

@Bot.command(pass_context = True)
async def glyph(ctx):
    hen = discord.Embed(title= "", color= 0xca8ef1 )
    hen.set_image(url= "https://i.imgur.com/Ld8d2Vq.jpg")
    await Bot.say(embed= hen)
    await Bot.delete_message(ctx.message)

@Bot.command(pass_context = True)
async def inv(ctx):
    inv = discord.Embed(title = "", color= 0x3079ec )
    inv.set_author(name = "Click here to invite" , url = "https://discordapp.com/oauth2/authorize?client_id=505040895200985089&scope=bot&permissions=37088334")
    inv.set_footer(text = Bot.user.name , icon_url = Bot.user.avatar_url)
    main = discord.Embed(title= "{} Sended! check pm".format(":mailbox_with_mail:"), color= 0x39d0d6 )
    main.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await Bot.delete_message(ctx.message)
    await Bot.say(embed = main)
    await Bot.send_message(ctx.message.author, embed= inv)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def rainoff(ctx):
    global rain
    rain = False
    rol = discord.utils.get(ctx.message.server.roles, name ='rainbow')
    await Bot.delete_message(ctx.message)
    await Bot.edit_role(ctx.message.server, rol , colour= discord.Colour.gold())
    off = discord.Embed(title= " ", color= 0x3079ec)
    off.add_field(name = "{}".format(":rainbow: Rainbow disabled") , value= "no more chaos")
    await Bot.say(embed= off)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def rainon(ctx):
    global rain
    rol = discord.utils.get(ctx.message.server.roles, name ='rainbow')
    rain = True
    o = discord.Embed(title= " ", color= 0x3079ec)
    o.add_field(name = "{}".format(":rainbow: Rainbow on!") , value= "Yeah ,lets get this party started")
    o.set_footer(text= "Requested by:{}".format(ctx.message.author.name))
    await Bot.say(embed= o)
    await Bot.delete_message(ctx.message)
    while rain == True:
        await Bot.edit_role(ctx.message.server, rol , colour= discord.Colour.red())
        await asyncio.sleep(1)
        await Bot.edit_role(ctx.message.server, rol , colour= discord.Colour.green())
        await asyncio.sleep(1)
        await Bot.edit_role(ctx.message.server, rol , colour= discord.Colour.blue())
        await asyncio.sleep(1)
        await Bot.edit_role(ctx.message.server, rol , colour= discord.Colour.gold())
        await asyncio.sleep(1)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def ban(ctx, user: discord.Member):
    baan = True
    love = discord.Embed(title= "", color= 0xac5ae7 )
    love.add_field(name = "No, i love my sempai" , value= ':two_hearts: {} :two_hearts: '.format(user.name))
    bann = discord.Embed(title= "", color= 0xfc0202 )
    bann.add_field(name = ":no_entry_sign: Banned " , value= user.name)
    bann.set_footer(text= "Banned by: {}".format(ctx.message.author.name))
    if user.id == '399575084521488385':
        await Bot.say(embed = love)
    else :
        await Bot.say(embed= bann)
        await Bot.ban(user)
    await Bot.delete_message(ctx.message)

@Bot.command(pass_context = True)
@commands.has_permissions(administrator= True)
async def clear(ctx, amount= 100):
    channel = ctx.message.channel
    messages = []
    if amount <= 10:
        now = "Dont waste my time"
    elif amount <= 50:
        now = "Thats all?"
    elif amount >= 90:
        now = "Big clear, buddy"
    elif amount >= 50:
        now = "Good cleaning"
    cln = discord.Embed(title= "Messages cleared: {} .{}".format(amount, now), color= 0x39d0d6 )
    async for message in Bot.logs_from(channel, limit= int(amount)):
        messages.append(message)
    await Bot.delete_messages(messages)
    msg = await Bot.say(embed = cln)
    await asyncio.sleep(3)
    await Bot.delete_message(msg)
    

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
