import discord
import datetime
import random
import requests
from discord import app_commands
from discord.ext import tasks
from config import TOKEN
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#Commands
#on user join send message to welcome channel
@client.event
async def on_member_join(member):
    channel = client.get_channel(1149671217322786857)
    await channel.send(f"{member.mention} és Épico!", file=discord.File('assets/epico.jpeg'))


#Start the bot
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="A ser super Épico!"))
    global start_time 
    start_time = datetime.datetime.now()
    print("Ready!")


#Run
client.run(TOKEN)