import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os

Bot = commands.Bot(command_prefix= '/')
Bot.remove_command('help')

global create, create_id 

create = 'test'
create_id = 557569433191710720

@Bot.event
async def on_ready():
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cosmic Background radiation'))

    
#token = os.environ.get('BOT_TOKEN')
#Bot.run(str(token))

Bot.run('NTYxNzgwMjk0OTU3NjYyMjA5.XLNcKA.fBgrDC4jNJlWYYM2-g3Ii81WD9o')
