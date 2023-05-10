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
        #send another message
        await interaction.channel.send("https://tenor.com/view/oshi-no-ko-wednesday-my-star-oshi-no-ko-wednesday-my-star-wednesday-gif-1411268737957778018")
    else:
        await interaction.response.send_message("It is not Oshi No Ko Wednesday.")

@tree.command(name="next-episode", description="Time until the next episode?")
async def next_episode(interaction):
    #time until next wednesday 2pm UTC
    now = datetime.datetime.now()
    next_wednesday = now + datetime.timedelta((2 - now.weekday()) % 7)
    next_wednesday = next_wednesday.replace(hour=14, minute=0, second=0, microsecond=0)
    time_until = next_wednesday - now
    await interaction.response.send_message("Time until next episode: " + str(time_until))

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run("MTEwMzMxODczMzMxMDY2ODgyMA.GE-o4J.n7xFXzUj1jhHZZWXrlwB-_D3NliWD7ZIZdqxeQ")