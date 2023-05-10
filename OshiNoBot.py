import datetime
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "oshi-no-ko-wednesday", description = "Is it Oshi No Ko Wednesday?")
async def wednesday(interaction):
    #if it is wednesday
    if datetime.datetime.today().weekday() == 2:
        await interaction.response.send_message("It is Oshi No Ko Wednesday!")
    else:
        await interaction.response.send_message("It is not Oshi No Ko Wednesday.")

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run("MTEwMzMxODczMzMxMDY2ODgyMA.GE-o4J.n7xFXzUj1jhHZZWXrlwB-_D3NliWD7ZIZdqxeQ")